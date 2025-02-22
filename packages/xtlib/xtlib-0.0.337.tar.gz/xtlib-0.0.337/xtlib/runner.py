#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# runner.py: code to prepare to build a run submission (shared code for all backends)
import enum
import os
import sys
import json
import math
import time
import yaml
import uuid
import shutil
from typing import List
from threading import Lock
from collections import defaultdict

from xtlib.client import Client
from xtlib.console import console
from xtlib.cmd_core import CmdCore
from xtlib.helpers import file_helper
from xtlib.helpers.scanner import Scanner
from xtlib.hparams.hp_client import HPClient
from xtlib.helpers.feedbackParts import feedback as fb
from xtlib.event_processor import get_ids_from_python_expression


from xtlib import qfe
from xtlib import utils
from xtlib import errors
from xtlib import capture
from xtlib import xt_dict
from xtlib import pc_utils
from xtlib import cs_utils
from xtlib import scriptor
from xtlib import cmd_utils
from xtlib import constants
from xtlib import file_utils
from xtlib import time_utils
from xtlib import job_helper
from xtlib import store_utils
from xtlib import process_utils
from xtlib import box_information

class Runner():
    ''' class to consolidate all shared code for run submission '''
    def __init__(self, config, core, temp_dir):
        self.config = config
        self.core = core
        self.store = core.store
        self.backend = None
        self.is_docker = None
        self.target_dir = None
        self.temp_dir = temp_dir

    def process_args(self, args):

        run_script = None
        parent_script = None
        run_cmd_from_script = None
        target_file = args["script"]
        target_args = args["script_args"]
        code_upload = args["code_upload"]

        # fix slashes to match target OS of compute node
        target_is_linux = True   
        target_file = file_utils.fix_slashes(target_file, is_linux=target_is_linux)

        if os.path.isabs(target_file):
            errors.user_error("path to app file must be specified with a relative path: {}".format(target_file))

        is_rerun = "is_rerun" in args
        if is_rerun:
            # will be running from script dir, so remove any path to script file
            self.script_dir = os.path.dirname(target_file)
            target_file = os.path.basename(target_file)

        if target_file.endswith(".py"):
            # PYTHON target
            cmd_parts = ["python"]
            cmd_parts.append("-u")
            cmd_parts.append(target_file)
        else:
            cmd_parts = [target_file] 

        if target_args:
            # split on unquoted spaces
            arg_parts = cmd_utils.user_cmd_split(target_args)
            cmd_parts += arg_parts

        if target_file == "docker":
            self.is_docker = True
            
        ps_path = args["parent_script"]
        alt_code = args["code"]
        working_dir = args["working_dir"]
        
        if alt_code:
            # TEMP process alt_code to extract the a few files
            alt_code_dir = os.path.join(self.temp_dir, "alt_code")
            self.copy_alt_code_to_snapshot(alt_code, alt_code_dir, args)

            temp_target_file = os.path.join(alt_code_dir, working_dir, target_file)
            if ps_path:
                temp_ps_path = os.path.join(alt_code_dir, working_dir, ps_path)

            if args["from_request"]:
                # process request files
                from_dir = os.path.join(alt_code_dir, constants.APPROVE_DIR)

                if os.path.exists(from_dir):
                    # copy all files from request dir to root of temp dir (so they will persist when we exit this function)
                    to_dir = os.path.join(self.temp_dir, constants.APPROVE_DIR)
                    #os.makedirs(to_dir, exist_ok=True)
                    shutil.copytree(from_dir, to_dir)

                    if args["hp_config"]:
                        # point to the hp_config file in the request dir
                        fn_hp_config = os.path.join(to_dir, "hp_config.yaml")
                        args["hp_config"] = fn_hp_config

        else:
            temp_target_file = target_file
            temp_ps_path = ps_path

        if code_upload and (not self.is_docker) and (not os.path.exists(temp_target_file)):
            errors.env_error("script file not found: {}".format(temp_target_file))

        if ps_path:
            parent_script = file_utils.read_text_file(temp_ps_path, as_lines=True)

        if temp_target_file.endswith(".bat") or temp_target_file.endswith(".sh"):
            # a RUN SCRIPT was specified as the target
            run_script = file_utils.read_text_file(temp_target_file, as_lines=True)
            run_cmd_from_script = scriptor.get_run_cmd_from_script(run_script)

        # remove temp directory
        if alt_code:
            shutil.rmtree(alt_code_dir)

        return cmd_parts, ps_path, parent_script, target_file, run_script, run_cmd_from_script

    def build_compute_def(self, args):
        compute = args["target"]
        box_def = self.config.get("boxes", compute, suppress_warning=True)

        compute_def = dict(self.config.get_target_def(compute))

        if not "service" in compute_def:
            errors.config_error("compute target '{}' must define a 'service' property".format(compute))

        service = compute_def["service"]
        if service in ["local", "pool"]:
            # its a list of box names
            boxes = compute_def["boxes"]
            if len(boxes)==1 and boxes[0] == "localhost":
                pool = None
                box = "local"
                service_type = "pool"
            else:
                pool = compute
                box = None
                service_type = "pool"
        else:
            # it a set of compute service properties
            pool = compute
            box = None
            service_name = compute_def["service"]
            service_type = self.config.get_service_type(service_name)

        # elif box_def:
        #     # translate single box name to a compute_def
        #     box = compute
        #     pool = None
        #     service_type = "pool"
        #     compute_def = {"service": service_type, "boxes": [box], setup: setup_name}
        # else:
        #     errors.config_error("unknown target or box: {}".format(compute))

        compute_def["name"] = compute

        hold = args["hold"]
        update_compute_def_from_cmd_options(compute_def, hold)

        args["target"] = compute
        args["compute_def"] = compute_def
        args["service_type"] = service_type

        # for legacy code
        args["box"] = box
        args["pool"] = pool

        # update args["setup"] with default
        setup_name = utils.safe_value(compute_def, "setup")
        if not setup_name:
            setup_name = utils.safe_value(box_def, "setup")
            args["setup"] = setup_name

        return compute, compute_def, service_type, setup_name

    def ensure_script_ext_matches_box(self, script_name, fn_script, box_info):
        _, file_ext = os.path.splitext(fn_script)
        if file_ext in [".bat", ".sh"]:
            expected_ext = ".bat" if box_info.box_os == "windows" else ".sh"

            if file_ext != expected_ext:
                errors.combo_error("{} file ext='{}' doesn't match box.os='{}'".format(script_name, file_ext, box_info.box_os))

    def build_primary_run_for_node(self, node_index, run_count, total_run_count, box_name, run_script_path, parent_script_path, 
            using_hp, use_aml_hparam, run_specs, job_id, parent_name, cmds, compute_def, repeat_count, fake_submit, 
            search_style, box_secret, node_count, run_name=None, args=None):
            
        exper_name = args['experiment']

        box_info = box_information.BoxInfo(self.config, box_name, self.store, args=args)

        if node_index == 0:
            # check that script file extensions match OS of first box
            if run_script_path:
                self.ensure_script_ext_matches_box("run script", run_script_path, box_info)

            if parent_script_path:
                self.ensure_script_ext_matches_box("parent script", parent_script_path, box_info)

        #node_id = "node" + str(node_index)
        # if using_hp:
        #     if not node_id in cmds_by_node:
        #         errors.combo_error("you specified more nodes/boxes than hyperparameter search runs")

        cmd_parts = run_specs["cmd_parts"]
        actual_parts = None

        is_direct_run = self.config.get("general", "direct-run")
        if is_direct_run and cmds:
            # adjust cmd in each job_run to use cmds[node_index]
            cmd = cmds[node_index]
            cmd_parts = cmd.split()

            run_specs["cmd_parts"] = cmd_parts
            run_specs["run_cmd"] = cmd

        if cmd_parts:
            actual_parts = list(cmd_parts)
            if box_info.box_os == "linux" and actual_parts[0] == "docker":
                # give our user permission to run DOCKER on linux
                actual_parts.insert(0, "sudo")
                # run nvidia-docker to gain access to machines GPUs
                actual_parts[1] = "nvidia-docker"
            #console.print("actual_parts=", actual_parts)

        # CREATE RUN 
        path = os.path.realpath(args["script"])

        run_name, full_run_name, box_name, pool = \
            self.create_run(job_id, actual_parts, box_name=box_name, parent_name=parent_name, 
                node_index=node_index, using_hp=using_hp, 
                repeat=repeat_count, app_info=None, path=path, exper_name=exper_name, compute_def=compute_def, 
                fake_submit=fake_submit, search_style=search_style, run_count=run_count, 
                total_run_count=total_run_count, run_name=run_name, args=args)

        run_data = {"run_name": run_name, "run_specs": run_specs, "box_name": box_name, "box_index": node_index, 
            "box_info": box_info, "repeat": repeat_count, "box_secret": box_secret}

        return run_data
       
    def write_node_info_data(self, _id, ws_name, job_id, node_index, total_run_count, node_count, 
        box_name, run_name, secret, service_info, exper_name, args):

        compute_target = args["target"]
        str_now = time_utils.get_arrow_now_str()

        job_num = job_helper.get_job_number(job_id)
        node_num = job_num*1000*1000 + node_index
        node_name = "{}/{}".format(job_id, node_index)

        # compute node_run_count
        first, last = self.core.compute_run_indexes_for_node(total_run_count, node_count, node_index)
        node_run_count = last - first + 1
        node_id = utils.node_id(node_index)
        service_info_text = json.dumps(service_info) if service_info else None
        
        compute_def = args["compute_def"]
        aml_compute = utils.safe_value(compute_def, "compute")

        dd = {"_id": _id, "ws_name": ws_name, "job_id": job_id, "exper_name": exper_name, 
            "node_name": node_name, "node_id": node_id, "node_index": node_index, "node_num": node_num, 
            "aml_compute": aml_compute, "compute_target": compute_target, "total_runs": node_run_count, "box_name": box_name, "run_name": run_name,
            "secret": secret, "service_info": service_info_text}

        # write dd record to node_info
        self.store.database.update_collection("node_info", ws_name, dd)

    def write_node_stats_data(self, _id, ws_name):
        str_now = time_utils.get_arrow_now_str()

        dd = {"_id": _id, "node_status": "created", 
            "completed_runs": 0, "error_runs": 0, "running_runs": 0,
            "create_time": str_now, "restarts": 0, "db_retries": 0, "storage_retries": 0}

        # write dd record to node_stats
        self.store.database.update_collection("node_stats", ws_name, dd)

    def write_node_tags_data(self, _id, ws_name, job_id, tag_dict):

        if not tag_dict:
            tag_dict = {}

        tag_dict["_id"] = _id        
        tag_dict["job_id"] = job_id        

        # write dd record to node_stats
        self.store.database.update_collection("node_tags", ws_name, tag_dict)

    def write_hparams_to_job(self, ws_name, job_id, cmds, fake_submit, using_hp, args):
        # write to job-level sweeps-list file
        #console.print("cmds=", cmds)   
        cmds_text = json.dumps(cmds)

        if not fake_submit:
            self.store.create_job_file(ws_name, job_id, constants.HP_SWEEP_LIST_FN, cmds_text)

        # NOTE: pool_info is legacy form of compute_def and is being eliminated 
        boxes, _, service_type = box_information.get_box_list(self, job_id=job_id, args=args)
        num_boxes = len(boxes)

        is_distributed = args["distributed"]
        if is_distributed:
            # check for conflicts
            if using_hp:
                errors.combo_error("Cannot do hyperparamer search on a distributed-training job")

            if service_type != "aml":
                errors.combo_error("Distributed-training is currently only supported for AML jobs")

        return boxes, num_boxes

    def create_run(self, job_id, user_cmd_parts, box_name="local", parent_name=None, rerun_name=None, node_index=0, 
            using_hp=False, repeat=None, app_info=None, path=None, exper_name=None, compute_def=None, fake_submit=False, 
            search_style=None, run_count=None, total_run_count=None, run_name=None, args=None):
        '''
        'create_run' does the following:
            - creates a new run name (from the job name and node)
            - logs a "created" record in the run log
            - logs a "created" record in the workspace summary log
            - logs a "cmd" record in the run log
            - log an optional "notes" record in the run log
            - captures the run's "before" files to the store's run directory
        '''
        console.diag("create_run: start")

        app_name = None   # app_info.app_name
        box_nane = args["box"]
        pool = args["pool"]
        
        log_to_store = self.config.get("logging", "log")
        aggregate_dest = args["aggregate_dest"]

        if log_to_store:
            if not exper_name:
                exper_name = input("experiment name (for grouping this run): ")

            #console.print("calling store.start_run with exper_name=", exper_name)
            username = args["username"]
            description = args["description"]
            workspace = args["workspace"]

            console.diag("create_run: before start_run")

            service_type = args["service_type"]
            compute = args["target"]
            search_type = args["search_type"]

            # compute_def has been updated with args[sku]
            sku = utils.safe_value(compute_def, "sku")
            if sku:
                sku = sku.lower()

            # create RUN in store
            if fake_submit:
                run_name = "fake_run123"
            else:
                is_parent = search_style != "single"

                if not run_name:
                    run_name = self.store.database.get_next_run_name(workspace, job_id, 
                        is_parent, total_run_count, node_index)

                tag_dict = args["tags"]

                display_name = args["display_name"]
                display_name = utils.expand_xt_vars(display_name, run_id=run_name, args=args)

                self.store.start_run_core(workspace, run_name=run_name, exper_name=exper_name, box_name=box_name, app_name=app_name, 
                    username=username, repeat=repeat, pool=pool, job_id=job_id, node_index=node_index, sku=sku,
                    description=description, aggregate_dest=aggregate_dest, path=path, compute=compute, service_type=service_type, 
                    search_style=search_style, is_parent=is_parent, tag_dict=tag_dict, display_name=display_name, 
                    cmd_line_args=str(user_cmd_parts), xt_cmd=args["xt_cmd"])

            console.diag("create_run: after start_run")

            # always log cmd (for re-run purposes)
            xt_cmd = args["xt_cmd"]

            if not fake_submit:
                self.store.log_run_event(workspace, run_name, "cmd", {"cmd": user_cmd_parts, "xt_cmd": xt_cmd }, job_id=job_id)

            # for now, don't log args (contain private credentials and not clear if we really need it)
            # record all "args" (from cmd line, user config, default config) in log (for audit/re-run purposes)
            #self.store.log_run_event(workspace, run_name, "args", args)

            store_type = self.config.get_storage_type()
            full_run_name = utils.format_workspace_exper_run(store_type, workspace, exper_name, run_name)

            # log NOTES record
            if not fake_submit:
                if self.config.get("logging", "notes") in ["before", "all"]:
                    text = input("Notes: ")
                    if text:
                        self.store.log_run_event(workspace, run_name, "notes", {"notes": text})
        else:
            full_run_name = ""

        console.diag("create_run: after logging")
        workspace = args['workspace']

        return run_name, full_run_name, box_name, pool

    def upload_sweep_data(self, sweeps_text, exper_name, job_id, args):
        '''
        we have extracted/parsed HP sweeps data; write it to the experiment/job store
        where we can find it during dynamic HP searches (running in controller).
        '''
        # upload SWEEP file to job or experiment directory
        fn_sweeps = args["hp_config"]
        agg_dest = args["aggregate_dest"]
        ws_name = args["workspace"]

        if not fn_sweeps:
            # must have extracted sweeps data from cmd line options
            fn_sweeps = constants.HP_CONFIG_FN
            args["hp_config"] = fn_sweeps

        # upload to a known folder name (since value of fn_sweeps can vary) and we need to find it later (HX usage)
        target_name = file_utils.path_join(constants.HP_CONFIG_DIR, os.path.basename(fn_sweeps))
        
        if agg_dest == "experiment":
            self.store.create_experiment_file(ws_name, exper_name, target_name, sweeps_text)
        else:
            self.store.create_job_file(ws_name, job_id, target_name, sweeps_text)

    def build_runs_by_box(self, job_runs, workspace):
        # build box_name => runs dict for job info file
        runs_by_box = {}
        last_run = None

        # for each node
        for run_data in job_runs:
            box_name = run_data["box_name"]

            # process a run for box_name
            # if not box_name in runs_by_box:
            #     runs_by_box[box_name] = [] 

            # create as dict; we will later add "service_run_id" to the dict (for philly, batch, aml)
            rr = {"ws_name": workspace, "run_name": run_data["run_name"], "box_index": run_data["box_index"]}

            runs_by_box[box_name] = rr
            last_run = run_data["run_name"]

        return runs_by_box, last_run

    def adjust_script_dir(self, cmd_parts, node_script_path=None):
        '''
        NOTE: cmd_parts is modified directly.
        '''

        script_dir = None    # default to the current directory
        found_script = False

        parts = cmd_parts
        dest_linux = not self.backend.gen_for_windows

        for i, part in enumerate(parts):

            if found_script and part.startswith("@"):
                part = part[1:]   # remove the "@"
                if os.path.isfile(part):
                    # ensure the slashes in the path match targeted OS 
                    parts[i] = "@" + file_utils.fix_slashes(part, is_linux=dest_linux)

            elif not part.startswith("-"):
                if os.path.isfile(part):
                    # ensure the slashes in the path match targeted OS 
                    fixed_path = file_utils.fix_slashes(part, is_linux=dest_linux)
                    script_dir = os.path.dirname(fixed_path)
                    script_fn = os.path.basename(fixed_path)

                    # adjust script_dir
                    if node_script_path:
                        parts[i] = node_script_path + "/" + script_fn
                        script_dir = node_script_path
                    else:                        
                        parts[i] = fixed_path
                    found_script = True

        if not script_dir:
            script_dir = "."

        return script_dir

    def remove_script_dir_from_parts(self, cmd_parts):
        '''
        NOTE: cmd_parts is modified directly.
        '''

        script_dir = "."    # default to the current directory
        found_script = False

        parts = cmd_parts
        for i, part in enumerate(parts):

            if found_script and part.startswith("@"):
                part = part[1:]   # remove the "@"
                if os.path.isfile(part):
                    # remove the path from the arg file 
                    parts[i] ="@" + os.path.basename(part)
            elif not part.startswith("-"):
                path = os.path.realpath(part)
                if os.path.isfile(path):
                    script_dir = os.path.dirname(path)

                    # remove the path from the script 
                    parts[i] = os.path.basename(path)
                    found_script = True

        return script_dir

    def build_docker_cmd(self, docker_name:str, target: str, service_type, bootstrap_dir: str, job_secret: str, 
            setup_name: str, env_vars: dict, args: List[str]):
        '''
        This is only called for backends that don't have their own support for running in docker.  Currently, this is
        just the POOL backend (and Azure Batch?).  This function will replace the user's script cmd with:

            - optional 'docker login' cmd
            - 'docker run' cmd
        '''
        for_windows = self.backend.is_windows
        login_cmd = None

        timeout = args["docker_pull_timeout"]
        if timeout:
            # validate timeout (e.g., "30s" or "5d")
            if timeout.isnumeric():
                # will default to seconds
                pass
            else:
                unit = timeout[-1]
                if not unit in 'smhd':
                    raise Exception("illegal duration specified for general.docker-pull-timeout (try: 30m)")
                if " " in timeout:
                    raise Exception("illegal duration specified for general.docker-pull-timeout (try: 30m)")

        docker_image, login_server, docker_registry, _ = self.config.get_docker_info(target, docker_name, required=False)
        creds_required = utils.make_numeric_if_possible( utils.safe_value(docker_registry, "login") )
        use_az_acr_login = utils.make_numeric_if_possible( utils.safe_value(docker_registry, "azure-login") )

        setup_def = self.config.get("setups", setup_name, suppress_warning=True)
        use_sudo = not for_windows   # utils.safe_value(setup_def, "use-sudo") or self.backend.name in ["pool", "batch"]
        sudo = "sudo " if use_sudo else ""

        if creds_required:
            username = utils.safe_value(docker_registry, "username")
            password = utils.safe_value(docker_registry, "password")

            # avoid docker login warning about password and CLI
            #login_cmd = "echo {} | {}docker login {} --username {} --password-stdin".format(password, sudo, login_server, username)
            if use_az_acr_login:
                # "az acr login" will supply username, password in a config file
                login_cmd = "{}docker login {}".format(sudo, login_server)
            else:
                login_cmd = "{}docker login {} --username {} --password {}".format(sudo, login_server, username, password)

        args["docker_login_cmd"] = login_cmd
        args["use_az_acr_login"] = use_az_acr_login
        args["login_server"] = login_server

        dest_src_dir = "/usr/src"     # "/root/.xt/cwd"
        script_dir = "%CD%" if for_windows else "$PWD"
        mappings = "-v {}:{}".format(script_dir, dest_src_dir)

        if service_type == "batch":
            # map a virtual docker drive to the azure batch logs directory
            mappings += " -v $(dirname $PWD):/usr/logs"

        options = "--rm"

        full_image = login_server + "/" + docker_image if login_server else docker_image

        # inherit ENV VARS from running environment
        env_vars["XT_IN_DOCKER"] = 1
        env_vars["XT_USERNAME"] = pc_utils.get_username()

        # we have to be careful here to correctly transfer env vars that are node-specific
        # this is done in the NodeScriptor.gen_docker_run()

        # write env vars to file in bootstrap_dir 
        fn_env_var = os.path.join(bootstrap_dir, constants.FN_DOCKER_ENV)
        lines = [name + "=" + str(value) for name,value in env_vars.items()]
        text = "\n".join(lines)
        file_utils.write_text_file(fn_env_var, text)

        # specify env var file (in current directory) to docker
        options += " --env-file={}".format(constants.FN_DOCKER_ENV)

        # flags needed by blobfuse usage
        #options += " --cap-add SYS_ADMIN --device /dev/fuse --security-opt apparmor:unconfined"
        if self.backend.get_name() != "singularity":
            options += " --privileged"

            # append user options
            other_options = " ".join(args["docker_other_options"])
            if other_options:
                options += " " + other_options

        # currently, we don't support running in a windows-based container
        docker_is_windows = False
        args["docker_is_windows"] = docker_is_windows
        args["full_docker_image"] = full_image

        pass_args = "%*" if for_windows else "$*"
        sh_prefix = "bash --login"

        # launching docker from linux
        # we set DOCKER_RUN just before this command is executed (see backend_base.py)
        docker_cmd = "{}$DOCKER_RUN {} {} {} {} {}/{} {}".format(sudo, mappings, options, full_image, sh_prefix, dest_src_dir, constants.FN_INNER_SCRIPT, pass_args)

        # store for use by backend_base.wrap_user_cmds()
        args["docker_cmd"] = docker_cmd

    def get_installed_package_version(self, pkg_name):
        version = None

        try:
            from importlib.metadata import version as get_version
            version = get_version(pkg_name)
        except:
            if pkg_name == "xtlib":
                # this assumes we have our "out of conda" xt installed in "xt_shared"
                # %CONDA3_DIR%\envs\xt_shared\python -m pip list

                # just extract it from our BUILD constant
                version_text = constants.BUILD    # version: 0.0.326a, build: Apr-28-2024
                version = version_text.split(",")[0].split(" ")[1].strip()
                if not version[-1].isdigit():
                    version = version[0:-1]
        
        return version

    def adjust_pip_packages(self, args):
        '''
        convert any package=* in pip-packages to use local machine version (from pip freeze)
        '''
        pip_packages = args["pip_packages"]
        new_pip_packages = []

        for pp in pip_packages:
            if pp.endswith("==*"):
                pp_spec = pp.split(" ")[-1]
                package = pp_spec[:-3]
                version = self.get_installed_package_version(package)
                if not version:
                    errors.env_error("version number for specified pip package not found in environment: " + package)
                pp = pp.replace("*", version)

            new_pip_packages.append(pp)

        args["pip_packages"] = new_pip_packages

    def copy_alt_code_to_snapshot(self, alt_code, snapshot_dir, args):

        if job_helper.is_job_id(alt_code):
            ws_name = args["workspace"]
            job_id = alt_code

            files = capture.download_before_files(self.store, job_id, ws_name, source_wildcard="before/code/xt_code.zip", 
                run_name=None, dest_dir=snapshot_dir, log_events=False, silent=True, unzip=False)

        elif store_utils.is_blob_path(alt_code):
            ws_name = args["workspace"]
            self.store.download_files_from_workspace(ws_name, alt_code + "/**", snapshot_dir)

        else:
            # copy files from alt_code to shotshot_dir
            file_utils.copy_tree(alt_code, snapshot_dir, args)

        # if xt_code.zip file found, unzip it and delete it
        fn_zip = snapshot_dir + "/xt_code.zip"
        if os.path.exists(fn_zip):
            file_helper.unzip_files(fn_zip, snapshot_dir)
            os.remove(fn_zip)

    def snapshot_all_code(self, bootstrap_dir, snapshot_dir, cmd_parts, args):
        '''
        keep code simple (and BEFORE upload fast):
            - always copy code dir to temp dir
            - if needed, copy xtlib subdir
            - later: if needed, add 2 extra controller files
            - later: zip the whole thing at once & upload 
        '''
        alt_code = args["code"]          # from previous run or --request
        code_dirs = args["code_dirs"]
        xtlib_capture = args["xtlib_upload"]
        code_omit = args["code_omit"]
        node_script_path = args["node_script_path"]
        code_upload = args["code_upload"]

        # LEGACY: this figures out the node's path to the script 
        script_dir = self.adjust_script_dir(cmd_parts, node_script_path)

        if alt_code:
            self.copy_alt_code_to_snapshot(alt_code, snapshot_dir, args)

        else:
            if code_upload:
                for i, code_dir in enumerate(code_dirs):
                    # LEGACY: remove SOON
                    # fixup "$scriptdir" relative paths
                    if "$scriptdir" in code_dir:
                        code_dir = code_dir.replace("$scriptdir", script_dir)

                    # fixup "$cwd" relative paths
                    if "$cwd" in code_dir:
                        code_dir = code_dir.replace("$cwd", ".")

                    if "==>" in code_dir:
                        code_dir, dest_dir = code_dir.split("==>")
                    # elif "::" in code_dir:
                    #     # "::" is legacy version of "==>"
                    #     code_dir, dest_dir = code_dir.split("::")
                    else:
                        dest_dir = "."
                    capture.make_local_snapshot(code_dir, snapshot_dir, dest_dir, code_omit)
            else:
                script_dir = snapshot_dir

            if xtlib_capture:
                xtlib_dir = file_utils.get_xtlib_dir()

                # copy XTLIB directory to "xtlib" subdir of CODE SNAPSHOT
                dest_dir = snapshot_dir + "/xtlib"
                file_utils.ensure_dir_deleted(dest_dir)
                shutil.copytree(xtlib_dir, dest_dir, ignore=shutil.ignore_patterns("demo_files"))

        console.diag("after create local snapshot")
        return script_dir

    def send_to_approvers(self, request_id, requested_by, description, target, nodes, runs, cmd):
        team_dict = self.config.get("team")

        requested_by_contacts = cs_utils.get_contacts(team_dict, requested_by)
        approver_contacts, approver_usernames = cs_utils.get_approvers(team_dict)

        # for now, assume all entries in approver_contacts are valid email names 
        # TODO: add support for SMS text to phone numbers
        subject = "job submission REQUESTED: {}".format(request_id)

        # make body HTML 
        store_name = self.config.get("store")

        body = ""
        body += "<b>job submission request:</b> {}".format(request_id)
        body += "<br><b>store:</b> {}".format(store_name)
        body += "<br><b>target:</b> {}".format(target)
        body += "<br><b>nodes:</b> {:,}, <b>runs:</b> {:,}".format(nodes, runs)
        body += "<br><b>requested by:</b> {}".format(requested_by)
        body += "<br><b>description:</b> {}".format(description)

        body += "<br><br><b>cmd:</b> {}".format(cmd)

        body += "<br><br><b>To approve:</b> xt approve {}".format(request_id)
        body += "<br><b>To reject:</b> xt reject {}\n".format(request_id)
        sent = False

        try:
            cs_utils.send_to_contacts_from_config(self.config, approver_contacts, requested_by_contacts, subject, body)
            sent = True
        except BaseException as ex:
            console.print("email/SMS failed: ex: {}".format(ex))

        return approver_usernames, sent

    def create_run_request(self, ws_name, snapshot_dir, username, target, nodes, runs, args):
        '''
        don't actually submit a job, but add a request to run the job to our database.
        '''
        description = args["description"]
        if not description:
            errors.user_error("when creating a request, the reason for the job must be specified with --description")

        # create a new request in database
        # include env_vars, which might have captured values from requestor's env vars
        env_vars = args["env_vars"]
        env_vars_text = json.dumps(env_vars)

        rd = {"status": "requested", "requested_by": username, "description": description, "env_vars": env_vars_text,
            "target": target, "nodes": nodes, "runs": runs}

        request_id = self.store.create_request(ws_name, rd)
        console.print("request created: {}".format(request_id))

        code_omit = args["code_omit"]
        code_zip = args["code_zip"]

        from xtlib.xt_cmds import orig_xt_cmd
        run_cmd = orig_xt_cmd
        new_options = " --code=$requests/{}/code".format(request_id) 

        # add the request id, so run command can fetch other info as needed related to the request
        new_options += " --from-request=" + request_id

        # add requestor's name as username
        new_options += " --username=" + username
        new_options += " "

        # replace the "--request" option with code_option
        index = run_cmd.index("--req")
        index2 = run_cmd.find(" ", index+5)
        if index2 > -1:
            run_cmd = run_cmd[0:index].strip() + new_options + run_cmd[index2:].strip()
        else:
            run_cmd = run_cmd[0:index].strip() + new_options

        # update the request record
        rd["cmd"] = run_cmd
        self.store.database.update_requests_record(ws_name, request_id, rd)

        # copy files needed at approval time to snapshot_dir
        hp_config = args["hp_config"]
        if hp_config:
            approve_dir = snapshot_dir + "/" + constants.APPROVE_DIR
            os.makedirs(approve_dir, exist_ok=True)
            # copy file to a fixed name (so we can find it later)
            shutil.copy(hp_config, approve_dir + "/hp_config.yaml")

        # zip up snapshot_dir and copy to storage: workspace/requests/requestNN/code/xt_code.zip
        remove_prefix_len = len(snapshot_dir)
        fn_zip, file_count, raw_mb, zipped_mb = capture.zip_before_files(snapshot_dir, code_omit, code_zip, 
            remove_prefix_len=remove_prefix_len)

        blob_fn = "/{}/requests/{}/code/xt_code.zip".format(ws_name, request_id)
        self.store.upload_file_to_workspace(ws_name, blob_fn, fn_zip)

        console.print("  code snapshot created: {:,} files (zipped to: {:,.2f} MB, stored: {})".format(file_count, zipped_mb, blob_fn))
        #console.print("  zipped & written to blob storage: {}".format(blob_fn))

        # send email/sms to approver(s)
        approvers, sent = self.send_to_approvers(request_id, username, description, target, nodes, runs, run_cmd)

        # final message to requesting user
        if sent:
            console.print("  request sent (email/SMS) to approvers: {}".format(", ".join(approvers)))

    def process_run_command(self, args):
        self.args = args

        result = self.create_job(args)
        if result:
            compute, compute_def, workspace, job_id, sweeps_text, cmds, fake_submit, using_hp, is_distributed, \
                total_run_count, target_file, ps_path, using_aml_hparam, run_specs, repeat_count, service_type, search_style, \
                runsets, bootstrap_dir, snapshot_dir, script_dir, snapshot_base, job_secret, resume_name, use_controller  = result

            result = self.submit_job(compute, compute_def, workspace, job_id, sweeps_text, cmds, fake_submit, using_hp, is_distributed, \
                total_run_count, target_file, ps_path, using_aml_hparam, run_specs, repeat_count, service_type, search_style, \
                runsets, bootstrap_dir, snapshot_dir, script_dir, snapshot_base, job_secret, resume_name, use_controller, args)

        return result

    def validate_col_name(self, col):
        if "." in col:
            prefix, col_name = col.split(".")
            if not prefix in ["metrics", "hparams"]:
                errors.user_error("unrecognized prefix on column name: {}".format(col))

    def validate_event(self, event_name, event):
        condition = utils.safe_value(event, "if")
        if condition:
            # validate python expression
            try:
                id_list = get_ids_from_python_expression(condition)
                for id in id_list:
                    self.validate_col_name(id)

            except BaseException as ex:
                console.print("invalid condition syntax: '{}' in event '{}'".format(condition, event_name))
                raise ex

        report = utils.safe_value(event, "report")
        if report:
            # validate col names (at a high level)
            for col in report:
                self.validate_col_name(col)

    def validate_nodify(self, notify_list):
        team_dict = self.config.get("team")

        for user in notify_list:
            if not user in team_dict:
                errors.user_error("notify user not found in teams dictionary: {}".format(user))

            user_dict = team_dict[user]
            if not "contact" in user_dict:
                errors.user_error("notify user does not have 'contact' entry in teams dictionary: {}".format(user))


    def create_job(self, args):

        # ensure workspace exists
        workspace = args['workspace']
        dry_run = args['dry_run']
        fake_submit = args["fake_submit"]

        if not fake_submit:
            self.store.ensure_workspace_exists(workspace, flag_as_error=False)

        # PRE-PROCESS ARGS
        cmd_parts, ps_path, parent_script, target_file, run_script, run_cmd_from_script = \
            self.process_args(args)

        compute, compute_def, service_type, setup_name = self.build_compute_def(args)

        # create backend helper (pool, philly, batch, aml)
        username = args["username"]

        self.backend = self.core.create_backend(compute, compute_def, username=username)

        # add conda_packages and pip_packages from SETUP to ARGS
        setup_def = self.config.get_setup_from_target_def(compute_def, setup_name)

        conda_packages = utils.safe_value(setup_def, "conda-packages")
        pip_packages = utils.safe_value(setup_def, "pip-packages")
        python_path = utils.safe_value(setup_def, "python-path")
        other_cmds = utils.safe_value(setup_def, "other-cmds")
        pre_cmds = utils.safe_value(setup_def, "pre-cmds")
        python_version = utils.safe_value(setup_def, "python-version", "3.6.0")
        use_legacy_resolver = utils.safe_value(setup_def, "use-legacy-resolver")
        install_blobfuse = utils.safe_value(setup_def, "install-blobfuse")

        args["conda_packages"] = conda_packages if conda_packages else []
        args["pip_packages"] = pip_packages if pip_packages else []
        args["python_path"] = python_path if python_path else []
        args["other_cmds"] = other_cmds if other_cmds else []
        args["pre_cmds"] = pre_cmds if pre_cmds else []
        args["python_version"] = python_version
        args["use_legacy_resolver"] = use_legacy_resolver

        # install blobfuse defaults to True
        args["install_blobfuse"] = True if install_blobfuse is None else install_blobfuse

        self.adjust_pip_packages(args)

        snapshot_base = self.temp_dir
        snapshot_dir = os.path.join(snapshot_base, "code")

        # for now, don't separate code and bootstrap (causes issues: requirements.txt file)
        bootstrap_dir = snapshot_dir   # os.path.join(snapshot_base, "bootstrap")

        # pass to everyone
        args["bootstrap_dir"] = bootstrap_dir

        # parse arguments before paths are removed
        # we no longer support this since it writes numeric hyperparameters as string which on SQL must always be strings
        # and having numeric hyperparameters as strings messes up HP search algorithms like DGD
        #job_hparams = self.build_job_hparams(cmd_parts)

        # # create CODE SNAPSHOT
        # if fake_submit:
        #     script_dir = snapshot_dir
        # else:
        #     # note: always create a snapshot dir for backends to add needed files
        #     file_utils.ensure_dir_deleted(snapshot_dir)
        #     script_dir = self.snapshot_all_code(bootstrap_dir, snapshot_dir, cmd_parts, args)

        # self.script_dir = script_dir

        direct_run = args["direct_run"]

        # do we need to start the xt controller?
        use_controller = not direct_run
        adjustment_scripts = None

        # create a job_secret that can later be used to authenticate with the XT controller
        # NOTE: we currently log this secret as a job property, which allows all team members to view and control this job
        job_secret = str(uuid.uuid4())

        # do we need to build a "docker run" command?
        args["docker_login_cmd"] = None
        args["docker_cmd"] = None
        args["docker_is_windows"] = False

        env_vars = args["env_vars"]

        # expand needed args (used by docker command, runner, and batch/pool backends)
        # TODO: centralize all this env var processing
        if env_vars:

            request_id = args["from_request"]
            if request_id:
                # use environment variables from the request
                filter_dict = {"request_id": request_id}
                records = self.store.database.get_info_for_requests(workspace, filter_dict)
                rr = records[0]
                env_vars_text = rr["env_vars"]
                env_vars = json.loads(env_vars_text)

            else:
                for name, value in env_vars.items():
                    if value.startswith("$$"):
                        value = os.getenv(value[2:])
                    env_vars[name] = value

            # add a special XT env var letting us know which user-specified vars were passed
            env_vars["XT_USER_ENV_VARS"] = " ".join(env_vars.keys())

            # update args copy
            args["env_vars"] = env_vars
            
        # create CODE SNAPSHOT
        if fake_submit:
            script_dir = snapshot_dir
        else:
            # note: always create a snapshot dir for backends to add needed files
            file_utils.ensure_dir_deleted(snapshot_dir)
            script_dir = self.snapshot_all_code(bootstrap_dir, snapshot_dir, cmd_parts, args)

        if not self.backend.provides_container_support():
    
            docker_name = args["docker"]
            if not docker_name:
                docker_name = utils.safe_value(compute_def, "docker")
                args["docker"] = docker_name
    
            if docker_name and docker_name != "none":
                self.build_docker_cmd(docker_name, compute, service_type, bootstrap_dir, job_secret, setup_name, 
                    env_vars, args)
                
        # BUILD CMDS (from static hparam search, user multi cmds, or single user cmd)
        cmds, runsets, total_run_count, repeat_count, run_specs, using_hp, using_aml_hparam, sweeps_text, search_style = \
            self.build_cmds_with_search(service_type, cmd_parts, parent_script, run_script, run_cmd_from_script, use_controller, dry_run, args)

        if dry_run:
            return None
        
        self.script_dir = script_dir

        request_flag = args["request"]
        if request_flag:
            node_count = args["nodes"]
            if not node_count:
                node_count = 1

            self.create_run_request(workspace, snapshot_dir, username, compute, node_count, total_run_count, args)
            return None

        if not using_hp and not using_aml_hparam:
            # zap values of related arguments for better run reports (omitting empty columns)
            search_type = None
            search_style = None
            static_search = None

            args["search_type"] = search_type
            args["static_search"] = static_search

        # make new values available
        args["search_style"] = search_style
        args["total_run_count"] = total_run_count

        resume_name = args['resume_name']
        keep_name = False  # args['keep_name']
        is_distributed = args['distributed']
        direct_run = args["direct_run"]
        events = args["events"]
        notify = args["notify"]

        if events:
            config_events = self.config.get("events")

            for event_name in events:
                if not event_name in config_events:
                    errors.user_error("specified event not found in events dictionary of xt_config file: {}".format(event_name))

                event = config_events[event_name]
                self.validate_event(event_name, event)

        if notify:
            self.validate_notify(notify)

        # CREATE JOB (in database and blobs) to hold all runs
        if fake_submit:
            # use lastrun/lastjob info to get a fast incremental fake job number
            xtd = xt_dict.read_xt_dict()
            fake_job_num = xtd["fake_job_num"] if "fake_job_num" in xtd else 1
            xtd["fake_job_num"] = fake_job_num + 1
            xt_dict.write_xt_dict(xtd)
            job_id = "fake_job" + str(fake_job_num)
        else:
            job_id = self.store.create_job(workspace)
        fb.feedback(job_id)

        return compute, compute_def, workspace, job_id, sweeps_text, cmds, fake_submit, using_hp, is_distributed, \
            total_run_count, target_file, ps_path, using_aml_hparam, run_specs, repeat_count, service_type, search_style, \
            runsets, bootstrap_dir, snapshot_dir, script_dir, snapshot_base, job_secret, resume_name, use_controller

    def submit_job(self, compute, compute_def, workspace, job_id, sweeps_text, cmds, fake_submit, using_hp, is_distributed, 
        total_run_count, target_file, ps_path, using_aml_hparam, run_specs, repeat_count, service_type, search_style, 
        runsets, bootstrap_dir, snapshot_dir, script_dir, snapshot_base, job_secret, resume_name, use_controller, args):

        # expand system names in experiment
        experiment = args["experiment"]
        experiment = utils.expand_xt_vars(experiment, job_id=job_id)
        args["experiment"] = experiment

        if experiment:
            # create the experiment, if it doesn't already exist
            if not self.store.does_experiment_exist(workspace, experiment):
                self.store.create_experiment(workspace, experiment)

        # start the feedback (by parts)
        fb.feedback("{}: {}".format("target", compute))

        # make available to everyone
        args["job_id"] = job_id

        # write hparams to job-level file
        boxes, num_boxes = self.write_hparams_to_job(workspace, job_id, cmds, fake_submit, using_hp, args)

        if sweeps_text and not fake_submit:
            self.upload_sweep_data(sweeps_text, experiment, job_id, args=args)

        # if num_boxes > 1 and service_type != "batch":
        #     fb.feedback("", is_final=True)

        parent_name = None

        # BUILD RUNS, by box
        job_runs = []
        run_count = 1 if is_distributed else len(boxes) 
        secrets_by_node = {}
        remote_control = args["remote_control"]

        job_create_time = time_utils.get_arrow_now_str()

        self.build_all_node_runs(boxes, remote_control, run_count, total_run_count, 
                target_file, ps_path, using_hp, using_aml_hparam, run_specs, job_id, 
                parent_name, cmds, compute_def, repeat_count, fake_submit, search_style, job_runs, 
                secrets_by_node, is_distributed, service_type, args)

        # build box: runs dict for job info file
        runs_by_box, last_run = self.build_runs_by_box(job_runs, workspace)

        node_count = len(boxes)
        args["node_count"] = node_count

        args["job_id"] = job_id
        experiment = utils.expand_xt_vars(experiment, job_runs=job_runs, args=args)

        # now that we have run names for all static run names for all nodes, we can adjust cmds (and before files) for using the controller
        if use_controller:
            # we will create 2 temp. controller files in the CURRENT DIRECTORY (that will be captured to JOB)
            # this will also adjust commands for each node to run the XT controller
            adjustment_scripts = self.core.adjust_job_for_controller_run(job_id, job_runs, cmds, runsets, using_hp, experiment, service_type, bootstrap_dir, 
                search_style, args=args)

        else:
            adjustment_scripts = self.core.adjust_job_for_direct_run(job_id, job_runs, cmds, using_hp, experiment, service_type, snapshot_dir, 
                search_style, args=args)

        service_name = utils.safe_value(self.backend.compute_def, "service")
        user_assigned_managed_identity = self.config.get("external-services", service_name, "user-identity-id")
        args["uami_id"] = user_assigned_managed_identity

        uami_client = self.config.get("external-services", service_name, "user-identity-client-id")
        args["uami_client_id"] = uami_client

        # add env vars used by: setup script, controller, and runs
        env_vars = args["env_vars"]

        # create a job guid to uniquely identify this job across all XT instances
        job_guid = str(uuid.uuid4())

        data_local = args["data_local"]
        if "$scriptdir" in data_local:
            data_local = os.path.realpath(data_local.replace("$scriptdir", script_dir))
            args["data_local"] = data_local

        model_local = args["model_local"]
        if "$scriptdir" in model_local:
            model_local = os.path.realpath(model_local.replace("$scriptdir", script_dir))
            args["model_local"] = model_local

        is_direct_run = self.config.get("general", "direct-run")
        if is_direct_run:
            run_count = len(cmds) if cmds else args["runs"]
            if len(job_runs) != run_count:
                errors.user_error("When specifying --direct-run=1, the number of runs must match the number of nodes.")

        # allows backend to build the node script (shared by all nodes of the run)
        self.backend.build_node_script_and_adjust_runs(job_id, job_runs, using_hp, experiment, service_type, snapshot_dir, env_vars, cmds=cmds, args=args)

        # upload CODE from snapshot_dir
        code_upload = args["code_upload"]
        code_omit = args["code_omit"]
        code_zip = args["code_zip"]
    
        fb.feedback("uploading files: ", add_seperator=False)
        copied_code_files = None

        if not fake_submit:
            if code_upload:
                # upload users CODE FILES
                copied_code_files = self.core.upload_before_files_to_job(job_id, snapshot_dir, "before/code", 
                    code_omit, code_zip, "code", args)

            # upload DATA from data_local (do we need to keep this?  should we upload to normal DATA location, vs. job?)
            data_upload = args["data_upload"]
            if data_upload:
                if not data_local:
                    errors.config_error("cannot do data-upload because no data-local path is defined in the XT config file")

                data_omit = args["data_omit"]
                data_zip = "none"

                self.core.upload_before_files_to_job(job_id, data_local, "before/data", data_omit, data_zip, "data", args)
        
        # dispatch to BACKEND submitters
        '''
        Note: backend submitter functions are responsible for:
            - submitting the job (for each node, queue runs for that node)
            - return service job id (or list of them if per node)
        '''
        code_uploaded_dir = snapshot_dir

        # change the snapshot_dir to a new dir that contains only files that were uploaded
        if not code_zip or code_zip == "none":
            pass
        elif copied_code_files:
            code_uploaded_dir = snapshot_base + "/code_uploaded"
            file_utils.ensure_dir_exists(code_uploaded_dir)
            
            for fn in copied_code_files:
                fn_dst = code_uploaded_dir + "/" + os.path.basename(fn)
                shutil.copyfile(fn, fn_dst)

        '''
        Order dependency analysis (updated: Aug-31-2022)
            - the job_info record is created in the above code

            - log_runs_queued() creates the following node records:
                - node_info 
                - node_stats
                - node_tags 

            - log_runs_queued() calls process_run_event() which creates the following PARENT run records:
                - run_tags
                - run_info
                - run_stats

            - call to store.log_job_info() calls odbc.update_job_info() which:
                - updates job_info
                - updates job_stats
                - creates job_tags

            -backend.submit_job():
                - submits each node as a job (singularity) or the set of nodes as a pool (azure batch)
                - as each node is submitted/processed, the associated node_stats record is updated (pool_info column)

            - When a node is started by the backend, the node will need to access:
                - the associated node_stats record (to update node timings)
                - the associated job_stats record (to allocate child run id's and update job timings)

            - finally, after all nodes have been started, update_job_info is called to update the
            columns: service_job_info and service_info_by_node

        '''
        # NOTE: order of next 3 statements must be maintained (see above).
        self.log_runs_queued(runs_by_box, workspace, job_id, total_run_count, secrets_by_node, 
            service_info_by_node=None, args=args)

        #self.store.database.create_job_stats(workspace, job_id)

        # create the JOB_INFO record (and fully initialize JOB_STATS)
        self.create_job_info(job_id, search_style, total_run_count, runs_by_box, experiment, job_guid, job_secret, repeat_count, 
            compute_def, workspace, secrets_by_node, job_create_time, args)

        # SUBMIT JOB to backend 
        # backend requirement: update each node_info ASAP with service_info_by_node
        service_job_info, service_info_by_node = \
            self.backend.submit_job(job_id, job_runs, workspace, compute_def, resume_name, 
                repeat_count, using_hp, runs_by_box, experiment, code_uploaded_dir, adjustment_scripts, args)

        # note: singularity/AML/ITP have no job-level info, so service_job_info is {} for them
        #assert service_job_info

        # POST SUBMIT processing
        if not fake_submit:

            # update job_info with: service_job_info, service_info_by_node
            self.update_job_info_post_submit(job_id, workspace, service_job_info, service_info_by_node)

        fb.feedback("done", is_final=True)

        escape = args["escape"]

        # update lastrun/lastjob info
        xtd = xt_dict.read_xt_dict()

        xtd["last_run"] = last_run
        xtd["last_job"] = job_id

        xt_dict.write_xt_dict(xtd)

        # return values for API support (X)
        return cmds, run_specs, using_hp, using_aml_hparam, sweeps_text, compute_def, job_id 

    def get_location(self, backend) -> str:
        cd = backend.compute_def
        service = cd["service"]

        location = backend.get_location(service)
        return location 
    
    def create_job_info(self, job_id, search_style, total_run_count, runs_by_box, experiment, job_guid, job_secret, repeat_count, 
            compute_def, workspace, secrets_by_node, job_create_time, args):

            fb.feedback("logging job")

            # write the job info file (now that backend has had a chance to update it)
            job_num = job_helper.get_job_number(job_id)

            xt_cmd = args["xt_cmd"]
            schedule = args["schedule"]
            concurrent = args["concurrent"]
            num_dgd_seeds = utils.safe_value(args, "num_dgd_seeds")

            # this job property is used to ensure we don't exceed the specified # of runs when using repeat_count on each node
            dynamic_runs_remaining = None if search_style == "single" else total_run_count
            node_count = len(runs_by_box)

            # NOTE: for mongo v2, we only support schedule=static
            #child_runs_by_node, child_runs_key = self.store.database.build_child_runs_schedule_data(total_run_count, node_count)

            tag_dict = args["tags"]

            locations = utils.safe_value(compute_def, "locations")
            if locations and (not self.backend.supports_setting_location()):
                console.print("warning: backend {} does not support setting compute location (only supports a single, preset location)".format(self.backend.get_name()))

            if not locations:
                # get the location associated with the backend compute being used
                locations = [ self.get_location(self.backend) ]

            # NEW COLS: sla, low_pri, vm_size, sku, service_name, service_type, aml_compute, compute_target, num_dgd_seeds
    
            dd = {
                # JOB_INFO: flat READONLY props (18)
                "sla": utils.safe_value(compute_def, "sla"),
                "low_pri": utils.safe_value(compute_def, "low-pri"),
                "vm_size": utils.safe_value(compute_def, "vm-size"),
                "sku": utils.safe_value(compute_def, "sku"),
                "service_name": utils.safe_value(compute_def, "service"),
                "service_type": utils.safe_value(args, "service_type"),
                "aml_compute": utils.safe_value(compute_def, "compute"),
                "compute_target": utils.safe_value(compute_def, "name"),
                "location": locations[0] if locations else None,           # for now, we only log primary location 

                # old cols
                "concurrent": concurrent,
                "exper_name": experiment, 
                "hold": args["hold"], 
                "job_id": job_id, 
                "job_num": job_num, 
                "job_guid": job_guid, 
                "job_secret": job_secret, 
                "node_count": node_count, 
                "num_dgd_seeds": num_dgd_seeds,
                #"maximize_metric": args["maximize_metric"],      # not yet in DB/job_stats
                "primary_metric": args["primary_metric"], 
                "run_count": total_run_count, 
                "repeat": repeat_count, 
                "schedule": schedule, 
                "search_style": search_style,     
                "search_type": args["search_type"], 
                "username": args["username"], 
                "ws_name": workspace, 
                "xt_cmd": xt_cmd, 
                "sleep_on_exit": args["sleep_on_exit"],

                # embedded READONLY props (2)
                "pool_info": compute_def, 
                #"service_job_info": service_job_info, 

                # JOB_STATS: flat UPDATABLE props (8)
                "completed_runs": 0, 
                "running_nodes": 0, 
                "running_runs": 0, 
                "error_runs": 0, 
                "restarts": 0,
                "db_retries": 0,
                "storage_retries": 0,
                "next_run_index": 0,
                "dynamic_runs_remaining": dynamic_runs_remaining, 
                "job_status": "submitted", 
                "started": job_create_time,

                # SERVICE_INFO: embedded READONLY props BY NODE (2)
                "runs_by_box": runs_by_box, 
                #"service_info_by_node": service_info_by_node,
                
                # CONNECT_INFO: embedded UPDATABLE props (2)
                "connect_info_by_node": {}, 
                "secrets_by_node": secrets_by_node,  

                # job-detectable HPARAMS
                #"hparams": job_hparams,

                # TAGS
                "tags": tag_dict,
            }

            self.store.log_job_info(workspace, job_id, dd)

    def update_job_info_post_submit(self, job_id, workspace, service_job_info, service_info_by_node):

        dd = {"ws_name": workspace, "job_id": job_id, "service_job_info": service_job_info, "service_info_by_node": service_info_by_node}
        self.store.log_job_info(workspace, job_id, dd, update_job_stats=False)

    def log_run_and_node(self, workspace, box_name, runs_by_box, job_id, total_run_count, secrets_by_node, 
        service_info_by_node, args):

        box_run = runs_by_box[box_name]
        run_name = box_run["run_name"]
        node_index = box_run["box_index"]
        node_count = len(runs_by_box)
        node_id = utils.node_id(node_index)

        box_secret = secrets_by_node[node_id]
        service_info = service_info_by_node[node_id] if service_info_by_node else None

        ws_name = args["workspace"]
        exper_name = args["experiment"]

        id_for_node = "{}/{}/{}".format(ws_name, job_id, node_index)

        # does format supports NODE INFO?
        if store_utils.STORAGE_FORMAT == "2":
            # create NODE_INFO record 
            self.write_node_info_data(id_for_node, ws_name, job_id, node_index, total_run_count, node_count, 
                box_name, run_name, box_secret, service_info, exper_name, args)

            # create NODE_STATS record 
            self.write_node_stats_data(id_for_node, ws_name)

            # create NODE_TAGS record 
            tag_list = args["tags"]
            td = utils.tag_dict_from_list(tag_list)
            self.write_node_tags_data(id_for_node, ws_name, job_id, td)

        # log QUEUED event for flat/parent run        
        self.store.log_run_event(workspace, run_name, "status-change", {"status": "queued"}, job_id=job_id) 

    def log_runs_queued(self, runs_by_box, ws_name, job_id, total_run_count, secrets_by_node, 
        service_info_by_node, args):

        from threading import Lock
        worker_lock = Lock()

        # create each run on a worker thread
        next_progress_num = 1
        box_name_list = list(runs_by_box.keys())

        def thread_worker(box_names, workspace):
            for box_name in box_names:
                nonlocal next_progress_num

                self.log_run_and_node(workspace, box_name, runs_by_box, job_id, total_run_count, 
                    secrets_by_node, service_info_by_node, args)

                with worker_lock:
                    node_msg = "logging runs: {}/{}".format(next_progress_num, len(box_name_list))
                    fb.feedback(node_msg, id="log_msg")  # , add_seperator=is_last)
                    next_progress_num += 1

        max_workers = args["max_workers"]

        # turn ON insert buffering
        self.store.database.set_insert_buffering(100)

        utils.run_on_threads(thread_worker, box_name_list, max_workers, [ws_name])

        # turn OFF insert buffering
        self.store.database.set_insert_buffering(0)

        # change status of all runs for this job to "queued", in database
        self.store.database.update_job_run_stats(ws_name, job_id, {"status": "queued"})

        # TODO: change all parent run status from created to queued with single:
        #   update [run_stats] set [status] = 'queued' where [_id] like 'ws4/job17_%'

    def build_all_node_runs(self, boxes, remote_control, run_count, total_run_count, 
        target_file, ps_path, using_hp, using_aml_hparam, run_specs, job_id, 
        parent_name, cmds, compute_def, repeat_count, fake_submit, search_style, job_runs, 
        secrets_by_node, is_distributed, service_type, args):

        # create each run on a worker thread
        thread_lock = Lock()   
        next_progress_num = 1

        def thread_worker(node_indexes, boxes, remote_control, run_count, total_run_count, 
            target_file, ps_path, using_hp, using_aml_hparam, run_specs, job_id, 
            parent_name, cmds, compute_def, repeat_count, fake_submit, search_style, job_runs, 
            secrets_by_node, is_distributed, service_type, run_names, args):

            node_count = len(node_indexes)

            for node_index in node_indexes:
                # generate a box secret for talking to XT controller for this node
                box_secret = str(uuid.uuid4()) if remote_control else ""
                run_name = run_names[node_index]
                node_run_specs = dict(run_specs)    # make a copy that this node can own

                run_data = self.build_primary_run_for_node(node_index, run_count, total_run_count, 
                    boxes[node_index], target_file, ps_path, using_hp, using_aml_hparam, node_run_specs, job_id, 
                    parent_name, cmds, compute_def, repeat_count, fake_submit, search_style, box_secret, 
                    node_count, run_name=run_name, args=args)

                with thread_lock:
                    nonlocal next_progress_num

                    # NEW CHANGE: we now only have 1 run per box/node (the primary/parent run)
                    job_runs.append(run_data)

                    node_id = utils.node_id(node_index)            
                    secrets_by_node[node_id] = box_secret

                    # FEEDBACK 
                    ptype = "single " if search_style == "single" else "parent "
                    if is_distributed:
                        ptype = "master "

                    if run_count == 1:
                        node_msg = "creating {}run".format(ptype)
                    else:
                        node_msg = "creating {}runs: {}/{}".format(ptype, next_progress_num, run_count)

                    fb.feedback(node_msg, id="node_msg")  # , add_seperator=is_last)
                    next_progress_num += 1

        max_workers = args["max_workers"]
        node_index_list = range(len(boxes))

        # we want to create run names in "normal order" (not subject to random bg workers races)
        # so, we create all the run_names up-front
        ws_name = args["workspace"]
        is_parent = search_style != "single"

        run_names = []
        for node_index in node_index_list:
            run_name = self.store.database.get_next_run_name(ws_name, job_id, is_parent, total_run_count, node_index)
            run_names.append(run_name)

        args_for_worker = [boxes, remote_control, run_count, total_run_count, 
            target_file, ps_path, using_hp, using_aml_hparam, run_specs, job_id, 
            parent_name, cmds, compute_def, repeat_count, fake_submit, search_style, job_runs, 
            secrets_by_node, is_distributed, service_type, run_names, args]

        # turn ON insert buffering
        self.store.database.set_insert_buffering(100)

        utils.run_on_threads(thread_worker, node_index_list, max_workers, args_for_worker)

        # turn OFF insert buffering (and flush buffers)
        self.store.database.set_insert_buffering(0)

        # sort job_runs to normal order
        job_runs.sort(key=lambda r: r["box_index"])

    def get_cmd_line_args_from_file(self, fn):
        with open(fn, "rt") as infile:
            text = infile.read()
            lines = text.split("\n")

        arg_parts = []

        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                # remove comments from line with arg(s)
                if "#" in line:
                    line = line.split("#", 1)[0]

                line = line.strip()
                if line:
                    parts = line.split()
                    arg_parts += parts

        hd = self.parse_script_args(arg_parts)
        return hd

    def build_job_hparams(self, cmd_parts):
        hparams = None

        # make copy to modify
        first_arg_index = None

        # first index of first script or app arg
        if cmd_parts[0].startswith("python"):

            # look for python options before script name
            for i, part in enumerate(cmd_parts[1:]):
                if not part.startswith("-"):
                    # found script at i+1
                    first_arg_index = i+2
                    break

        else:
            first_arg_index = 1

        if first_arg_index:
            pending_name = None

            args = cmd_parts[first_arg_index:]
            hparams = self.parse_script_args(args)

        return hparams

    def parse_script_args(self, args):
        hparams = {}
        pending_name = None

        for arg in args:
            '''
            look for arg/value in 3 forms:
                - arg=value
                - arg
                - arg value  (value is in following arg)
            '''
            if arg.startswith("-"):
                # strip the leading dashes
                arg = arg.lstrip("-")

                # found an arg name
                if "=" in arg:
                    name, value = arg.split("=")
                    hparams[name] = value
                    pending_name = None

                    if value.startswith("["):
                        # in-line HPARAM SEARCH specification
                        return None
                else:
                    # for now, treat as option without value
                    hparams[arg] = None
                    pending_name = arg
            elif arg.startswith("@"):
                fn = arg[1:]
                ad = self.get_cmd_line_args_from_file(fn)
                hparams.update(ad)
            else:
                # is this a value for a pending name?
                if pending_name:
                    hparams[pending_name] = arg
                    pending_name = None

                    if arg.startswith("["):
                        # in-line HPARAM SEARCH specification
                        return None

        return hparams if hparams else None

    def fixup_script_in_cmd(self, cmd, node_script_path):
        # cmd_parts = cmd_utils.user_cmd_split(cmd)
        
        # self.adjust_script_dir(cmd_parts, node_script_path)

        # # add "-u" for python cmds
        # if len(cmd_parts) > 1 and cmd_parts[0].startswith("python") and cmd_parts[1] != "-u":
        #     cmd_parts.insert(1, "-u")

        # new_cmd = " ".join(cmd_parts)
        # return new_cmd
        return cmd

    def read_user_multi_commands(self, using_hp, run_script, cmd_parts, args):
        '''
        args:
            using_hp: if True, we are doing a hyperparameter search
            run_script: the path to the ML script specified for the run command
            cmd_parts: the run command and args, in list form
            args: the big list of run command arguments, options, and flags

        processing:
            - there are 2 possible sources of user-generated commands:
                - the run script (if --multi-commands option was specified)
                - the config file (if it contains a "commands" outer property)
            
            - if using the run script for commands, it can be a text file
              (containing 1 command per line), or a .yaml file with the
              outer property constants.HPARAM_RUNSETS.

        returns:
            - if no commands or runsets found, returns None
            - else, returns (commands, runsets)
        '''
        cmds = None
        runsets = None
        
        lines = self.config.get("commands")
        multi_commands = args["multi_commands"]
        node_script_path = args["node_script_path"]
 
        if lines:
            if using_hp:
                errors.combo_error("Cannot specify commands in config file with hyperparameter search")
            if multi_commands:
                errors.combo_error("Cannot specify commands in config file with --multi-commands")

            # commands specified in the config file
            args["multi_commands"] = True
            cmds = [self.fixup_script_in_cmd(line, node_script_path) for line in lines]

        elif multi_commands:
            if using_hp:
                errors.combo_error("Cannot specify --multi-commands with hyperparameter search")

            # read MULTI CMDS
            fn_script = args["script"]  # run_script if run_script else cmd_parts[0]
            ext = os.path.splitext(fn_script)[1]

            if ext == ".yaml":
                data = file_utils.load_yaml(fn_script)

                if not constants.HPARAM_RUNSETS in data:
                    errors.ConfigError("--multi-commands .yaml file is missing required section: {}".format( \
                        constants.HPARAM_RUNSETS))

                if not constants.HPARAM_COMMAND in data:
                    errors.ConfigError("--multi-commands .yaml file is missing required section: {}".format( \
                        constants.HPARAM_COMMAND))

                runsets = data[constants.HPARAM_RUNSETS]
                cmd = data[constants.HPARAM_COMMAND]
                cmds = [self.fixup_script_in_cmd(cmd, node_script_path)]
            else:
                lines = file_utils.read_text_file(fn_script, as_lines=True)
                lines = [line.strip() for line in lines if line and not line.strip().startswith("#")]
                cmds = [self.fixup_script_in_cmd(line, node_script_path) for line in lines]

        return (cmds, runsets) if cmds else None

    def gen_runsets_report(self, runsets):
        fn = os.path.expanduser("~/.xt/runsets.txt")
        fn = os.path.abspath(fn)

        with open(fn, "wt") as outfile:
            for rs in runsets:
                outfile.write("runset: {}\n".format(rs))

        console.print("--> to view generated HP runsets, see the file: {}".format(fn))

    def extract_shared_args(self, args, cmds):
        # make a list of shared args in each cmd
        prefix = args["option_prefix"]

        # create a dict initialized with 0 as args are added
        args_count = defaultdict(int)

        for cmd in cmds:
            args = cmd.split(" " + prefix)
            args = args[1:]    # skip first part (python -u scriptname @foo)
            for arg in args:
                pass

        fn_shared_args = None   
        return cmds, fn_shared_args
    
    def build_cmds_with_search(self, service_type, cmd_parts, parent_script, run_script, run_cmd_from_script, 
        use_controller, dry_run, args):
        '''
        args:
            - service_type: the type of backend service being used (aml, batch, etc.)
            - cmd_parts: list of the user's ML app and arg/options 
            - parent_script: user-specified script that needs to be run to configure box for all child runs
            - run_script: if user app is a shell script or command line .bat file, the text of file
            - run_cmd_from_script: if user's ML app is a shell or command line script, the run command located within it
            - use_controller: if False, XT controller is not being used (direct run)
            - dry_run: if True, job will not be submitted (user just wants to see list of static runs)

        processing:
            - determine the search_style needed, the associated list of user commands, and the total number of runs

        returns:
            - cmds: the list of 1 or more commands to be run
            - run_count: to total number runs to be executed
            - repeat_count: if number of runs per node (approximately)
            - run_specs: a dictionary of run information (easier to pass around)
            - using_hp: if True, a static or dynamic hyperparameter search is being done
            - using_aml_hparam: if True, we are doing a direct-run AML hyperparameter search
            - sweeps_text: hyperparameter search specs 
            - search_style: one of: single, multi, repeat, static, dynamic
        '''
        using_hp = False
        show_run_report = True
        repeat_count = None
        using_aml_hparam = False
        search_style = None
        cmds = None
        runsets = None
        run_count = None

        # get run_cmd
        run_cmd = run_cmd_from_script
        if not run_cmd:
            run_cmd = " ".join(cmd_parts)

        # by default, we return same cmd
        new_run_cmd = run_cmd

        is_aml = (service_type == "aml")        # self.is_aml_ws(workspace)
        use_aml_for_hparam = (is_aml and not use_controller)

        # get info about nodes/boxes
        boxes, _, service_type = box_information.get_box_list(self.core, args=args)
        node_count = len(boxes)

        # HPARAM SEARCH
        cmds, runsets, sweeps_text, new_run_cmd, fn_gen_shared = self.build_static_hparam_cmds(run_cmd, node_count, args)
        
        # NOTE: if runsets is not None, then this is a static search where user needs YAML files generated for each child run 
        #       if this is a static search and runsets is None, then runsets have already been applied to cmdlines

        # adjust cmds
        if runsets is not None:
            show_run_report = False
            
        using_hp = not(not sweeps_text)
        if using_hp and use_aml_for_hparam:
            using_aml_hparam = True
            # for AML hyperdrive, we pass only constant args from cmd_parts
            #cmd_parts = [tp for tp in template_parts if tp != '{}']

        if runsets:
            self.gen_runsets_report(runsets)

        if cmds:
            # STATIC HPARAM SEARCH
            #run_count = len(runsets) if runsets else len(cmds)
            run_count = len(cmds)
            #runsets = None      # do not process further in controller
            search_style = "static"

        runs = args["runs"]
        max_runs = args["max_runs"]
        grid_repeat = args["grid_repeat"]
        runs_per_set = args["runs_per_set"]

        # USER MULTI CMDS
        result = self.read_user_multi_commands(using_hp, run_script, cmd_parts, args)
        if result:
            cmds, runsets = result

            # set run_count 
            result_count = len(runsets) if runsets else len(cmds)

            if runs:
                run_count = runs
            elif max_runs:
                run_count = min(max_runs, result_count)
            else:
                run_count = result_count

            search_style = "multi"
            new_run_cmd = cmds[0]

        if not cmds:
            # SINGLE CMD 
            # DYNAMIC HPARAM or REPEAT or SINGLE search style

            # we will use repeat_count on each node, as needed, to reach specified runs
            run_count = runs if runs else node_count 
            
            if using_hp:
                search_style = "dynamic"
            else:
                search_style = "repeat" if run_count > 1 else "single"

            if search_style != "single":
                repeat_count = math.ceil(run_count / node_count)

            cmds = [new_run_cmd]
            show_run_report = False

        if grid_repeat:
            # duplicate cmds so they are repeated N times on each node
            # nodes are assigned runs in contigous blocks (node 1: runs 1-N, node 2: runs N+1-2N, etc.)
            cmds = [x for x in cmds for _ in range(grid_repeat)]
            run_count = len(cmds)

        elif using_hp and search_style == "grid" and runs_per_set and runs is None:
            # commands (presumably from search_type=grid) are repeated N times (with no run/node assoication)
            new_cmds = []
            for cmd in cmds:
                new_cmds += [cmd]*runs_per_set
            
            cmds = new_cmds
            run_count = len(cmds)

        if run_count > 1:
            # move shared args into a .yaml file and add it to the commands in place of the args
            # cmds, fn_shared_args = self.extract_shared_args(args, cmds)
            pass

        if show_run_report:
            console.print()   
            dr = " (dry-run)" if dry_run else ""
            search_type = args["search_type"]
            stype = "(search-type=" + search_type + ") " if search_style=="static" else ""

            console.print("{} {}runs{}:".format(search_style, stype, dr))

            if grid_repeat:
                runsets = None
                search_style = "static"
                node_index = -1

                for i, run_cmd_parts in enumerate(cmds):
                    if i % grid_repeat == 0:
                        node_index += 1
                        print("\nnode {}:".format(node_index))

                    node_id = utils.node_id(node_index)
                    console.print("  {}. {}".format(i+1, run_cmd_parts))
            else:
                if runsets:
                    console.print("  command: {}".format(cmds[0]))
                    console.print("  runsets:")

                    for i, runset in enumerate(runsets):
                        console.print("    {}. {}".format(i+1, runset))
                else:
                    for i, run_cmd_parts in enumerate(cmds):
                        console.print("  {}. {}".format(i+1, run_cmd_parts))

            console.print()   

        # finally, package info into run_specs to make info easier to pass thru various APIs
        new_cmd_parts = cmd_utils.user_cmd_split(new_run_cmd)
        run_specs = {"cmd_parts": new_cmd_parts, "run_script": run_script, "run_cmd": new_run_cmd, "parent_script": parent_script}

        return cmds, runsets, run_count, repeat_count, run_specs, using_hp, using_aml_hparam, sweeps_text, search_style

    def adjust_cmds(self):
        pass


    def build_static_hparam_cmds(self, cmd_line, node_count, args):
        '''
        args:
            - cmd_line: user's ML app and its arguments
            - args: dictionary of XT run cmd args/options

        processing:
            - gather hyperparameter search specs from either special app command line options or
              user-specified hp-config file (.yaml)
            - if doing random or grid search, generate the commands that comprise
              the search
             
        return:
            - generated run commands
            - runsets (a list of runset dicts)
            - the search specs (sweeps text)
            - the run cmd (with hp search options removed, if any found)
        '''
        num_runs = args["runs"]
        max_runs = args["max_runs"]
        option_prefix = args["option_prefix"]
        search_type = args["search_type"]
        fn_sweeps = args["hp_config"]
        static_search = args["static_search"]

        # if not cmd_line:
        #     cmd_line = " ".join(cmd_parts)

        # default return values
        run_cmd = cmd_line
        sweeps_text = None
        run_cmds = None
        runsets = None
        fn_gen_shared = None

        # gather hyperparameters (command line options or hp-search.yaml file)
        if search_type != None:
            hp_client = HPClient()
            dd = {}
            
            if option_prefix:
                # see if hp search params specified in ML app's command line options
                dd, run_cmd = hp_client.extract_dd_from_cmdline(cmd_line, option_prefix)

            if not dd and fn_sweeps:
                # get hp search params from search.yaml file
                dd = hp_client.yaml_to_dist_dict(fn_sweeps)

            if dd:
                # write parameters to YAML file for run record 
                # and use by dynamic search, if needed
                sweeps_yaml = hp_client.dd_to_yaml(dd)
                sweeps_text = yaml.dump(sweeps_yaml)
                
                # should we preform the search now?
                if (search_type == "grid") or (static_search and search_type in ["random"]):
                    extract_single_hps = args["extract_single_hps"]

                    runsets, single_values = hp_client.generate_hp_sets(dd, search_type, num_runs, max_runs, node_count, extract_single_hps)
        
                    if single_values:
                        fn_gen_shared = "_gen_.yaml"    # make it look like a temp/system generated file
                        # write single values to a generated .yaml file
                        with open(fn_gen_shared, "wt") as outfile:
                            outfile.write("args:\n")
                            for name, value in single_values:
                                outfile.write("  {}: {}\n".format(name, value))

                    # why was this conditional on option_prefix being found in cmd_line?
                    #if option_prefix and option_prefix in cmd_line:
                    if option_prefix:
                        # apply runsets to run_cmd to generate cmd list
                        cmd_line_base = run_cmd

                        # add the generated .yaml file of common args to the command line
                        if fn_gen_shared:
                            cmd_line_base += " @{}".format(fn_gen_shared)

                        run_cmds = hp_client.generate_runs(runsets, cmd_line_base, option_prefix)
                        runsets = None    # since we have applied them to run_cmds
                    else:
                        # controller will use runsets when launching each child run (and generate a runset yaml file to be read by that child)
                        # run_cmds = [cmd_line]
                        run_cmds = len(runsets)*[cmd_line]   # duplicate the cmd_line for each run_set

                else:
                    # dynamic HP
                    pass
                #print("{} commands generated".format(len(run_cmds)))



        return run_cmds, runsets, sweeps_text, run_cmd, fn_gen_shared

# flat functions
def update_compute_def_from_cmd_options(compute_def, hold=False):
    # support for DEFAULT_FROM_COMPUTE:
    compute_props = ["vm-size", "azure-image", "low-pri", "box-class", "docker", "setup", "boxes", 
        "vc", "cluster", "queue", "sku", "nodes", "sla", "aml_compute", "service", "locations"]

    # apply any compute-def properties found in explicit args to compute_def
    explict_opts = qfe.get_explicit_options()

    for name, value in explict_opts.items():
        if name in compute_props:

            if name == "aml_compute":
                compute_def["compute"] = value
            else:
                compute_def[name] = value

    # if "hold" specified and queue not explictly set, queue defaults to "interactive"
    if hold and "cluster" in compute_def and "queue" not in explict_opts:
        compute_def["queue"] = "interactive"

            
