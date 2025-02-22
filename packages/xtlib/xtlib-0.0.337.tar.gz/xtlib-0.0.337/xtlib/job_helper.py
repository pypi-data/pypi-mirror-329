#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# job_helper.py: functions needed for processing job-related information
import json
import time
import fnmatch
from typing import List

from .console import console
from .report_builder import ReportBuilder   

from xtlib import qfe
from xtlib import utils
from xtlib import errors
from xtlib import file_utils
from xtlib import store_utils
from xtlib import run_helper
from xtlib import query_helper

'''
To add a new job info column (defined at job submit time):
    - add it to the following job_helper.py dicts:
        - add to "job_info_props" dict
        - add to "user_to_actual" dict (recommend using same name for friendly name)
        - add to "std_cols_desc" dict (describes what the column holds)

    - add it to the following odbc.py dicts:
        - the job_info sub-dict in _init_core_tables()

    - add it to runner.py:
        - in the "dd" dict that is passed to the call: self.store.log_job_info()

'''

job_info_props = {"_id": 1, "aml_compute": 1, "compute": 1, "compute_target": 1,"concurrent": 1, "exper_name": 1, "hold": 1, "job_id": 1, "job_num": 1,
    "job_guid": 1, "job_secret": 1, "location": 1, "low_pri": 1, "node_count": 1, "num_dgd_seeds": 1, "primary_metric": 1, "run_count": 1, "repeat": 1, 
    "schedule": 1, "search_type": 1, "search_style": 1, "service_name": 1, "service_type": 1, "username": 1, "xt_cmd": 1, "started": 1,
    "pool_info": 1, "service_job_info": 1, "sku": 1, "sla": 1, "schedule": 1, "sleep_on_exit": 1, "vm_size": 1, "ws_name": 1}

job_stats_props = {"job_status": 1, "completed_runs": 1, "error_runs": 1, "running_runs": 1, "run_started": 1,
    "running_nodes": 1, "total_runs": 1, "db_retries": 1, "storage_retries": 1,
    "restarts": 1, "next_run_index": 1, "queue_duration": 1, "run_duration": 1, "heartbeat": 1, "end_time": 1}

all_job_props = {**job_info_props, **job_stats_props}


def is_job_id(name):
    '''
    needs to handle:
        prefix-job234
        job234-job434
    '''
    # is_job = False
    # if name.startswith("job"):
    #     part = name[3:]
    #     if part.isdigit():
    #         is_job = True

    # return is_job
    
    # compatible with version 1 (prefix-jobNNNN) and version 2 (jobNNNN)
    return "job" in name.lower()

def expand_job_list(store, db, workspace, name_list, can_mix=True):
    '''
    parse jobs, expand job ranges
    '''
    actual_ws = None
    job_list = None

    if name_list:
        first_name = name_list[0]
        if len(name_list)==1 and file_utils.has_wildcards(first_name):
            # match wildcard to all job names in workspace
            filter_dict = {}

            if workspace:
                filter_dict["ws_name"] = workspace

            all_names = db.get_job_names(filter_dict)
            job_list = [jn for jn in all_names if fnmatch.fnmatch(jn, first_name)]
        else:            
            job_list, actual_ws = parse_job_list(store, workspace, name_list, can_mix=can_mix)
    else:
        actual_ws = workspace
        job_list = name_list

    return job_list, actual_ws

def set_job_tags(store, db, name_list, tag_list, ws_name, tag_dict, clear):
    job_list, actual_ws = expand_job_list(store, db, ws_name, name_list, can_mix=True)
    
    if job_list:

        filter_dict = {"job_id": {"$in": job_list}}
        matched_count = db.set_job_tags(ws_name, filter_dict, tag_dict, clear)

        if clear:
            console.print("{} jobs updated, tags cleared: {}".format(matched_count, tag_list))
        else:
            console.print("{} jobs updated, tags set: {}".format(matched_count, tag_list))

    else:
        console.print("no matching jobs found")


