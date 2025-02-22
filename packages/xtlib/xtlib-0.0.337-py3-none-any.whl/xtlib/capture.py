#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# capture.py: support for uploading and download files to/from cloud storage
import os
import math
import time
import shutil

from xtlib import utils
from xtlib import errors
from xtlib import constants
from xtlib import file_utils

from xtlib.console import console
from xtlib.helpers import file_helper
from xtlib.helpers.feedbackParts import feedback as fb

def calc_size_of_files(filenames):
    total = 0

    for fn in filenames:
        size = os.path.getsize(fn)
        total += size

    return total

def zip_before_files(snapshot_dir, omit_files, zip_type, remove_prefix_len=0):

    filenames = file_helper.get_filenames_from_include_lists([snapshot_dir], omit_files, recursive=True)
    count = len(filenames)

    size = calc_size_of_files(filenames)
    unzipped_mb = size/(1024*1024)
    zip_name = constants.CODE_ZIP_FN 

    fn_zip = os.path.expanduser(constants.CWD_DIR + "/" + zip_name)
    use_compress = (zip_type == "compress")
    file_helper.zip_up_filenames(fn_zip, filenames, use_compress, remove_prefix_len)

    size = calc_size_of_files([fn_zip])
    zipped_mb = size/(1024*1024)

    return fn_zip, count, unzipped_mb, zipped_mb

def capture_before_files_zip(store, source_dir, ws_name=None, run_name=None, extra_files = [], rerun_name=None, 
        job_id=None,  omit_files=None, zip_before="none", store_dest="before", remove_prefix_len=None, 
        upload_type=None, service_type=None, args=None):
    
    copied_files = []
    started = time.time()
    feedback = True   # (upload_type != "bootstrap")
    nowrap = args["nowrap"]

    dest_code_count = count_files_in_subdir(source_dir, "\\user_code\\code\\")
    #print("dest_code_count=", dest_code_count)

    if rerun_name:
        if "/" in rerun_name:
            ws, rerun_name = rerun_name.split("/")
            
        copied_files = store.copy_run_files_to_run(ws_name, rerun_name, store_dest + "/", run_name, store_dest)
    else:
        # CAPTURE user-specified INPUT FILES

        before_files = [source_dir] + extra_files
        
        #console.print("before_files=", before_files)
        #console.print("omit_files=", omit_files)
        filenames = file_helper.get_filenames_from_include_lists(before_files, omit_files, recursive=True)
        count = len(filenames)
        where = "job" if job_id else "run"

        size = calc_size_of_files(filenames)
        mb_size = size/(1024*1024)
        total_size = "{:.2f} MB".format(mb_size)

        # code_count = 0
        # for fn in filenames:
        #     print(fn)
        #     if "/user_code/code/" in fn:
        #         code_count += 1
        #print("zipping code_count=", code_count)

        #console.print("zip-before=", zip_before)

        if zip_before in ["fast", "compress"]:

            if feedback:
                fb.feedback("{} {} ({}, zip)".format(count, upload_type, total_size), add_seperator=False)

            if upload_type == "code":
                zip_name = constants.CODE_ZIP_FN 
            else:
                errors.internal_error("unexpected upload type: " + str(upload_type))

            fn_zip = os.path.expanduser(constants.CWD_DIR + "/" + zip_name)
            use_compress = (zip_before=="compress")
            file_helper.zip_up_filenames(fn_zip, filenames, use_compress, remove_prefix_len)

            # redefine our files to be copied
            before_files = [fn_zip]
            omit_files = []

            if service_type in ["batch", "itp", "aml", "singularity"]:
                # add a copy of bootstrap files in parallel to the .zip file so they are available when we start to run
                if service_type == "batch":
                    bootstrap_files = [
                        constants.FN_DOCKER_PULL_SH, constants.FN_BATCH_NODE_ID, constants.FN_JOB_RELEASE_TASK, \
                        constants.FN_INNER_SCRIPT, constants.FN_NODE_SCRIPT, constants.FN_DOCKER_ENV, constants.FN_BATCH_HELPER]      

                    if nowrap:
                        fn_script = args["script"]
                        bootstrap_files.append(fn_script)   
                        bootstrap_files.append("code/mnist.py")
                else:
                    bootstrap_files = [
                        constants.PY_RUN_CONTROLLER, constants.FN_MULTI_RUN_CONTEXT, constants.FN_AML_SHIM, 
                        constants.FN_INNER_SCRIPT, constants.FN_NODE_SCRIPT, constants.FN_SET_ENV_VARS] 

                for bs in bootstrap_files:
                    fn_bs = source_dir + "/" + bs
                    if os.path.exists(fn_bs):
                        before_files.append(fn_bs)
        else:
            if feedback:
                fb.feedback("uploading {} {} files ({})".format(count, upload_type, total_size), add_seperator=False)

        console.diag("after zip of files")

        for input_wildcard in before_files:
            if job_id:
                # "input_wildcard" is a wildcard string relative to the current working directory
                copied_files += store.upload_files_to_job(ws_name, job_id, store_dest, input_wildcard, exclude_dirs_and_files=omit_files)
                dest_name = "job"
                elapsed = time.time() - started
                store.log_job_event(ws_name, job_id, "capture_before", {"elapsed": elapsed, "count": len(copied_files)})
            else:
                # "input_wildcard" is a wildcard string relative to the current working directory
                copied_files += store.upload_files_to_run(ws_name, run_name, store_dest, input_wildcard, exclude_dirs_and_files=omit_files)
                dest_name = "run"
                elapsed = time.time() - started
                store.log_run_event(ws_name, run_name, "capture_before", {"elapsed": elapsed, "count": len(copied_files)})

    if feedback:
        fb.feedback("")    # just add comma to indicte current op has completed

    return copied_files

