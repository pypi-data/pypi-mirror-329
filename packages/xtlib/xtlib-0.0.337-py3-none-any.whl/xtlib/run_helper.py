    #
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# run_helper.py: functions needed for processing run-related information
import json
import math
import fnmatch
import pandas as pd
from os import fdopen
from datetime import timedelta
from collections import defaultdict

from xtlib import qfe
from xtlib import utils
from xtlib import errors
from xtlib import constants
from xtlib import job_helper
from xtlib import file_utils
from xtlib import time_utils
from xtlib import store_utils
from xtlib.console import console
from xtlib.helpers import file_helper
from xtlib.helpers.feedbackParts import feedback as fb
from xtlib import query_helper 

run_info_props = {"_id": 1, "app_name": 1, "box_name": 1, "compute": 1, "cmd_line_args": 1, "create_time": 1, "description": 1, 
    "display_name": 1, "exper_name": 1,
    "from_ip": 1, "from_computer_name": 1, "hp_set": 1, "is_child": 1, "is_parent": 1, "is_outer": 1, "job_id": 1, 
    "node_index": 1, "path": 1, "repeat": 1, "script": 1, "run_index": 1, "run_name": 1, "run_num": 1, "run_guid": 1,
    "search_style": 1, "search_type": 1, "service_type": 1, "sku": 1, "username": 1, "ws_name": 1, 
    "xt_build": 1, "xt_version": 1, "xt_cmd": 1, "cluster": 1, "vc":1, "service_run_id": 1}

run_stats_props = {"status": 1, "start_time": 1, "last_time": 1, "exit_code": 1, "error_msg": 1, "restarts": 1, 
    "end_time": 1, "queue_duration": 1, "run_duration": 1, "end_id": 1, "metric_names": 1,
     "db_retries": 1, "storage_retries": 1}

all_run_props = {**run_info_props, **run_stats_props}

def expand_run_list(store, db, workspace, name_list):
    '''
    args:
        - db: instance of our database mgr
        - workspace: name of the workspace associated with name_list
        - name_list: a list of run sources (run_names, job_names, experiment_names)

    processing:
        - extract pure list of run names from the name_list (all runs must be from same workspace)

    returns:
        - pure run_list
        - actual workspace used

    special:
        - name_list is a comma separated list of entries
        - entry format:
            <name>           (run_name, job_name, or experiment_name)
            <run wildcard>   (must start with "run" and can contain "*" and "?" chars)
            <name>-<name>    (a range of run or job names)
    '''
    run_list = []
    actual_ws = workspace

    if name_list:
        for entry in name_list:
            if is_run_name(entry):
                actual_ws = expand_run_entry(store, db, workspace, run_list, entry)
            elif job_helper.is_job_id(entry):
                actual_ws = expand_job_entry(store, db, workspace, run_list, entry)
            else:
                actual_ws = expand_experiment_name(store, db, workspace, run_list, entry)

    return run_list, actual_ws

def expand_run_entry(store, db, ws_name, run_list, name):
    
    if name in ["*", "run*"]:
        # return  "all records" indicator
        sub_list = ["*"]
        actual_ws = ws_name
    elif "*" in name:
        #match wildcard to all run names in workspace
        re_pattern = utils.wildcard_to_regex(name)
        filter_dict = {"_id": {"$regex": re_pattern} }

        records = db.get_info_for_runs(ws_name, None, {"_id": 1})
        sub_list = [rec["_id"] for rec in records]
        actual_ws = ws_name
    else:            
        sub_list, actual_ws = parse_run_list(store, ws_name, [name])
        
    run_list += sub_list
    return actual_ws

def expand_job_entry(store, db, ws_name, run_list, job_term):
    '''
    Arguments:
        store: an instance of Store (access to storage) 
        db: an instance of Mongo (access to related mongoDB)
        workspace: name of the workspace to search within
        run_list: a list of run names being accumulated
        job_term: a single job_id, or range of job_id's (job3-job5)
    Processing:
        Expand job_term to a list of job_id's and then for each job, 
        add its run names to run_list
    '''
    from xtlib import job_helper

    # expand job name_entry into a list of job names
    job_list, actual_ws = job_helper.expand_job_list(store, db, ws_name, [job_term], can_mix=False)

    run_filter = {"job_id": {"$in": job_list}}
    records = db.get_info_for_runs(ws_name, run_filter, {"_id": 1, "run_num": 1})
    if records:
        # records are not in any order from db, so sort by run_num
        records.sort(key=lambda r: r["run_num"])

        names = [run["_id"] for run in records]
        run_list += names

    return actual_ws

def expand_experiment_name(store, db, ws_name, run_list, exper_name):

    actual_ws = ws_name

    run_filter = {"exper_name": exper_name}
    result = db.get_info_for_runs(ws_name, run_filter, {"_id": 1})
    if result:
        names = [run["_id"] for run in result]
        run_list += names

    return actual_ws

def set_run_tags(store, db, name_list, tag_list, ws_name, tag_dict, clear):
    run_list, actual_ws = expand_run_list(store, db, ws_name, name_list)

    if run_list:

        filter_dict = {"run_name": {"$in": run_list}}
        matched_count = db.set_run_tags(ws_name, filter_dict, tag_dict, clear)

        if clear:
            console.print("{} runs updated, tags cleared: {}".format(matched_count, tag_list))
        else:
            console.print("{} runs updated, tags set: {}".format(matched_count, tag_list))
    else:
        console.print("no matching runs found")

def list_run_tags(store, db, ws_name, name_list, tag_list, sort):
    run_list, actual_ws = expand_run_list(store, db, ws_name, name_list)

    if run_list:
        filter_dict = {"run_name": {"$in": run_list}}
        #fields_dict = {"tags": 1}
        fields_dict = {"tags": 1}

        records = db.get_info_for_runs(ws_name, filter_dict, fields_dict)
        for record in records:
            run = record["_id"]
            console.print("{}:".format(run))

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
        console.print("no matching run found")

def remove_run_stats(dd: dict):
    run_stats = {}

    for prop in run_stats_props.keys():
        if prop in dd:
            value = dd[prop]
            run_stats[prop] = value
            del dd[prop]

    return run_stats



