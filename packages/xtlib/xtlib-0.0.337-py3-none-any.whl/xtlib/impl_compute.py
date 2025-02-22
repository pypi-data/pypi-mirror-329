#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# impl_compute.py: implementation of XT compute commands
import os
import sys
import json
from textwrap import wrap
import time
import datetime
import tempfile
import numpy as np 

import xtlib.xt_run as xt_run
from xtlib import cs_utils
from xtlib import pc_utils as pc
from xtlib import report_builder
from xtlib.client import Client
from xtlib.runner import Runner
from xtlib.console import console
from xtlib.storage.store import Store
from xtlib.cmd_core import CmdCore
from xtlib.impl_base import ImplBase
from xtlib.backends import backend_aml 
from xtlib.xt_client import XTClient
from xtlib.helpers.scanner import Scanner
from xtlib.qfe import inner_dispatch, get_dispatch_cmd, Dispatcher
from xtlib.qfe import command, argument, option, flag, root, clone
from xtlib.qfe import hidden, example, command_help, keyword_arg
from xtlib.helpers.key_press_checker import KeyPressChecker, single_char_input

from xtlib import qfe
from xtlib import utils
from xtlib import errors
from xtlib import capture
from xtlib import pc_utils
from xtlib import constants
from xtlib import file_utils
from xtlib import job_helper
from xtlib import run_helper
from xtlib import time_utils
from xtlib import process_utils
from xtlib import box_information

'''
This module implements the following commands:

run creation:
     - xt <filename> <app args>                 # run file (.sh, .bat, .py) under control to xt on specified box/pool
     - xt python <filename> <app args>          # run python on file 
     - xt run app <app args>                    # run the app 
     - xt docker run <args>                     # run the specified docker image 

run control/information:
     * xt start tensorboard [ <name> ]          # start tensorboard process for specified box or run
     * xt stop tensorboard [ <name> ]           # stop tensorboard for specified box or run
     * xt collect logs <log path> <runs>        # copy log files from specified runs (on blob store) to grok server

     - xt monitor <name>                        # create a jupyter notebook to monitor an Azure ML run
     - xt attach <name>                         # attach output of run to console (use ESC to detach)
     - xt status                                # display the controller status on the specified box (flags: mirror, tensorboard, controller)
     - xt rerun <name> [ <app args> ]           # rerun the specified run with optional new cmd args
     - xt kill controller                       # terminates the controller on the specified box

     - xt kill runs [ <name list> ]             # terminates the specifed runs or (--boxes, --job, --workspace)

    (*) not yet completed
'''     

DEFAULT_FROM_COMPUTE = None