def download_before_files(store, job_id, ws_name, run_name, dest_dir, silent=False, log_events=True, source="job", 
    unzip=True, source_wildcard=None):

    files = []
    if not source_wildcard:
        source_wildcard = "before/**"

    if source == "job":
        # all files contained in JOB BEFORE
        files += store.download_files_from_job(ws_name, job_id, source_wildcard, dest_dir)
        count = len(files)
        if not silent:
            console.print("  {} CODE files downloaded from store (JOB dir)".format(count))

        if log_events and run_name:
            store.log_run_event(ws_name, run_name, "download_before", {"source": "job", "count": count}, job_id=job_id)
    else:
        if "." in run_name:
            # download from parent's RUN before files
            parent_name = run_name.split(".")[0]
            files += store.download_files_from_run(ws_name, parent_name, source_wildcard, dest_dir)
            count = len(files)
            if not silent:
                console.print("  {} files downloaded from store (PARENT'S RUN dir)".format(count))

            if log_events:
                store.log_run_event(ws_name, run_name, source_wildcard, {"source": "parent-run", "count": count})
        
        # download from normal/child RUN before files
        files += store.download_files_from_run(ws_name, run_name, "before/**", dest_dir, job_id=job_id)
        count = len(files)
        if not silent:
            console.print("  {} files downloaded from store (RUN dir)".format(count))

        if log_events:
            store.log_run_event(ws_name, run_name, "download_before", {"source": "run", "count": count})

    if unzip:
        unzip_before_if_found(dest_dir, silent=silent)

    return files

def unzip_before_if_found(dest_dir, remove_after=True, silent=False):
    fn_zip = dest_dir + "/" + constants.CODE_ZIP_FN
    names = []

    if os.path.exists(fn_zip):
        found = True
        if not silent:
            console.print("unzipping fn_zip=", fn_zip)
        names = file_helper.unzip_files(fn_zip, dest_dir)

        if remove_after:
            os.remove(fn_zip)

    return names