user_to_actual = {"box": "box_name", "cmd_line_args": "cmd_line_args", "created": "create_time", "child": "is_child", "cluster": "cluster",
    "description": "description", "display_name": "display_name", "experiment": "exper_name", "exit_code": "exit_code", 
    "error_msg": "error_msg",
    "from_host": "from_computer_name", "from_ip": "from_ip", 
    "guid": "run_guid", "hp_set": "hp_set", "job": "job_id", "last_time": "last_time",
    "node_index": "node_index", "outer": "is_outer", "parent": "is_parent", "path": "path", 
    "pool": "pool", "repeat": "repeat", "restarts": "restarts", "run": "run_name", "run_index": "run_index", 
    "run_num": "run_num", "script": "script", "search": "search_type", "search_style": "search_style", 
    "service_type": "service_type", "sku": "sku", "started": "start_time", "status": "status", "target": "compute", 
    "username": "username", "vc": "vc", "workspace": "ws_name", "xt_build": "xt_build", "xt_cmd": "xt_cmd",
    "xt_version": "xt_version", "cluster": "cluster", "vc": "vc", "service_run_id": "service_run_id",

    # embedded properties
    "hparams": "hparams", "metrics": "metrics", "tags": "tags",

    # run stats
    "ended": "end_time", "started": "start_time", "duration": "run_duration", "queued": "queue_duration",
    "db_retries": "db_retries", "storage_retries": "storage_retries", "end_id": "end_id",

        # special info (not a simple property)
        "metric_names": "metric_names",
    }

std_cols_desc = {
    #"app": "the application associated with the run",
    "box": "the name of the box the run executed on",
    "child": "indicates that this run is a child run",
    "cluster": "the name of the service cluster for the run", 
    "cmd_line_args": "the script and its arguments used for this run", 
    "created": "the time when the run was created", 
    "ended": "when the run execution ended",
    "db_retries": "the total number of database retries performed by the runs of this node",
    "description": "the user specified description associated with the run",
    "display_name": "the singularity display name for this run",
    "duration": "how long the run has been executing",
    "end_id": "a unique serial number assigned to each run when it has ended",
    "ended": "when the run completed",
    "experiment": "the name of the experiment associated with the run",
    "error_msg": "set to the last stacktrace error seen in runs that terminate with an error",
    "exit_code": "the integer value returned by the run",
    "from_host": "the name of the computer that submitted the run",
    "from_ip": "the IP address of the computer that submitted the run",
    "guid": "a string that uniquely identifies the run",
    "hp_set": "a string that describes the hyperparameter search values used for the run",
    "job": "the job id that the run was part of",
    "last_time": "the time of the most recent operation associated with the run",
    "metric_names": "list of metrics names, ordered by their reporting",
    "node_index": "the 0-based node index of the run's box",
    "outer": "indicates this run is not a child run",
    "parent": "indicates that the run spawned child runs",
    "path": "the full path of the run's target script or executable file",
    "pool": "the user-defined name describing the backend service or set of boxes on which the run executed",
    "queued": "how long the run was waiting to start",
    "repeat": "the user-specified repeat-count for the run",
    "restarts": "the number of times the run was preempted and restarted",
    "run": "the name of the run",
    "run_index": "the job command index assigned to this run",
    "run_num": "the sort-compatible number portion of run",
    "script": "the base name of the run's script or executable file",
    "search": "the type of hyperparameter search used to start the run",
    "search_style": "describes how search is being accomplished (one of: static, dynamic, multi, repeat, single)",
    "service_type": "the type of service of the compute target",
    "service_run_id": "the run id assigned by the backend service",
    "sku": "the name of the service SKU (machine size) specified for the run",
    "started": "when the run started executing",
    "status": "the current status of the run",
    "storage_retries": "the total number of storage retries performed by the runs of this node",
    "target": "the compute target the run was submitted to",
    "username": "the login name of the user who submitted the run",
    "vc": "the name of the virtual cluster for the run",
    "workspace": "the name of the workspace containing the run",
    "xt_build": "the build date of xt that was used to launch the run",
    "xt_cmd": "the xt command used to initiate this run",
    "xt_version": "the version of xt that was used to launch the run",
    }

def get_run_property_dicts():
    # user-friendly property names for jobs

    return user_to_actual, std_cols_desc
        
def get_run_property_internal_name(name):
    if name in user_to_actual:
        return user_to_actual[name]
    return None

def build_filter_from_mixed_run_list(store, ws_name, run_list, fd):

    exper_names = []
    job_names = []
    run_names = []

    exper_fd = {}
    job_fd = {}
    run_fd = {}

    # group into experiments, jobs, runs
    for name in run_list:
        if "-" in name:
            low, high = name.split("-")
            if is_run_name(low):
                expand_run_range(store, ws_name, low, high, run_names)
            elif job_helper.is_job_id(low):
                job_helper.expand_job_range(store, ws_name, low, high, can_mix=False, job_list=job_names)
            else:
                errors.general_error("only runs and jobs can be used in ranges: {}".format(name))
        elif is_run_name(name):
            run_names.append(name)
        elif job_helper.is_job_id(name):
            job_names.append(name)
        else:
            # must be an experiment name
            # TODO: validate experiment name using database query on jobs 
            exper_names.append(name)
                
    # add EXPERIMENTS
    if len(exper_names) == 1:
        exper_fd["exper_name"] = exper_names[0]
    elif len(exper_names) > 1:
        exper_fd["exper_name"] = {"$in": exper_names}

    # add JOBS
    if len(job_names) == 1:
        job_fd["job_id"] = job_names[0]
    elif len(job_names) > 1:
        job_fd["job_id"] = {"$in": job_names}

    # add RUNS
    if len(run_names) == 1:
        run_fd["run_name"] = run_names[0]
    elif len(run_names) > 1:
        run_fd["run_name"] = {"$in": run_names}

    # merge them together
    fd_list = []
    for fdx in [exper_fd, job_fd, run_fd]:
        if fdx:
            fd_list.append(fdx)

    count = len(fd_list)
    if count == 1:
        # merge our only fdx into fd
        fd.update(fd_list[0])
    elif count > 1:
        # combine with an OR
        fd["$or"] = fd_list

