# update_workspace.py: support for the "update workspace" command
import json
import time
import arrow

from xtlib import utils
from xtlib import console
from xtlib import run_helper
from xtlib import time_utils

class UpdateWorkspace():
    def __init__(self, config, core, store):
        self.config = config
        self.core = core
        self.store = store
        self.backend_location_cache = {}

    def group_by(self, records, group_col):
        groups = {}
        for rec in records:
            if not group_col in rec:
                group_value = "<unknown>"
            else:
                group_value = rec[group_col]

            if not group_value in groups:
                groups[group_value] = []

            groups[group_value].append(rec)

        return groups

    def get_alive_jobs(self, workspace):

        filter_dict = {"ws_name": workspace, "job_status": {"$nin": ["error", "cancelled", "completed"]}}
        
        fields_dict = {"job_id": 1, "compute": 1, "compute_target": 1, "service_name": 1, "service_type": 1, "pool_info":1, 
            "started": 1, "run_started": 1, "completed_runs": 1, "error_runs": 1}
        
        records = self.store.database.get_info_for_jobs(workspace, filter_dict, fields_dict)
        
        count = len(records)
        console.print("workspace: {}, found {:,} potentially false ALIVE jobs".format(workspace, count))

        service_groups = self.group_by(records, "service_type")
        return service_groups

    def update_jobs_completed(self, workspace):
        '''
        Goal: find all nodes in the database marked as not completed, but actually have completed.  For these nodes, 
        update each of their "not completed" runs as completed, update the node as completed, and update the associated job as 
        completed.  Also update time and duration fields for the runs, nodes, and jobs.

        Algorithm: 
            - to determine if a node is completed, we check the status of the node from its backend service.  If the service
              is no longer supported (e.g., Philly) or the node is unknown to the service (e.g., Azure Batch deleted job), we 
              assume the node is completed.
        
            - for completed nodes:
                - if the node is reported as completed, we use the completed time from the service.  Otherwise, we use the time that the node
                  uploaded its after files.  If no after files are found, we use the last event time in the node log + 1 hour.

                - once we have the node completion time, we use it to "wrapup" any runs that are not completed.  
                - next, we mark the node as "cancelled" and update the node completion time.
                - finally, we use the latest node completion time to update the job completion time.
        '''
        # get all alive jobs in workspace
        job_service_groups = self.get_alive_jobs(workspace)

        # get all alive nodes in workspace
        filter_dict = {"ws_name": workspace, "node_status": {"$nin": ["error", "cancelled", "completed"]}}
        fields_dict = {"job_id": 1, "target": 1, "exper_name": 1, "box_name": 1, "node_id": 1, "node_status": 1, "service_info": 1, 
                       "create_time": 1, "prep_start_time": 1, "app_start_time": 1, "post_start_time": 1, "post_end_time": 1, 
                       "completed_runs": 1, "error_runs": 1}
        alive_nodes = self.store.database.get_info_for_nodes(workspace, filter_dict, fields_dict)
        nodes_by_job = self.group_by(alive_nodes, "job_id")
        
        count = len(alive_nodes)
        console.print("workspace: {}, found {:,} potentially false ALIVE nodes".format(workspace, count))

        # process by service_type and job
        for service_type, jobs in job_service_groups.items():
            for job in jobs:
                job_id = job["job_id"]
                self.process_job_completed(workspace, job_id, job, nodes_by_job)

                # delete so we can find orphaned nodes at end
                # for unknown reason, sometimes job_id is not in nodes_by_job
                if job_id in nodes_by_job:
                    del nodes_by_job[job_id]

        # process orphaned nodes (have no job object)
        for job_id, nodes in nodes_by_job.items():
            job_end_time, completed_runs, error_runs, all_nodes_completed, job_status = self.update_job_nodes(workspace, job_id, None, nodes)

        self.update_orphaned_runs_fast(workspace)
        #self.update_orphaned_runs(workspace)

    def update_orphaned_runs_fast(self, workspace):
        # NOT YET TESTED...  this is an attempt to speed up the update_orphaned_runs() function
        # find remaining runs that are not completed but have a job that is completed; mark those runs as "cancelled"

        # select a._id, a.status, a.job_id, a.ws_name, b.job_status from [run_stats] as a
        # inner join [job_stats] as b on a.ws_name + '/' + a.job_id =  b._id
        # where not a.status in ('error', 'completed', 'cancelled') and b.job_status in ('error', 'completed', 'cancelled')

        count_cmd = "select count(*) from [run_stats] where not status in ('error', 'completed', 'cancelled') " + \
            " and job_id in (select job_id from [job_stats] where job_status in ('completed', 'error', 'cancelled'))"

        output_record = self.store.database.execute_sql_command(workspace, count_cmd, "update_orphaned_runs_fast/count", fetch_type="fetchone")
        print("found {:,} orphaned runs".format(output_record[0]))

        update_cmd = "update [run_stats] set status = 'cancelled' where not status in ('error', 'completed', 'cancelled') " + \
            " and job_id in (select job_id from [job_stats] where job_status in ('completed', 'error', 'cancelled'))"

        count = self.store.database.execute_sql_command(workspace, update_cmd, "update_orphaned_runs_fast/update")
        print("updated {:,} orphaned runs".format(count))

    def update_orphaned_runs(self, workspace):
        # find remaining runs that are not completed but have no node
        filter_dict = {"ws_name": workspace, "status": {"$nin": ["error", "cancelled", "completed", "restarted"]}}
        fields_dict = {"job_id": 1, "ws_name": 1, "run_name": 1, "status": 1, "start_time": 1, "end_time": 1, "node_index": 1}
        runs = self.store.database.get_info_for_runs(workspace, filter_dict, fields_dict)

        count = len(runs)
        console.print("workspace: {}, found {:,} potentially orphaned/missed RUNS".format(workspace, count))
        processed_count = 0
        skipped_count = 0

        for r, run in enumerate(runs):
            assert run["status"] not in ["error", "cancelled", "completed", "restarted"]
            assert run["ws_name"] == workspace

            if r % 50 == 0:
                print("  processing run: {:,} of {:,} (updated: {:,} runs)".format(r, len(runs), processed_count))

            # try to find node for this run (it may not exist)
            job_id = run["job_id"]
            node_index = run["node_index"]
            run_name = run["run_name"]

            filter_dict = {"ws_name": workspace, "job_id": job_id, "node_index": node_index}
            fields_dict = {"job_id": 1, "node_index": 1, "node_status": 1, "create_time": 1, "prep_start_time": 1, "app_start_time": 1, "post_start_time": 1, "post_end_time": 1, "completed_runs": 1, "error_runs": 1}
            nodes = self.store.database.get_info_for_nodes(workspace, filter_dict, fields_dict)
            if nodes:
                node = nodes[0]
            else:
                node = None
                
            mark_completed = True

            if node:
                node_status = node["node_status"]
                if node_status in ["error", "cancelled", "completed"]:
                    # node exists and is completed, so run should be marked as completed
                    mark_completed = True
                else:
                    # node exists and is not completed, so run should be skipped
                    mark_completed = False
            else:
                # node does not exist, so run should be marked as cancelled
                mark_completed = True

            if mark_completed:
                run_status = "cancelled"
                self.store.database.mark_run_ended_in_past(workspace, run_name, run_status, create_time=None, start_time=None, end_time=None, exit_code=None, error_msg=None)
                processed_count += 1
            else:            
                skipped_count += 1

        console.print("workspace: {}, processed {:,} orphaned runs, skipped {:,}".format(workspace, processed_count, skipped_count))

    def process_job_completed(self, workspace, job_id, job, nodes_by_job):
        # process job
        job_nodes_alive = nodes_by_job[job_id] if job_id in nodes_by_job else None
        
        if job_nodes_alive:
            job_end_time, completed_runs, error_runs, all_nodes_completed, job_status = self.update_job_nodes(workspace, job_id, job, job_nodes_alive)

        else:
            # no alive nodes found for job
            # get max end time from of all nodes
            filter_dict = {"ws_name": workspace, "job_id": job["job_id"]}
            fields_dict = {"job_id": 1, "create_time": 1, "prep_start_time": 1, "app_start_time": 1, "post_start_time": 1, "post_end_time": 1}
            job_nodes_all = self.store.database.get_info_for_nodes(workspace, filter_dict, fields_dict)

            end_times = [self.get_node_last_event_time(node) for node in job_nodes_all]
            if not end_times:
                # no nodes found, so just update the runs
                completed_runs, error_runs = self.mark_node_and_runs_completed(workspace, job_id, node_id=0, node=None, node_status=None, end_time_utc=None)
                all_nodes_completed = True
                job_end_time = None
        
            else:
                job_end_time = max(end_times) 
                completed_runs = 0
                error_runs = 0
                all_nodes_completed = True

        if all_nodes_completed and job:
            job_status = "cancelled"
            print("  marking job as cancelled: {}".format(job_id))

            self.store.database.mark_job_ended_in_past(workspace, job_id, job_status, job, end_time_secs=job_end_time, 
                new_completed_runs=completed_runs, new_error_runs=error_runs)
            print("---------------")

    def unwrap_service_info(self, si_text):
        si = None

        if si_text:
            # check for legacy format
            if si_text[1] == "'":
                si_text = si_text.replace("'", '"').replace("True", "true").replace("False", "false")

            try:
                si = json.loads(si_text)
            except:
                #print("  error in si_text - not valid json: {}".format(si_text))
                pass

        return si

    def get_node_first_event_time(self, node):
        first_time_secs = None

        if node["prep_start_time"]:
            first_time = arrow.get(node["prep_start_time"])
            first_time_secs = first_time.float_timestamp
    
        return first_time_secs

    def get_node_last_event_time(self, node):
        end_time = None

        if node["post_end_time"]:
            end_time = arrow.get(node["post_end_time"])
        elif node["post_start_time"]:
            end_time = arrow.get(node["post_start_time"])
        elif node["app_start_time"]:
            end_time = arrow.get(node["app_start_time"])
        elif node["prep_start_time"]:
            end_time = arrow.get(node["prep_start_time"])
        elif node["create_time"]:
            end_time = arrow.get(node["create_time"])
        else:
            assert False, "node has no start time: {}".format(node)

        end_time_secs = end_time.float_timestamp
        return end_time_secs

    def update_job_nodes(self, workspace, job_id, job, job_nodes):

        nodes_by_id = {node["node_id"]: node for node in job_nodes}
        all_nodes_completed = True
        latest_end_time_secs = None

        try:
            target = job["compute_target"]
            compute_def = job["pool_info"]
            service_name = job["service_name"]
            service_infos = [self.unwrap_service_info(node["service_info"]) for node in job_nodes]

            backend = self.core.create_backend(target, compute_def)
            sd = backend.get_timestamped_status_of_nodes(service_name, service_infos)
        except Exception as ex:
            if job:
                print("  error getting status of nodes: {}".format(ex))
            sd = {node["node_id"]: (None,None) for node in job_nodes}

        total_completed_runs = 0
        total_error_runs = 0
        job_status = "cancelled"
        print("processing {} nodes...".format(len(job_nodes)))

        if len(job_nodes) > 1:
            b = 9

        for node_id, (node_status, end_time_utc) in sd.items():
            if node_status in [None, "error", "cancelled", "completed"]:
                if node_id in nodes_by_id:
                    node = nodes_by_id[node_id]

                    end_time_secs, completed_runs, error_runs, stop_processing = self.process_node_and_runs_for_completed(workspace, job_id, node_id, 
                        node, node_status, end_time_utc)

                    if not latest_end_time_secs or end_time_secs > latest_end_time_secs:
                        latest_end_time_secs = end_time_secs

                else:
                    # node not found in database; just update the runs
                    completed_runs, error_runs = self.mark_node_and_runs_completed(workspace, job_id, node_id=None, node=None, node_status=None, end_time_utc=None)
                    stop_processing = False
                    end_time_secs = None

                total_completed_runs += completed_runs
                total_error_runs += error_runs

                # if stop_processing:
                #     break

            else:
                # at least one node is still running
                all_nodes_completed = False
                break

        if not all_nodes_completed:
            latest_end_time_secs = None

        return latest_end_time_secs, total_completed_runs, total_error_runs, all_nodes_completed, job_status

    def process_node_and_runs_for_completed(self, workspace, job_id, node_id, node, node_status, end_time_utc):

        stop_processing = False
        
        if node_status is None:
            # backend service doesn't know about the node (or service is no longer supported)
            stop_processing = True
            end_time_secs = self.get_node_last_event_time(node) 
            
            node_was_running = (node["prep_start_time"] is not None)
            if node_was_running:
                end_time_secs += 3600    # add 1 hour to last event time
            else:
                end_time_secs += 60    # juat add 1 min

        else:
            end_time_secs = time_utils.get_time_from_arrow_str(end_time_utc)

        completed_runs, error_runs = self.mark_node_and_runs_completed(workspace, job_id, node_id, node, node_status, end_time_secs)

        return end_time_secs, completed_runs, error_runs, stop_processing

    def mark_node_and_runs_completed(self, workspace, job_id, node_id, node, node_status, end_time_utc):
        # find all alive runs for node and mark them completed
        db = self.store.database

        if node:
            node_index = utils.node_index(node_id)
            filter_dict = {"ws_name": workspace, "job_id": job_id, "node_index": node_index, "status": {"$nin": ["error", "cancelled", "completed", "restarted"]}}
            fields_dict = {"job_id": 1, "node_index": 1, "ws_name": 1, "run_name": 1, "create_time": 1, "start_time": 1, "is_parent": 1, "exit_code": 1, "status": 1}
            end_time = str(arrow.get(end_time_utc))       # convert form UTC format to arrrow UTC format
            alive_runs = db.get_info_for_runs(workspace, filter_dict, fields_dict)

        else:
            # no node exists; just cancel all alive runs for job
            node_index = 0
            filter_dict = {"ws_name": workspace, "job_id": job_id, "status": {"$nin": ["error", "cancelled", "completed", "restarted"]}}
            fields_dict = {"job_id": 1, "node_index": 1, "ws_name": 1, "run_name": 1, "create_time": 1, "start_time": 1, "is_parent": 1, "exit_code": 1, "status": 1}
            alive_runs = db.get_info_for_runs(workspace, filter_dict, fields_dict)
            end_time = None
            
        ended_count = 0
        error_count = 0

        for run in alive_runs:

            # ensure we have the right run if we are about to update it
            assert run["job_id"] == job_id
            assert run["ws_name"] == workspace
            assert run["status"] not in ["error", "cancelled", "completed", "restarted"]

            if node:            
                assert run["node_index"] == node_index

            # mark the run completed
            run_name = run["run_name"]
            create_time = run["create_time"]
            start_time = run["start_time"]

            # since we don't know exactly what happened, leave exit_code and error_msg as is
            exit_code = None
            error_msg = None
            run_status = "cancelled"
            #is_parent = run["is_parent"]

            # mark the run CANCELLED
            print("  marking run as cancelled: {}".format(run_name))
            db.mark_run_ended_in_past(workspace, run_name, run_status, create_time, start_time, end_time, exit_code, error_msg)
            
            ended_count += 1
            if run_status == "error":
                error_count += 1

        if node:
            # mark the node completed
            print("  marking node as cancelled: {}/{}".format(job_id, node_index))
            node_status = "cancelled"
            db.mark_node_ended_in_past(workspace, job_id, node, node_status, end_time, ended_count, error_count)

        # will zero counts in node/job in subsequent call
        # db.job_node_exit(workspace, job_id)

        return ended_count, error_count
   
    def update_jobs_compute_target(self, workspace):
        '''
        Find jobs in workspace with a null COMPUTE_TARGET; update them with the COMPUTE 
        '''
        filter_dict = {"ws_name": workspace, "compute_target": None}
        fields_dict = {"job_id":1, "compute": 1}
        records = self.store.database.get_info_for_jobs(workspace, filter_dict, fields_dict)
        
        count = len(records)
        console.print("\nworkspace: {}, found {:,} jobs missing COMPUTE_TARGET".format(workspace, count))

        found_count = 0
        missing_count = 0

        for r, record in enumerate(records):

            if r % 50 == 0:
                print("  processing record: {:,} of {:,} (updated: {:,} records)".format(r, len(records), found_count))

            target = utils.safe_value(record, "compute")
            if target:
                # add vm_size to job record
                record["compute_target"] = target
                
                # remove pool_info (not changed and takes time to serialize/pass thru)
                del record["compute"]

                # update job record
                job_id = record["job_id"]
                self.store.database.update_job_info_only(workspace, job_id, record)
                found_count += 1

            else:
                missing_count += 1

        print("updated COMPUTE_TARGET from compute on {:,} jobs ({:,} still missing COMPUTE_TARGET)".format(found_count, missing_count))
        a = 9

    def update_jobs_vmsize(self, workspace):
        '''
        Find jobs in workspace with a null vm_size; update them with the vm_size pool_info
        '''
        filter_dict = {"ws_name": workspace, "vm_size": None}
        fields_dict = {"job_id":1, "vm_size": 1, "pool_info": 1}
        records = self.store.database.get_info_for_jobs(workspace, filter_dict, fields_dict)
        
        count = len(records)
        console.print("\nworkspace: {}, found {:,} jobs missing VM_SIZE".format(workspace, count))

        found_count = 0
        missing_count = 0

        for r, record in enumerate(records):

            if r % 50 == 0:
                print("  processing record: {:,} of {:,} (updated: {:,} records)".format(r, len(records), found_count))

            pool_info = utils.safe_value(record, "pool_info")
            if pool_info:
                vm_size = utils.safe_value(pool_info, "vm-size")
                if vm_size:
                    # add vm_size to job record
                    record["vm_size"] = vm_size
                    
                    # remove pool_info (not changed and takes time to serialize/pass thru)
                    del record["pool_info"]

                    # update job record
                    job_id = record["job_id"]
                    self.store.database.update_job_info_only(workspace, job_id, record)
                    found_count += 1

                else:
                    missing_count += 1

        print("updated VM_SIZE from pool_info on {:,} jobs ({:,} still missing VM_SIZE)".format(found_count, missing_count))
        a = 9

    def get_location_from_target(self, target):

        if target in self.backend_location_cache:
            location = self.backend_location_cache[target]

        else:
            try:
                backend = self.core.create_backend(target)
                cd = backend.compute_def
                service = cd["service"]
                location = backend.get_location(service)
            
            except Exception as ex:
                print("  error getting location from target: {}, ex: {}".format(target, ex))
                location = None

            self.backend_location_cache[target] = location

        return location
        
    def update_parent_runs_start_time(self, workspace):
        '''
        Find parent runs in workspace with a null start_time; update them with the node.app_start_time
        '''
        filter_dict = {"ws_name": workspace, "start_time": None, "is_parent": 1}
        fields_dict = {"job_id": 1, "node_index": 1, "run_name": 1, "is_parent": 1, "create_time": 1, "start_time": 1, "end_time": 1, "ws_name": 1}
        runs = self.store.database.get_info_for_runs(workspace, filter_dict, fields_dict)
        
        count = len(runs)
        console.print("\nworkspace: {}, found {:,} parent runs missing START_TIME".format(workspace, count))

        # get all nodes in workspace
        filter_dict = {"ws_name": workspace}
        fields_dict = {"ws_name": 1, "job_id": 1, "node_index": 1, "app_start_time": 1}
        nodes = self.store.database.get_info_for_nodes(workspace, filter_dict, fields_dict)
        nodes_by_job_ni = {"{}-{}".format(node["job_id"], node["node_index"]): node for node in nodes}

        found_count = 0
        missing_count = 0

        for r, run in enumerate(runs):

            if r % 50 == 0: 
                print("  processing record: {:,} of {:,} (updated: {:,} records)".format(r, len(runs), found_count))

            job_id = run["job_id"]
            node_index = run["node_index"]
            key = "{}-{}".format(job_id, node_index)

            # ensure we have a correct run
            assert run["ws_name"] == workspace
            assert run["is_parent"]
            assert not run["start_time"]

            if not key in nodes_by_job_ni:
                missing_count += 1
                continue

            node = nodes_by_job_ni[key]

            # ensure we have the matching node
            assert node["ws_name"] == workspace
            assert node["job_id"] == job_id
            assert node["node_index"] == node_index

            app_start_time = utils.safe_value(node, "app_start_time")
            if app_start_time:
                # add app_start_time to run record
                update_run = {"start_time": app_start_time}
                run_name = run["run_name"]

                # if we have create_time, compute and set queue_duration
                create_time = run["create_time"]
                if create_time:            
                    create_time_secs = time_utils.get_time_from_arrow_str(create_time)
                    app_start_time_secs = time_utils.get_time_from_arrow_str(app_start_time)

                    duration = app_start_time_secs - create_time_secs
                    update_run["queue_duration"] = duration

                # if we have end_time, compute and set run_duration
                end_time = run["end_time"]
                if end_time:            
                    end_time_secs = time_utils.get_time_from_arrow_str(end_time)
                    app_start_time_secs = time_utils.get_time_from_arrow_str(app_start_time)

                    duration = end_time_secs - app_start_time_secs
                    update_run["run_duration"] = duration

                # update run record
                self.store.database.update_run_stats_only(workspace, run_name, update_run)
                found_count += 1

            else:
                missing_count += 1

        print("updated START_TIME from node.app_start_time on {:,} runs ({:,} still missing START_TIME)".format(found_count, missing_count))
        a = 9


    def update_jobs_location(self, workspace):
        '''
        Find jobs in workspace with a null location; update them with the location from compute_target
        '''
        filter_dict = {"ws_name": workspace, "location": None, "ws_name": workspace}
        fields_dict = {"job_id":1, "compute_target": 1}
        records = self.store.database.get_info_for_jobs(workspace, filter_dict, fields_dict)
        
        count = len(records)
        console.print("\nworkspace: {}, found {:,} jobs missing LOCATION".format(workspace, count))

        found_count = 0
        missing_count = 0

        for r, record in enumerate(records):

            if r % 50 == 0:
                print("  processing record: {:,} of {:,} (updated: {:,} records)".format(r, len(records), found_count))

            target = utils.safe_value(record, "compute_target")
            location = self.get_location_from_target(target)

            if location:
                # add vm_size to job record
                record["location"] = location
                
                # remove compute_target (not changed)
                del record["compute_target"]

                # update job record
                job_id = record["job_id"]
                self.store.database.update_job_info_only(workspace, job_id, record)
                found_count += 1

            else:
                missing_count += 1

        print("updated LOCATION from service on {:,} jobs ({:,} still missing LOCATION)".format(found_count, missing_count))
        a = 9

    def update_jobs_end_time(self, workspace):
        '''
        Find non-alive jobs in workspace with end_time in (null, 0, '0').  Update the end_time & duration columns from the latest node end_time
        '''
        filter_by_end_time = True     # normally, this set set to True

        # get non-alive jobs in workspace
        filter_dict = {"ws_name": workspace, "job_status": {"$in": ["error", "cancelled", "completed"]}}
        fields_dict = {"job_id":1, "started": 1, "end_time": 1, "ws_name": 1, "job_status": 1}
        jobs = self.store.database.get_info_for_jobs(workspace, filter_dict, fields_dict)
        count = len(jobs)
        
        if filter_by_end_time:
            # filter jobs for end_time is None, 0, or '0'
            jobs = [r for r in jobs if (not r["end_time"]) or (r["end_time"] == "0")]

            count = len(jobs)
        
        console.print("\nworkspace: {}, found {:,} completed jobs missing END_TIME".format(workspace, count))

        # get all non-alive nodes in workspace
        filter_dict = {"ws_name": workspace, "node_status": {"$in": ["error", "cancelled", "completed"]}}
        fields_dict = {"job_id": 1, "target": 1, "node_id": 1, "node_status": 1, "ws_name": 1,
                       "create_time": 1, "prep_start_time": 1, "app_start_time": 1, "post_start_time": 1, "post_end_time": 1}
        nodes = self.store.database.get_info_for_nodes(workspace, filter_dict, fields_dict)
        nodes_by_job = self.group_by(nodes, "job_id")

        found_count = 0
        missing_count = 0

        for j, job in enumerate(jobs):

            assert job["ws_name"] == workspace
            assert job["job_status"] in ["error", "cancelled", "completed"]

            if filter_by_end_time:
                assert (not job["end_time"]) or (job["end_time"] == "0")
            
            if j % 50 == 0:
                print("  processing job: {:,} of {:,} (updated: {:,} records)".format(j, len(jobs), found_count))

            job_id = job["job_id"]
            start_time = time_utils.get_time_from_arrow_str(job["started"])

            if job_id not in nodes_by_job:
                # no nodes for job; will just use start time + 1 min
                assert start_time > 0
                latest_end_time_secs = start_time + 60

            else:
                nodes_of_job = nodes_by_job[job_id]
                assert len(nodes_of_job) > 0
                latest_end_time_secs = None

                for node in nodes_of_job:
                    assert node["ws_name"] == workspace
                    assert node["job_id"] == job_id
                    #assert node["node_status"] in ["error", "cancelled", "completed"]
                    
                    end_time_secs = self.get_node_last_event_time(node) 
                    assert end_time_secs > 0

                    if not latest_end_time_secs or end_time_secs > latest_end_time_secs:
                        latest_end_time_secs = end_time_secs

            # this update no longer makes sense (comment out call to this function)
            job_status = job["job_status"]

            self.store.database.mark_job_ended_in_past(workspace, job_id, job_status, job=None, end_time_secs=end_time_secs, 
                new_completed_runs=None, new_error_runs=None)
            
            found_count += 1

        print("updated END_TIME from nodes on {:,} non-alive jobs ({:,} jobs still missing END_TIME)".format(found_count, missing_count))
        a = 9

    def update_jobs_run_started(self, workspace):
        '''
        Find all jobs in workspace with NULL RUN_STARTED; Update the RUN_STARTED & QUEUE_DURATION columns from the min(node.create_time)
        '''
        # get all jobs in workspace with NULL run_started
        filter_dict = {"ws_name": workspace, "run_started": None}
        fields_dict = {"job_id":1, "run_started": 1, "started": 1, "ws_name": 1, "job_status": 1, "end_time": 1}
        jobs = self.store.database.get_info_for_jobs(workspace, filter_dict, fields_dict)
        count = len(jobs)
        console.print("\nworkspace: {}, found {:,} jobs missing RUN_STARTED".format(workspace, count))

        # get all nodes in workspace
        filter_dict = {"ws_name": workspace}   
        fields_dict = {"job_id": 1, "node_id": 1, "node_status": 1, "ws_name": 1, "create_time": 1, "prep_start_time": 1}
        nodes = self.store.database.get_info_for_nodes(workspace, filter_dict, fields_dict)
        nodes_by_job = self.group_by(nodes, "job_id")

        found_count = 0
        missing_count = 0

        for j, job in enumerate(jobs):

            assert job["ws_name"] == workspace
            assert job["run_started"] is None

            if j % 50 == 0:
                print("  processing job: {:,} of {:,} (updated: {:,} records)".format(j, len(jobs), found_count))

            job_id = job["job_id"]
            start_time = time_utils.get_time_from_arrow_str(job["started"]) if job["started"] else None
            end_time = time_utils.get_time_from_arrow_str(job["end_time"]) if job["end_time"] else None

            if job_id not in nodes_by_job:
                # no nodes for job; will not update run_started
                run_started = None

            else:
                nodes_of_job = nodes_by_job[job_id]
                assert len(nodes_of_job) > 0
                run_started = None

                for node in nodes_of_job:
                    assert node["ws_name"] == workspace
                    assert node["job_id"] == job_id
                    #assert node["node_status"] in ["error", "cancelled", "completed"]
                    
                    run_start_time_secs = self.get_node_first_event_time(node) 

                    if (not run_started) or ((run_start_time_secs) and (run_start_time_secs < run_started)):
                        run_started = run_start_time_secs

            js = {}
            if run_started:

                if start_time:
                    # set QUEUE_DURATION
                    if run_started < start_time:
                        # older jobs may have run_started < node prep start time
                        # to fix, adjust the start time to be 1 minute before run_started
                        start_time = run_started - 60
                        job["started"] = time_utils.get_arrow_str_from_time(start_time)

                    queue_duration = run_started - start_time
                    assert queue_duration > 0
                    js["queue_duration"] = queue_duration

                if end_time:
                    # set RUN_DURATION
                    if run_started > end_time:
                        # dirty jobs in xt_dilbert may have end_time < node prep start time (incorrect schema fixing code)
                        # to fix, adjust the end_time to be 1 minute after run_started
                        end_time = run_started + 60
                        job["end_time"] = time_utils.get_arrow_str_from_time(end_time)

                    run_duration = end_time - run_started
                    assert run_duration > 0
                    js["run_duration"] = run_duration

                js["run_started"] = time_utils.get_arrow_str_from_time(run_started)

                self.store.database.update_job_stats(workspace, job_id, js)
                found_count += 1

            else:
                missing_count += 1

        print("updated RUN_STARTED from nodes on {:,} jobs ({:,} jobs still missing RUN_STARTED)".format(found_count, missing_count))
        a = 9
