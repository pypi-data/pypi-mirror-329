#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# backend_pool.py: handles the platform submit/manage operations for service_types of pool and local
import os
import time
import uuid
import shutil
import stat
from interface import implements

from xtlib import utils
from xtlib import errors
from xtlib import attach
from xtlib import pc_utils
from xtlib import scriptor
from xtlib import constants
from xtlib import file_utils
from xtlib import run_helper
from xtlib import process_utils
from xtlib import box_information
from xtlib.xt_client import XTClient
from xtlib.backends.mount_helper import MountHelper
from xtlib.backends.node_scriptor import NodeScriptor

from xtlib.console import console
from xtlib.helpers.feedbackParts import feedback as fb
from xtlib.psm.local_psm_client import LocalPsmClient
from xtlib.psm.remote_psm_client import RemotePsmClient

from .backend_interface import BackendInterface
from .backend_base import BackendBase

class PoolBackend(BackendBase):
    def __init__(self, compute, compute_def, core, config, username=None, arg_dict=None):
        super(PoolBackend, self).__init__(compute, compute_def, core, config, username, arg_dict)

        self.compute = compute
        self.compute_def = compute_def
        self.core = core
        self.config = config
        self.username = username
        self.env_vars = None
        self.client = self.core.client

        if pc_utils.is_localhost(compute) and pc_utils.is_windows():
            self.is_windows = True

    # API 
    def get_name(self):
        return "pool"

    # API call
    def get_timestamped_status_of_nodes(self, service_name, service_infos):
        # return "nodes not recognized"
        sd = {"node"+str(i): (None,None) for i in range(len(service_infos))}
        return sd

    # API 
    def get_location(self, service):
        return None

    # API 
    def provides_container_support(self):
        '''
        Returns:
            returns True if docker run command is handled by the backend.
        '''
        return False

    def build_node_script_and_adjust_runs(self, job_id, job_runs, using_hp, experiment, service_type, snapshot_dir, env_vars, args, cmds=None):
        '''
        This method is called to allow the backend to inject needed shell commands before the user cmd.  This 
        base implementation does so by generating a new script file and adding it to the snapshot_dir.
        '''
        nowrap = args["nowrap"]
        is_direct_run = args["direct_run"]
        docker_cmd = args["docker_cmd"]

        # local or POOL of vm's
        data_local = args["data_local"]
        model_local = args["model_local"]

        # build the node script
        first_run = job_runs[0]
        fn_script, fn_inner = self.build_node_script(first_run, args)

        if docker_cmd:
            # best to use blobfuse since it will be available and will be closer to testing remote node 
            data_local = None
            model_local = None

        for i, box_run in enumerate(job_runs):
            box_info = box_run["box_info"]
            box_name = box_info.box_name
            box_secret = box_run["box_secret"]
            actions = box_info.actions
            node_id = utils.node_id(i)

            run_specs = box_run["run_specs"]
            cmd_parts = run_specs["cmd_parts"]
            run_name = box_run["run_name"]

            if is_direct_run:
                direct_cmd = cmds[i] if i < len(cmds) else cmds[0]
                run_specs["run_cmd"] = direct_cmd
            else:
                direct_cmd = None
                    
            self.gather_env_vars_and_store_in_file(i, run_name, direct_cmd, args)

            # if not fn_wrapped:

                #     # we only do this once (for the first box/job)
                #     using_localhost =  pc_utils.is_localhost(box_name, box_info.address)

                #     if docker_cmd:
                #         actions = ["data", "model"]
                #     else:
                #         # data_local overrides store_data_dir for LOCAL machine
                #         if using_localhost and data_local:
                #             store_data_dir = os.path.join(os.path.expanduser(data_local), store_data_dir)
                #             store_data_dir = file_utils.fix_slashes(store_data_dir, is_linux=not self.gen_for_windows)

                #             data_action = "use_local"
                #             if not "data" in actions:
                #                 actions.append("data")

                #         # model_local overrides store_model_dir for LOCAL machine
                #         if using_localhost and model_local:
                #             store_model_dir = os.path.join(os.path.expanduser(model_local), store_model_dir)
                #             model_action = "use_local"
                #             if not "model" in actions:
                #                 actions.append("model")

                #     setup_name = args["setup"]
                #     setup = self.config.get_setup_from_target_def(self.compute_def, setup_name)

                #     env_vars = self.get_env_vars_for_box(box_name, box_info, i, box_secret, args)
                #     pre_cmds = []

                #     # add commands to set ENV VARs
                #     self.append_title(pre_cmds, "SET/EXPORT POOL environment vars:")

                #     for name, value in env_vars.items():
                #         self.append_export(pre_cmds, name, value)

                #     use_username = not docker_cmd
                #     install_blobfuse = bool(docker_cmd)

                #     if self.gen_for_windows:
                #         node_index = "%1"
                #         run_name = "%2"
                #         homebase = os.getenv("HOMEDRIVE") + "\\."
                #         cwd = homebase + "\\.xt\\cwd"
                #     else:
                #         node_index = "$1"
                #         run_name = "$2"
                #         homebase = "$HOME"
                #         cwd = "$HOME/.xt/cwd"

                # fn_wrapped = super().wrap_user_command(cmd_parts, snapshot_dir, store_data_dir, data_action, 
                #     data_writable, store_model_dir, model_action, model_writable, storage_name, storage_key, actions, 
                #     is_windows=is_windows, sudo_available=False, use_allow_other=False, use_username = use_username, 
                #     setup=setup, pre_setup_cmds=pre_cmds, post_setup_cmds=None, args=args, nonempty=True, 
                #     install_blobfuse=install_blobfuse, node_index=node_index,
                #     run_name=run_name, homebase=homebase, cwd=cwd)   

            # we update each box's command
            script_part = "{}".format(os.path.basename(fn_script))
            if self.is_windows:
                sh_parts = [script_part]
            else:
                sh_parts = ['/bin/bash', '--login', script_part]
            run_specs["cmd_parts"] = sh_parts

    def build_node_script(self, first_run, args):

        run_specs = first_run["run_specs"]

        cmd_parts = run_specs["cmd_parts"]
        node_cmd = " ".join(cmd_parts)
        actions = ["data", "model"]
        manual_docker = bool(args["docker_cmd"]) 
        homebase = "$HOME"
  
        # sudo is available, but causes problems with subsequent MNT directory access
        sudo_available = False     

        mount_helper = MountHelper(compute_def=self.compute_def, homebase=homebase, sudo_available=sudo_available, actions=actions,
            use_username=False, use_allow_other=False, nonempty=True, backend=self, config=self.config, args=args)
        
        cwd="$HOME/.xt/cwd"

        node_scriptor = NodeScriptor(homebase=homebase, cwd=cwd, controller_cmd=node_cmd, 
            manual_docker=manual_docker, mount_helper=mount_helper, backend=self, get_env_vars_from_file=True,
            compute_def=self.compute_def, config=self.config, args=args)
        
        fn_script, fn_inner = node_scriptor.generate_script()
        return fn_script, fn_inner

    def gen_code_prep_cmds(self, ca, cmds, cwd, using_docker):

        if using_docker:
            ca.append_title(cmds, "CODE PREP: copy files from /usr/src to CWD")
            ca.append(cmds, "mkdir -p {}".format(cwd))
            ca.append(cmds, "cp -r {}/* {}".format("/usr/src", cwd))
            ca.append(cmds, "cd {}".format(cwd))
            ca.append(cmds, "rm {}".format(constants.CODE_ZIP_FN))

        else:
            # just need to delete the .zip file
            ca.append_title(cmds, "CODE PREP: delete code zip file")
            ca.append(cmds, "rm {}".format(constants.CODE_ZIP_FN))

    def submit_job(self, job_id, job_runs, workspace, compute_def, resume_name, 
           repeat_count, using_hp, runs_by_box, experiment, snapshot_dir, controller_scripts, args):

        fake_submit = args["fake_submit"]
        info_by_node = {}
        job_info = {"job": job_id}

        if not fake_submit:
            # first pass - ensure all boxes are NOT already running the controller
            # for i, box_runs in enumerate(job_runs):
            #     box_info = box_runs[0]["box_info"]

            #     box_name = box_info.box_name
            #     box_addr = box_info.address
            #     port = constants.CONTROLLER_PORT

                # if self.core.client.is_controller_running(box_name, box_addr, port):
                #     errors.config_error("XT controller already running on box: " + box_name)

            # second pass - transfer the main script to each box and start it
            for i, box_run in enumerate(job_runs):
                box_info = box_run["box_info"]

                # start run on specified box
                service_node_info = self.run_job_on_box(job_id, box_run, box_index=i, box_info=box_info, app_info=None, 
                    pool_info=compute_def,  resume_name=resume_name, repeat=repeat_count, 
                    using_hp=using_hp, exper_name=experiment, snapshot_dir=snapshot_dir, args=args)

                node_id = "node" + str(i)
                info_by_node[node_id] = service_node_info

                # update node_info record in database with service_info
                db = self.client.store.get_database()
                db.update_node_info_with_service_info(workspace, job_id, i, service_node_info)

        return job_info, info_by_node

    def run_job_on_box(self, job_id, box_run, box_index, box_info, app_info, pool_info,  
            resume_name=None, repeat=None, using_hp=None, exper_name=None, snapshot_dir=None, args=None):

        '''
        Remote box run - order of operations:
            1. psm_client = RemotePsmClient()

            2. psm_client runs locally and starts SSH with remote box

            3. psm_client.restart_psm_if_needed()
                - kills psm on remote if using old psm
                - copies psm.py to remote box
                - starts running psm.py on remote box
            
            4. psm_client.enqueue()
                - adds .zip file for run to node's queue 
        '''

        box_name = box_info.box_name
        box_addr = box_info.address
        box_os = box_info.box_os
        is_box_windows = (box_os == "windows")
        
        run_name = box_run["run_name"]

        if pc_utils.is_localhost(box_addr=box_addr):
            psm_client = LocalPsmClient()
        else:
            psm_client = RemotePsmClient(box_addr, is_box_windows)

        psm_client.restart_psm_if_needed()
        #print("psm created for box: " + box_addr)

        store_name = self.config.get("store")
        node_id = utils.node_id(box_index)

        cwd_dir = os.path.expanduser(constants.CWD_DIR)
        fn_src_zip = file_utils.path_join(cwd_dir, constants.CODE_ZIP_FN)
        workspace = args["workspace"]

        fn_entry = psm_client.enqueue(store_name, workspace, job_id, run_name, box_index, fn_src_zip)

        service_node_info = {"fn_entry": fn_entry, "box_addr": box_addr, "box_os": box_os, 
            "box_name": box_name, "job_id": job_id, "run_name": run_name, 
            "node_id": "node"+str(box_index), "workspace": workspace}

        fb.feedback("submitted") 

        return service_node_info

    def gather_env_vars_and_store_in_file(self, node_index, run_name, direct_cmd, args):

        # TODO: figure out a schmeme for delivering node-specific env var to pool boxes
        # one idea: create a new outer .zip file that contains the env var file + xt_code.zip
        env_vars = {}
        scriptor.add_controller_env_vars(env_vars, self.config, node_index=node_index, run_name=run_name, 
            batch_key=None, direct_cmd=direct_cmd, args=args)

        # for pool, we move them all into the FN_SET_ENV_VARS file
        text = ""
        for key, value in env_vars.items():
            text += "{}={}\n".format(key, value)

        # write text to set_env file in bootstrap dir
        bootstrap_dir = args["bootstrap_dir"]
        fn = bootstrap_dir + "/" + constants.FN_SET_ENV_VARS

        # specify "newline="" to ensure a \r is NOT written with \n char
        with open(fn, "wt", newline="") as outfile:
            outfile.write(text)
            
    def get_client_cs(self, service_node_info):
        '''
        Args:
            service_node_info: info that service maps to a compute node for a job
        Returns:
            {"ip": value, "port": value, "box_name": value}
        '''
        box_name = service_node_info["box_name"]
        controller_port = constants.CONTROLLER_PORT
        tensorboard_port = None
        ssh_port = 22

        if not box_name in self.config.get("boxes"):
            if pc_utils.is_localhost(box_name):
                box_name = "local"

        box_addr = self.config.get("boxes", box_name, dict_key="address", default_value=box_name, 
            prop_error="box not defined in config file: " + box_name)

        if "@" in box_addr:
            # strip off the username
            _, box_addr = box_addr.split("@", 1)
        #console.print("box_addr=", box_addr)

        if not "." in box_addr and box_addr != "localhost":
            raise Exception("box option must specify a machine by its IP address: " + str(box_addr))

        cs = {"ip": box_addr, "port": controller_port, "box_name": box_name}
        return cs
    
    def view_status(self, run_name, workspace, job, monitor, escape_secs, auto_start, 
            stage_flags, status, max_finished):

        boxes, pool_info, service_type = box_information.get_box_list(self.core, job_id=job, pool=self.compute)

        def monitor_work():
            # BOX LOOP
            text = ""
            for b, box_name in enumerate(boxes):
                # make everyone think box_name is our current controller 
                self.client.change_box(box_name)

                if run_name in ["tensorboard", "mirror"]:
                    text += self.get_box_process_status_inner(box_name, workspace, run_name)
                else:
                    text += self.core.get_box_run_status_inner(box_name, workspace, run_name, stage_flags)

            return text

        # MONITOR-ENABLED COMMAND
        attach.monitor_loop(monitor, monitor_work, escape_secs=escape_secs)

    def cancel_runs_by_names(self, workspace, run_names, box_name):
        '''
        Args:
            workspace: the name of the workspace containing the run_names
            run_names: a list of run names
            box_name: the name of the box the runs ran on (pool service)
        Returns:
            cancel_results: a list of kill results records 
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''

        # our strategy for this API: 
        #   - use the XT controller to kill specified runs (when controller is available)
        #   - use batch_client "cancel node" if controller not available

        # we build service-based box names to have 3 parts
        active_jobs = self.get_active_jobs(workspace)
        cancel_results = []
        if active_jobs:
            for job_record in active_jobs:
                service_job_info = job_record["service_job_info"]
                service_info_by_node = job_record["service_info_by_node"]
                
                for node, node_service_info in service_info_by_node.items():
                    if node_service_info.get("run_name") in run_names:
                        cancel_result = self.cancel_node(node_service_info)
                        cancel_results.append(cancel_result)

        return cancel_results

    def cancel_runs_by_property(self, prop_name, prop_value, box_name):
        cancel_results = None

        try:
            # connect to specified box
            if self.client.change_box(box_name):
                cancel_results = self.client.cancel_runs_by_property(prop_name, prop_value)
            else:
                console.print("couldn't connect to controller for {}".format(box_name))
        except BaseException as ex:
            errors.report_exception(ex)
            pass

        return cancel_results
        
    def cancel_runs_by_job(self, job_id, runs_by_box):
        '''
        Args:
            job_id: the name of the job containing the run_names
            runs_by_box: a dict of box_name/run lists
        Returns:
            cancel_results_by box: a dict of box_name, cancel_result records
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''
        cancel_results_by_box = {}

        for box_name, runs in runs_by_box.items():
            cancel_results = self.cancel_runs_by_property("job_id", job_id, box_name)
            cancel_results_by_box[box_name] = cancel_results

        return cancel_results_by_box

    def cancel_runs_by_user(self, ws_name, box_name):
        '''
        Args:
            box_name: the name of the box the runs ran on (pool service)
        Returns:
            cancel_results: a list of kill results records 
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''
        active_jobs = self.get_active_jobs(ws_name)
        cancel_results = []
        if active_jobs:
            for job_record in active_jobs:
                service_job_info = job_record["service_job_info"]
                service_info_by_node = job_record["service_info_by_node"]
                for node, node_service_info in service_info_by_node.items():
                    cancel_result = self.cancel_node(node_service_info)
                    cancel_results.append(cancel_result)

        return cancel_results

    def get_psm_client(self, service_node_info):
        box_os = service_node_info["box_os"]
        box_addr = service_node_info["box_addr"]
        is_box_windows = (box_os == "windows")

        if pc_utils.is_localhost(box_addr=box_addr):
            psm_client = LocalPsmClient()
        else:
            psm_client = RemotePsmClient(box_addr, is_box_windows)

        return psm_client

    # BACKEND API
    def read_log_file(self, service_node_info, log_name, start_offset=0, end_offset=None, 
        encoding='utf-8', use_best_log=True, log_source=None):
        '''
        returns subset of specified log file as text.
        '''
        job_id = service_node_info["job_id"]
        fn_entry = service_node_info["fn_entry"]

        # safe values for newly-added fields
        node_id = utils.safe_value(service_node_info, "node_id", "node0")
        workspace = utils.safe_value(service_node_info, "workspace", "<unavailable>")

        psm_client = self.get_psm_client(service_node_info)

        next_offset = 0
        new_text = None
        found_file = False

        if log_name is None:
            log_name = "stdboth.txt"
        file_path = os.path.basename(log_name)

        if log_source != "live":
            # try to read from service logs (job has completed), assuming we haven't already read some of LIVE log
            node_index = utils.node_index(node_id)

            job_path = "nodes/node{}/after/service_logs/{}".format(node_index, file_path)
            if self.core.store.does_job_file_exist(workspace, job_id, job_path):
                new_text = self.core.store.read_job_file(workspace, job_id, job_path)
                service_status = "completed"
                simple_status = "completed"
                found_file = True
                log_source = "after_logs"

        if not found_file:
            # read log from live node
            #start = time.time()
            new_bytes = psm_client.read_log_file(fn_entry, start_offset, end_offset)
            next_offset = start_offset + len(new_bytes)
            #utils.report_elapsed(start, "read log")

            new_text = new_bytes.decode(encoding)
            service_status = None

            if new_text:
                service_status = "running"
            else:
                # refresh STATUS 
                # we retry "completed" a few times to avoid a false positive when transitioning between the 
                # wrapper script and the controller app
                count = 10 if start_offset == 0 else 3

                for _ in range(count):
                    service_status = psm_client.get_status(fn_entry)
                    if service_status != "completed":
                        break

            simple_status = self.get_simple_status(service_status)
            log_source = "live"

        return {"new_text": new_text, "simple_status": simple_status, "log_name": log_name, "next_offset": next_offset, 
            "service_status": service_status, "log_source": log_source}

    # API call
    def get_simple_status(self, status):
        # translates an BATCH status to a simple status (queued, running, completed)

        queued = ["queued"]
        running = ["running"]
        completed = ["completed"]

        if status in queued:
            ss = "queued"
        elif status in running:
            ss = "running"
        elif status in completed:
            ss = "completed"
        else:
            errors.internal_error("unexpected Pool status value: {}".format(status))

        return ss

    # API call
    def cancel_job(self, service_job_info, service_info_by_node):
        result_by_node = {}

        for node_id, node_info in service_info_by_node.items():
            result = self.cancel_node(node_info)
            result_by_node[node_id] = result

        return result_by_node

    # API call
    def cancel_node(self, service_node_info):

        psm_client = self.get_psm_client(service_node_info)
        fn_entry = service_node_info["fn_entry"]

        service_status = psm_client.get_status(fn_entry)
        simple_status = self.get_simple_status(service_status)
        cancelled = False

        if simple_status != "completed":
            
            cancelled, service_status = psm_client.cancel(fn_entry)
            simple_status = self.get_simple_status(service_status)

        result = {"cancelled": cancelled, "service_status": service_status, "simple_status": simple_status}
        return result

    # API call
    def get_service_queue_entries(self, service_node_info):

        psm_client = self.get_psm_client(service_node_info)
        entries, current = psm_client.enum_queue()

        queue = []
        
        if entries:
            queue = [{"name": entry, "current": False} for entry in entries]

        if current:
            queue.insert(0, {"name": current, "current": True})

        return queue

    def get_active_jobs(self, ws_name):
        ''' return a list of job_id's running on this instance of Azure Batch '''
        db = self.client.store.get_database()

        filter_dict = {
            "username": self.username,
            "compute": "local",
            "ws_name": self.config.get("general", "workspace"),
            "job_status": {
                "$nin": ["created", "completed"]
            }
        }

        fields_dict = {"job_id": 1, "service_info_by_node": 1, "service_job_info": 1}

        job_records = db.get_info_for_jobs(ws_name, filter_dict, fields_dict)

        return job_records

   # API call
    def add_service_log_copy_cmds(self, ca, cmds, dest_dir, args):
        # if using docker, must use /usr/src/logs for log dir
        docker_cmd = args["docker_cmd"]
        
        if self.gen_for_windows:
            ca.append(cmds, "xcopy logs\* {}\\".format(dest_dir))
        else:
            if docker_cmd:
                ca.append(cmds, "mkdir {} && cp /usr/src/logs/* {}".format(dest_dir, dest_dir))
            else:
                ca.append(cmds, "mkdir {} && cp logs/* {}".format(dest_dir, dest_dir))
    # API call
    def get_log_files_dir(self, args):
        docker_cmd = args["docker_cmd"]

        path = "/usr/src/logs" if docker_cmd else "logs"
        return path