def list_job_tags(store, db, ws_name, name_list, tag_list, sort):
    job_list, actual_ws = expand_job_list(store, db, ws_name, name_list, can_mix=True)

    if job_list:
        filter_dict = {"job_id": {"$in": job_list}}
        #fields_dict = {"tags": 1}
        fields_dict = {"tags": 1}

        records = db.get_info_for_jobs(ws_name, filter_dict, fields_dict)
        for record in records:
            job = record["_id"]
            console.print("{}:".format(job))

            if "tags" in record:
                tags = record["tags"] 
                tag_names = list(tags.keys())

                if sort == "ascending":
                    tag_names.sort()
                elif sort == "descending":
                    tag_names.sort(reverse=True)
                elif sort:
                    raise Exception("Unrecognized sort value: {}".format(sort))

                for tag in tag_names:
                    if tag_list and not tag in tag_list:
                        continue
                    console.print("  {}: {}".format(tag, tags[tag]))
    else:
        console.print("no matching jobs found")

def build_filter_part(fd, args, arg_name, store_name):
    value = utils.safe_value(args, arg_name)
    if value:
        if isinstance(value, list):
            fd[store_name] = {"$in": value}
        else:
            fd[store_name] = value

def build_job_filter_dict(ws_name, job_list, user_to_actual, builder, workspace, args):
    fd = {}
    option_filters = ["experiment", "compute_target", "service_type", "username", "status"]   # "application"

    if job_list:
        # filter by specified job names
        job_list = [store_utils.make_id(ws_name, job) for job in job_list]
        fd["_id"] = {"$in": job_list}

    # filter by workspace
    if workspace:
        fd["ws_name"] = workspace
        
    # filter by specified options
    for name in option_filters:
        build_filter_part(fd, args, name, user_to_actual[name])

    # filter by filter_list
    filter_exp_list = args["filter"]          
    if filter_exp_list:
        builder.process_filter_list(fd, filter_exp_list, user_to_actual)

    # filter by tag
    if "tag" in args:
        tag_name = args["tag"]
        if tag_name:
                fd["tags." + tag_name] = {"$exists": True}

    # filter by tags_all
    tags_all = args["tags_all"]
    if tags_all:
        for tag in tags_all:
            fd["tags." + tag] = {"$exists": True}

    # filter by tags_any
    tags_any = args["tags_any"]
    if tags_any:
        fany_list = []
        
        for tag in tags_any:
            f = {"tags." + tag: {"$exists": True}}
            fany_list.append(f)

        # or all of fany conditions together
        fd["$or"] = fany_list

    # filter by tags_none
    if "tags_none" in args:
        tags_none = args["tags_none"]
        if tags_none:
            for tag in tags_none:
                fd["tags." + tag] = {"$exists": False}

    return fd

# NEW COLS: sla, low_pri, vm_size, sku, service_name, service_type, aml_compute, compute_target, num_dgd_seeds
# LEGACY column for old jobs: "compute" (logged as "target")

user_to_actual = {"aml_compute": "aml_compute", "cluster": "cluster", "compute_target": "compute_target", 
    "docker": "environment", "experiment": "exper_name",
    "hold": "hold", "hparams": "hparams", "job": "job_id","job_num": "job_num", "location": "location", "low_pri": "low_pri", "num_dgd_seeds": "num_dgd_seeds",
    "node_count": "node_count", "primary_metric": "primary_metric", "queue": "queue", 
    "repeat": "repeat", "schedule": "schedule", "search": "search_type", "service_name": "service_name", 
    "service_type": "service_type", "sku": "sku", "sleep_on_exit": "sleep_on_exit", 
    "runs": "run_count", "search_style": "search_style", "sla": "sla", 
    "started": "started", "tags": "tags", "target": "compute", "username": "username", "xt_cmd": "xt_cmd",
    "vc": "vc", "vm_size": "vm_size", "workspace": "ws_name",  
     
    # dynamic properties (get updated at various stages of job)
    "status": "job_status", "running_nodes": "running_nodes", 
    "running_runs": "running_runs", "error_runs": "error_runs", "completed_runs": "completed_runs",
    "total_runs": "total_runs", "db_retries": "db_retries", "storage_retries": "storage_retries",
    "restarts": "restarts", "next_run_index": "next_run_index",
    "queue_duration": "queue_duration", "run_duration": "run_duration", "heartbeat": "heartbeat", "end_time": "end_time",
    "run_started": "run_started",
    }