def build_filter_part(fd, args, arg_name, store_name):
    value = args[arg_name]

    if value is not None:
        if isinstance(value, list):
            if len(value) == 1:
                fd[store_name] = value[0]
            else:
                fd[store_name] = {"$in": value}
        else:
            fd[store_name] = value

def build_run_filter_dict(store, ws_name, run_list, user_to_actual, builder, args):
    fd = {}
    option_filters = ["job", "experiment", "target", "service_type", "box", "status", "parent", "child", 
        "outer", "username", "node_index"]  

    # special hanndling for parent/child options
    parent = utils.safe_value(args, "parent")
    child = utils.safe_value(args, "child")
    if parent and child:
        # both specified, so we need to do an OR
        # best accomplished by turning them both off
        args["parent"] = None
        args["child"] = None

    if run_list:
        build_filter_from_mixed_run_list(store, ws_name, run_list, fd)

    use_explict_options = False

    if use_explict_options:
        # older approach: do we still need this?
        explict_options = qfe.get_explicit_options()
        explict_options = {key.replace("-", "_"): value for key,value in explict_options.items()}

        # # handle properties that are exceptions to needing to be explicit
        # for key in ["child", "parent"]:
        #     if (key in args) and (args[key] is not None) and (key not in explict_options):
        #         explict_options[key] = args[key]

        # filter by specified options
        for name in option_filters:
            if name in explict_options:
                build_filter_part(fd, args, name, user_to_actual[name])

    else:
        # filter by specified options
        for name in option_filters:
            if name in args:
                build_filter_part(fd, args, name, user_to_actual[name])

    # filter by filter_list
    if "filter" in args:
        filter_exp_list = args["filter"]
        if filter_exp_list:
            builder.process_filter_list(fd, filter_exp_list, user_to_actual)

    # filter by tag
    if "tag" in args:
        tag_name = args["tag"] 
        if tag_name:
                fd["tags." + tag_name] = {"$exists": True}

    # filter by tags_all
    if "tags_all" in args:
        tags_all = args["tags_all"]
        if tags_all:
            for tag in tags_all:
                fd["tags." + tag] = {"$exists": True}

    # filter by tags_any
    if "tags_any" in args:
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

def extract_dotted_cols(records, prefix):
    nd = {}
    prefix += "."
    prefix_len = len(prefix)

    for record in records:
        for key in record.keys():
            if key.startswith(prefix):
                col = key[prefix_len:]
                nd[col] = 1

    cols = list(nd.keys())
    return cols

def get_different_cols(records):
    # first pass, gather last value of each column seen
    col_values = {}
    for rd in records:
        col_values.update(rd)

    # second pass, build dict of diff columns
    diff_cols = {}
    for rd in records:
        for key, value in col_values.items():
            if not key in rd or rd[key] != value:
                diff_cols[key] = True

    return list(diff_cols)

def get_filtered_sorted_limit_runs(store, config, show_gathering, col_dict=None, preserve_order=False, 
        col_names_are_external=True, flatten_records=True, user_columns=None, args=None):
    # JIT import (workaround cyclic imports)
    from xtlib.report_builder import ReportBuilder   

    console.diag("start of: get_filtered_sorted_limit_runs")
    # required
    run_list = args["run_list"]

    # optional
    pool = utils.safe_value(args, "target")

    # correct value of available (can be on/off flag, or string to be used type of available column)
    available = utils.safe_value(args, "available")
    if available in ["0", "none"]:
        available = None
    elif available in ["", "1", "all"]:
        available = "all"

    args["available"] = available
        
    workspace = utils.safe_value(args, "workspace")

    # if not col_dict:
    #     col_list = utils.safe_value(args, "columns")
    #     if col_list:
    #         col_dict = {col: 1 for col in col_list}
    
    if workspace:
        store.ensure_workspace_exists(workspace, flag_as_error=False)

    db = store.get_database()

    # get info about run properties
    user_to_actual, std_cols_desc = get_run_property_dicts()        
    actual_to_user = {value: key for key, value in user_to_actual.items()}

    builder = ReportBuilder(config, store)

    # build a filter dict for all specified filters
    filter_dict = build_run_filter_dict(store, workspace, run_list, user_to_actual=user_to_actual, 
        builder=builder, args=args)

    if "latest" in args and args["latest"]:
        # only show the latest run for each job
        filter_dict["status"] = {"$ne": "restarted"}

    aux_filter = utils.safe_value(args, "aux_filter")
    if aux_filter:
        # merge filters together
        filter_dict = {**filter_dict, **aux_filter}

    # if show_gathering:
    #     console.print("gathering run data...", flush=True)

    highight_exp = config.get("run-reports", "highlight") 
    need_alive = highight_exp == "$alive"
    hide_empty_cols = config.get("run-reports", "hide-empty-cols")

    # get the db records for the matching RUNS
    records, limiter, limiter_value = builder.get_db_records(db, filter_dict, workspace, which="runs", 
        actual_to_user=actual_to_user, col_dict=col_dict, col_names_are_external=col_names_are_external, 
        flatten_records=flatten_records, need_alive=need_alive, user_columns=user_columns, hide_empty_cols=hide_empty_cols, 
        args=args)

    # remove key info from _id in records
    store_utils.simplify_records_id(records)

    sort = utils.safe_value(args, "sort")
    if preserve_order and not sort:
        # get list of specified runs
        pure_run_list, actual_ws = expand_run_list(store, db, workspace, run_list)
        if run_list and not pure_run_list:
            errors.general_error("no matching runs found")

        # remove key from pure_run_list
        pure_run_list = [pr.split("/")[-1] for pr in pure_run_list]
        records = order_runs_by_user_list(records, pure_run_list)

    console.diag("end of: get_filtered_sorted_limit_runs")

    return records, limiter, user_to_actual, available, builder, limiter_value, std_cols_desc

def order_runs_by_user_list(runs, user_list):
    new_records = list(user_list)

    for run in runs:
        run_name = run["_id"] if "_id" in run else run["run"]
        index = new_records.index(run_name)
        if index > -1:
            new_records[index] = run

    # finally, remove dummy entries
    new_records = [nr for nr in new_records if isinstance(nr, dict)]
    return new_records

