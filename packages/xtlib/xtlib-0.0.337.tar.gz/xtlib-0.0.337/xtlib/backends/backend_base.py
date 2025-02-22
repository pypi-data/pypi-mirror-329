#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# backend_base.py: provides a baseclass for backend classes, and defines the API they implement.
import os
import inspect
from time import time
from typing import List
from interface import implements

from xtlib.console import console

from xtlib import utils
from xtlib import errors
from xtlib import cs_utils
from xtlib import scriptor
from xtlib import pc_utils
from xtlib import run_errors
from xtlib import constants
from xtlib import file_utils
from xtlib import store_utils

from xtlib.backends.backend_interface import BackendInterface

class BackendBase(implements(BackendInterface)):

    '''
    Order of command building:
        - wrap_user_command() adds commands to cmds
        - add_mount_cmds
        - create_wrapper_and_inner() adds commands to docker_cmds
        - append_pre_docker_cmds()

    Order of command execution on node WITH docker:
        - pre_docker_cmds
        - docker_cmds
            - docker prep/install commands
            - docker pull with optional timeout
            - docker run (2-7 below)

    Order of command execution on node WITHOUT docker:
        1. pre_docker_cmds
        2. add_first_cmds
        3. add_setup_cmds
        4. add_other_cmds
        5. add_report_cmds
        6. mount cmds
        7. run controller (or direct run)
        8. node wrapup cmds
    '''
    def __init__(self, compute, compute_def, core, config, username=None, arg_dict=None):
        self.compute = compute
        self.compute_def = compute_def
        self.blobfuse_index = 0
        self.fn_wrapped = None
        self.blobfuse_installed = False
        self.capture_setup_cmds = False
        self.echo_cmds = True
        self.default_docker_image = ""
        self.mounted_drives = []

        # TODO: change this to rely on API for this info
        self.add_time = config.get("logging", "add-timestamps")

        # if these are set to constant values, backend must use unique scripts for each node
        # default for backends is to pass these 3 args to their __wrapped__.xx script (philly is different)
        self.node_index = "$1"
        self.node_id = "node$1"
        self.run_name = "$2"
        self.mounting_enabled = True

        # if backend is running windows
        self.is_windows = False

        # if code should be generated for windows (if targeting a docker container, this can be different than self.is_windows)
        self.gen_for_windows = False
        
    # API
    def supports_setting_location(self):
        # not currently supported
        return False
    
    # API 
    def get_name(self):
        '''
        This method is called return the name of the backend service.
        '''
        pass

    # API 
    def build_node_script_and_adjust_runs(self, job_id, job_runs, using_hp, experiment, service_type, snapshot_dir, env_vars, args, cmds=None):
        '''
        This method is called to allow the backend to inject needed shell commands before the user cmd.  At the
        time this is called, files can still be added to snapshot_dir.
        '''
        pass

    # API 
    def submit_job(self, job_id, job_runs, workspace, compute_def, resume_name, 
            repeat_count, using_hp, runs_by_box, experiment, snapshot_dir, controller_scripts, args):
        raise Exception("backend API function not implemented: submit_job")

    # API 
    def view_status(self, run_name, workspace, job, monitor, escape_secs, auto_start, 
            stage_flags, status, max_finished):
        raise Exception("backend API function not implemented: view_status")

    # API 
    def get_client_cs(self, service_node_info):
        raise Exception("backend API function not implemented: get_client_cs")
    
    # API 
    def provides_container_support(self):
        '''
        Returns:
            returns True if docker run command is handled by the backend.
        '''
        return True

    # API 
    def cancel_runs_by_names(self, workspace, run_names, box_name):
        '''
        Args:
            workspace: the name of the workspace containing the run_names
            run_names: a list of run names
            box_name: the name of the box the runs ran on (pool service)
        Returns:
            cancel_results: a list of cancel_result records 
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''
        raise Exception("backend API function not implemented: cancel_runs")

    # API 
    def cancel_runs_by_job(self, job_id, runs_by_box):
        '''
        Args:
            job_id: the name of the job containing the run_names
            runs_by_box: a dict of box_name/run lists
        Returns:
            cancel_results_by box: a dict of box_name, cancel_result records
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''
        raise Exception("backend API function not implemented: cancel_runs_by_job")

    # API 
    def cancel_runs_by_user(self, ws_name, box_name):
        '''
        Args:
            box_name: the name of the box the runs ran on (pool service)
        Returns:
            cancel_results: a list of kill results records 
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''
        raise Exception("backend API function not implemented: cancel_runs_by_user")

    # common code
    def append(self, cmds, cmd, expand=False, log=None, echo=None, add_time=None):

        if add_time is None:
            add_time = self.add_time

        if expand:
            cmd = self.expand_system_names(cmd)

        # if self.gen_for_windows and not cmd.startswith("@"):
        #     cmd = "@" + cmd

        if log and self.capture_setup_cmds:
            assert isinstance(log, str)
            
            if self.gen_for_windows:
                cmd = "{} > {}\\__{}__.log".format(cmd, constants.WINDOWS_AFTER_LOGS, log)
            else:
                cmd = "{} > {}/__{}__.log".format(cmd, constants.LINUX_AFTER_LOGS, log)

        if echo is None:
            echo = self.echo_cmds

        if echo:
            # avoid echo of super long (multiple line) commands
            max_echo_len = 300        
            cmd_text = cmd
            if len(cmd_text) > max_echo_len:
                cmd_text = cmd_text[0:max_echo_len-3] + "..."

            # ECHO the command before it is run 
            if self.gen_for_windows:
                # WINDOWS 
                cmd_text = cmd_text.replace(">", "^>")    # must escape the ">" to prevent cmd redirection

                if add_time:
                    # %date% is subject to local formatting, etc. so we use python instead
                    # cmd = '''python -c "import datetime as dt; print(dt.date.today().strftime('%m/%d/%Y'))"'''
                    # we use sed (.git install required) to remove double quotes here so that cmd piping can be echoed
                    #cmds.append('''echo "@%date% %time%     ++ {}" | sed 's/"//g' '''.format(cmd_text))
                    cmds.append('''echo "%date% %time%     ++ {}" | sed 's/^...../@/' '''.format(cmd_text))
                else:
                    cmds.append('''echo ++ {}'''.format(cmd_text))

            else:
                # LINUX 
                #cmd_text = cmd.replace(">", "\>")    # must escape the ">" to prevent cmd redirection
                cmd_text = "'{}'".format(cmd_text)

                if add_time:
                    cmds.append('''echo @$(date +%b-%d-%Y"  "%T)"     "++ {}'''.format(cmd_text))
                else:
                    cmds.append('''echo ++ {}'''.format(cmd_text))

        # finally, add the cmd to be run
        cmds.append(cmd)

    def get_activate_cmd(self, args):

        setup_name = args["setup"]
        setup_def = self.config.get_setup_from_target_def(self.compute_def, setup_name)
        activate_cmd = utils.safe_value(setup_def, "activate")

        if activate_cmd:
            if self.gen_for_windows:
                activate_cmd = activate_cmd.replace("$call ", "call ")
            else:
                activate_cmd = activate_cmd.replace("$call ", "")
                # Attempting to activate the Conda shell from within a bash script
                # fails, with Conda saying that the bash environment has not
                # been correctly initialized to use Conda.
                # This thread https://stackoverflow.com/questions/34534513/calling-conda-source-activate-from-bash-script
                # eventually led me to the following command which is taken
                # from the lines of bash script that Conda appends to your
                # .bashrc file upon installation. This command is what
                # allows you to activate the Conda environment within a
                # bash shell. It returns a script generated by Conda
                # which is executed, and which stes up the conda
                # activate / deactivate commands in the encironment.
                conda_shell_bash_hook_cmd = 'eval "$(conda shell.bash hook)"'
                activate_cmd = "{} && {}".format(
                    conda_shell_bash_hook_cmd, activate_cmd)

        return activate_cmd

    def get_service_name(self):
        if not "service" in self.compute_def:
            errors.config_error("missing 'service' property for xt config file compute target '{}'".format(self.compute))
        service_name = self.compute_def["service"]
        return service_name

    def object_to_dict(self, obj, columns):
       obj_dict = {col: getattr(obj, col) for col in columns if hasattr(obj, col)}
       return obj_dict
        
    def expand_system_names(self, cmd):
        if self.gen_for_windows:
            cmd = cmd.replace("$call", "call")
            cmd = cmd.replace("$export", "set")
        else:
            cmd = cmd.replace("$call ", "")
            cmd = cmd.replace("$export", "export")

        if "$current_conda_env" in cmd:
            conda = pc_utils.get_conda_env() 
            if conda:
                cmd = cmd.replace("$current_conda_env", conda)
        
        return cmd


    def xt_report(self, cmds):

        self.append_title(cmds, "XT report:", True)
        if self.gen_for_windows:
            self.append(cmds, "which xt python conda")
        else:
            self.append(cmds, "which xt python conda blobfuse")

        self.append(cmds, "xt --version", echo=True)

    def add_other_cmds(self, cmds, args):
        pp = args["other_cmds"]

        if pp:
            #console.print("other_cmds: {}".format(pp))
            self.append_title(cmds, "OTHER setup cmds:", False)
            for cmd in pp:
                self.append(cmds, cmd)

            self.cd_back_to_setup_dir(cmds)

    def set_gen_for_windows(self, for_windows: bool, args: List[str]):
        docker_cmd = args["docker_cmd"]
        docker_is_windows = args["docker_is_windows"]

        if docker_cmd:
            gen_for_windows = docker_is_windows
        else:
            gen_for_windows = self.is_windows

        self.gen_for_windows = gen_for_windows
        return gen_for_windows

    def define_xt_dir(self, cmds, name, path):

        # ensure dir is empty but present
        if self.gen_for_windows:
            path = file_utils.fix_slashes(path, False, protect_ws_run_name=False)
            self.append_export(cmds, name, path, fix_value=False)
            self.append(cmds, "rd /s /q {}".format(path))
            self.append(cmds, 'mkdir "{}"'.format(path))
        else:
            path = file_utils.fix_slashes(path, True, protect_ws_run_name=False)
            self.append_export(cmds, name, path)
            self.append(cmds, "rm -rf {}".format(path))
            self.append(cmds, 'mkdir -p "{}"'.format(path))

        self.append_dir(cmds, path)

    # API call
    def get_node_status(self, service_node_info):
        pass

    # API call
    def read_log_file(self, service_node_info, log_name, start_offset=0, end_offset=None, 
        encoding='utf-8', use_best_log=True, log_source=None):
        pass

    # API call
    def get_simple_status(self, status):
        # translates an Philly status to a simple status (queued, running, completed)
        pass

    # API call
    def cancel_job(self, service_job_info, service_info_by_node):
        pass
    
    # API call
    def cancel_node(self, service_node_info):            
        pass

    # API call
    def get_service_queue_entries(self, service_node_info):
        pass

    # helper
    def download_log(self, items, service_node_info, log_name, dest_dir, service_context=None):

        result = self.read_log_file(service_node_info, log_name, service_context=None)  # service_context)
        found_file = utils.safe_value(result, "found_file")

        text = result["new_text"]
        if text or found_file:
            base_log_name = os.path.basename(log_name)
            console.print("found log: {}".format(base_log_name))

            fn_log = "{}/{}".format(dest_dir, base_log_name)
            file_utils.write_text_file(fn_log, text)
            items.append(fn_log)
        return result

    # API call
    def add_service_log_copy_cmds(self, ca, cmds, dest_dir, args):
        pass        