std_cols_desc = {
    # the key here is the USER friendly name (not the physical name)
    "aml_compute": "the AML compute name specified in the target for this job",
    "cluster": "the Philly Cluster that the job ran on",
    "compute_target": "the name of the compute target specified for this job",
    "docker": "the Docker environment specified for this job",
    "experiment": "the experiment associated with the job",
    "hold": "if the Azure Batch pool for this job was requested to be held open after runs were completed",
    "job": "the job name",
    "job_num": "the sort compatible, numeric portion of the job_id",
    "location": "the location (aka region) of the compute for the job",
    "low_pri": "if the nodes requested for this job were specified as preemptable",
    "node_count": "the number of compute nodes requested for this job",
    "num_dgd_seeds": "the number of random HP configurations used to initialize the DGD search",
    "primary_metric": "the name of the metric used for hyperparameter searching",
    "queue": "the Philly queue that the job was submitted to",
    "repeat": "the repeat count specified for the job",
    "runs": "the total number of runs for the job",
    "run_started": "the datetime when the first node of the job was started",
    "schedule": "how runs are assigned to nodes (static or dynamic)",
    "search": "the type of hyperparameter search requested",
    "search_style": "describes how search is being accomplished (one of: static, dynamic, multi, repeat, single)",
    "service_name": "the name of the service specified in the target for this job",
    "service_type": "the service type of the target specified for this job",
    "sku": "the machine type requested for this job",
    "sla": "the singularity service level specified for this job",
    "sleep_on_exit": "the amount of time controller should wait before it's normal process exist",
    "started": "the datetime when the job was started",
    "target": "the name of the compute target the job was submitted to",
    "username": "the login name of the user who submitted the job",
    "vc": "the Philly Virtual Cluster that the job ran on",
    "vm_size": "the Azure Batch machine size requested for this job",
    "workspace": "the workspace associated with the job",
    "xt_cmd": "the XT command line used to start the job",

    # dynamic properties (get updated at various stages of job)
    "completed_runs": "the number of runs that have completed (with or without errors)",
    "error_runs": "the number of runs that have terminated with an error",
    "db_retries": "the total number of database retries performed by the runs of this node",
    "end_time": "the datetime when the job was completed",
    "heartbeat": "the last time the job was updated",
    "next_run_index": "the number to be used for the next dynamic run within the job",
    "queue_duration": "the amount of time the job spent in the queue",
    "restarts": "the number of times a node has been preempted and restarted",
    "run_duration": "the amount of time the job spent running",
    "running_nodes": "the number of nodes in the running state",
    "running_runs": "the number of this job's runs that are current running",
    "status": "one of: submitted, running, completed",
    "storage_retries": "the total number of storage retries performed by the runs of this node",
    "total_runs": "the total number of runs specified for the job",
}

def get_job_property_dicts():
    # user-friendly property names for jobs
    return user_to_actual, std_cols_desc

def get_job_property_internal_name(name):
    if name in user_to_actual:
        return user_to_actual[name]
    return None

def get_list_jobs_records(store, config, user_columns, args):
    list_nodes = utils.safe_value(args, "list_nodes")

    job_list = args["node_list"] if list_nodes else args["job_list"]
    pool = args["target"]

    if job_list and store_utils.STORAGE_FORMAT == "1":
        # only use workspace if it was explictly set  
        workspace = None   
        explict = qfe.get_explicit_options()
        if "workspace" in explict:
            workspace = explict["workspace"]
    else:
        workspace = args["workspace"]

    console.diag("before ensure_workspace_exists")

    if workspace:
        store.ensure_workspace_exists(workspace, flag_as_error=True)

    console.diag("after ensure_workspace_exists")

    # get info about job properties
    user_to_actual, std_cols_desc = get_job_property_dicts()        
    actual_to_user = {value: key for key, value in user_to_actual.items()}

    builder = ReportBuilder(config, store)

    # get list of specified jobs
    db = store.get_database()
    job_list, actual_ws = expand_job_list(store, db, workspace, job_list)

    # build a filter dict for all specified filters
    filter_dict = build_job_filter_dict(workspace, job_list, user_to_actual, builder, workspace, args)

    hide_empty_cols = config.get("job-reports", "hide-empty-cols")

    # get the db records for the matching JOBS
    #console.print("gathering job data...", flush=True)
    records, limiter, limiter_value = builder.get_db_records(db, filter_dict, workspace, "jobs", actual_to_user, 
        user_columns=user_columns, hide_empty_cols=hide_empty_cols, args=args)

    return records, limiter, limiter_value, user_to_actual, builder