def list_runs(store, config, args, compare=False):

    if compare:
        args["columns"] = ["job", "run", "hparams.*"]

    report_type = "run-reports"
    user_columns = utils.get_user_columns(args["columns"], report_type, config)

    records, limiter, user_to_actual, available, builder, limiter_value, std_cols_desc = \
        get_filtered_sorted_limit_runs(store, config, show_gathering=True, 
            col_names_are_external=True, flatten_records=True, user_columns=user_columns, args=args)

    if available:
        std_cols = list(user_to_actual.keys())
        hparams_cols = extract_dotted_cols(records, "hparams")
        metrics_cols = extract_dotted_cols(records, "metrics")
        tags_cols = extract_dotted_cols(records, "tags")

        lines = builder.available_cols_report("run", std_cols, std_cols_desc, hparams_list=hparams_cols, 
            metrics_list=metrics_cols, tags_list=tags_cols, avail_filter=available)

        for line in lines:
            console.print(line)
    else:            
        if compare:
            # filter cols to those that are different
            diff_cols = get_different_cols(records)
            
            # remove any cols that user want to hide
            omit_cols = args["omit_columns"]
            for omit in omit_cols:
                if omit in diff_cols:
                    diff_cols.remove(omit)

            args["columns"] = diff_cols 
            user_columns = utils.get_user_columns(args["columns"], report_type, config)

        #avail_list = list(user_to_actual.keys())
        lines, row_count, was_exported = builder.build_report(records, user_columns=user_columns, report_type=report_type, args=args)

        query_helper.print_report(lines, "runs", config, store, args, builder, was_exported, row_count, limiter, limiter_value)

def get_run_record(store, workspace, run_name, fields_dict = None):
    run_records = get_run_records_simple(store, workspace, [run_name], fields_dict)
    if not run_records:
        errors.store_error("Run {} does not exist in workspace {}".format(run_name, workspace))
    rr = run_records[0]
    return rr

def get_job_node_index(store, core, workspace, run_name):
    rr = get_run_record(store, workspace, run_name, {"job_id": 1, "node_index": 1})
    job_id = rr["job_id"]
    node_index = rr["node_index"]
    return job_id, node_index

def get_service_node_info_with_backend(store, core, workspace, run_name):
    rr = get_run_record(store, workspace, run_name, {"job_id": 1, "node_index": 1})
    job_id = rr["job_id"]
    node_index = rr["node_index"]

    return job_helper.get_service_node_info_with_backend(store, core, workspace, job_id, node_index)
    
def get_rightmost_run_num(run):
    if not is_run_name(run):
        errors.syntax_error("Illegal run name, must start with 'run'")

    if "." in run:
        prefix, num = run.split(".")
        prefix += "."
    else:
        num = run[3:]
        prefix = "run"

    num = int(num)
    return num, prefix

def parse_run_helper(store, workspace, run, validate, actual_ws, run_names):
    if validate:
        ws, run_name, full_run_name = validate_run_name(store, workspace, run)

        run_names.append(run_name)
        actual_ws = ws
    else:
        run_names.append(run)
        if not actual_ws:
            actual_ws = workspace

    return actual_ws

def correct_slash(name):
    if "\\" in name:
        name = name.replace("\\", "/")
    return name

def expand_run_range(store, ws_name, low, high, run_names):
    low, low_prefix = get_rightmost_run_num(low)
    high, high_prefix = get_rightmost_run_num(high)

    if low_prefix != high_prefix:
        errors.user_error("for run name range, prefixes must match: {} vs. {}".format(low_prefix, high_prefix))

    for rx in range(low, high+1):
        rxx = low_prefix + str(rx)
        actual_ws = parse_run_helper(store, ws_name, rxx, validate=True, actual_ws=ws_name, run_names=run_names)

def parse_run_list(store, ws_name, runs, validate=True):
    run_names = []
    actual_ws = None

    if runs:
        for run in runs:
            run = run.strip()
            run = correct_slash(run)

            if "/" in run:
                ws, run_name = run.split("/")
                if actual_ws and actual_ws != ws:
                    errors.syntax_error("Cannot mix run_names from different workspaces for this command")

            if not is_run_name(run):
                errors.argument_error("run name", run)

            if "-" in run:
                # parse run range
                low, high = run.split("-")
                expand_run_range(store, ws_name, low, high, run_names)                
            else:
                actual_ws = parse_run_helper(store, ws_name, run, validate, actual_ws, run_names)
    else:
        actual_ws = ws_name
        
    #console.print("actual_ws=", actual_ws)
    return run_names, actual_ws   

def parse_run_name(workspace, run):
    actual_ws = None
    run_name = None

    run = correct_slash(run)
    if "/" in run:
        actual_ws, run_name = run.split("/")
    else:
        run_name = run
        actual_ws = workspace

    return run_name, actual_ws

def full_run_name(store_type, ws, run_name):
    #return "xt-{}://{}/{}".format(store_type, ws, run_name)
    run_name = correct_slash(run_name)
    if "/" in run_name:
        full_name = run_name
    else:
        full_name = "{}/{}".format(ws, run_name)
    return full_name

def is_well_formed_run_name(text):
    well_formed = True
    if not "*" in text:
        text = correct_slash(text)
        if "/" in text:
            parts = text.split("/")
            if len(parts) != 2:
                well_formed = False
            elif not is_run_name(parts[1]):
                well_formed = False
        elif not is_run_name(text):
            well_formed = False
    return well_formed

def validate_run_name(store, ws, run_name, error_if_invalid=True, parse_only=False):
    run_name = correct_slash(run_name)
    if "/" in run_name:
        parts = run_name.split("/")
        if len(parts) != 2:
            errors.syntax_error("invalid format for run name: " + run_name)
        ws, run_name = parts

    run_name = run_name.lower()
    if not parse_only and not "*" in run_name:
        if not store.database.does_run_exist(ws, run_name):
            if error_if_invalid:
                errors.store_error("run '{}' does not exist in workspace '{}'".format(run_name, ws))
            else:
                return None, None, None
    return ws, run_name, ws + "/" + run_name