def download_run(store, ws_name, run_name, dest_dir, others_dict):
    '''
       - first, download entire RUN store
       - then, if BEFORE files are in job, download them
    '''
    files = []

    files += store.download_files_from_run(ws_name, run_name, "**", dest_dir)
    
    job_id = store.get_job_id_of_run(ws_name, run_name)
    node_id = store.get_node_id_of_run(ws_name, run_name)

    # download BEFORE files of job, if needed
    before_key = job_id + "/before"

    if not before_key in others_dict:
        before_dir = dest_dir + "/before"
        before_files = store.download_files_from_job(ws_name, job_id, "before/**", before_dir)

        zip_files = unzip_before_if_found(before_dir + "/code", silent=True)
        if zip_files:
            files += zip_files
        else:
            files += before_files

        others_dict[before_key] = 1

    # download NODE files of job, if needed
    node_key = job_id + "/nodes/{}".format(node_id)
    if not node_key in others_dict:
        from_node = "nodes/{}/**".format(node_id)
        to_node = dest_dir + "/nodes/{}".format(node_id)
        node_files = store.download_files_from_job(ws_name, job_id, from_node, to_node)

        files += node_files
        others_dict[node_key] = 1    

    return files

def make_local_snapshot(from_dir, dest_dir, dest_name, omit_list):
    if dest_name and dest_name != ".":
        dest_dir += "/" + dest_name

    console.diag("before create local snapshot")

    # fixup slashes for good comparison
    dest_dir = os.path.realpath(dest_dir)

    # fully qualify path to from_dir for simpler code & more informative logging
    from_dir = os.path.realpath(from_dir)

    recursive = True

    if from_dir.endswith("**"):
        from_dir = from_dir[:-2]   # drop the **
    elif from_dir.endswith("*"):
        recursive = False

    # copy user's source dir (as per config file options)
    omit_list = utils.parse_list_option_value(omit_list)

    # build list of files matching both criteria
    filenames = file_helper.get_filenames_from_include_lists(None, omit_list, recursive=recursive, from_dir=from_dir)

    file_utils.ensure_dir_exists(dest_dir)
    prefix_len = 2 if from_dir == "." else len(from_dir)
    copy_count = 0

    # copy files recursively, preserving subdir names
    from_dir = os.path.realpath(from_dir)   # fix slashes and capitalization

    # add trailing slash for correct comparisons below
    from_dir += "\\" if os.name == "nt" else "/"

    # debug: count code/xxx files
    copy_code_count = 0
    # print("fn_dest=", dest_dir)
    # print("prefix_len=", prefix_len)
    # print("filenames=", filenames)
    # print("from_dir=", from_dir)

    for fn in filenames:
        fn = os.path.realpath(fn)           # fix slashes

        if fn.startswith(from_dir) and fn != from_dir:
            fn_dest = dest_dir + "/" + fn[prefix_len:]
            # print("copy fn", fn)
            # print("copy fn_dest", fn_dest)
            file_utils.ensure_dir_exists(file=fn_dest)
            shutil.copyfile(fn, fn_dest)
        else:
            shutil.copy(fn, dest_dir)
            #print("copy fn=", fn)

        if "\\cmdlinetest\\code\\" in fn.lower():
            copy_code_count += 1
        copy_count += 1

    # # debug
    # print("------------------------------------------------------------")
    # print("copy_code_count=", copy_code_count)  

    # # print all files in source_dir (recursively)
    # dest_code_count = count_files_in_subdir(dest_dir, "\\user_code\\code\\")
    # print("dest_code_count=", dest_code_count)

    #console.diag("after snapshot copy of {} files".format(copy_count))
    return copy_count

def count_files_in_subdir(dir_name, subdir_name):
    dest_code_count = 0
    # print("count_files_in_subdir: dir_name=", dir_name)

    for root, dirs, files in os.walk(dir_name):
        for name in files:
            fn = os.path.join(root, name)
            #print("dest fn: ", fn)
            if subdir_name in fn.lower():
                dest_code_count += 1

    return dest_code_count