def list_jobs(store, config, args, compare=False):

    console.diag("job_helper.list_jobs")

    available = args["available"]
    if available in ["0", "none"]:
        available = None
    elif available in ["", "1", "all"]:
        available = "all"

    report_type = "job-reports"
    user_columns = utils.get_user_columns(args["columns"], report_type, config)

    if compare:
        args["columns"] = ["job", "hparams.*"]

    records, limiter, limiter_value, user_to_actual, builder \
        = get_list_jobs_records(store, config, user_columns=user_columns, args=args)

    console.diag("after get_list_jobs_records")

    if available:
        user_to_actual, std_cols_desc = get_job_property_dicts()        
        hparams_cols = run_helper.extract_dotted_cols(records, "hparams")
        std_cols = list(user_to_actual.keys())
        tag_cols = extract_tag_cols(records)
        lines = builder.available_cols_report("job", std_cols, std_cols_desc, hparams_list=hparams_cols, 
            tags_list=tag_cols, avail_filter=available)

        for line in lines:
            console.print(line)
    else:    
        if compare:
            # filter cols to those that are different
            diff_cols = run_helper.get_different_cols(records)
            args["columns"] = diff_cols 

        avail_list = list(user_to_actual.keys())
        lines, row_count, was_exported = builder.build_report(records, user_columns=user_columns, report_type=report_type, args=args)

        query_helper.print_report(lines, "jobs", config, store, args, builder, was_exported, row_count, limiter, limiter_value)

def extract_tag_cols(records):
    tag_dict = {}

    for record in records:
        if "tags" in record:
            tags = record["tags"]
            for tag in tags.keys():
                tag_dict[tag] = 1

    return list(tag_dict.keys())

def validate_job_name_with_ws(store, ws_name, job_name, validate):
    job_name = job_name.lower()
    if not is_job_id(job_name):
        return errors.syntax_error("Illegal job name: {}".format(job_name))

    exists = store.does_job_exist(ws_name, job_name)
    if validate and not exists:
        errors.store_error("job '{}' does not exist in workspace '{}'".format(job_name, ws_name))

def parse_job_helper(store, job, job_list, actual_ws, validate=True, can_mix=True):

    if not can_mix:
        validate_job_name_with_ws(store, actual_ws, job, validate)

    job_list.append(job)
    return actual_ws

def get_job_number(job):
    if not is_job_id(job):
        errors.syntax_error("illegal job name, must start with 'job'")

    # allow for import prefixes
    part = job.split("_")[-1]  
    if part.startswith("job"):
        part = part[3:] 
    return int(part)

def expand_job_range(store, ws_name, low, high, can_mix, job_list):
    low = get_job_number(low)
    high = get_job_number(high)

    for jx in range(low, high+1):
        jxx = "job" + str(jx)
        actual_ws = parse_job_helper(store, jxx, job_list, ws_name, False, can_mix=can_mix)

def parse_job_list(store, workspace, jobs, can_mix=False):
    actual_ws = workspace
    job_list = []

    if jobs:
        for job in jobs:
            job = job.strip()

            if "-" in job:
                # range specified
                low, high = job.split("-")
                expand_job_range(store, workspace, low, high, can_mix, job_list)
            else:
                actual_ws = parse_job_helper(store, job, job_list, actual_ws, can_mix=can_mix)
        
    #console.print("actual_ws=", actual_ws)
    return job_list, actual_ws

def validate_job_name(job_id):
    if job_id:
        safe_job_id = str(job_id)
        if not is_job_id(safe_job_id):
            errors.syntax_error("job id must start with 'job': " + safe_job_id)

def get_num_from_job_id(job_id):
    # job341
    return job_id[3:]