def build_metrics_sets(records, steps=None, merge=False, metrics=None, timebase=None, cleanup=True, 
    alias_to_actual=None):
    '''
    Args:
        records: the set of dict records of a run log.
        steps: an optional list of step values to filter by (return only matching step records).
        merge: when True, merge all datasets into a single one
        metrics: list of specific metric names to extract
        cleanup: when True, restarts are detected and their older records are removed 
        alias_to_actual: a dict of name/value pairs.  if defined, use to translate metric names (from name to value).

    Processing:
        We process all "metrics" event log records, grouping each by their property names.  Each group is a metric set.

    '''
    # first step: put each metric into their own set (with time-stamped records)
    metric_sets_by_keys = {}
    step_index = None
    next_step = None
    step_name = None
    step_value = None
    
    # for merge
    last_record = {}
    last_step = None
    merged_records = []
    need_run_start = False
    need_first_metric = False
    time_offset = None

    if timebase == "none":
        timebase = None
    elif timebase == "run":
        need_run_start = True
    elif timebase == "metric":
        need_first_metric = True
    else:
        errors.UserError("unrecognized timebase value: {}".format(timebase))

    if steps:
        step_index = 0
        next_step = steps[0]

    for log_dict in records:
        if not log_dict:
            continue

        if need_run_start and "event" in log_dict and log_dict["event"] == "started":
            arrow_str = log_dict["time"]
            time_offset = time_utils.parse_time(arrow_str).timestamp()
            need_run_start = False

        if not "event" in log_dict or not "data" in log_dict or log_dict["event"] != "metrics":
            continue

        # this is a metric record
        if need_first_metric:
            arrow_str = log_dict["time"]
            time_offset = time_utils.parse_time(arrow_str).timestamp()
            need_first_metric = False

        dd = log_dict["data"]

        if alias_to_actual:
            # translate metric names
            key_list = list(dd.keys())
            
            for key in key_list:
                if key in alias_to_actual:
                    actual = alias_to_actual[key]
                    utils.rename_dict_key(dd, key, actual)
        
        # sort items by keys to ensure matches by all-key-string 
        dd = dict(sorted(dd.items()))

        if step_name is None:
            if "step" in dd:
                step_name = "step"
            elif "epoch" in dd:
                step_name = "epoch"
            elif "iter" in dd:
                step_name = "iter"
            elif constants.STEP_NAME in dd:
                step_name = dd[constants.STEP_NAME]

        if step_name:
            step_value = dd[step_name]

            if steps:
                # filter this record (skip if neq next_step)
                while step_value > next_step:
                    # compute next step
                    step_index += 1
                    if step_index < len(steps):
                        next_step = steps[step_index]
                    else:
                        # found all specified steps
                        break

                if step_value < next_step:
                    continue

        # add time to record
        arrow_str = log_dict["time"]
        dt = time_utils.parse_time(arrow_str)
        if time_offset:
            dt = dt - timedelta(seconds=time_offset)
        dd[constants.TIME] = dt

        if metrics:
            # only collect step_name and metrics in "metrics"
            dd2 = {}
            dd2[step_name] = dd[step_name]
            for name, value in dd.items():
                if name in metrics:
                    dd2[name] = value

            # store back into dd
            dd = dd2

        if merge:
            if last_step == step_value:
                # add to last_record
                for name, value in dd.items():
                    last_record[name] = value
            else:
                merged_records.append(dd)
                last_record = dd
                last_step = step_value
        else:
            # collect into multiple metric sets
            keys = list(dd.keys())
            #keys.sort()
            keys_str = json.dumps(keys)

            if not keys_str in metric_sets_by_keys:
                metric_sets_by_keys[keys_str] = []

            metric_set = metric_sets_by_keys[keys_str]
            metric_set.append(dd)

    metric_sets = []

    if merge:
        # build set of keys that covers all records
        keys = {}
        for dd in merged_records:
            for name in dd:
                keys[name] = 1

        key_list = list(keys.keys())

        df = {"keys": key_list, "records": merged_records}
        metric_sets.append(df)
    else:
        for keys_str, records in metric_sets_by_keys.items():
            df = {"keys": json.loads(keys_str), "records": records}
            metric_sets.append(df)

    if cleanup and step_name:
        for ms in metric_sets:
            if has_restarts(ms["records"], step_name):
                ms["records"] = cleanup_metric_set(ms["records"], step_name)
                assert not has_restarts(ms["records"], step_name)

    return metric_sets

def has_restarts(orig_records, step_name):
    '''
    Return True if log metric records have 1 or more restarts.
    '''
    last_step = None
    restart_count = 0

    # process list backwards
    records = list(orig_records)
    records.reverse()

    for dd in records:
        step = dd[step_name]
        if not last_step or step < last_step:
            last_step = step
        else:
            # RESTART detected
            restart_count += 1
            #console.print("skipping step: {}".format(step))

    return restart_count > 0

def cleanup_metric_set(orig_records, step_name):
    '''
    Processing:
        Remove out of order records (caused by run restarts).
    '''
    last_step = None
    new_records = []
    restart_count = 0

    # process list backwards
    records = list(orig_records)
    records.reverse()

    for dd in records:
        step = dd[step_name]
        if not last_step or step < last_step:
            new_records.append(dd)
            last_step = step
        else:
            # RESTART detected
            restart_count += 1
            #console.print("skipping step: {}".format(step))

    if restart_count:
        console.diag("  restarts removed: {}".format(restart_count))

    # need to reverse the new list
    new_records.reverse()

    return new_records

def get_int_from_run_name(run_name):
    id = float(run_name[3:])*100000
    id = int(id)
    return id

def get_client_cs(core, ws, run_name):

    cs = None
    box_secret = None

    filter = {"_id": run_name}
    runs = core.store.database.get_info_for_runs(ws, filter, {"run_logs": 0})
    if not runs:
        errors.store_error("Unknown run: {}/{}".format(ws, run_name))

    if runs:
        from xtlib import job_helper

        run = runs[0]
        job_id = utils.safe_value(run, "job_id")
        node_index = utils.safe_value(run, "node_index")

        cs_plus = job_helper.get_client_cs(core, job_id, node_index)
        cs = cs_plus["cs"]
        box_secret = cs_plus["box_secret"]

    return cs, box_secret