class ImplCompute(ImplBase):
    def __init__(self, config, store=None):
        super(ImplCompute, self).__init__()
        self.config = config
        self.store = store if store else Store(config=config)
        self.client = Client(config, store, None)
        self.core = CmdCore(self.config, self.store, self.client)
        self.client.core = self.core
        
        #self.azure_ml = backend_aml.AzureML(self.core)

    def is_aml_ws(self, ws_name):
        return False  # self.azure_ml.does_ws_exist(ws_name)

    def validate_and_add_defaults(self, cmd, args):
        dispatcher = Dispatcher({}, self.config)
        full_args = dispatcher.validate_and_add_defaults_for_cmd(cmd, args)

        return full_args

    #---- VIEW STATUS command ----
    @argument(name="run-name", required=False, help="return status only for the specified run")

    @option("cluster", help="the name of the cluster to be viewed")
    @option("vc", default="all", help="the name of the virtual cluster")
    @option("status", help="only show jobs with a matching status")
    @option("max-finished", default=100, type=int, help="the maximum number of finished jobs to show")
    @flag("tensorboard", help="shows the status of tensorboard processes on the box")
    @flag("mirror", help="shows the status of mirror processes on the box")
    @flag("monitor", help="continually monitor the status")
    @flag("auto-start", help="when specified, the controller on the specified boxes will be started when needed")
    @flag("queued", help="when specified, only queued runs are reported")
    @flag("active", help="when specified, only active runs are reported")
    @flag("completed", help="when specified, only completed runs are reported")
    @option("escape-secs", type=int, help="how many seconds to wait before terminating the monitor loop")
    @option("target", default=None, type=str, help="the name of the compute target to query for status")
    @option("username", default="$general.username", type=str, help="the username used to filter runs")
    @option("workspace", default="$general.workspace", type=str, help="the workspace used to filter runs")
    @option(name="job", help="query all boxes defined for the specified job")
    @example(task="show the status of runs on the local machine", text="xt view status")
    @example(task="show the status of run68", text="xt view status curious/run68")
    @command(kwgroup="view", help="displays the status of the specified compute target")
    def view_status(self, run_name, tensorboard, mirror, target, workspace, job, monitor, escape_secs, auto_start, 
            username, active, cluster, vc, status, max_finished, queued, completed):
        '''The view status command is used to display status information about the XT controller process
        running on a box (or pool of boxes).  
        
        The'tensorboard' flag is used to return information about the running tensorboard-related processes.
        The 'mirror' flag is used to return information about Grok server mirroring processes.
        '''

        if not target:
            ss_info = self.config.get_store_info()
            target = utils.safe_value(ss_info, "target")

        if tensorboard:
            run_name = "tensorboard"
        elif mirror:
            run_name = "mirror"
        elif run_name:
            run_name, workspace = run_helper.parse_run_name(workspace, run_name)

        if not queued and not active and not completed:
            # if none of these are specified, it implies we want to see all info
            stage_flags = "queued, active, completed"
        else:
            # at least one flag was specified, so logically "or" them
            stage_flags = ""
            if queued:
                stage_flags += "queued, "
            if active:
                stage_flags += "active, "
            if completed:
                stage_flags += "completed, "

        # active = self.config.get("general", "active")
        # queued = self.config.get("general", "queued")

        if target == "all":
            # enumerate all registered targets and call their view_status method
            targets = self.config.get_targets()

            for target in targets:
                print("\nSTATUS for target '{}':".format(target))

                backend = self.core.create_backend(target, username=username)
                backend.view_status(run_name, workspace, job, monitor, escape_secs, auto_start, 
                    stage_flags, status, max_finished)
        else:
            # view status on a single target
            backend = self.core.create_backend(target, username=username)
            backend.view_status(run_name, workspace, job, monitor, escape_secs, auto_start, 
                stage_flags, status, max_finished)

    #---- MONITOR command ----
    # other candidate names for this command: watch, attach
    @argument(name="name", help="The name of the run or job to be monitored")
    @option("escape", type=int, default=0, help="breaks out of attach or --monitor loop after specified # of seconds")
    @flag("jupyter", help="to monitor a job from a jupyter notebook (AML only)")
    @option("log-name", default=None, help="the name of the log file to be monitored")
    @option("node-index", default=0, type=int, help="the node index for multi-node jobs")
    @option("sleep", default=1, type=float, help="the number of seconds between download calls")
    @option("workspace", default="$general.workspace", type=str, help="the workspace that the run resides within")
    @example(task="monitor job3321's primary log file", text="xt monitor job3321")
    @command(help="view a job's log file, as it grows in real-time")
    def monitor(self, name, escape=None, jupyter=None, log_name=None, node_index=None, sleep=1, workspace=None):
        if jupyter:
            return self.monitor_with_jupyter(workspace, name)

        if job_helper.is_job_id(name):
            if "/" in name:
                name, node_index = name.split("/")
                
            return self.monitor_job_node(workspace, name, sleep, node_index, log_name, escape) 

        if run_helper.is_run_name(name):
            rr = run_helper.get_run_record(self.store, workspace, name)
            job_id = rr["job_id"]
            node_index = rr["node_index"]
            return self.monitor_job_node(workspace, job_id, sleep, node_index, log_name, escape) 

        errors.syntax_error("name must be a job or run name: {}".format(name))

    def show_monitor_help(self):
        print("\ntraining interaction menu:")
        print("  ESCAPE: stop monitoring job")
        print("  control-c: cancel job")
        print("  +: change to next node index")
        print("  -: change to prev node index")
        print()
        print("  q: show queued jobs (for pool nodes)")
        print("  t: show a prediction from TRAIN data")
        print("  e: show a prediction from EVAL data")
        print("  h: help (show this menu)")
        print("  ?: show hyperparameter values")
        print("  =: change the value of a hyperparameter")
        print()

    def send_user_request(self, request, ws_name, job_id, node_index):
        rd = None

        if request == "help":
            self.show_monitor_help()
        elif request == "set_hparam":
            console.print()
            name = input("enter HP name to set: ")
            if name:
                value = input("enter new value of {}: ".format(name))
                rd = {"set_hparam": {"name": name, "value": value}}
            console.print()
        else:
            rd = {request: 1}

        if rd:
            rd_text = json.dumps(rd)

            # get the connection string for the job/node
            cs_plus = job_helper.get_client_cs(self.core, ws_name, job_id, node_index)
            cs = cs_plus["cs"]
            box_secret = cs_plus["box_secret"]  

            with XTClient(self.config, cs, box_secret) as xtc:
                if xtc.connect():
                    result = xtc.queue_user_request(rd_text)        

    def monitor_job_node(self, workspace, job_id, sleep, node_index, log_name, escape_secs):

        if node_index is None:
            node_index = 0

        # enable ANSI escape chars on Windows 10 for color output
        pc.enable_ansi_escape_chars_on_windows_10()

        backend, job_info = job_helper.get_job_info_with_backend(self.store, self.core, workspace=workspace, 
            job_id=job_id, node_index=node_index)

        node_id = utils.node_id(node_index)
        service_info_by_node = job_info["service_info_by_node"]  
        if not service_info_by_node:
            errors.general_error("job is missing service_info_by_node table (terminated during submit?): {}".format(job_id))

        service_node_info = service_info_by_node[node_id]
        pool_info = job_info["pool_info"]
        node_count = len(service_info_by_node)

        target = utils.safe_value(pool_info, "name")
        merge_batch_logs = utils.safe_value(service_node_info, "merge_batch_logs")
        if merge_batch_logs and log_name is None:
            log_name = "stdboth.txt"

        target_str = self.config.get_target_desc(target, backend)
        log_source = None

        # local func
        def print_status_msg(msg):
            if log_source == "live":
                dt = time_utils.get_arrow_now_str()
                console.print("{} \t({})".format(msg, dt), flush=True)

            else:
                console.print(msg, flush=True)
    
        console.print("xt monitor: press escape or control-c to exit, h for help menu")
        print_status_msg("==> monitoring: {}, node{} [{}]".format(job_id, node_index, target_str))

        # the monitoring loop
        # start_offset = 0
        simple_status = None
        service_status = None
        kb_sleep = .1       # be quick to respond to user's key presses
        sleeps_per_call = max(1, sleep//kb_sleep)
        sleep_count = 0
        ch = None
        first_call = True
        # offset_by_node = {}
        node_id = utils.node_id(node_index)
        first_text_of_stream = True
        display_count = 0
        started = time.time()
        last_status_shown = None
        request_dict = {"t": "predict_train", "e": "predict_eval", "?": "show_hparams", "=": "set_hparam", "h": "help"}
        from_storage = None
        is_queued = False            # used to detect when we switch into a new node (restart after preemption)

        # for now, disable this (not being used)
        interactive_monitoring = False

        backend_log_reader = backend.get_log_reader(service_node_info)

        try:
            with KeyPressChecker() as checker:

                while simple_status != "completed":

                    ch = checker.getch_nowait()
                    if ch is not None:
                        console.print("detected user input key: {}".format(ch))

                    if interactive_monitoring:
                        if ch == constants.ESCAPE or ch == constants.CONTROL_C:
                            break

                        if ch in ["+", "-"] and node_count > 1:
                            # save current context
                            offset_by_node[node_id] = start_offset

                            # increment node_index
                            delta = 1 if ch == "+" else -1
                            node_index = (delta + node_index) % node_count
                            node_id = utils.node_id(node_index)

                            # set new context
                            service_node_info = service_info_by_node[node_id]
                            start_offset = offset_by_node[node_id] if node_id in offset_by_node else 0
                            first_text_of_stream = not start_offset
                            print_status_msg("==> switching to: node{}".format(node_index))

                        if ch == "q":
                            # diagnostic aid (undocumented, only for pool service)
                            console.print("{} service queue:".format(node_id), flush=True)

                            entries = backend.get_service_queue_entries(service_node_info)
                            if entries is None:
                                console.print("  <not supported for this service>")
                            else:
                                if entries:
                                    for entry in entries:
                                        marker = "*" if entry["current"] else " "
                                        console.print("  {} {}".format(marker, entry["name"]))
                                else:
                                    console.print("  <no entries>")

                        # turn this off for now (to easy to type in monitor window accidently and get interaction errors)
                        # if ch in request_dict:
                        #     request = request_dict[ch]
                        #     self.send_user_request(request, workspace, job_id, node_index)

                    if sleep_count == sleeps_per_call:

                        # time to read the log file
                        result = backend_log_reader.read()

                        new_text = result["new_text"]
                        new_simple = result["simple_status"]
                        new_status = result["service_status"]
                        new_log = result["log_name"]

                        from_storage = utils.safe_value(result, "from_storage")
                        file_path = utils.safe_value(result, "file_path")
                        log_source = utils.safe_value(result, "log_source")

                        if first_call or new_log != log_name:
                            log_name = new_log                
                            if file_path:
                                print_status_msg("==> node{} streaming log: {} ({})".format(node_index, log_name, file_path))
                            else:
                                print_status_msg("==> node{} streaming log: {}".format(node_index, log_name))
                            first_text_of_stream = True

                        if new_status != service_status:
                            # status of service has changed
                            service_status = new_status
                            simple_status = new_simple
                            print_status_msg("==> node{} status: {} ({})".format(node_index, service_status, simple_status))
                            last_status_shown = simple_status

                            if simple_status == "queued":
                                # we are just started or have been preempted
                                is_queued = True
                            elif simple_status == "running":
                                if is_queued:
                                    # we are running on a new node after being preempted 
                                    start_offset = 0
                                    is_queued = False

                        if new_text:

                            if node_count > 1:
                                # prepend each new line with node_id
                                prefix = node_id + ": "
                                new_text = new_text.replace("\n", "\n" + prefix)

                                if first_text_of_stream:
                                    new_text = prefix + new_text
                                    first_text_of_stream = False

                            console.print(new_text, end="")
                            display_count += 1

                        first_call = False
                        sleep_count = 0

                    time.sleep(kb_sleep)
                    sleep_count += 1

                    if escape_secs:
                        # have we exceeded max time in monitoring?
                        elapsed = time.time() - started
                        if elapsed >= escape_secs:
                            break

        except KeyboardInterrupt:
           ch = constants.CONTROL_C

        show_final_status = (display_count > 0)

        if ch == constants.ESCAPE:
            print_status_msg("==> monitoring cancelled (escape key detected)")

        elif ch == constants.CONTROL_C:
            print_status_msg("==> monitoring cancelled (control-c detected)")
            ch = single_char_input("do you want to cancel the job? (y/n): ")
            if ch == "y":
                max_workers = self.config.get("general", "max-run-workers")
                self.cancel_job([job_id], workspace, max_workers, cancel=True, wrapup=True)
                show_final_status = False

        if show_final_status:    #  and last_status_shown != simple_status:
            print_status_msg("==> node{} final status: {} ({})".format(node_index, service_status, simple_status))

        source_msg = ""
        if from_storage is not None:
            source_msg = " (from storage)" if from_storage else " (from service)"

        console.print("end of monitoring: {}{}".format(job_id, source_msg))

    def monitor_with_jupyter(self, workspace, run_name):
        if not self.is_aml_ws(workspace):
            errors.combo_error("the monitor command is only supported for Azure ML runs")

        run_name, actual_ws = run_helper.parse_run_name(workspace, run_name)

        fn = self.azure_ml.make_monitor_notebook(actual_ws, run_name)
        dir = os.path.dirname(fn)
        #console.print("jupyter notebook written to: " + fn)
        monitor_cmd = "jupyter notebook --notebook-dir=" + dir
        console.print("monitoring notebook created; to run:")
        console.print("  " + monitor_cmd)

    #---- COLLECT LOGS command ----
    @argument(name="run-names", type="str_list", help="comma-separated list of run names")
    @argument(name="log-path", help="the wildcard path of the log files to collect")
    @option("workspace", default="$general.workspace", type=str, help="the workspace that the runs reside within")
    @example(task="collect the log files matching *tfevent* from run68", text="xt collect logs run68, run69 *tfevent* --work=curious")
    @command(help="copy log files from specified runs (on blob store) to grok server")
    def collect_logs(self, workspace, run_names, log_path):

        run_names, actual_ws = run_helper.parse_run_list(self.store, workspace, run_names)
        if len(run_names) == 0:
            self.store_error("No matching runs found")

        grok_server = None   # self.config.get("logging", "grok-server")

        count = 0
        for run_name in run_names:
            count += self.core.collect_logs_for_run(actual_ws, run_name, log_path, grok_server)

        console.print("{} log file collected to grok server: {}".format(count, grok_server))

    #---- START TENSORBOARD command ----
    @example(task="start tensorboard curious/run68", text="xt start tensorboard curious/run68")
    @command(help="start tensorboard for the specified run")
    def start_tensorboard(self):
        console.print("start_tensorboard cmd goes here...")

    #---- STOP TENSORBOARD command ----
    @example(task="stop tensorboard curious/run68", text="xt stop tensorboard curious/run68")
    @command(help="stop tensorboard for the specified run")
    def stop_tensorboard(self):
        console.print("stop_tensorboard cmd goes here...")

    def get_info_for_run(self, ws, run_name):
        cmdline = None
        box_name = None
        parent_name = None
        node_index = None
        xt_cmdline = None

        records = self.store.get_run_log(ws, run_name)

        # get cmdline
        for record in records:
            if record["event"] == "cmd":
                dd = record["data"]
                cmdline = dd["cmd"]
                xt_cmdline = dd["xt_cmd"]
                break

        for record in records:
            if record["event"] == "created":
                dd = record["data"]
                box_name = dd["box_name"]
                node_index = dd["node_index"]
                # looks like we no longer log the parent name
                #parent_name = dd["parent_name"]
                parent_name = run_name.split(".")[0] if "." in run_name else None
                break

        return cmdline, xt_cmdline, box_name, parent_name, node_index

    #---- RERUN command ----
    @argument("run-name", help="the name of the original run")
    @option("workspace", default="$general.workspace", type=str, help="the workspace that the runs reside within")
    @option("response", default=None, help="the automatic response to be used to supplement the cmd line args for the run")
    @example(task="rerun run74", text="xt rerun curious/run74")
    @command(help="submits a run to be run again")
    def rerun(self, run_name, workspace, response):
        # NOTE: validate_run_name() call must be AFTER we call process_named_options()
        run_name, workspace = run_helper.parse_run_name(workspace, run_name)

        # extract "prompt" and "args" from cmdline
        cmdline, xt_cmdline, box_name, parent_name, node_index = self.get_info_for_run(workspace, run_name)

        #console.print("cmdline=", cmdline)
        prompt = ""

        if xt_cmdline:
            args = "  " + xt_cmdline
        else:
            # legacy run; just use subset of xt cmd
            args = "  xt " + cmdline

        console.print("edit/accept xt cmd for {}/{}".format(workspace, run_name))
        if response:
            # allow user to supplement the cmd with automation
            if "$cmd" in response:
                response = response.replace("$cmd", args)
            console.print(response)
        else:
            response = pc_utils.input_with_default(prompt, args)

        # keep RERUN cmd simple by reusing parse_python_or_run_cmd()
        full_cmd = response.strip()
        #console.print("  new_cmd=" + full_cmd)
        if not full_cmd.startswith("xt "):
            errors.syntax_error("command must start with 'xt ': {}".format(full_cmd))

        # this temp dir cannot be removed immediately after job is submitted (TBD why)
        tmp_dir = file_utils.make_tmp_dir("rerun_cmd")
        job_id = self.store.get_job_id_of_run(workspace, run_name)
        capture.download_before_files(self.store, job_id, workspace, run_name, tmp_dir, 
            silent=True, log_events=False, source="run")
         
        # move to tmp_dir so files get captured correctly
        prev_cwd = os.getcwd()
        os.chdir(tmp_dir)

        try:
            # recursive invoke of QFE parser to parse command (orginal + user additions)
            args = full_cmd.split(" ")
            args = args[1:]    # drop the "xt" at beginning
            inner_dispatch(args, is_rerun=True)
        finally:
            # change back to original dir
            os.chdir(prev_cwd)

    # #---- STOP CONTROLLER command ----
    # @option("box", default="local", type=str, help="the name of the box")
    # @option("pool", type=str, help="the name of the pool of boxes")
    # @example(task="stop the controller process on the local machine", text="xt stop controller")
    # @example(task="terminate the controller process on box 'vm10'", text="xt stop controller --box=vm10")
    # @command(help="stops the XT controller process on the specified box")
    # def stop_controller(self, box, pool):

    #     boxes, pool_info, service_type = box_information.get_box_list(self.core, box=box, pool=pool)
    #     #console.print("boxes=", boxes, ", is_azure_pool=", is_azure_pool)

    #     self.client.cancel_controller_by_boxes(boxes)

    def print_cancel_results(self, cancel_results_by_boxes, run_summary=None, is_aml=False):
        #console.print("cancel_results_by_boxes=", cancel_results_by_boxes)

        if run_summary:
            console.print(run_summary)

        if not cancel_results_by_boxes:
            console.print("no matching runs found")
            return
            
        for box_name, results in cancel_results_by_boxes.items():

            # show box name as upper to emphasize where kill happened
            box_name = box_name.upper()

            if not run_summary:
                console.print(box_name + ":")

            if not results:
                console.print("  no matching active runs found")
            else:
                for result in results:
                    if not result:
                        continue

                    #console.print("result=", result)
                    ws_name = result["workspace"]
                    run_name = result["run_name"]
                    exper_name = result["exper_name"] if "exper_name" in result else None
                    killed = result["cancelled"]
                    status = result["status"]
                    before_status = result["before_status"]
                        
                    run_name = exper_name + "." + run_name if exper_name else run_name
                    full_name = ws_name + "/" + run_name

                    if killed:
                        console.print("  {} cancelled (status was '{}')".format(full_name, before_status))
                    else:
                        console.print("  {} has already exited, status={}".format(full_name, status))

    def print_cancel_all_results(self, cancel_results_by_boxes):
        for target, results in cancel_results_by_boxes.items():
            console.print("Target: {}".format(target))

            for result in results:
                if result:
                    console.print(
                        "cancelled: {}, service_status: {}, simple_status: {}".format(
                            result.get("cancelled"),
                            result.get("service_status"),
                            result.get("simple_status")))

    def get_runs_by_box(self, run_names, workspace=None):
        run_names, actual_ws = run_helper.parse_run_list(self.store, workspace, run_names)

        db = self.store.get_database()
        fields_dict = {"box_name": 1, "compute": 1, "ws_name": 1, "run_name": 1, "job_id": 1}

        filter_dict = {}
        filter_dict["run_name"] = {"$in": run_names}

        box_records = db.get_info_for_runs(actual_ws, filter_dict, fields_dict)

        # group by box_name
        runs_by_box = {}

        for br in box_records:
            if "box_name" in br:
                box_name = br["box_name"] 
                runs_by_box[box_name] = br

        return runs_by_box

    #---- CANCEL RUN command ----
    @argument("run-names", type="str_list", help="the list of run names to cancel")
    @option("workspace", default="$general.workspace", type=str, help="the workspace that contains the runs")
    @example(task="cancel run103 in curious workspace", text="xt cancel runs run103 --work=curious")
    @command(kwgroup="cancel", kwhelp="cancels active runs, jobs, or requests", help="cancels the specified run(s)")
    def cancel_run(self, run_names, workspace):

        runs_by_box = self.get_runs_by_box(run_names, workspace)

        cancel_results_by_box = {}

        for box_name, box_run in runs_by_box.items():

            run_names = [box_run["run_name"]]
            compute = box_run["compute"] if "compute" in box_run else "pool"    # some legacy support

            backend = self.core.create_backend(compute)
            cancel_results = backend.cancel_runs_by_names(workspace, run_names, box_name)

            cancel_results_by_box[box_name] = cancel_results

            if "_" in box_name:
                # normal backend service
                job_id, service_id, node_index = box_name.split("-")

            else:
                # single box name
                job_id = box_run["job_id"]
                node_index = 0
                service_id = "pool"

            self.store.database.mark_node_cancelled(workspace, job_id, node_index)

        self.print_cancel_all_results(cancel_results_by_box)

    #---- CANCEL JOB command ----
    @argument("job-names", type="str_list", help="the names of the jobs to be cancelled")
    @option("workspace", default="$general.workspace", help="the workspace that contains the jobs to be cancelled")
    @option("max-workers", type=int, default="$general.max-run-workers", help="the max number of background workers for this command")
    @flag("cancel", default=1, help="call the backend service to cancel the job")
    @flag("wrapup", default=1, help="wrapup the nodes and runs associated with the job")
    @example(task="cancel jobs job3 and job15", text="xt cancel job job3, job15")
    @command(kwgroup="cancel", help="cancels the specified jobs and their active or queued runs")
    def cancel_job(self, job_names, workspace, max_workers, cancel, wrapup):

        for job_id in job_names:
            service_job_info, service_info_by_node, backend = \
                job_helper.get_service_job_info(self.store, self.core, workspace, job_id)

            if cancel:
                console.print("cancelling {} (service: {}):".format(job_id, backend.get_name()))
                node_end_times = None

                try:
                    result_by_node, node_end_times = backend.cancel_job(service_job_info, service_info_by_node)

                    for node_id, result in result_by_node.items():
                        console.print("  {}: {}".format(node_id, result))
                except BaseException as ex:
                    console.print("Exception during service cancel call: {}".format(ex))

            if wrapup and node_end_times:
                # whether or not the cancel succeeded, cleanup the RUNS
                node_list = list(service_info_by_node.keys())
                runs = run_helper.wrapup_runs_nodes_job(self.store, workspace, job_id, node_list, node_end_times, max_workers)

    #---- CANCEL REQUESTS command ----
    @argument("names", type="str_list", help="the names of the requests to be cancelled")
    @option("workspace", default="$general.workspace", help="the workspace that contains the requests")
    @example(task="cancel requests request3 and request5", text="xt cancel requests request3, request5")
    @command(kwgroup="cancel", help="cancels job submission requests (created by xt run --request)")
    def cancel_requests(self, names, workspace):

        filter_dict = {"request_id": {"$in": names}}
        records = self.store.database.get_info_for_requests(workspace, filter_dict)
        for record in records:
            status = record["status"]
            name = record["request_id"]

            if status == "requested":
                username = self.config.get("general", "username")
                self.store.update_request_status(record, "cancelled", username)
                console.print("request cancelled: {}".format(name))

                # notify requester (and cc-canceller)
                requester = record["requested_by"]
                self.send_cancel_email_to_approvers(name, requester, username)
                console.print("cancellation sent (email/SMS) to requester: {}".format(requester))

            else:
                console.print("request '{}' not pending; status: {}".format(name, status))

    def send_approval_email_to_requester(self, request_id, requester, approver, job_id):
        team_dict = self.config.get("team")

        requester_contacts = cs_utils.get_contacts(team_dict, requester)
        approver_contacts, approver_usernames = cs_utils.get_approvers(team_dict)
        
        subject = "{} APPROVED: {}".format(request_id, job_id)

        # make body HTML 
        body = ""
        body += "<b>job submission request:</b> {}".format(request_id)
        body += "<br><b>approved by:</b> {}".format(approver)
        body += "<br><b>created job_id:</b> {}".format(job_id)
        sent = False

        try:
            cs_utils.send_to_contacts_from_config(self.config, requester_contacts, approver_contacts, subject, body)
            sent = True
        except BaseException as ex:
            console.print("email/SMS send failed: ex: {}".format(ex))

    def send_cancel_email_to_approvers(self, request_id, requester, canceller):
        team_dict = self.config.get("team")

        requester_contacts = cs_utils.get_contacts(team_dict, requester)
        canceller_contacts = cs_utils.get_contacts(team_dict, canceller)
        approver_contacts, approver_usernames = cs_utils.get_approvers(team_dict)

        cc_list = cs_utils.combine_contacts(requester_contacts, canceller_contacts)
        
        subject = "job request CANCELLED: {}".format(request_id)

        # make body HTML 
        body = ""
        body += "<b>job submission request:</b> {}".format(request_id)
        body += "<br><b>cancelled by:</b> {}".format(canceller)
        sent = False

        try:
            cs_utils.send_to_contacts_from_config(self.config, approver_contacts, cc_list, subject, body)
            sent = True
        except BaseException as ex:
            console.print("email/SMS send failed: ex: {}".format(ex))

    #---- APPROVE command ----
    @argument("names", type="str_list", help="the names of the requests to be approved")
    @option("workspace", default="$general.workspace", help="the workspace that contains the requests")
    @flag("force", help="when specified, previously processed requests can be approved")
    @example(task="approve requests request3 and request5", text="xt approve request3, request5")
    @command(help="approves and submits a job for the specified requests ")
    def approve(self, names, workspace, force):

        filter_dict = {"request_id": {"$in": names}}
        records = self.store.database.get_info_for_requests(workspace, filter_dict)
        for record in records:
            status = record["status"]
            name = record["request_id"]

            if force or status == "requested":
                username = self.config.get("general", "username")
                self.store.update_request_status(record, "approved", username)
                console.print("request approved: {}".format(name))

                xt_cmd = record["cmd"]
                console.print("  running: " + xt_cmd)

                # submit the job by running xt_cmd, capturing the output so we can extract the job_id
                console.set_capture(True, clear_captured=True)
                xt_run.main(xt_cmd)

                output_parts = console.set_capture(False)

                # find line that begins with "job"
                job_id = None
                for line in output_parts:
                    if line.startswith("job"):
                        job_id = line.split(",", 1)[0]
                        break

                # update record with job_id
                record["job_id"] = job_id
                self.store.database.update_requests_record(workspace, name, record)

                requester = record["requested_by"]
                self.send_approval_email_to_requester(name, requester, username, job_id)
                console.print("approval sent (email/SMS) to requester: {}".format(requester))

            else:
                console.print("request '{}' not pending; status: {}".format(name, status))

    # #---- RESUME command ----
    # @argument("job-id", type=str, help="the name of the job whose node will be resumed")
    # @option("workspace", default="$general.workspace", type=str, help="the workspace of the job")
    # @option("node-index", default=0, type=int, help="the 0-based node index to be resumed")
    # @option("monitor", default="$general.monitor", values=["new", "bg", "same", "none"], help="how to monitor primary run of the new job")
    # @example(task="resume node 1 of job42", text="xt resume job42 --node-index=1")
    # @command(pass_by_args=True, help="resumes a node of a job that was previously cancelled (used for testing XT's handling of preempted jobs) ")
    # def resume(self, args):
    #     workspace = args["workspace"]
    #     job_id = args["job_id"]
    #     node_index = args["node_index"]

    #     filter_dict = {"ws_name": workspace, "job_id": job_id}
    #     jobs = self.store.database.get_info_for_jobs(workspace, filter_dict)
    #     if not jobs:
    #         errors.general_error("job not found: {}".format(job_id))

    #     job = jobs[0]
    #     console.print("resuming job: {}, node: {}".format(job_id, node_index))

    #     xt_cmd = job["xt_cmd"]
    #     # add the --resume-node option to the xt_cmd
    #     resume_option = '--resume-node="{}/{}" '.format(job_id, node_index)
    #     index = 4 + xt_cmd.index("run ")

    #     xt_cmd = xt_cmd[:index] + resume_option + xt_cmd[index:]
    #     console.print("  running: " + xt_cmd)

    #     # submit the job by running xt_cmd, capturing the output so we can extract the job_id
    #     #console.set_capture(True, clear_captured=True)
    #     xt_run.main(xt_cmd)

    # TODO: this will replace the 'view status' command
    #---- LIST QUEUES command ----
    @argument("target", help="the name of the compute target")
    @option("queues", type="str_list", values=["queued", "running", "completed"], help="the queues to list")
    @option("username", default="$general.username", help="the username to filter entries with")
    @option("workspace", default="$general.workspace", help="the workspace that contains the jobs to be cancelled")
    @example(task="list my all of my queued jobs on the target philly-rr1", text="list queues philly-rr1  --queues=queued ")
    @command(kwgroup="list", kwhelp="displays the specified storage items", help="list the queue entries for the specified compute target")
    def list_queues(self, target, username, queues, workspace):
        backend = self.core.create_backend(target, username=username)
        target_def = self.config.get_target_def(target)
        builder = report_builder.ReportBuilder()

        results_by_queue, columns = backend.get_queue_jobs(target_def, username, queues, workspace)

        for queue, entries in results_by_queue.items():
            console.print("\nqueue: {}".format(queue))

            text, _ = builder.build_formatted_table(entries, columns, columns)
            # indent all lines by 2 spaces
            text = "  " + text.replace("\n", "\n  ")
            console.print(text)


    #---- CANCEL ALL command ----
    @argument("target", help="the name of the compute target (or backend service) whose runs will be cancelled")
    @hidden("username", default="$general.username", help="the username to log as the author of this run")
    @option("workspace", default="$general.workspace", help="the workspace to cancel runs in")
    @example(task="cancel all runs for current user on Philly", text="xt cancel all philly")
    @command(kwgroup="cancel", kwhelp="cancels jobs, runs, requests", help="cancels all queued/active runs on the specified compute target")
    def cancel_all(self, target, username, workspace):

        backend = self.core.create_backend(target, username=username)
        cancel_results_by_box = {}

        compute_info = self.config.get_target_def(target)
        service_name = compute_info["service"]

        if service_name == "pool":
            boxes = compute_info["boxes"]
            for box_name in boxes:
                cancel_results = backend.cancel_runs_by_user(ws_name=workspace, box_name=box_name)
            
                cancel_results_by_box[box_name] = cancel_results
        else:
            cancel_results = backend.cancel_runs_by_user(ws_name=workspace, box_name=None)
            cancel_results_by_box[target] = cancel_results

        self.print_cancel_all_results(cancel_results_by_box)

    #---- RESTART CONTROLLER command ----
    @argument("job-id", help="the name of the job whose node will be restarted")
    @option("node-index", default=0, help="the 0-based node index to be restarted")
    @option("delay", type=float, default=15, help="the number of seconds to delay after cancelling runs and before restarting the controller")
    @example(task="simulate a service-level restart on job23, node 1", text="xt restart controller job23 --node=1")
    @command(help="uses the XT controller to simulate a service-level restart on the specified job/node")
    def restart_controller(self, job_id, node_index, delay):

        result = None

        # get the connection string for the job/node
        cs_plus = job_helper.get_client_cs(self.core, job_id, node_index)
        cs = cs_plus["cs"]
        box_secret = cs_plus["box_secret"]

        with XTClient(self.config, cs, box_secret) as xtc:
            if xtc.connect():
                result = xtc.restart_controller(delay)

        if result:
            console.print("controller restarted")
        else:
            console.print("could not connect to controller: ip={}, port={}".format(cs["ip"], cs["port"]))

    #---- VIEW CONTROLLER STATUS command ----
    @argument("job-id", help="the name of the job whose node will be restarted")
    @option("node-index", default=0, type=int, help="the 0-based node index to be restarted")
    @example(task="view the status of the 2nd node running job100", text="xt view controller status job100 --node=1")
    @command(kwgroup="view", help="uses the XT controller to view the status of the specified job/node")
    def view_controller_status(self, job_id, node_index):

        # get the connection string for the job/node
        cs_plus = job_helper.get_client_cs(self.core, job_id, node_index)
        cs = cs_plus["cs"]
        box_secret = cs_plus["box_secret"]
        
        job = cs_plus["job"]
        compute = job["compute"]

        if not cs:
            console.print("could not find controller for job={}".format(job_id))
        else:
            stage_flags="queued, active, completed"

            with XTClient(self.config, cs, box_secret) as xtc:
                if xtc.connect():
                    elapsed = xtc.get_controller_elapsed()
                    xt_version = xtc.get_controller_xt_version()
                    max_runs = xtc.get_controller_concurrent()
                    ip_addr = xtc.get_controller_ip_addr()
                    status_text = xtc.get_runs(stage_flags)

                    elapsed = str(datetime.timedelta(seconds=elapsed))
                    elapsed = elapsed.split(".")[0]   # get rid of decimal digits at end

                    box_name = cs["box_name"]
                    indent = "  "
                    cname = "localhost" if box_name=="local" else box_name

                    fmt_str = "XT controller:\n" + \
                        indent + "{}:{}, {}, SSL, xtlib: {}\n" + \
                        indent + "IP: {}:{}, running time: {}, max-runs: {}"
                        
                    text = fmt_str.format(job_id, cname, compute, xt_version, ip_addr, cs["port"], elapsed, max_runs)

                    text +=  "\n\n" + stage_flags + " runs on " + box_name.upper() + ":\n"
            
                    report = self.core.build_jobs_report(status_text)

                    console.print(text)
                    console.print(report)
                else:
                    console.print("could not connect to controller")

    #---- VIEW CONTROLLER LOG command ----
    @argument("job-id", help="the name of the job whose node will be restarted")
    @option("node-index", default=0, help="the 0-based node index to be restarted")
    @example(task="view the conntroller log for single node job100", text="xt view controller status job100")
    @command(kwgroup="view", kwhelp="view information about a node using the XT controller", help="uses the XT controller to view it's log on the specified job/node")
    def view_controller_log(self, job_id, node_index):

        result = None

        # get the connection string for the job/node
        cs_plus = job_helper.get_client_cs(self.core, job_id, node_index)
        cs = cs_plus["cs"]
        box_secret = cs_plus["box_secret"]
        stage_flags="queued, active, completed"

        with XTClient(self.config, cs, box_secret) as xtc:
            if xtc.connect():
                text = xtc.get_controller_log()

                box = cs["box_name"]
                console.print("box={}, controller log:".format(box.upper()))
                console.print(text)
            else:
                console.print("could not connect to controller")

    #---- RUN command ----
    @argument("script", required=True, type=str, help="the name of the script to run")
    @argument("script-args", required=False, type="text", help="the command line arguments for the script")

    # visible and hidden options (currently=71 total, 41 visible)
    @hidden("aggregate-dest", default="$hyperparameter-search.aggregate-dest", help="where hyperparameter searches should be aggregated for HX ('job' or 'experiment')")
    @hidden("after-dirs", default="$after-files.after-dirs", help="the files and directories to upload after the run completes")
    @hidden("after-omit", default="$after-files.after-omit", help="the files and directories to omit from after uploading")
    @flag("after-upload", default="$after-files.after-upload", help="when true, the after files are upload when the run completes")
    @option("aml-compute", type=str, default=DEFAULT_FROM_COMPUTE, help="specifies the name of the AML compute resource for the job")
    @hidden("capture_setup_cmds", type=bool, default="$logging.capture-setup-cmds", help="specifies if some setup cmds should output to a log file")
    @option("cluster", help="the name of the Philly cluster to be used")
    @option("code", type=str, help="the source of a code snapshot (job id, file path, or blob path) to use in place of current code")
    @hidden("code-dirs", default="$code.code-dirs", help="paths to the main code directory and dependent directories")
    @hidden("code-omit", default="$code.code-omit", help="the list wildcard patterns to omit uploading from the code files")
    @flag("code-upload", default="$code.code-upload", help="when true, code is uploaded to job and download for each run of job")
    @hidden("code-zip", default="$code.code-zip", type=str, help="the type zip file to create for the CODE files: none/fast/compress")
    @option("concurrent", default="$hyperparameter-search.concurrent", type=int, help="the maximum concurrent runs to be allowed on each node")
    @option("data-action", default="$data.data-action", values=["none", "download", "mount"], help="the data action to take on the target, before run is started")
    @hidden("data-local", default="$data.data-local", help="the path on the local machine specifying where the data for this job resides")
    @hidden("data-omit", default="$data.data-omit", help="the list wildcard patterns to omit uploading from the data files")
    @hidden("data-share-path", default="$data.data-share-path", help="the path on the data share where data for this run will be stored")
    @flag("data-upload", default="$data.data-upload", help="when true, the data for this job will be automatically upload when the job is submitted")
    @flag("data-writable", default="$data.data-writable", help="when true, a mounted data path can be written to")
    @hidden("delay-evaluation", default="$early-stopping.delay-evaluation", type=int, help="number of evals (metric loggings) to wait before applying early stopping policy")
    @option("description", help="your description of this run")
    @flag("direct-run", default="$general.direct-run", help="when True, the script is run without the controller (on Philly or AML)")
    @option("display-name", default="$general.display-name", type=str, help="the singularity display name for this job")
    @flag("distributed", default="$general.distributed", help="when True, the multiple nodes will be put into distributed training mode")
    @hidden("distributed-training", default="$aml-options.distributed-training", help="the name of the backend process to use for distributed training")
    @option("docker", type=str, help="the name of the docker entry to use with the target (from one of the entries in the config file [dockers] section")
    @hidden("docker-pull-timeout", default="$general.docker-pull-timeout", type=str, help="duration to wait for docker pull cmd (with retries)")
    @hidden("docker-other-options", default="$general.docker-other-options", type=str, help="extra user options to append to docker run command")
    @flag("dry-run", help="when True, the planned runs are displayed but not submitted")
    @hidden("early-policy", default="$early-stopping.early-policy", help="the name of the early-stopping policy to use (bandit, median, truncation, none)")
    @option("escape", type=int, default=0, help="breaks out of attach or --monitor loop after specified # of seconds")
    @hidden("env-vars", default="$general.env-vars", help="the environment variable to be passed to the run when it is launched")
    @hidden("evaluation-interval", default="$early-stopping.evaluation-interval", type=int, help="the frequencency (# of metric logs) for testing the policy")
    @option("events", type="str_list", help="the list of events used to generate notifications for this job")
    @option("experiment", default="$general.experiment", type=str, help="the name of the experiment to create this run under")
    @flag("extract-single-hps", help="when True, single valued hyperparameters are extracted into their own generated .yaml file")
    @option("fake-error-percent", default="$database.fake-error-percent", type=float, help="for testing only: the percentage of database calls to fail")
    @flag("fake-submit", help="when True, we skip creation of job and runs and the submit (used for internal testing)")
    @option("force-restart", default=None, type=str, help="for testing only: simulates a preemption and restart after running the specified time (e.g., 15m or 3h)")
    @hidden("fn_generated_config", default="$hyperparameter-search.fn-generated-config", type=str, help="the name for the generated HP config file")
    @hidden("framework", default="$aml-options.framework", help="the name of the framework to be installed for the run (pytorch, tensorflow, chainer)")
    @option("from-request", type=str, help="The name of the request this generated this run)")
    @hidden("fw-version", default="$aml-options.fw-version", help="the framework version number")
    @option("goal-metric", default="$hyperparameter-search.goal-metric", type=float, help="goal for primary metrics (stops CCD hp search when reached)")
    @option("grid-repeat", type=int, help="the number of times to repeat each hyperparameter set")
    #@hidden("grok-server", default="$logging.grok-server", help="the ip address of the grok-server to be used for mirroring")
    @flag("hold", help="when True, the Azure Pool (VM's) are held open for debugging)")
    @option("hp-config", default="$hyperparameter-search.hp-config", type=str, help="the path of the hyperparameter config file")
    @flag("jupyter-monitor", help="when True, a Jupyter notebook is created to monitor the run")
    @option("locations", type="str_list", default=DEFAULT_FROM_COMPUTE, help="specifies the region(s) in which to run the job")
    @hidden("log", default="$logging.log", help="specifes if run-related events should be logged")
    @flag("log-file-uploads", default="$after-files.log-file-uploads", help="if set, log each AFTER file/size before uploading")
    @hidden("log-reports", default="$logging.log-reports", help="specifies if various systems reports should be included in setup log")
    @option("low-pri", type=bool, default=DEFAULT_FROM_COMPUTE, help="when true, use low-priority (preemptable) nodes for this job")
    @option("max-passes", default="$hyperparameter-search.max-passes", type=int, help="used to limit number of passes over hyperparameters in hp search")
    @option("max-node-duration", default="$general.max-node-duration", type=str, help="the maximum time that the node can execute before being terminated")
    @option("max-run-duration", default="$general.max-run-duration", type=str, help="the maximum time that a run can execute before being terminated")
    @option("max-minutes", default="$hyperparameter-search.max-minutes", type=int, help="the maximum number of minutes the run can execute before being terminated")
    @hidden("max-seconds", type=int, default="$aml-options.max-seconds", help="the maximum number of seconds this run will execute before being terminated")
    @option("max-run-delay", default="$database.max-run-delay", type=float, help="the maximum random delay applied to each run in the job")
    @option("max-runs", default="$hyperparameter-search.max-runs", type=int, help="the total number of runs across all nodes (for hyperparameter searches)")
    @option("max-workers", type=int, default="$general.max-run-workers", help="the max number of background workers to use during run command")
    @hidden("maximize-metric", default="$general.maximize-metric", help="whether to minimize or maximize value of primary metric")
    @hidden("merge-batch-logs", type=int, default="$logging.merge-batch-logs", help="replaces STDOUT.txt and STDERR.txt with STDBOTH.txt")
    @hidden("mirror-dest", default="$mirroring.mirror-dest", help="the location where mirrored information is stored (none, storage, grok)")
    @hidden("mirror-files", default="$mirroring.mirror-files", help="the wildcard path that specifies files to be mirrored")
    @hidden("mirror-log-files", default="$mirroring.mirror-log-files", help="when true, the job's log file directory is mirrored")
    @option("model-action", default="$model.model-action",  values=["none", "download", "mount"], help="the model action to take on the target, before run is started")
    @hidden("model-local", default="$model.model-local", help="the path on the local machine specifying where the model for this job resides")
    @hidden("model-share-path", default="$model.model-share-path", help="the model share name for the model")
    @flag("model-writable", default="$model.model-writable", help="when true, a mounted model path can be written to")
    @option("monitor", default="$general.monitor", values=["new", "bg", "same", "none"], help="how to monitor primary run of the new job")
    @hidden("mount-retry_count", type=int, default="$mounting.mount-retry-count", help="the number of times to retry each blobfuse mount command")
    @hidden("mount-retry_interval", type=str, default="$mounting.mount-retry-interval", help="the time to sleep between retries of blobfuse mount command")
    @flag("multi-commands"   , help="the script file contains multiple run commands (one per line)")
    @option("node-delay", type=str, default="$general.node-delay", help="maximum time to randomly delay start of node execution")
    @hidden("node-script-path", type=str, default="$code.node-script-path", help="relative path to script on computing node")
    @option("nodes", type=int, help="the number of normal (non-preemptable) nodes to allocte for this run")
    @option("notify", type="str_list", help="the list of users to notify for notifications generated by this job")
    @option("nowrap", type=bool, help="when true, don't generate a wrapper script for XT setup; run user script directly")
    @option("num-dgd-seeds", type=int, default="$hyperparameter-search.num-dgd-seeds", help="the number of random HP configurations used to initialize the DGD search")
    @hidden("option-prefix", default="$hyperparameter-search.option-prefix", help="the prefix to be used for specifying hyperparameter options to the script")
    @option("parent-script", type=str, help="path of script used to initialize the target for repeated runs of primary script")
    @hidden("pip-freeze", default="$logging.pip-freeze", help="when true, installed pip packges are included in the setup log")
    @hidden("primary-metric", default="$general.primary-metric", help="the name of the metric to use for hyperparameter searching")
    @option("python-version", type=str, help="the python version passed to AML/ITP/Singularity for pip and conda operations")
    @option("queue", type=str, help="the name of the Philly queue to use when submitting this job")
    @hidden("remote-control", default="$general.remote-control", help="specifies if XT controller will listen for XT client commands")
    @hidden("report-rollup", default="$run-reports.report-rollup", help="whether to rollup metrics by primary metric or just use last reported metric set")
    @flag("request", help="instead of submitting this job directly, create a request to have it submitted by a team member with approval authority")
    @option("resume-name", help="when resuming a run, this names the previous run")
    @option("resume-node", help="specifies the job_id/node_index to be resumed; this is an internal option")
    @option("runs", default=None, type=int, help="the total number of runs across all nodes (for hyperparameter searches)")
    @option("runs-per-set", default="$hyperparameter-search.runs-per-set", type=int, help="how many runs to do for each CCD hp set explored")
    @option("schedule", default="$general.schedule", values=["static", "dynamic"], help="specifies if runs are pre-assigned to each node or allocate on demand")
    @option("search-type", values=["random", "grid", "bayesian", "dgd", "ccd"], default="$hyperparameter-search.search-type", help="the type of hyperparameter search to perform")
    @option("seed", type=int, default=None, help="the random number seed that can be used for reproducible HP searches")
    @option("service", type=str, default=DEFAULT_FROM_COMPUTE, help="the name of the xt config-specified compute service to use for this job")
    @option("setup", type=str, help="the name of the setup entry to use with the target (from one of the entries in the config file [setups] section")
    @option("sku", default=DEFAULT_FROM_COMPUTE, type=str, help="the name of the Philly SKU to be used (e.g, 'G1')")
    @option("sla", type=str, default=DEFAULT_FROM_COMPUTE, values=["premium", "standard", "basic"], help="the level of anti-preemption service for the job (Singularity)")
    @hidden("slack-factor", default="$early-stopping.slack-factor", type=float, help="(bandit only) specified as a ratio, the delta between this eval and the best performing eval")
    @hidden("slack-amount", default="$early-stopping.slack-amount", type=float, help="(bandit only) specified as an amount, the delta between this eval and the best performing eval")
    @option("sleep-on-exit", type=str, default="0", help="the amount of time to sleep (e.g., '45m'), before controller exits it's process")
    @flag("snapshot-dirs", default="$logging.snapshot-dirs", help="when True, the node script logs contents of various directories during execution")
    @flag("static-search",  default="$hyperparameter-search.static-search", help="if true, hyperparameter searches are performed at job submit time, when possible")
    @hidden("storage", default=None, type=str, help="name of storage service to be used for this run")
    @option("submit-logs", default=None, help="specifies a directory to which log files for the submit are saved")
    @option("tags", default=None, type="tag_list", help="tags to be applied to the job, nodes, and runs")
    @option("target", default=None, type=str, help="one of the user-defined compute targets on which to run")
    @hidden("truncation-percentage", default="$early-stopping.truncation-percentage", type=float, help="(truncation only) percent of runs to cancel at each eval interval")
    @option("use-gpu", type=bool, default="$aml-options.use-gpu", help="when True, the gpu(s) on the nodes will be used by the run")
    @option("username", default="$general.username", help="the username to log as the author of this run")
    # @hidden("user-managed", type=bool, default="$aml-options.user-managed", help="if true, it implies that the local machine or VM will be managed by the user")
    @option("vc", help="the name of the Philly virtual cluster to be used")
    @option("vm-size", type=str, default=DEFAULT_FROM_COMPUTE, help="the type of Azure VM computer to run on")
    @hidden("working-dir", default="$code.working-dir", type=str, help="the run's working directory, relative to the code directory")
    @option("workspace", default="$general.workspace", type=str, help="the workspace to create and manage the run")
    @flag("xtlib-upload", default="$code.xtlib-upload", help="when True, local source code for xtlib is included in the source code snapshot ")
    
    @example(task="run the script miniMnist.py", text="xt run miniMnist.py")
    @example(task="run the linux command 'sleep3d' on singularity", text="xt run --target=singularity --code-upload=0 sleep 3d")
    @command(options_before_args=True, keyword_optional=False, pass_by_args=True, help="submits a script or executable file for running on the specified compute target")
    def run(self, args):
        '''
        The run command is used to run a program, python script, batch file, or shell script on 
        one of following compute services:

        - local (the local machine)
        - pool (a specified set of computers managed by the user)
        - Azure Batch
        - Azure ML
        - Singularity
        '''
        #console.diag("run_cmd")

        target = args["target"]
        storage = args["storage"]
        nowrap = args["nowrap"]

        if nowrap:
            # this debug option doesn't use merged logs
            args["merge_batch_logs"] = False

        if not target:
            ss_info = self.config.get_store_info()
            target = utils.safe_value(ss_info, "target")
            args["target"] = target

        if not storage:
            ss_info = self.config.get_store_info()
            storage = utils.safe_value(ss_info, "storage")
            args["storage"] = storage

        # add xt cmd to args
        cmd = get_dispatch_cmd()
        args["xt_cmd"] = "xt " + cmd if cmd else ""
        args["uami_id"] = None

        # backdoor way to set database options from a command
        fake_error_percent = args["fake_error_percent"]
        if fake_error_percent:
            self.config.data["database"]["fake-error-percent"] = fake_error_percent

        with tempfile.TemporaryDirectory(prefix="import-") as temp_dir:
            runner = Runner(self.config, self.core, temp_dir)
            result = runner.process_run_command(args)

        if result:
            cmds, run_specs, using_hp, using_aml_hparam, sweeps_text, pool_info, job_id = result

            monitor = args["monitor"]
            escape = args["escape"]
            workspace = args["workspace"]

            if monitor == "same":
                self.monitor(name=job_id, workspace=workspace, escape=escape)

            elif monitor in ["bg", "new"]:
                cmd = "xt --echo monitor {} ".format(job_id)
                noactivate = (monitor=="bg")
                process_utils.run_cmd_in_new_console(cmd, noactivate=noactivate)