def get_client_cs(core, ws_name, job_id, node_index):
    '''
    instantiate the backend service that owns the specified job node and 
    request it's client connection string
    '''
    cs = None
    box_secret = None

    filter = {"_id": job_id}
    jobs = core.store.database.get_info_for_jobs(ws_name, filter, None)
    if not jobs:
        errors.store_error("unknown job_id: {}".format(job_id))

    job = jobs[0]
    node_id = utils.node_id(node_index)

    compute = utils.safe_value(job, "compute")
    secrets_by_node = utils.safe_value(job, "secrets_by_node")
    if not secrets_by_node:
        errors.store_error("unknown node_index={} for job={}".format(node_index, job_id))

    box_secret = utils.safe_value(secrets_by_node, node_id)

    service_info_by_node = utils.safe_value(job, "service_info_by_node")
    node_info = utils.safe_value(service_info_by_node, node_id)

    if compute and node_info:
        backend = core.create_backend(compute)
        cs = backend.get_client_cs(node_info)

    cs_plus = {"cs": cs, "box_secret": box_secret, "job": job}
    return cs_plus

def get_job_records(store, workspace, job_names, fields_dict=None):
    ''' return job records for specified job names'''

    db = store.get_database()

    filter_dict = {}
    filter_dict["job_id"] = {"$in": job_names}

    job_records = db.get_info_for_jobs(workspace, filter_dict, fields_dict)

    return job_records
    
def get_job_record(store, workspace, job_id, fields_dict = None):
    job_records = get_job_records(store, workspace, [job_id], fields_dict)
    if not job_records:
        errors.store_error("job {} does not exist".format(job_id))
    jr = job_records[0]
    return jr
    
def get_job_info_with_backend(store, core, workspace, job_id, node_index):
    
    # FYI: getting job record from storage: 2.75 secs, from db: 2.39 secs (db slightly faster)
    job_info = get_job_record(store, workspace, job_id, {"pool_info": 1, "username": 1, "service_info_by_node": 1})

    pool_info = job_info["pool_info"]
    target = pool_info["name"]
    username = job_info["username"]
    backend = core.create_backend(target, compute_def=pool_info, username=username)

    if not "service_info_by_node" in job_info:
        # db v2 requires a separate call for this
        service_info_by_node = store.database.get_service_info_by_node(workspace, job_id)
        job_info["service_info_by_node"] = service_info_by_node

    return backend, job_info

def get_service_node_info_with_backend(store, core, workspace, job_id, node_index):
    
    backend, job_info = get_job_info_with_backend(store, core, workspace, job_id, node_index)
    service_info_by_node = job_info["service_info_by_node"]  

    node_id = utils.node_id(node_index)
    service_node_info = service_info_by_node[node_id]

    return service_node_info, backend

def get_service_job_info(store, core, ws_name, job_id):

    # get JOB_INFO 
    job_info = get_job_record(store, ws_name, job_id, {"pool_info": 1, "service_job_info": 1, "service_info_by_node": 1})
    service_job_info = job_info["service_job_info"]
    service_info_by_node = job_info["service_info_by_node"]

    # # get SERVICE_INFO_BY_NODE
    # service_info_by_node = store.database.get_service_info_by_node(ws_name, job_id)
    # job_info["job_info"] = job_info

    target = job_info["pool_info"]["name"]
    backend = core.create_backend(target)

    return service_job_info, service_info_by_node, backend

# helper
def download_logs_from_storage(ws_name: str, store, items: List[str], job_id: str, node_index: int, store_path: str,
        dest_dir: str):

    job_path = "nodes/node{}/{}".format(node_index, store_path)
    new_items = store.download_files_from_job(ws_name, job_id, job_path, dest_dir)

    for ni in new_items:
        items.append(ni)

def is_job_name(name):
    is_valid = False
    low_name = name.lower()
    if low_name.startswith("job"):
        part = name[3:]
        if "_" in part:
            is_valid = part.replace("_", "").isdigit()
        elif "." in part:
            is_valid = part.replace(".", "").isdigit()
        else:
            is_valid = part.isdigit()

    return is_valid

def job_num(name):
    if not is_job_name(name):
        errors.syntax_error("illegal job name: {}".format(name))

    return int(name[3:])