def get_job_context(store, job_id, workspace):
    # get job_record
    job_info = job_helper.get_job_record(store, workspace, job_id)
    ws_name = job_info["ws_name"]

    # loads the controller's MRC for context of this node
    if store.does_job_file_exist(workspace, job_id, constants.FN_MULTI_RUN_CONTEXT):
        text = store.read_job_file(workspace, job_id, constants.FN_MULTI_RUN_CONTEXT)
    else:
        # need to download xt_code.zip and extract MRC file (why different for some jobs?)
        tmp_dir = file_utils.make_tmp_dir("unzip_code")
        fn_zip_local = "{}/{}".format(tmp_dir, constants.CODE_ZIP_FN)
        store_path = "before/code/{}".format(constants.CODE_ZIP_FN)
        store.download_file_from_job(workspace, job_id, store_path, fn_zip_local)

        # now, extract the MRC file
        file_helper.unzip_file(fn_zip_local, constants.FN_MULTI_RUN_CONTEXT, tmp_dir)
        fn_mrc = "{}/{}".format(tmp_dir, constants.FN_MULTI_RUN_CONTEXT)
        text = file_utils.read_text_file(fn_mrc)

    mrc_data = json.loads(text)
    return mrc_data

def get_wrapup_runs_for_node_list(store, ws_name, job_id, node_list, max_workers):

    mrc_data = get_job_context(store, job_id, ws_name)
    context_by_nodes = mrc_data["context_by_nodes"]

    node_indexes = [utils.node_index(node_id) for node_id in node_list]

    filter_dict = {"job_id": job_id, "node_index": {"$in": node_indexes}, "status": {"$nin": ["error", "completed", "cancelled", "restarted"]}}
    fields_dict = {"status": 1, "run_index": 1, "run_name": 1, "node_index": 1, "create_time": 1, "start_time": 1, "is_parent": 1 }

    # get runs for specified nodes
    runs = store.database.get_info_for_runs(ws_name, filter_dict, fields_dict)

    # filter runs to those that need wrapping up
    filtered_runs = []
    unwrapped = ["created", "queued", "spawning", "allocating", "running"]

    for run in runs:
        # watch our for runs that never got promoted to "queued", so they are missing a status
        status = utils.safe_value(run, "status", "created")
        if status in unwrapped:
            filtered_runs.append(run)

    return runs, context_by_nodes

def wrapup_runs_nodes_job(store, ws_name, job_id, node_ids, node_end_times, max_workers):
    '''
    wrap up a run.  run may have started, or may have completed.  
    '''
    fb.reset_feedback()
    node_ended_run_counts = defaultdict(int)

    run_list, context_by_nodes = get_wrapup_runs_for_node_list(store, ws_name, job_id, node_ids, max_workers)
    if run_list:
        # mark each run as cancelled
        next_progress_num = 1

        from threading import Lock
        worker_lock = Lock()

        def run_thread_worker(runs, store):

            for run in runs:
                node_index = run["node_index"]
                node_id = utils.node_id(node_index)
                run_name = run["run_name"]
                run_status = "cancelled"
                create_time = run["create_time"]
                start_time = run["start_time"]
                node_end_time = node_end_times[node_id]

                store.database.mark_run_ended_in_past(ws_name, run_name, run_status, create_time=create_time, start_time=start_time, end_time=node_end_time, exit_code=None, error_msg=None)

                with worker_lock:
                    nonlocal next_progress_num
                    node_msg = "wrapping up runs: {}/{}".format(next_progress_num, len(run_list))
                    fb.feedback(node_msg, id="wrapup_msg")  

                    next_progress_num += 1
                    node_ended_run_counts[node_id] += 1

        utils.run_on_threads(run_thread_worker, run_list, max_workers, [store])
        fb.feedback("done", is_final=True)
    
    if node_ids:
        # mark each node as cancelled
        next_progress_num = 1

        from threading import Lock
        worker_lock = Lock()

        # get nodes for specified node_ids
        filter_dict = {"ws_name": ws_name, "job_id": job_id, "node_id": {"$in": node_ids}}
        fields_dict = {"job_id": 1, "target": 1, "node_index": 1, "node_id": 1, "node_status": 1, "ws_name": 1,
                       "create_time": 1, "prep_start_time": 1, "app_start_time": 1, "post_start_time": 1, "post_end_time": 1,
                       "completed_runs": 1, "error_runs": 1}
        node_list = store.database.get_info_for_nodes(ws_name, filter_dict, fields_dict)

        def node_thread_worker(nodes, store):

            for node in nodes:
                node_id = node["node_id"]
                node_end_count = node_ended_run_counts[node_id]
                node_end_time = node_end_times[node_id]
                node_status = "cancelled"

                #wrapup_run_with_context(store, run, context, job_id=job_id)
                store.database.mark_node_ended_in_past(ws_name, job_id, node, node_status, node_end_time, node_end_count, 0)

                with worker_lock:
                    nonlocal next_progress_num
                    node_msg = "wrapping up nodes: {}/{}".format(next_progress_num, len(node_list))
                    fb.feedback(node_msg, id="wrapup_msg")  

                    next_progress_num += 1

        utils.run_on_threads(node_thread_worker, node_list, max_workers, [store])
        fb.feedback("done", is_final=True)

    # finally, mark the job as CANCELLED
    filter_dict = {"ws_name": ws_name, "job_id": job_id}
    fields_dict = {"job_id":1, "started": 1, "run_started": 1, "completed_runs": 1, "error_runs": 1}
    jobs = store.database.get_info_for_jobs(ws_name, filter_dict, fields_dict)
    job = jobs[0]
    job_status = "cancelled"
    job_end_time = max(node_end_times.values())
    job_runs_ended = sum(node_ended_run_counts.values())

    store.database.mark_job_ended_in_past(ws_name, job_id, job_status, job, end_time_secs=job_end_time, 
        new_completed_runs=job_runs_ended, new_error_runs=None)
    console.print("wrapped up job: {}".format(job_id))

