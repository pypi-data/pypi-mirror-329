#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# backend_aml.py: support for running jobs under Azure Machine Learning

import os
import time
import shutil
import logging
import urllib.request
import uuid
from hyperopt import hp

from xtlib import utils, xt_vault
from xtlib import errors
from xtlib import scriptor
from xtlib import constants
from xtlib import file_utils
from xtlib import time_utils
from xtlib import run_helper
from xtlib import pc_utils
from xtlib.hparams.hp_process import HPList, HPDist

from xtlib.console import console
from xtlib.hparams import hp_helper
from xtlib.report_builder import ReportBuilder
from xtlib.helpers.feedbackParts import feedback as fb
from xtlib.backends.mount_helper import MountHelper
from xtlib.backends.node_scriptor import NodeScriptor
from xtlib.helpers.notebook_builder import NotebookBuilder

from xtlib.backends.backend_base import BackendBase

SECTION = "external-services"

# azure library loaded on demand
Workspace = None 
Experiment = None
Run = None
ComputeTarget = None

class AzureML(BackendBase):

    def __init__(self, compute, compute_def, core, config, username=None, arg_dict=None, disable_warnings=True):
        super(AzureML, self).__init__(compute, compute_def, core, config, username, arg_dict)

        self.compute = compute
        self.compute_def = compute_def
        self.core = core
        self.config = config
        self.username = username

        self.store = self.core.store
        self.request = None

        # load azure libraries on demand
        global Workspace, Experiment, Run, ComputeTarget
        import azureml.core
        from azureml.core import Experiment, Run
        from azureml.core.workspace import Workspace
        from azureml.core.compute import ComputeTarget

        if disable_warnings:
            # turn off all azure warnings
            logging.getLogger("azureml").setLevel(logging.ERROR)

    def get_name(self):
        return "aml"

    def build_node_script_and_adjust_runs(self, job_id, job_runs, using_hp, experiment, service_type, snapshot_dir, env_vars, args, cmds=None):
        '''
        This method is called to allow the backend to inject needed shell commands before the user cmd.  At the
        time this is called, files can still be added to snapshot_dir.
        '''
        # store_data_dir, data_action, data_writable, store_model_dir, model_action, model_writable,  \
        #     storage_name, storage_key = self.get_action_args(args)

        # local or POOL of vm's
        fn_script = None     # we use same script for each box (but with different ARGS)
        # username = args["username"]
        fn_shim = constants.FN_AML_SHIM
        is_direct_run = args["direct_run"]

        for i, box_run in enumerate(job_runs):
            # wrap the user commands in FIRST RUN of each box (apply data/model actions)
            # box_info = box_run["box_info"]
            # actions = ["data", "model"]
            run_name = box_run["run_name"]
            # is_windows = False
            # node_id = utils.node_id(i)

            run_specs = box_run["run_specs"]
            cmd_parts = run_specs["cmd_parts"]

            if not fn_script:
                # just wrap the user cmd once (shared by all boxes/nodes)
                assert cmd_parts[0] == "python"
                assert cmd_parts[1] == "-u"
                assert len(cmd_parts[2]) > 0 

                # # update the target_fn (might have been switched to the xt controller)
                # target_fn = cmd_parts[2]
                # arg_parts = cmd_parts[3:]

                setup = self.config.get_setup_from_target_def(self.compute_def)
                # use_sudo = utils.safe_value(setup, "use-sudo")       # some AML clusters need sudo

                # fn_wrapped = self.create_wrapper_script(cmd_parts, snapshot_dir, store_data_dir, data_action, 
                #     data_writable, store_model_dir, model_action, model_writable, storage_name, storage_key, actions, 
                #     use_sudo, username, setup, use_allow_other=use_sudo, args=args)

                fn_script, fn_inner = self.build_node_script(box_run, args)

                # AML wants a python script, so use our tiny python shim to run FN_NODE_SCRIPT
                bootstrap_dir = args["bootstrap_dir"]
                fn_from = file_utils.get_xtlib_dir() + "/backends/" + constants.FN_AML_SHIM
                fn_to = bootstrap_dir + "/" + fn_shim
                shutil.copyfile(fn_from, fn_to)

                # copy to submit-logs
                utils.copy_to_submit_logs(args, fn_from)

                # 1/2 calls to this (TODO: remove one)
                # this first call forces singularity to write out the long credential env vars to: constants.FN_SET_ENV_VARS
                dummy_env_vars = {}
                self.get_controller_env_vars(dummy_env_vars, box_run, node_index=i, args=args)

            # NOTE: we pass the NODE_INDEX, RUN_NAME, and DIRECT_CMD as parameters to the fn_wrapped script
            # so that we can share a single script among all nodes
            if args["direct_run"]:
                direct_cmd = cmds[i] if i < len(cmds) else cmds[0]
                run_specs["run_cmd"] = direct_cmd

            script_parts = '{}'.format(os.path.basename(fn_script))

            # using "source" to the script is failing on ITP (Nov-4-2022, so changing it back to /bin/bash)
            #sh_parts = ['source', script_part]
            bash_parts = ['/bin/bash', '--login', script_parts]

            # pass sh_parts as a single argument to avoid wierd "arg": 1 problems with AML estimators
            shim_parts = ["python", "-u", fn_shim, " ".join(bash_parts)]
            run_specs["cmd_parts"] = shim_parts

    def build_node_script(self, first_run, args):

        run_specs = first_run["run_specs"]

        # username = args["username"]ssss
        # cwd = "$HOME/.xt/cwd"

        cmd_parts = run_specs["cmd_parts"]
        node_cmd = " ".join(cmd_parts)
        actions = ["data", "model"]

        # sudo is available, but causes problems with subsequent MNT directory access
        setup = self.config.get_setup_from_target_def(self.compute_def)
        use_sudo = utils.safe_value(setup, "use-sudo")       # some AML clusters need sudo  
        # turn it off for now: (creates mount dirs that normal user code cannot access)
        #if self.get_name() != "singularity":
        use_sudo = False     

        # we need to move our cwd (default working dir is blob-mapped and slow)
        # as of 10/21/2020, ITP recommends we use "/var/tmp" until they disable the NFS mount for $HOME
        # homebase = "$HOME/{}".format(guid)
        homebase = "/var/tmp"
        mountbase = "/var/tmp/.xt"      
        cwd = "{}/.xt/cwd".format(homebase)
        get_env_vars_from_file = (self.get_name() == "singularity")

        mount_helper = MountHelper(compute_def=self.compute_def, homebase=homebase, mountbase=mountbase, sudo_available=use_sudo, actions=actions, 
            use_username=False, use_allow_other=False, nonempty=True, backend=self, config=self.config, args=args)
        
        # native or docker, AML deliveers the code to us as: unzipped bootstrap files and a code .zip file
        use_gpu = args["use_gpu"]
        default_docker_image = self.get_default_docker_image(use_gpu)

        node_scriptor = NodeScriptor(homebase=homebase, cwd=cwd, controller_cmd=node_cmd, 
            manual_docker=False, mount_helper=mount_helper, backend=self, compute_def=self.compute_def, use_sudo=use_sudo, 
            default_docker_image=default_docker_image, get_env_vars_from_file=get_env_vars_from_file, config=self.config, args=args)
        
        fn_script, fn_inner = node_scriptor.generate_script()
        return fn_script, fn_inner

    def gen_code_prep_cmds(self, ca, cmds, cwd, using_docker):

        code_dir = "."       # on singularity, its always in the current dir
        code_fn = code_dir + "/" + constants.CODE_ZIP_FN

        ca.append_title(cmds, "CODE PREP: UNZIP code files to cwd:")

        # AML reuses directories, so we need to clean up first
        ca.append_dir_clean(cmds, cwd)

        # unzip and remove the code.zip file
        ca.append_unzip(cmds, code_fn, cwd)
        if not using_docker:
            ca.append(cmds, "rm {}".format(constants.CODE_ZIP_FN))

        # this step not needed, since bootstrap files are also in the .zip file
        # copy the bootstrap files __*__ type files
        #ca.append(cmds, "cp {}/__* {}".format(code_dir, cwd))

        # move to CWD
        ca.append(cmds, "cd {}".format(cwd))

    def get_default_docker_image(self, use_gpu):
        if use_gpu:
            # recommended for IPT w/GPU: 
            #mcr.microsoft.com/azureml/base-gpu:openmpi3.1.2-cuda10.0-cudnn7-ubuntu16.04
            aml_default = "mcr.microsoft.com/azureml/base-gpu:intelmpi2018.3-cuda9.0-cudnn7-ubuntu16.04"
        else:
            aml_default = "mcr.microsoft.com/azureml/base:intelmpi2018.3-ubuntu16.04"

        return aml_default

    def create_wrapper_script(self, cmd_parts, snapshot_dir, store_data_dir, data_action, 
            data_writable, store_model_dir, model_action, model_writable, storage_name, storage_key, actions, 
             sudo_available, username, setup, use_allow_other, args):
        '''
        ITP subclass overwrites this method.
        '''
        # we need to move our cwd (default working dir is blob-mapped and slow)
        # as of 10/21/2020, ITP recommends we use "/var/tmp" until they disable the NFS mount for $HOME
        # job_home = "$HOME/{}".format(guid)

        # add a GUID as of Aug-21-2022, to make a .xt dir unique and work around unexplainable problems with MNT directories on singularity
        # guid = str(uuid.uuid4())
        # job_home = "/var/tmp/" + guid
        job_home = "/var/tmp/"
        cwd = "{}/.xt/cwd".format(job_home)

        use_gpu = args["use_gpu"]
        self.default_docker_image = self.get_default_docker_image(use_gpu)

        # we only do this once (for the first box/job)
        fn_wrapped = super().wrap_user_command(cmd_parts, snapshot_dir, store_data_dir, data_action, 
            data_writable, store_model_dir, model_action, model_writable, storage_name, storage_key, actions, 
            is_windows=False, sudo_available=sudo_available, username=username, use_username=False, 
            install_blobfuse=True, setup=setup,  use_allow_other=use_allow_other, 
            remove_zip=False, homebase=job_home, cwd=cwd, args=args, copy_code=True)

        return fn_wrapped

    def provides_container_support(self):
        '''
        Returns:
            returns True if docker run command is handled by the backend.
        '''
        return True
        
    def match_stage(self, run, stage_flags):
        
        status = run["status"]

        if status in ["NotStarted", "Starting", "Provisioning", "Preparing", "Queued"]:
            match = "queued" in stage_flags
        elif status == "Running":
            match = "active" in stage_flags
        else:
            match = "completed" in stage_flags

        return match

    def view_status(self, run_name, workspace, job, monitor, escape_secs, auto_start, 
            stage_flags, status, max_finished):

        # collect all runs by experiment
        aml_ws_name = self.get_service_name()
        experiments = self.get_experiments(aml_ws_name)
        runs_by_exper = {}

        for exper_name, experiment in experiments.items():
            # apply username filter
            if not exper_name.startswith(self.username + "__"): 
                continue

            # request RUNS from AML
            runs = list(experiment.get_runs())

            # convert to a list of dict items
            #runs = [run.__dict__ for run in runs]
            columns = ["number", "id", "status", "xt_run_name", "PORTAL_URL", "tags"]
            runs = [self.object_to_dict(run, columns) for run in runs]

            for run in runs:
                if "tags" in run and "xt_run_name" in run["tags"]:
                    run["xt_run_name"] = run["tags"]["xt_run_name"]
                    del run["tags"]

            runs_by_exper[exper_name] = runs

        # report by stage
        if "queued" in stage_flags:
            self.report_on_runs(runs_by_exper, "queued")

        if "active" in stage_flags:
            self.report_on_runs(runs_by_exper, "active")

        if "completed" in stage_flags:
            self.report_on_runs(runs_by_exper, "completed", max_finished)

    def report_on_runs(self, runs_by_exper, stage, max_items=None):
        runs_reported = 0

        console.print("target={} runs: {}".format(self.compute, stage))

        exper_names = list(runs_by_exper.keys())
        exper_names.sort()

        for exper_name in exper_names:
            runs = runs_by_exper[exper_name]

            # filter runs for this stage
            runs = [run for run in runs if self.match_stage(run, stage)]
            if runs:
                console.print("\nruns for experiment {}:".format(exper_name))

                columns = ["xt_run_name", "status", "id", "number", "PORTAL_URL"]
                lb = ReportBuilder(self.config, self.store)

                if max_items and len(runs) > max_items:
                    runs = runs[:max_items]

                text, rows = lb.build_formatted_table(runs, columns, max_col_width=100)
                console.print(text)
                runs_reported += len(runs)

        if runs_reported:
            console.print("total runs {}: {}".format(runs_reported, stage))
        else:
            console.print("  no {} runs found\n".format(stage))

    def does_ws_exist(self, ws_name):
        return self.config.name_exists(SECTION, ws_name)
        
    def get_workspaces(self):
        ''' return aml workspaces registered in config file
        '''
        services = self.config.get_group_properties(SECTION)
        names = [ name for name,value in services.items() if "type" in value and value["type"] == "aml"  ]
        return names

    # API
    def supports_setting_location(self):
        return True

    # API 
    def get_location(self, ws_name):
        ws = self.get_aml_ws(ws_name)
        location = ws.location

        return location

    def get_experiments(self, ws_name):
        ws = self.get_aml_ws(ws_name)
        return ws.experiments

    def attach_to_run(self, ws, run_name):
        run = self.get_run(ws, run_name)
        run.wait_for_completion(show_output=True)

    def get_run(self, ws_name, run_name):
        if not "." in run_name:
            errors.general_error("Azure ML run name must be of the form: exper.runname")

        ws = self.get_aml_ws(ws_name)
        console.diag("after get_aml_ws() call")

        exper_name, run_part = run_name.split(".")
        experiment = Experiment(ws, name=exper_name)
        runs = experiment.get_runs(properties={"xt_run_name": run_name})
        console.diag("after experiment.get_runs() call")

        runs = list(runs)
        console.diag("after list(runs), len={}".format(len(runs)))

        # run_number = int(run_part[3:])
        # target_run = None

        #runs = [run for run in runs if run.number == run_number]
        target_run = runs[0] if len(runs) else None
    
        return target_run

    def get_run_files(self, ws_name, run_name):
        run = self.get_run(ws_name, run_name)
        files = run.get_file_names()
        return files

    def download_run_files(self, ws_name, run_name, store_path, local_path):
        run = self.get_run(ws_name, run_name)
        if store_path in [".", "*"]:
            store_path = None
        run.download_files(store_path, local_path)

    def make_monitor_notebook(self, ws_name, run_name):
        lines =  \
        [
            "from xtlib.backend_aml import AzureML \n",
            "from xtlib.helpers.xt_config import XTConfig\n",
            "from azureml.widgets import RunDetails\n",
            "\n",
            "config = XTConfig()\n",
            "azure_ml = AzureML(config, True)\n",
            'run = azure_ml.get_run("{}", "{}")\n'.format(ws_name, run_name),
            "\n",
            "RunDetails(run).show()\n"
        ]

        kernel_name = pc_utils.get_conda_env()
        kernel_display = file_utils.get_kernel_display_name(kernel_name)
        #console.print("kernel_display=", kernel_display)

        builder = NotebookBuilder(kernel_name, kernel_display)
        builder.add_code_cell(lines)
        fn = os.path.expanduser("~/.xt/notebooks/monitor.ipynb")
        builder.save_to_file(fn)
        return fn

    def cancel_run(self, ws_name, run_name):
        console.diag("start of azure_ml.cancel_run()")

        target_run = self.get_run(ws_name, run_name)
        if not target_run:
            errors.store_error("run not found: {}".format(run_name))

        console.diag("after get_run() call")

        before_status = target_run.status.lower()
        if before_status in ["preparing", "queued"]:
            target_run.cancel()
            killed = True
            status = "cancelled"
        elif before_status in ["starting", "running"]:
            target_run.cancel()
            killed = True
            status = "cancelled"
        else:
            killed = False
            status = target_run.status

        console.diag("after run.cancel() call")

        return {"workspace": ws_name, "run_name": run_name, "cancelled": killed, "status": status}
        
    def cancel_runs(self, ws_name, exper_name, run_names):
        results = []

        for ws_run_name in run_names:
            if "/" in ws_run_name:
                run_name = ws_run_name.split("/")[1]
            else:
                run_name = ws_run_name

            if run_helper.is_run_name(run_name):
                run_name = exper_name + "." + run_name

            result = self.cancel_run(ws_name, run_name)
            results.append(result)

        results_by_aml = {"Azure ML": results}
        return results_by_aml

    def get_active_jobs(self, ws_name, job_list=None):
        ''' return a list of job_id's running on this instance of Azure Batch '''
        db = self.store.get_database()

        if job_list:
            filter_dict = {"job_id": {"$in": job_list}}
        
        else:
            filter_dict = {
                "username": self.username,
                "compute": "aml",
                "job_status": {
                    "$nin": ["created", "completed"]
                }
            }

        fields_dict = {"job_id": 1, "service_info_by_node": 1, "service_job_info": 1}

        job_records = db.get_info_for_jobs(ws_name, filter_dict, fields_dict)

        return job_records

    def cancel_runs_by_user(self, ws_name, box_name):
        '''
        Args:
            box_name: the name of the box the runs ran on (pool service)
        Returns:
            cancel_results: a list of kill results records 
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''
        cancel_results = []

        # get list of active jobs from batch
        if box_name:
            job_id = box_name.split("-")[0]
            active_jobs = self.get_active_jobs(ws_name, [job_id])

        else:
            active_jobs = self.get_active_jobs(ws_name)

        console.diag("after get_active_jobs()")

        if active_jobs:
            for job_record in active_jobs:
                # watch out for older jobs that didn't have service_job_info/service_info_by_node properties
                service_job_info = utils.safe_value(job_record, "service_job_info")
                service_info_by_node = utils.safe_value(job_record, "service_info_by_node")

                if service_job_info and service_info_by_node:
                    job_id = job_record["job_id"]
                    cancel_result = self.cancel_job(service_job_info, service_info_by_node)
                    for _, node_result in cancel_result.items():
                        cancel_results.append(node_result)

        return cancel_results

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
        job_id, service_name, node_index = box_name.split("-")
        active_jobs = self.get_active_jobs(workspace, [job_id])
        cancel_results = []
        if active_jobs:
            for job_record in active_jobs:
                # watch out for older jobs that didn't have service_job_info/service_info_by_node properties
                service_info_by_node = utils.safe_value(job_record, "service_info_by_node")
                
                if service_info_by_node:
                    for node, node_service_info in service_info_by_node.items():
                        if node_service_info.get("run_name") in run_names:
                            cancel_result, node_end_time = self.cancel_node(node_service_info)
                            cancel_results.append(cancel_result)

        return cancel_results


    def build_env_vars(self, workspace, aml_ws_name, xt_exper_name, aml_exper_name, run_name, job_id, 
        compute_target, username, description, aggregate_dest, node_id, args):

        vars = dict(args["env_vars"])            
        vars["XT_NODE_ID"] = node_id
        
        vars["XT_WORKSPACE_NAME"] = workspace
        vars["XT_EXPERIMENT_NAME"] = xt_exper_name
        vars["XT_RUN_NAME"] = run_name
        vars["XT_RESUME_NAME"] = None

        vars["AML_WORKSPACE_NAME"] = aml_ws_name
        vars["AML_EXPERIMENT_NAME"] = aml_exper_name

        vars["XT_USERNAME"] = username
        vars["XT_DESCRIPTION"] = description
        vars["XT_AGGREGATE_DEST"] = aggregate_dest
        vars["XT_JOB_ID"] = job_id
        vars["XT_COMPUTE_TARGET"] = compute_target

        return vars

    def get_azure_cred(self):
        from azureml.core.authentication import TokenAuthentication
        from azure.identity import InteractiveBrowserCredential, AuthenticationRecord, TokenCachePersistenceOptions 

        token = None

        def get_the_token_func(audience):
            nonlocal token

            if not token:
                vault = self.config.get_vault()
                credential, _ = vault.get_creds_core("auto")

                yyy = credential.get_token("https://management.azure.com/.default")
                token = yyy.token
            return token

        amlauth = TokenAuthentication(get_the_token_func)
        amlauth.get_token()
        return amlauth

    def get_aml_ws(self, ws_name):

        ws_info = self.config.get("external-services", ws_name, suppress_warning=True)
        if not ws_info:
            errors.config_error("Azure ML workspace '{}' is not defined in [external-services] section of the XT config file".format(ws_name))

        subscription_id = self.config.get_required_service_property(ws_info, "subscription-id", ws_name)
        resource_group = self.config.get_required_service_property(ws_info, "resource-group", ws_name)

        cred = self.get_azure_cred()
        ws = Workspace.get(name=ws_name, subscription_id=subscription_id, resource_group=resource_group, auth=cred) 
        return ws
    
    def get_aml_ws_sizes(self, aml_ws_name):
        ws = self.get_aml_ws(self.config, aml_ws_name)

        # TODO: make this an xt cmd: xt list sizes
        from azureml.core.compute import ComputeTarget, AmlCompute
        sizes = AmlCompute.supported_vmsizes(workspace=ws)
        # for size in sizes:
        #     if size["gpus"] > 0:
        #         console.print(size)

        return sizes

    def build_hyperdrive_dict(self, hp_sets):
        hd = {}

        for name, value in hp_sets.items():
            if isinstance(value, HPList):
                hd[name] = hp.choice(*value.values)
            elif isinstance(value, HPDist):
                # convert from comma sep. string to list of float values
                values = utils.get_number_or_string_list_from_text(value.values)

                dist_name = value.dist_name
                #hd[name] = self.make_distribution(dist_name, values)
                hd[name] = hp_helper.build_dist_func_instance(name, dist_name, values)

        return hd

    def build_hyperdrive_dict_from_file(self, fn):
        ''' parse hyperdrive params from text file '''
        hd = {}

        with open(fn, "rt") as infile:
            text_lines = infile.readlines()

        for text in text_lines:
            text = text.strip()
            if not text or text.startswith("#"):
                continue

            if "#" in text:
                # remove comment part of line
                index = text.index("#")
                text = text[0:index].strip()

            name, value = text.split("=")   
            name = name.strip()
            value = value.strip()

            if value.startswith("@"):
                dist_name, values = value[1:].split("(")
                if not dist_name in utils.distribution_types:
                    errors.config_error("Unsupported distribution type: " + dist_name)

                assert values.endswith(")")
                values = values[:-1]   # remove ending paren

                # convert from comma sep. string to list of float values
                values = utils.get_number_or_string_list_from_text(values)

                #hd[name] = self.make_distribution(dist_name, values)
                hd[name] = hp_helper.build_dist_func_instance(name, dist_name, values)
            else:
                # convert from comma sep. string to list of float values
                values = utils.get_number_or_string_list_from_text(value)
                # treat as "choice"
                #hd[name] = self.make_distribution("choice", values)
                hd[name] = hp_helper.build_dist_func_instance(name, "choice", values)

        return hd

    def make_early_term_policy(self, policy_type, eval_interval=1, delay_eval=0, truncation_percentage=.1, slack_factor=None, slack_amount=None):
        from azureml.train.hyperdrive import BanditPolicy, MedianStoppingPolicy, TruncationSelectionPolicy, NoTerminationPolicy

        if policy_type == "bandit":
            policy = BanditPolicy(evaluation_interval=eval_interval, slack_factor=slack_factor, slack_amount=slack_amount, delay_eval=delay_eval)
        elif policy_type == "median":
            policy = MedianStoppingPolicy(evaluation_interval=eval_interval, delay_evaluation=delay_eval)
        elif policy_type == "truncation":
            policy = TruncationSelectionPolicy(truncation_percentage=truncation_percentage, evaluation_interval=eval_interval, delay_evaluation=delay_eval)
        elif policy_type == "none":
            policy = NoTerminationPolicy()
        else:
            errors.config_error("Unrecognized policy type=" + policy_type)
        
        return policy

    def create_hyperdrive_trainer(self, estimator, hd_dict, search_type, metric_name, maximize_metric, early_term_policy, max_total_runs, 
        max_concurrent_runs, max_minutes):

        from azureml.train.hyperdrive import RandomParameterSampling, GridParameterSampling , BayesianParameterSampling

        if search_type == "random":
            ps = RandomParameterSampling(hd_dict)
        elif search_type == "grid":
            ps = GridParameterSampling (hd_dict)
        elif search_type == "bayesian":
            ps = BayesianParameterSampling(hd_dict)
        else:
            errors.config_error("Azure ML Hyperdrive search_type not supported: " + search_type)

        max_concurrent_runs = min(max_total_runs, max_concurrent_runs)

        from azureml.train.hyperdrive import HyperDriveConfig, PrimaryMetricGoal

        trainer = HyperDriveConfig(estimator=estimator, 
            hyperparameter_sampling=ps, 
            policy=early_term_policy, 
            primary_metric_name=metric_name, 
            primary_metric_goal=PrimaryMetricGoal.MAXIMIZE if maximize_metric else PrimaryMetricGoal.MINIMIZE, 
            max_total_runs=max_total_runs,
            max_concurrent_runs=max_concurrent_runs,
            max_duration_minutes=max_minutes)     

        return trainer

    def get_docker_container_registry(self, args):
        import azureml

        target = args["target"]
        docker_name = args["docker"]
        creds_required = False

        docker_image, login_server, docker_registry, sing_dict = self.config.get_docker_info(target, docker_name, required=False)

        # aml doesn't like/recognized docker.io
        if self.get_name() == "aml" and login_server == "docker.io":
            login_server = None

        if not docker_image:
            docker_image = None

        if login_server:
            container_registry = azureml.core.ContainerRegistry()
            container_registry.address = login_server
            creds_required = utils.make_numeric_if_possible( utils.safe_value(docker_registry, "login") )
            if creds_required:
                # get username/password to log into private docker registry service (Azure)
                container_registry.username = utils.safe_value(docker_registry, "username")
                container_registry.password = utils.safe_value(docker_registry, "password")
        else:
            container_registry = None

        return container_registry, docker_image, sing_dict

    def create_estimator(self, job_id, workspace, node_run, aml_ws_name, xt_exper_name, aml_exper_name, run_name, code_dir, target_fn, arg_dict, 
        compute_target, node_id, nodes, fake_submit, args):

        config = self.config
        ps = None

        if not aml_exper_name:
            errors.config_error("experiment name must be specified (thru config file or command line option '--experiment')")

        if fake_submit:
            # for speed of testing, avoid creating real Workspace, Experiment instances
            ws = {"name": aml_ws_name}
            experiment = {"ws": ws, "name": aml_exper_name}
        else:
            ws = self.get_aml_ws(aml_ws_name)
            experiment = Experiment(ws, name=aml_exper_name)

        is_distributed = args['distributed']
        dist_training = args["distributed_training"]
        dist_training = dist_training.lower()

        # debug code
        # targets = ComputeTarget.list(ws)
        # console.print("available compute targets in workspace {}: {}".format(ws, targets))

        # set AML target 
        if compute_target == "amlcompute":
            actual_target = "amlcompute"    
        else:
            if fake_submit:
                actual_target = "amlcompute"
            else:
                if compute_target in ws.compute_targets:
                    # its the name of a known AML target for this ws (compute instance, cluster, etc.)
                    # use the actual predefined compute_target object (not the string)
                    actual_target = ws.compute_targets[compute_target]
                else:
                    # it appears under certain conditions, we can just pass a string as the target
                    #errors.config_error("compute target '{}' does not exist in AML workspace '{}'".format(compute_target, aml_ws_name))
                    #errors.warning("compute target '{}' not defined in AML compute targets for AML workspace '{}'".format(compute_target, aml_ws_name))
                    
                    actual_target = compute_target

                    # # rfernand experiment: Jun-18-2024
                    # td = self.config.get_service(compute_target)
                    # compute_subscription_id = td["subscription-id"]
                    # compute_resource_group = td["resource-group"]
                    # cred = self.get_azure_cred()
                    # ws_name = compute_target[0:-2] + "ws"

                    # target_workspace = Workspace.get(name=ws_name, subscription_id=compute_subscription_id, resource_group=compute_resource_group, auth=cred)
                    # actual_target = ComputeTarget(target_workspace, name)

        # build ENV VARS
        store_creds = self.config.get_storage_creds()

        # store_name = store_creds["name"]
        # store_key = store_creds["key"]

        provider_code_path = config.get_storage_provider_code_path(store_creds)
        
        mongo_creds = self.config.get_database_creds()
        mongo_conn_str = mongo_creds["connection-string"]

        username = args["username"]
        description = args["description"]
        aggregate_dest = args["aggregate_dest"]
        conda_packages = args["conda_packages"]
        pip_packages = args["pip_packages"]
        
        env_vars = self.build_env_vars(workspace, aml_ws_name, xt_exper_name, aml_exper_name, run_name, job_id=job_id, 
            compute_target=compute_target, username=username, description=description, aggregate_dest=aggregate_dest, 
            node_id=node_id, args=args)
        
        node_index = utils.node_index(node_id)
        is_direct_run = args["direct_run"]

        box_secret = None     # obsoleted
        batch_key = None      # doesn't apply to AML
        direct_cmd = None
        if is_direct_run:
            run_specs = node_run["run_specs"]
            direct_cmd = run_specs["run_cmd"]

        # 2/2 calls to this (TODO: remove one)
        # this second call really updates the env_vars to be passed to singularity for this node run
        self.get_controller_env_vars(env_vars, node_run, node_index, args)
       
        container_registry, docker_image, _, = self.get_docker_container_registry(args)

        framework = args["framework"]
        if framework:
            framework = framework.lower()
        else:
            framework = "none"
        framework_version = args["fw_version"]

        use_docker = bool(docker_image)
        user_managed = bool(docker_image)

        # AML issues warnings if this is not set
        aml_use_docker = True

        if docker_image:
            # when user specified docker_image, he takes responsibility for python/conda and framework (torch, tensorflow, etc.)
            framework = "none"
            framework_version = None

        import azureml
        from azureml.train.estimator import Estimator, Mpi, Gloo, Nccl
        from azureml.train.dnn import PyTorch, Chainer, TensorFlow
        
        fw_dict = {"pytorch": PyTorch, "tensorflow": TensorFlow, "chainer": Chainer, "none": Estimator}
        dt_dict = {"mpi": Mpi, "gloo": Gloo, "nccl": Nccl}

        if not framework in fw_dict:
            errors.user_config_errorerror("framework must be set to 'pytorch', 'tensorflow', 'chainer', or 'estimator'")

        estimator_ctr = fw_dict[framework]

        if is_distributed:
            if not dist_training in dt_dict:
                errors.config_error("distributed-training must be set to 'mpi', 'gloo', or 'nccl'")

            distributed_ctr = dt_dict[dist_training]
            distributed_obj = distributed_ctr()
        else:
            distributed_obj = None

        compute_def = args["compute_def"]

        if is_direct_run:
            # relying on AML for full control (not using XT controller)
            node_count = utils.safe_value(compute_def, "nodes")

            # did cmd line overwrite nodes?
            if args["nodes"]:
                node_count = args["nodes"]

            if node_count is None:
                errors.config_error("must specify 'nodes' property for Azure ML service '{}' in XT config file or as --nodes option in cmd line".format(args["target"]))
        else:
            # run as separate AML runs, each with a single node
            node_count = 1

        vm_size = args["vm_size"]
        use_gpu = args["use_gpu"]
        max_secs = args["max_seconds"]
        # user_managed = args["user_managed"]

        # if pip_packages includes a requirements file, extract it
        fn_requirements = None
        for pp in pip_packages:
            if pp.startswith("-r "):
                fn_requirements = pp[3:].strip()
                pip_packages.remove(pp)
                break

        activate_cmd = self.get_activate_cmd(args)
        if activate_cmd:
            # we have no way of running this on AML before conda_packages and pip_packages are installed (or used to build a docker image)
            errors.config_error("setup.activate property cannot be specified for AML targets")

        #max_secs = 10080 if max_secs <= 0 else max_secs
        
        setup = self.config.get_setup_from_target_def(self.compute_def)
        use_sudo = utils.safe_value(setup, "use-sudo")       # some AML clusters need sudo
        allow_other = use_sudo      # if setup with sudo, then we need allow_other

        # must use environment to specify docker registry username/password
        #use_envionement = bool(container_registry)  #   use_docker
        use_environment = True   # for AML/docker flags to be used 
        estimator_keyword_args = {}

        # dynamic args for estimator ctr
        if framework != "none":
            estimator_keyword_args["framework_version"] = framework_version

        if fake_submit or self.submit_logs:
            # for testing (this should match exact args used in estimator ctr below)
            if use_environment:
                serializable_environment = {"environment_variables": env_vars, "docker": {"enabled": aml_use_docker, # deprecated: "gpu_support": use_gpu,
                    "base_image": docker_image}}

                self.serializable_estimator = {"source_directory": code_dir, "script_params": arg_dict, "compute_target": actual_target, 
                    "entry_script": target_fn, "node_count": node_count, "distributed_training": {},
                    "max_run_duration_seconds": max_secs, "user_managed": user_managed, "vm_size": vm_size, 
                    "environment_definition": serializable_environment, **estimator_keyword_args}
            else:
                self.serializable_estimator = {"source_directory": code_dir, "script_params": arg_dict, "compute_target": actual_target, 
                    "vm_size": vm_size, "entry_script": target_fn, "conda_packages": conda_packages, "pip_packages": pip_packages, 
                    "pip_requirements_file": fn_requirements, "use_gpu": use_gpu, "use_docker": aml_use_docker, 
                    "user_managed": user_managed, "environment_variables": env_vars, "node_count": node_count, "distributed_training": {},
                    "max_run_duration_seconds": max_secs, **estimator_keyword_args}

        if fake_submit:
            estimator = self.serializable_estimator
        else:
            if use_environment:

                environment = azureml.core.Environment("myenv")
                environment.environment_variables = env_vars
                environment.python.user_managed_dependencies = user_managed

                environment.docker.enabled = aml_use_docker
                #environment.docker.gpu_support = use_gpu            # deprecated

                if container_registry:
                    environment.docker.base_image_registry = container_registry

                # singularity backend doesn't support other docker commands
                if self.get_name() != "singularity":
                    # let user specify additional docker options
                    other_args = args["docker_other_options"] if args["docker_other_options"] else []

                    if use_sudo:
                        # specify additional docker run flags so that we can use blobfuse
                        other_args += ["--privileged"]

                    # AML doesn't support $PWD (why?)
                    other_args = [arg for arg in other_args if not "$PWD" in arg]

                    environment.docker.arguments = other_args

                if docker_image:
                    # override AML default base image with user-specified image
                    environment.docker.base_image = docker_image 
                else:
                     environment.docker.base_image = self.get_default_docker_image(use_gpu)

                # specify conda_packages and pip_packages here
                python_version = args["python_version"]

                conda = azureml.core.environment.CondaDependencies.create(pip_packages=pip_packages, 
                    conda_packages=conda_packages, python_version=python_version)

                environment.python.conda_dependencies = conda

                estimator = estimator_ctr(source_directory=code_dir, script_params=arg_dict, compute_target=actual_target, 
                    vm_size=vm_size, distributed_training=distributed_obj, 
                    entry_script=target_fn, node_count=node_count, max_run_duration_seconds=max_secs, environment_definition=environment)
                    
            else:
                pip_packages = None

                estimator = estimator_ctr( source_directory=code_dir, script_params=arg_dict, compute_target=actual_target, 
                    vm_size=vm_size, entry_script=target_fn, conda_packages=conda_packages, pip_packages=pip_packages, 
                    pip_requirements_file=fn_requirements, use_gpu=use_gpu, use_docker=aml_use_docker, 
                    user_managed=user_managed, environment_variables=env_vars, node_count=node_count, distributed_training=distributed_obj,
                    max_run_duration_seconds=max_secs, custom_docker_image=docker_image)

            # supress AML/ITP warnings about duplicate script/arguments values
            # estimator.run_config.arguments = []
            # estimator.run_config.script = None
            # estimator.arguments = []
            # estimator.script = None

            # update estimator for ITP 
            sku = utils.safe_value(self.compute_def, "sku", "g1")
            gpu_count = int(sku[1:]) if isinstance(sku, str) else 0

            low_pri = utils.safe_value(self.compute_def, "low-pri", False)

            # give sublclasses a chance to chime in
            self.update_estimator(estimator, gpu_count, low_pri)

        return estimator, experiment

    def get_controller_env_vars(self, env_vars, node_run, node_index, args):
        #node_index = node_run["node_index"]
        run_name = node_run["run_name"]
        is_direct_run = args["direct_run"]

        batch_key = None      # doesn't apply to AML
        direct_cmd = None
        if is_direct_run:
            run_specs = node_run["run_specs"]
            direct_cmd = run_specs["run_cmd"]

        scriptor.add_controller_env_vars(env_vars, self.config, node_index=node_index, run_name=run_name, 
            batch_key=batch_key, direct_cmd=direct_cmd, args=args)
        
        # give subclass a chance to update env vars
        self.update_env_vars(env_vars, args)

    def update_env_vars(self, env_vars, args):
        pass

    def update_estimator(self, estimator, gpu_count, preemption_allowed):
        pass

    def submit_job(self, job_id, job_runs, workspace, compute_def, resume_name, 
        repeat_count, using_hp, runs_by_box, experiment, snapshot_dir, controller_scripts, args):

        username = args["username"]
        aml_exper_name = "{}__{}__{}".format(username, workspace, experiment)

        cwd = os.getcwd()

        #bootstrap_dir = args["bootstrap_dir"]

        compute = args["target"]
        compute_def = args["compute_def"]
        aml_ws_name = compute_def["service"]
        show_aml_run_name = True

        if show_aml_run_name:
            fb.stop_feedback()

        nodes = len(job_runs)
        service_info_by_node = {}

        for i, node_run in enumerate(job_runs):
            node_info = self.submit_node_run(job_id, node_run, workspace, aml_ws_name, experiment, aml_exper_name, 
                compute_def, resume_name, repeat_count, using_hp, compute, runs_by_box, snapshot_dir, i, 
                show_aml_run_name, nodes, args)

            node_id = "node" + str(i)
            service_info_by_node[node_id] = node_info

            # update node_info record in database with service_info
            self.store.database.update_node_info_with_service_info(workspace, job_id, i, node_info)

        fb.reset_feedback()
        fb.feedback("submitted")

        service_job_info = {}    # AML has updated the job, so don't return this
        return service_job_info, service_info_by_node     

    def submit_node_run(self, job_id, node_run, ws_name, aml_ws_name, xt_exper_name, aml_exper_name, 
        compute_def, resume_name, repeat_count, using_hp, compute, runs_by_box, code_dir, node_index, 
        show_aml_run_name, nodes, args):

        first_run_name = node_run["run_name"]
        fake_submit = args["fake_submit"]
        trainer = None

        # this indicates we should make serializable versions of estimator and trainer
        self.submit_logs = True   #  fake_submit  # must be true if we are using fake_submit

        self.serializable_estimator = None
        self.serializable_trainer = None
        
        box_name = node_run["box_name"]

        run_specs = node_run["run_specs"]
        cmd_parts = run_specs["cmd_parts"]
        target_fn = args["script"]
        node_id = "node" + str(node_index)

        assert cmd_parts[0] == "python"
        assert cmd_parts[1] == "-u"
        assert len(cmd_parts[2]) > 0 

        # update the target_fn (might have been switched to the xt controller)
        target_fn = cmd_parts[2]
        arg_parts = cmd_parts[3:]

        # parse target's cmdline args
        arg_dict = {} 
        for ap in arg_parts:
            # arg name can start with or without "-" here
            if "=" in ap:
                name, value = ap.split("=")
                if not value.startswith('"[') and not value.startswith('"@'):
                    arg_dict[name] = value
            else:
                # for unspecified values
                arg_dict[ap] = 1

        compute_target = utils.safe_value(compute_def, "compute")
        if not compute_target:
            errors.config_error("'compute' property missing on compute target '{}' in XT config file".format(compute))

        # append job/run name to AML experiment name (make locating XT runs in AML portal easier)
        aml_exper_name += "__{}__{}".format(job_id, first_run_name)

        estimator, experiment = self.create_estimator(job_id, ws_name, node_run, aml_ws_name, xt_exper_name, aml_exper_name, first_run_name, 
            code_dir, target_fn, arg_dict, compute_target, node_id, nodes, fake_submit, args)

        hp_config = args["hp_config"]
        direct_run = args["direct_run"]

        if using_hp and direct_run:
            # EXPERIMENT with hyperdrive
            max_runs = args["max_runs"]
            max_minutes = args["max_minutes"]

            policy_name = args["early_policy"]
            eval_interval = args["evaluation_interval"]
            delay_eval = args["delay_evaluation"]
            truncation_percentage = args["truncation_percentage"]
            slack_factor = args["slack_factor"]
            slack_amount = args["slack_amount"]

            primary_metric = args["primary_metric"]
            maximize_metric = args["maximize_metric"]
            search_type = args["search_type"]
            concurrent = args["concurrent"]

            max_concurrent_runs = nodes * concurrent

            if max_minutes <= 0:
                #max_minutes = 43200   # aml workaround: None not supported, either is -1 or 0, so use max value
                max_minutes = 10080   # aml workaround: documented max not supported

            hp_sets = None     # where is this supposed to come from?

            if hp_sets:
                hd_dict = self.build_hyperdrive_dict(hp_sets)
            else:
                hd_dict = self.build_hyperdrive_dict_from_file(hp_config)

            if not policy_name:
                # use default policy (not that same as no policy)
                early_term = None
            else:
                if self.submit_logs:
                    early_term = {"policy_type": policy_name, "eval_interval": eval_interval, "delay_eval": delay_eval, 
                        "truncation_percentage": truncation_percentage, "slack_factor": slack_factor, "slack_amount": slack_amount}

                    self.serializable_trainer = {"estimator": self.serializable_estimator, "hd_dict": hd_dict, "search_type": search_type, "primary_metric": primary_metric, 
                        "maximize_metric": maximize_metric, "early_term": self.serializable_early_term, "max_total_runs": max_runs, "max_concurrent_runs": max_concurrent_runs, 
                        "max_minutes": max_minutes}

                if fake_submit:
                    trainer = self.serializable_trainer
                else:
                    early_term = self.make_early_term_policy(policy_type=policy_name, eval_interval=eval_interval, delay_eval=delay_eval, 
                        truncation_percentage=truncation_percentage, slack_factor=slack_factor, slack_amount=slack_amount)

                    trainer = self.create_hyperdrive_trainer(estimator, hd_dict, search_type, primary_metric, maximize_metric, early_term, 
                        max_total_runs=max_runs, max_concurrent_runs=max_concurrent_runs, max_minutes=max_minutes)
        else:
            # not using AML hyperdrive
            trainer = estimator

        run_name, monitor_cmd, aml_run_name, aml_run_number, aml_run_id = \
            self.run_job_on_service(job_id, ws_name, aml_ws_name, trainer, experiment, xt_exper_name, aml_exper_name, compute_target, code_dir, first_run_name, 
                box_name, node_index, repeat_count, fake_submit, arg_parts, args)

        if show_aml_run_name:
            if self.get_name() != "singularity":
                console.print("  {} (AML: {}/Run {})".format(run_name, aml_exper_name, aml_run_number))
        else:
            fb.feedback("{}".format(run_name))

        run_name = node_run["run_name"]
        node_info = {"ws": ws_name}

        node_info["aml_exper_name"] = aml_exper_name
        node_info["aml_run_number"] = aml_run_number
        node_info["aml_run_id"] = aml_run_id
        node_info["run_name"] = run_name
        node_info["job_id"] = job_id
        node_info["node_id"] = node_id

        if monitor_cmd:
            console.print("monitoring notebook created; to run:")
            console.print("  " + monitor_cmd)

        return node_info

    def run_job_on_service(self, job_id, workspace, aml_ws_name, trainer, experiment, xt_exper_name, aml_exper_name, compute_target, cwd, run_name, box_name, 
            node_index, repeat, fake_submit, arg_parts, args):
        monitor_cmd = None

        console.diag("before AML experiment.submit(trainer)")

        # SUBMIT the run and return an AML run object
        if fake_submit:
            aml_run = None 
            aml_run_id = "fake_aml_id"
            aml_run_number = 999
        else:
            aml_run = experiment.submit(trainer)
            aml_run_id = aml_run.id
            aml_run_number = aml_run.number

            # set AML/ITP display_name 
            display_name = args["display_name"]
            display_name = utils.expand_xt_vars(display_name, run_id=run_name, node_index=node_index, args=args)
            aml_run.display_name = display_name

        # copy to submit-logs
        utils.copy_data_to_submit_logs(args, self.serializable_trainer, "aml_submit.json")

        console.diag("after AML experiment.submit(trainer)")

        config = self.config
        username = args["username"]
        description = args["description"]
        aggregate_dest = args["aggregate_dest"]
        jupyter_monitor = args["jupyter_monitor"]

        aml_run_name = aml_exper_name + ".{}".format(run_name)

        # set "xt_run_name" property for fast access to run in future
        if not fake_submit:
            aml_run.add_properties({"xt_run_name": aml_run_name})
            aml_run.set_tags({"xt_run_name": aml_run_name})

        # # partially log the start of the RUN
        # self.store.start_run_core(workspace, run_name, exper_name=xt_exper_name, description=description, username=username,
        #         box_name=box_name, app_name=None, repeat=repeat, is_parent=False, job_id=job_id, pool=compute_target, node_index=node_index,
        #         aggregate_dest=aggregate_dest, path=cwd, aml_run_id=aml_run_id)

        if jupyter_monitor:
            fn = self.make_monitor_notebook(aml_ws_name, aml_run_name)
            dir = os.path.dirname(fn)
            #console.print("jupyter notebook written to: " + fn)
            monitor_cmd = "jupyter notebook --notebook-dir=" + dir
        
        return run_name, monitor_cmd, aml_run_name, aml_run_number, aml_run_id

    def get_client_cs(self, service_node_info):
        '''
        Args:
            service_node_info: info that service maps to a compute node for a job
        Returns:
            {"ip": value, "port": value, "box_name": value}
        '''
        errors.general_error("support for talking to XT controller for AML jobs not yet supported")

    # def mount(self, storage_name, storage_key, container):

    #     ws = Workspace(subscription_id, resource_group, ws_name)     # , auth=svc_pr)

    #     from azureml.core import Datastore
    #     datastore = Datastore.register_azure_blob_container(workspace=ws, 
    #         datastore_name=container, container_name=container,
    #         account_name=storage_name, account_key=storage_key,
    #         create_if_not_exists=True)

    #     console.print("datastore=", datastore)

    #     dataref = datastore.as_mount()
    #     dir_name = dataref.path_on_compute
    #     console.print("datastore MOUNT dir_name=", dir_name)
    #     return dir_name


    def get_log_reader(self, service_node_info):
        log_reader = AmlLogReader(self.store, self, service_node_info)
        return log_reader

    # API call
    def get_simple_status(self, status):
        # translates an AML status to a simple status (queued, running, completed)

        queued = ["NotStarted", "Starting", "Provisioning", "Preparing", "Queued", "Paused"]
        running = ["Running", "Finalizing"]
        completed = ["CancelRequested", "Completed", "Failed", "Canceled", "NotResponding"]

        if status in queued:
            ss = "queued"
        elif status in running:
            ss = "running"
        elif status in completed:
            ss = "completed"
        elif status == "Unapproved":
            #errors.warning("unexpected Azure ML status value: {}".format(status))
            ss = "queued"
        else:
            errors.warning("unexpected Azure ML status value: {}".format(status))
            ss = "queued"

        return ss

    def get_node_run(self, service_node_info):
        # create aml workspace
        aml_ws_name = utils.safe_value(self.compute_def, "service")
        ws = self.get_aml_ws(aml_ws_name)

        # create aml experiment
        aml_exper_name = service_node_info["aml_exper_name"]
        experiment = Experiment(ws, name=aml_exper_name)

        # create aml run
        aml_run_id = service_node_info["aml_run_id"]
        run = Run(experiment, aml_run_id)

        return run

    # API call
    def get_timestamped_status_of_nodes(self, service_name, service_infos):
        '''
        nodes must all be from the same AML experiment
        '''
        first_si = None

        for si in service_infos:
            if si:
                first_si = si
                break

        if not first_si or not service_name:
            sd = {"node"+str(i): (None,None) for i in range(len(service_infos))}
            return sd
        
        experiment_name = first_si["aml_exper_name"]

        ws = self.get_aml_ws(service_name)
        sd = {}

        experiment = Experiment(ws, name=experiment_name)
        #run = Run(experiment, aml_node_id_list[0])

        # enumerate just specified runs
        for si in service_infos:
            if not si:
                sd[node_id] = (None, None)
            
            else:
                aml_run_id = si["aml_run_id"]
                node_id = si["node_id"]

                run = Run(experiment, aml_run_id)

                status = self.get_simple_status(run.status)
                details = run.get_details()

                if not "endTimeUtc" in details:
                    print("----> WARNING: AML/ITP/SINGULARITY node: {} has not terminated according to service.  status: {}".format(aml_run_id, status))
                    sd[node_id] = (status, None)

                else:
                    end_time_utc = details["endTimeUtc"]
                    sd[node_id] = (status, end_time_utc)

        return sd
         
    # API call
    def get_status_of_nodes(self, service_name, experiment_name, service_info_list):
        ws = self.get_aml_ws(service_name)
        sd = {}

        experiment = Experiment(ws, name=experiment_name)
        #run = Run(experiment, aml_node_id_list[0])

        # enumerate just specified runs
        started = time.time()
        print("  getting {:,} specified AML runs".format(len(service_info_list)))
        
        for si in service_info_list:
            aml_run_id = si["aml_run_id"]
            node_id = si["node_id"]

            run = Run(experiment, aml_run_id)
            print("    id: {}, status: {}".format(run.id, run.status))
            sd[node_id] = run.status
        
        elapsed = time.time() - started
        print("  enumerated {:,} desired runs ({:.2f} secs)".format(len(service_info_list), elapsed))

        # # enumerate all runs in experiment
        # started = time.time()
        # run_count = 0
        # match_count = 0

        # # pd = {"id": {"$in": aml_node_id_list}}
        # # runs = experiment.get_runs(properties=pd)

        # print("getting all AML runs for exper: {}".format(experiment_name))
        # runs = experiment.get_runs()

        # for run in runs:
        #     run_count += 1
        #     if run["id"] in aml_node_id_list:
        #         print("id: {}, status: {}".format(run.id, run.status))
        #         match_count += 1

        # elapsed = time.time() - started
        # print("enumerated {:,} total runs, {:,} desired runs ({:.2f} secs".format(run_count, match_count, elapsed))

        return sd

    # API call
    def cancel_job(self, service_job_info, service_info_by_node):
        result_by_node = {}
        node_end_times = {}

        for node_id, node_info in service_info_by_node.items():
            result, node_end_time = self.cancel_node(node_info)

            if result is not None:
                result_by_node[node_id] = result
                node_end_times[node_id] = node_end_time

        return result_by_node, node_end_times

    # API call
    def cancel_node(self, service_node_info):
        result = None
        if "aml_run_id" in service_node_info:
            run = self.get_node_run(service_node_info)

            service_status = run.get_status()
            simple_status = self.get_simple_status(service_status)
            before_status = simple_status
            cancelled = False

            if simple_status in ["error", "completed", "cancelled"]:
                # node already terminated
                details = run.get_details()

                if not "endTimeUtc" in details:
                    print("----> WARNING: AML/ITP/SINGULARITY node: {} has not terminated according to service.  status: {}".format(service_node_info, service_status))
                    node_end_time = None
                else:
                    node_end_time_str = details["endTimeUtc"]
                    node_end_time = time_utils.get_time_from_arrow_str(node_end_time_str)
                
            else:
                # node is alive - cancel it
                run.cancel()

                service_status = run.get_status()
                simple_status = self.get_simple_status(service_status)
                cancelled = (simple_status == "completed") 
                node_end_time = time.time()    

            result = {"cancelled": cancelled, "service_status": service_status, "simple_status": simple_status}

        return result, node_end_time

   # API call
    def add_service_log_copy_cmds(self, ca, cmds, dest_dir, args):

        ca.append(cmds, "mkdir -p {}".format(dest_dir))
        #ca.append(cmds, "cp -r -v $AZUREML_LOGDIRECTORY_PATH/* {}".format(dest_dir))
        #ca.append(cmds, "cp -r -v $AZ_BATCHAI_STDOUTERR_DIR/* {}".format(dest_dir))
        ca.append(cmds, "cp -r $XT_ORIG_WORKDIR/azureml_compute_logs/. {}".format(dest_dir))
        ca.append(cmds, "cp -r $XT_ORIG_WORKDIR/azureml-logs/. {}".format(dest_dir))
        ca.append(cmds, "cp -r $XT_ORIG_WORKDIR/logs/. {}".format(dest_dir))

    # API call
    def get_log_files_dir(self, args):
        return "$XT_ORIG_WORKDIR/logs"


class AmlLogReader():
    def __init__(self, store, aml_backend, service_node_info, encoding='utf-8'):
        self.store = store
        self.aml_backend = aml_backend
        self.service_node_info = service_node_info
        self.encoding = encoding

        self.start_offset = 0
        self.end_offset = 1024*1024*1024*16     # 16 GB should be big enough for a log file
        self.log_name = None
        self.log_source = None
        self.request = None
        self.last_node_started_msg = None

        self.run = self.get_run()

    def get_run(self):
        for r in range(3):
            # try 3 times, then just bail
            try:
                run = self.aml_backend.get_node_run(self.service_node_info)
                break
            except BaseException as ex:
                print("error during get_node_run(): {}".format(ex))
                time.sleep(2)

        if not run:
            errors.env_error(msg="unable to get run for node: {}".format(self.service_node_info))

        return run
    
    def refresh_creds(self):
        # refresh credentials from the XT vault
        self.aml_backend.config.refresh_credentials()

        self.run = self.get_run()
        self.request = None

    def read_from_service(self):
        new_text = None

        run = self.run
        current_details = run.get_details() 

        aml_status = current_details["status"] 
        simple_status = self.aml_backend.get_simple_status(aml_status)
        
        if self.log_name:
            # reuse request for better perf (hopefully)
            log_files = current_details["logFiles"]
            aml_log_path = "user_logs/" + self.log_name

            # try to read one of Singularity-hosted service logs
            url = None
            for log_path in [self.log_name, aml_log_path]:
                for lf_name in log_files:
                    if lf_name.startswith(log_path):         # match prefix
                        url = log_files[lf_name]
                        break

                if url:
                    # create the request object to read the URL
                    if not self.request:
                        self.request = urllib.request.Request(url)
                    elif self.request.full_url != url:
                        #self.request.close()
                        range_hdr = {"Range": f"bytes={self.start_offset}-"}
                        self.request = urllib.request.Request(url=url, headers=range_hdr)

                    try:
                        # read the URL
                        with urllib.request.urlopen(self.request) as response:
                            all_bytes = response.read()
                    except BaseException as ex:
                        # note: we get exception "invalid range" if no new data is available
                        # treat any error as "no new data"
                        all_bytes = b""

                    # since we are now reading with range header, we only get new bytes
                    new_bytes = all_bytes[0:]   #    [start_offset:]
                    new_count = len(new_bytes)

                    # not sure if we have new acceptable text yet, so default to "none found"
                    next_offset = self.start_offset

                    if new_count:
                        # found some new text
                        text = new_bytes.decode(self.encoding)
                        found_new_text = True   

                        # workaround for wierdness in singularity: find "node started" message and ensure it is different
                        ns_marker = "Node started:"
                        
                        if ns_marker in text:
                            index = text.find(ns_marker)
                            index2 = text.find("\n", index)
                            ns_line = text[index:index2]

                            #print("ns_line: {}\nlast_node_started_msg: {}".format(ns_line, self.last_node_started_msg))

                            if self.last_node_started_msg == ns_line:
                                # discard this text (its a repeat of old log); new node log is coming
                                found_new_text = False
                                #print("found repeated text; ignoring...")
                            else:
                                self.last_node_started_msg = ns_line

                        if found_new_text:
                            self.start_offset += new_count
                            new_text = text

                        # debug
                        #print("url:", url)
                    break

        return new_text, simple_status, aml_status

    def read(self):
        '''
        used by the "xt montior" command to read the log file for a Singularity running job
        '''
        # FN_STDOUT_LOG = "azureml-logs/00_stdout.txt"
        # FN_STDOUT2_LOG = "azureml-logs/70_driver_log.txt"
        # FN_STD_OUT_TXT = "user_logs/std_out.txt"
        # FN_STD_LOG_TXT = "user_logs/std_log.txt"

        service_node_info = self.service_node_info
        from_storage = True
        simple_status = "queued"
        aml_status = "queued"

        job_id = utils.safe_value(service_node_info, "job_id", service_node_info["aml_exper_name"].split("-")[-1])
        node_id =  utils.safe_value(service_node_info, "node_id", "node0")
        workspace = service_node_info["ws"]

        new_text = None
        node_status = "queued"
        next_offset = None
        found_file = False
        
        try:
            if self.log_name is None:
                # exact default log name: std_log_process_0.txt   (will the "0" change?)
                file_path = "std_log"     # prefix only for now
            else:
                file_path = self.log_name

            if self.log_source != "live":
                # try to read log from job storage (task has completed)
                node_index = utils.node_index(node_id) 

                job_path = "nodes/node{}/after/service_logs/{}".format(node_index, file_path)
                if self.store.does_job_file_exist(workspace, job_id, job_path):
                    new_text = self.store.read_job_file(workspace, job_id, job_path)
                    aml_status = "completed"
                    simple_status = "completed"
                    found_file = True
                    self.log_source = "after_logs"

            if not found_file:
                from_storage = False
                self.log_name = file_path
                self.log_source = "live"

                # read URL of log file from singularity service
                new_text, simple_status, aml_status = self.read_from_service()

        except BaseException as ex:
            # note: we get exception "...Unauthorized" when our credentials expire 
            ex_text = str(ex)
            if "Unauthorized" in ex_text:
                self.refresh_creds()
                time.sleep(2)
            else:
                print("==> error during read_from_service(): {}".format(ex))
                print("==> will retry error after delay")
                time.sleep(2)

        return {"new_text": new_text, "simple_status": simple_status, "log_name": self.log_name, 
            "service_status": aml_status, "from_storage": from_storage, "log_source": self.log_source}


    