def wrapup_run_with_context(store, run, context_dict, job_id=None):
    context = utils.dict_to_object(context_dict)
    if job_id:
        context.job_id = job_id
        
    status = "cancelled"
    exit_code = 0
    node_id = utils.node_id(context.node_index)

    # use info from run, when possible (context is shared among all child runs)
    run_index = utils.safe_value(run, "run_index")
    run_name = run["run_name"]

    # these we don't have info for
    rundir = None    # unknown
    log = True
    capture = True

    store.wrapup_run(context.ws, run_name, context.aggregate_dest, context.dest_name, 
        status, exit_code, context.primary_metric, context.maximize_metric, context.report_rollup, 
        rundir, context.after_files_list, log, capture, job_id=context.job_id, node_id=node_id,
        run_index=run_index)    

def get_run_records_simple(store, ws_name, run_names, fields_dict=None):
    ''' return run records for specified run names'''

    db = store.get_database()

    filter_dict = {}
    filter_dict["run_name"] = {"$in": run_names}

    if not fields_dict:
        # by default, get everything but the log records
        #fields_dict = {"log_records": 0}
        fields_dict = {"run_info": 1, "run_stats": 1}

    run_records = db.get_info_for_runs(ws_name, filter_dict, fields_dict)

    return run_records

def get_store(config=None):
    # JIT import to prevent circular references
    from xtlib.storage.store import Store
    from xtlib.helpers.xt_config import get_merged_config

    if config is None:
        config = get_merged_config()
    store = Store(config=config)

    return store

def get_run_records(job_id, run_ids=None,  metric_names=None, filter_dict=None, fields_dict=None, include_hparams=False, include_log_records=None, 
    workspace_name=None, config=None, include_metrics=True):

    store = get_store(config)

    if not workspace_name:
        workspace_name = config.get("general", "workspace")

    # how to filter records
    if not filter_dict:
        filter_dict = {}
    
    filter_dict["job_id"] = job_id
    if run_ids:
        filter_dict["run_name"] = {"$in": run_ids}

    if not fields_dict:
        # return these fields
        fields_dict = {"status": 1, "job_id": 1, "run_name": 1, "last_time": 1}

    if include_hparams:
        fields_dict["hparams"] = 1

    if metric_names:
        full_metric_names = ["metrics." + metric for metric in metric_names]

        for name in full_metric_names:
            #filter_dict[name] = {"$exists": True}
            fields_dict[name] = 1

    elif include_metrics:
        # include all metrics
        fields_dict["metrics"] = 1
    
    fetch_logs = include_log_records   #  or metric_names
    run_records = store.database.get_info_for_runs(workspace_name, filter_dict, fields_dict, include_log_records=fetch_logs)

    if metric_names and include_log_records:
        step_name = None

        for record in run_records:
            log_records = record["log_records"]
            metric_sets = build_metrics_sets(log_records)
            metrics_dict = {}

            # for each metric name to plot
            for metric_name in metric_names:
                msr = [md["records"] for md in metric_sets if metric_name in md["keys"]]
                if msr:
                    values = msr[0]
                    
                    if not step_name:
                        # extract step name
                        step_name = values[0][constants.STEP_NAME]

                        # add to last_metrics dict
                        if "metrics" in record:
                            record["metrics"][constants.STEP_NAME] = step_name

                    steps = [value[step_name] for value in values]
                    metric_values = [value[metric_name] for value in values]

                    metrics_dict[metric_name] = {"steps": steps, "values": metric_values}

            # update record
            record["metrics_dict"] = metrics_dict

            # del log records if user didn't explictly include them
            if not include_log_records:
                del record["log_records"]

    return run_records

def flatten_prop(rr, prop):
    if prop in rr:
        # remove dict
        pd = rr[prop]
        del rr[prop]

        # zap _id column
        if "_id" in pd:
            del pd["_id"]

        # add pd key/value pairs to record dict
        rr.update(pd)

def replicate_run_record_with_metrics_dict(rr, step_name):
    records_by_step = {}

    md = rr["metrics_dict"]
    del rr["metrics_dict"]

    for name, kd in md.items():
        steps = kd["steps"]
        values = kd["values"]

        for step, value in zip(steps, values):
            if step in records_by_step:
                new_record = records_by_step[step]
            else:
                new_record = dict(rr)
                records_by_step[step] = new_record

            new_record[step_name] = step
            new_record[name] = value

    records = list(records_by_step.values())
    return records

def get_run_records_as_dataframe(job_id, run_ids=None, metric_names=None, filter_dict=None, fields_dict=None, include_hparams=False, 
    workspace_name=None, config=None, detail=False, melt=False):

    if not filter_dict:
        filter_dict = {"is_child": 1}

    run_records = get_run_records(job_id=job_id, run_ids=run_ids, metric_names=metric_names, filter_dict=filter_dict, fields_dict=fields_dict, 
        include_hparams=include_hparams, include_log_records=detail, workspace_name=workspace_name, config=config)

    # find step name for this set of run_records
    step_name = None

    if run_records:
        rr = run_records[0]
        md = rr["metrics"]

        if constants.STEP_NAME in md:
            step_name = md[constants.STEP_NAME]

        elif "epoch" in md:
                step_name == "epoch"

        elif "step" in md:
            step_name = "step"

        elif config:
            step_name = config.get("general", "step-name")

    # flatten metrics
    new_records = []

    for rr in run_records:
        flatten_prop(rr, "metrics")
        flatten_prop(rr, "hparams")

        if "log_records" in rr:
            del rr["log_records"]

        if detail:
            records = replicate_run_record_with_metrics_dict(rr, step_name)
            new_records += records

        else:
            new_records.append(rr)

    df = pd.DataFrame.from_records(new_records)

    if melt:
        pd.melt(df, step_name)

    return df

# functions for manipulating the run_name

def is_run_name(name):
    is_valid = False
    if name:
        low_name = name.lower()

        if low_name.startswith("run"):
            part = name[3:]

            # replace "_" with ""
            part = part.replace("_", "")

            parts = part.split(".")

            if len(parts) == 3:
                parent, index, restart = parts
                if restart.startswith("r"):
                    is_valid = parent.isdigit() and index.isdigit() and restart[1:].isdigit()

            elif len(parts) == 2:
                parent, index = parts
                is_valid = parent.isdigit() and index.isdigit()

            elif len(parts) == 1:
                is_valid = part.isdigit()

    return is_valid

def is_parent_run(name):
    if not is_run_name(name):
        errors.syntax_error("illegal run name: {}".format(name))
        
    is_parent = ("_" in name)
    return is_parent

def get_parent_run_number(name):
    num = 0
    if name and name.startswith("run"):
        part = name[3:]

        if ".r" in part:
            # remove restart number
            part = part.split(".r")[0]

        if constants.NODE_PREFIX in part:
            parent, node = part.split(constants.NODE_PREFIX, 1)
            num = int(parent)
        elif "." in part:
            parent, child = part.split(".", 1)
            num = int(parent)
        else:
            num = int(part)

    return num

def get_job_id_from_run_name(name):
    if not is_run_name(name):
        errors.syntax_error("illegal run name: {}".format(name))

    rest = name[3:]
    if "." in rest:
        run_number = rest.split(".")[0]
    else:
        run_number = rest.split("_")[0]

    job_id = "job" + run_number
    return job_id

# def get_run_name_parts(name):
#     if not is_run_name(name):
#         errors.syntax_error("illegal run name: {}".format(name))

#     run_part = None
#     run_index = None
#     node_index = None
#     restart_part = None

#     if ".r" in name:
#         run_part, restart_part = name.split(".r")

#     if "." in run_part:
#         run_part, run_index = run_part.split(".", 1)

#     elif "_" in run_part:
#         run_part, node_index = run_name.split("_")

#     return run_part, run_index, node_index, restart_part

def get_base_run_name(name):
    if not is_run_name(name):
        errors.syntax_error("illegal run name: {}".format(name))

    base_name = name
    if ".r" in name:
        base_name, _ = name.split(".r")

    return base_name

def get_run_number(name):
    parent = 0
    node = 0
    child = 0

    if name and name.startswith("run"):
        part = name[3:]

        if ".r" in part:
            # remove restart number
            part = part.split(".r")[0]

        if constants.NODE_PREFIX in part:
            parent, node = part.split(constants.NODE_PREFIX, 1)
            parent = int(parent)
            node = int(node)
        elif "." in part:
            parent, child = part.split(".", 1)
            parent = int(parent)
            child = 1 + int(child)
        else:
            parent = int(part)

        # allow for 1M children, 1M nodes
        oneM = 1000*1000

        # sort such that all parent (node runs) come before all child runs
        run_num = oneM*oneM*int(parent) + oneM*int(child) + int(node)
        
        return run_num

def get_run_index(name):
    if not is_run_name(name):
        errors.syntax_error("illegal run name: {}".format(name))

    index = None 
    parts = name.split(".")
    if len(parts) >= 2:
        index = int(parts[1])

    return index


def get_restart_number(run_name):
    restart_num = 0

    if is_run_name(run_name):
        if ".r" in run_name:
            _, restart_num_text = run_name.split(".r")
            restart_num = int(restart_num_text)

    else:
        errors.syntax_error("illegal run name: {}".format(run_name))
        
    return restart_num

def increment_restart_number(run_name):

    if not is_run_name(run_name):
        errors.syntax_error("illegal run name: {}".format(run_name))

    parts = run_name.split(".r")
    if len(parts) == 1:
        # no restart number; add r1
        run_name += ".r1"
    else:
        # extract the restart number
        restart_num = int(parts[1]) + 1
        run_name = "{}.r{}".format(parts[0], restart_num)

    return run_name

def decrement_restart_number(run_name):

    if not is_run_name(run_name):
        errors.syntax_error("illegal run name: {}".format(run_name))

    parts = run_name.split(".r")
    if len(parts) == 1:
        # no restart number; add r1
        run_name = None
    else:
        # extract the restart number
        restart_num = int(parts[1]) - 1
        if restart_num == 0:
            run_name = parts[0]
        else:
            run_name = "{}.r{}".format(parts[0], restart_num)

    return run_name
    
def merge_metric_log_records_from_restarts(log_records, metric_log_records):
    '''
    merge the METRIC log records from all restart instances into the base run log records.
    '''

    # extract metric log records from base and add to metric_log_records
    metric_log_records += [rr for rr in log_records if rr["event"] == "metrics"]

    # now, extract the metric records, sort by step number, and remove any duplicates
    if metric_log_records:
        # extract the step_name from the first record
        dd = metric_log_records[0]["data"]
        if "step_name" in dd:
            step_name = dd["step_name"]
        elif "step" in dd:
            step_name = "step"
        elif "epoch" in dd:
            step_name = "epoch"
        elif "iter" in dd:
            step_name = "iter"
        else:
            errors.internal_error("step_name not logged with metrics")

        # create a dict by <step_name + data.keys> to remove duplicate step records
        metric_records_by_step_only = {str(rr["data"][step_name]):rr for rr in metric_log_records}
        metric_records_by_step = {str(rr["data"][step_name]) + str(list(rr["data"])):rr for rr in metric_log_records}

        # sort by step number
        metric_records = list(metric_records_by_step.values())
        metric_records.sort(key=lambda x: x["data"][step_name])

        # remove metric_records from base run's log_records
        new_log_records = [rr for rr in log_records if not rr["event"] == "metrics"]

        # add back to log_records (just append to end, for now)
        new_log_records += metric_records
    else:
        new_log_records = log_records

    return new_log_records

def merge_log_records(base_record, restart_records):
    '''
    Merge the log records from the restart instances into the base_record.
    '''
    log_records = base_record["log_records"]
    all_metric_records = []

    for rr in restart_records:
        metric_log_records = [rr for rr in rr["log_records"] if rr["event"] == "metrics"]
        all_metric_records += metric_log_records

    new_log_records = merge_metric_log_records_from_restarts(log_records, all_metric_records)
    base_record["log_records"] = new_log_records

def merge_restart_log_records(records):
    '''
    Find all restart instances and merge their log records into a single list for the
    base run_name.  Then, remove the restart instances from the list.
    '''
    base_run_names = {rr["run_name"]:rr for rr in records if not ".r" in rr["run_name"]}
    merged_records = []

    for base_run_name, rr in base_run_names.items():
        # find all restart instances for this base run_name
        restart_records = [rr for rr in records if rr["run_name"].startswith(base_run_name + ".r")]

        # merge the metric log records from the restart instances
        merge_log_records(rr, restart_records)

        merged_records.append(rr)

    return merged_records