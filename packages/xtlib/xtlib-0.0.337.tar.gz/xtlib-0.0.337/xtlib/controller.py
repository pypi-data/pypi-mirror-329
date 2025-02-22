#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# controller.py - running on the compute box, controls the management of all XT or XTLib initiated jobs for that machine.
import os
import sys
import json
import rpyc
import copy
import time
import psutil
import logging
import datetime
import traceback
import threading
import subprocess
import numpy as np

from threading import Thread, Lock
from signal import signal, SIGTERM, SIGINT
from rpyc.utils.server import ThreadedServer
from rpyc.utils.authenticators import SSLAuthenticator

# xtlib 
from xtlib import cmd_utils
from xtlib import store_utils
from xtlib import time_utils
from xtlib.helpers.bag import Bag
from xtlib.console import console
from xtlib.run_info import RunInfo
from xtlib.helpers import file_helper
from xtlib import network_utils
from xtlib.node_creds import NodeCreds
from xtlib.mirror_worker import MirrorWorker
from xtlib.node_usage_logger import NodeUsageLogger
from xtlib.event_processor import EventProcessor
from xtlib.storage.store import store_from_context
from xtlib.hparams.hparam_search import HParamSearch
from xtlib.helpers.stream_capture import StreamCapture

from xtlib import utils
from xtlib import errors
from xtlib import capture
from xtlib import pc_utils
from xtlib import scriptor
from xtlib import constants
from xtlib import run_errors
from xtlib import run_helper
from xtlib import file_utils
from xtlib import process_utils
from xtlib import xt_vault
from xtlib.log_helper import LogHelper

logger = logging.getLogger(__name__)
MAX_IDLE_CHECK = 1000

'''
Our controller is implemented as a Service so that client apps (XT and XTLib apps) from the same or different machines 
can connect to it.  Services offered include:
    - start a run  
    - get status of a run
    - enumerate runs on the hosting computer
    - kill a run
    - attach/detach to run's streaming console output
    - run a command on the box
    - copy files to/from box
'''

queue_lock = Lock()            
runs_lock = Lock()            
rundir_lock = Lock()

def read_from_stdout_pipe(stdout_pipe, run_info:RunInfo, controller, stdout_is_text:bool):

    in_traceback = False
    traceback_lines = None
    
    # expand any "~" in path
    try:
        run_name = run_info.run_name
        first_output = True

        while True:
            if stdout_is_text:
                text_msg = stdout_pipe.readline()
            else:
                binary_msg = stdout_pipe.readline()
                text_msg = binary_msg.decode("utf-8")

            if len(text_msg) == 0 or run_info.killing:
                controller.log_title("run ENDED: " + run_name, force_log=True)
                break      # EOF / end of process

            if first_output:
                controller.log_title("run OUTPUT: " + run_name)
                first_output = False

            # remember last exception for error_runs logging
            if text_msg.startswith(constants.TRACEBACK):
                in_traceback = True
                traceback_lines = []
            elif in_traceback:
                traceback_lines.append(text_msg.strip())
                if not text_msg.startswith(" "):
                    run_info.last_run_exception = text_msg
                    in_traceback = False    

            run_info.process_run_output(text_msg)

            run_info.check_for_time_exceeded()

        # run post-processing
        controller.exit_handler(run_info, called_from_thread_watcher=True, 
            traceback_lines=traceback_lines)

        # remove the store instance for this watcher thread
        controller.remove_store()

    except BaseException as ex:

        logger.exception("Error in controller.read_from_stdout_pipe, ex={}".format(ex))
        console.print("** Exception during read_from_stdout_pipe(): ex={}".format(ex))

        # for debugging print stack track
        traceback.print_exc()

        # log end of controller to JOB
        store = controller.get_store()
        if store:
            try:
                store.log_node_event(run_info.workspace, controller.job_id, controller.node_id, "node_error", 
                    {"node_id": controller.node_id, "run": controller.parent_run_name, "exception": str(ex)})
            except:
                pass

        # give dev a chance to read the error before exiting (if viewing live log)
        console.print("controller sleeping 30 secs before exiting ...")
        time.sleep(30)    

        # shutdown app now
        console.print("controller calling os._exit(1)...")
        os._exit(1)

    # normal exit for watcher thread
    thread = threading.current_thread()
    controller.log_info("normal THREAD EXIT", thread.name)


class XTController(rpyc.Service, LogHelper):

    def __init__(self, concurrent=1, my_ip_addr=None, multi_run_context_fn=None, multi_run_hold_open=False, 
            port=None, is_aml=False, *args, **kwargs):
        
        rpyc.Service.__init__(self, *args, **kwargs)
        LogHelper.__init__(self, "controller")

        self.log_time_msg("starting XTController")

        self.concurrent = concurrent
        self.my_ip_addr = my_ip_addr
        self.multi_run_context_fn = multi_run_context_fn
        self.multi_run_hold_open = multi_run_hold_open
        self.port = port
        self.is_aml = is_aml
        self.restarting = False
        self.restart_delay = None
        self.idle_check_count = 0
        self.ws_name = None
        self.node_restart = False
        self.app_start_str = time_utils.get_arrow_now_str()
        self.event_processor = None
        self.node_heartbeat = None
        self.last_heartbeat_sent = time.time()
        self.start_time = time.time()
        self.force_restart = None
        self.force_restart_enabled = True
        
        node_creds = NodeCreds()              # just done once
        self.credential = node_creds.node_credential   

        self.test_storage(self.credential)
        self.test_sql(self.credential)

        # if previous controller log file exists, remove it
        fn = os.path.expanduser(constants.FN_CONTROLLER_EVENTS)
        if os.path.exists(fn):
            os.remove(fn)

        run_errors_dir = run_errors.clear_run_errors_for_node()        
        self.log_info("clearing run_errors dir", run_errors_dir)
        exists = os.path.exists(run_errors_dir)
        self.log_info("exists(run_errors dir)", exists)

        self.reset_state(start_queue_worker=True)

    # def cleanup_on_error_exit(self):
    #     store = self.get_store()
    #     if store is not None:ssss
    #         sd = {"status": "cancelled"}
    #         store.database.update_job_stats(self.ws_name, self.job_id, sd)

    def test_sql(self, credential):
        import pyodbc, struct
            
        sql_name = "xtsandboxsql2"  # "tpxsql"   # "xtsandboxsql2"

        cs = "Driver={ODBC Driver 17 for SQL Server};Server=tcp:" + sql_name + ".database.windows.net,1433;Database=xt_db;"  + \
            "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

        # convert the new style credential into a token that can be used by pyodbc
        token_bytes = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
        token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
        # print("token_bytes=", token_bytes)
        # print("token_struct=", token_struct)

        SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h
        print("SQL cs:", cs)
        dbx = pyodbc.connect(cs, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})

        # show names of tables in the database
        cmd = "SELECT NAME FROM SYSOBJECTS WHERE xtype = 'U'"
        cursor = dbx.cursor()
        cursor.execute(cmd)

        results = cursor.fetchall()
        print(results)

        print("sql test passed!")

    def test_storage(self, credential):
        from azure.storage.blob import BlobServiceClient   

        print("test_storage")

        # test access to storage account
        storage_url="https://sandboxstoragev2s.blob.core.windows.net"         # tpxstoragev2     # URL of storage account
        container_name = constants.INFO_CONTAINER_V2

        print("  credential: {}".format(credential))
        print("  storage URL: {}".format(storage_url))

        blob_service_client = BlobServiceClient(storage_url, credential=credential)
        container_client = blob_service_client.get_container_client(container_name)

        exists = container_client.exists()
        print("  container exists=", exists)

        blob_client = blob_service_client.get_blob_client(container_name, constants.STORAGE_INFO_FILE)
        exists2 = blob_client.exists()
        print("  blob exists=", exists2)

        if exists and exists2:
            print("storage test PASSED!") 
        else:
            print("storage test FAILED!")

    def reset_state(self, start_queue_worker=False):
        self.killing_process = False
        self.started = time.time()
        self.rundirs = {}
        self.shutdown_requested = None
        self.queue_check_count = 0
        self.runs = {}       # all runs that we know about (queued, spawing, running, or completed)
        self.queue = []      # runs that are waiting to run (due to concurrent)
        self.mirror_workers = []
        self.running_job = None
        self.next_run_list_index = 0
        self.stop_processing_runs = False
        self.total_run_count = 0
        self.store_instances = {}
        self.last_heartbeat_sent = time.time()
        self.restart_list = None
        self.node_logger = None

        self.box_secret = os.getenv("XT_BOX_SECRET")
        self.node_id = os.getenv("XT_NODE_ID")

        self.node_index = utils.node_index(self.node_id)
        # self.state_changed = False

        utils.init_logging(constants.FN_CONTROLLER_EVENTS, logger, "XT Controller")

        is_windows = pc_utils.is_windows()
        
        self.node_script_cwd = os.path.abspath(os.getenv("XT_CWD"))

        # keep everything inside of the CWD folder tree
        self.rundir_parent = "{}/rundirs".format(self.node_script_cwd)     # os.path.abspath(os.getenv("XT_HOMEBASE") + "/.xt/rundirs")

        # for backend services (vs. pool jobs)
        self.job_id = 0
        self.mrc_cmds = None
        self.search_style = None

        fn_inner_log = os.path.expanduser(constants.CONTROLLER_INNER_LOG)
        file_utils.ensure_dir_exists(file=fn_inner_log)

        # capture STDOUT
        self.cap_stdout = StreamCapture(sys.stdout, fn_inner_log, True)
        sys.stdout = self.cap_stdout

        # capture STDERR
        self.cap_stderr = StreamCapture(sys.stderr, True, file=self.cap_stdout.log_file)
        sys.stderr = self.cap_stderr

        self.log_title("XT Controller", double=True)
        self.log_info("build", constants.BUILD)
        self.log_info("date", datetime.datetime.now())
        self.log_info("PATH",  os.getenv("PATH"))

        self.log_info("concurrent", self.concurrent)
        self.log_info("my_ip_addr", self.my_ip_addr)
        self.log_info("multi_run_context_fn", self.multi_run_context_fn)
        self.log_info("multi_run_hold_open", self.multi_run_hold_open)

        conda = os.getenv("CONDA_DEFAULT_ENV")

        file_utils.ensure_dir_exists(self.rundir_parent)

        # NOTE: do NOT add "store" as a class or instance member since it may vary by run/client
        # it should just be created when needed (at beginning and end of a run)

        self.hparam_search = HParamSearch(self.is_aml)

        if self.multi_run_context_fn:
            self.process_multi_run_context(self.multi_run_context_fn)

        self.log_info("port", self.port)
        if self.port:
            self.log_info("xt client msgs", "enabled")
        else:
            self.log_info("xt client msgs", "disabled")

        self.log_info("is_aml", self.is_aml)
        
        self.log_info("PYTHONPATH",  os.getenv("PYTHONPATH"))
        self.log_info("PYTHON version", sys.version)

        self.log_info("workspace",  self.ws_name)

        if not conda:
            self.log_info("CONDA env",  "NOT SET")
        else:
            self.log_info("current CONDA env",  conda)

        self.log_info("node_id", self.node_id)
        self.log_info("node_script cwd", self.node_script_cwd)
        self.log_info("rundirs", self.rundir_parent)

        if start_queue_worker:
            # start a queue manager thread to start jobs as needed
            # NOTE: when running without the rypyc thread, the queue manager thread holds this process open
            queue_worker = Thread(name="queue_worker", target=self.bg_queue_worker)
            #queue_worker.daemon = True          # don't wait for this thread before exiting
            queue_worker.start()
    
    def get_store(self):
        '''
        Ensure we don't share store instances between threads (each thread will use their own dedicated instance)
        '''
        thread_id = threading.get_ident()
        store = None

        if self.mrc_context:
            if not thread_id in self.store_instances:
                # make a new instance of Store for this thread
                self.log_info("creating a new store instance for thread=", thread_id)

                store =  store_from_context(self.mrc_context, self.credential)
                self.store_instances[thread_id] = store
            else:
                store = self.store_instances[thread_id]

        return store

    def remove_store(self):
        '''
        Remove the allocated store instance for the current thread
        '''
        thread_id = threading.get_ident()

        if self.mrc_context:
            if thread_id in self.store_instances:
                self.log_info("removing store instance for thread=", thread_id)
                del self.store_instances[thread_id]
        
    def process_notification_events(self, current_event_when, run_name=None):
        if self.job_events:

            if not self.event_processor:
                # JIT create
                self.event_processor = EventProcessor(self.mrc_context.ws, self.job_id, self.node_index)

            # create store on correct thread
            store =  store_from_context(self.mrc_context, self.credential)
            
            self.event_processor.process_notifications(store, self.mrc_context, current_event_when, run_name)

    def process_multi_run_context(self, multi_run_context_fn):
        # read the cmd and context from the file

        with open(multi_run_context_fn, "rt") as tfile:
            text = tfile.read()

        mrc_data = json.loads(text)

        # NEW mrc data = {"search_style": xxx, "cmds": [], "context_by_nodes": {}
        self.search_style = mrc_data["search_style"]
        self.mrc_cmds = mrc_data["cmds"]
        self.runsets = mrc_data["runsets"]
       
        context_by_nodes = mrc_data["context_by_nodes"]
        dd = context_by_nodes[self.node_id]
        self.job_id = dd["job_id"]

        context_dict = dd["runs"][0]
        context = utils.dict_to_object(context_dict)

        # # report all times in client timezone
        # this call is no longer needed because we set the local timezone in the node script (setup for the node)
        # time_utils.set_local_timezone(context.client_time_zone)
        
        # turn off logging ASAP 
        self.logging_enabled = context.log_controller
        utils.log_info_enabled = context.log_controller

        parent_run_name = context.run_name

        console.add_timestamps = context.add_timestamps

        self.mrc_context = context
        self.node_heartbeat = context.node_heartbeat
        self.ws_name = context.ws
        self.job_id = context.job_id
        self.total_run_count = context.total_run_count
        self.job_events = context.job_events

        self.first_run_index = context.first_run_index
        self.last_run_index = context.last_run_index

        # cache store for later use (don't want storge/db traffic needed for subsequent creations)
        store = self.get_store()
        db = store.database

        if context.node_usage_logging_enabled:
            self.node_logger = NodeUsageLogger(store, self.ws_name, self.job_id, self.node_id, 
                context.node_usage_sample_frequency, context.node_usage_storage_frequency)
            self.node_logger.start()

            # set up a signal handler for flushing the node usage log
            action_dict = {"flush_usage_stats": self.node_logger.flush_samples}
            network_utils.run_msg_reciever_on_bg_thread(action_dict)

        # is this node restarting after a low-priority preemption (or a simulated one)?
        # check the existance of the node.log file for this node 
        node_path = "nodes/{}/node.log".format(self.node_id)
        self.log_info("self.ws_name", self.ws_name)
        self.log_info("self.job_id", self.job_id)
        self.log_info("node_path", node_path)

        # TODO: support node_stats.pull_start_time and node_stats.pull_duration
        pull_start_time_str = os.getenv("XT_PULL_START_TIME", None)
        prep_start_time_str = os.getenv("XT_PREP_START_TIME")

        # TODO: add pull_start_time_str to API to compute PULL_ELAPSED time
        self.node_restart = db.node_start(self.ws_name, self.job_id, node_index=self.node_index, node_restart=False, prep_start_str=prep_start_time_str)
        self.log_info("node_restarted", self.node_restart)

        # for now, always request the restart list (to help debug the restart code)
        self.restart_list = db.get_restart_list(self.ws_name, self.job_id, self.node_index)

        # print the indexes of the restart_list (if any)
        console.print("restart_runs=", self.restart_list)

        if self.node_restart:
            text = self.make_event_text("restarted")
            store.append_job_file(self.ws_name, self.job_id, node_path, text)

        else:
            text = self.make_event_text("started")
            store.append_job_file(self.ws_name, self.job_id, node_path, text)

            assert len(self.restart_list) == 0

        # log NODE_START / NODE_RESTART to job
        start_name = "node_restart" if self.node_restart else "node_start"

        store.log_node_event(self.ws_name, self.job_id, self.node_id, start_name,
            {"node_id": self.node_id, "run": parent_run_name})

        # tell db the first time this job node starts running
        self.log_info("calling job_node_start", self.job_id)
        db.job_node_start(self.ws_name, self.job_id, node_index=self.node_index, is_restart=self.node_restart)

        self.process_notification_events("start_node")

        was_queued = []    # list of runs that were queued before we were restarted

        # queue the single or parent job in context
        context = self.mrc_context
        cmd_parts = context.cmd_parts
        aml_run = False

        # support for scheduling
        self.parent_run_name = parent_run_name
        self.next_child_id = 1
        self.first_run_index = context.first_run_index
        self.last_run_index = context.last_run_index

        self.write_connect_info_to_job(store, self.job_id)
        
        '''
        Some notes on scheduling and restarts:
            - self.restart_list is a list of run indexes that were running on this node when it was restarted
            - self.run_indexes is the list of all runs assigned to this mode (minus the db.completed() runs) 
            - self.run_indexes is only used when sched=static

            - if sched=dynamic, then we need to:
                a. process self.restart_list 
                b. loop: ask db for list of unprocessed runs until it runs out

            - if sched=static, then we need to:
                a. remove any runs in self.restart list from self.run_indexes (prevent them from being run twice)
                a. process self.restart_list
                b. process self.run_indexes
        '''
        # simple scheduling
        if context.schedule != "dynamic":
            self.run_indexes = list(range(context.first_run_index, 1 + context.last_run_index))
            self.log_info("full run_indexes", self.run_indexes)

            if self.node_restart:
                # remove any runs that have completed (don't rely on v1/v2 child run name differences)
                filter_dict = {"ws_name": self.ws_name, "job_id": self.job_id, "node_index": self.node_index, 
                    "end_id": {"$exists": True}}

                store = self.get_store()
                completed_run_docs = store.database.get_info_for_runs(self.ws_name, filter_dict, {"run_index": 1})
                completed_run_indexes = [doc["run_index"] for doc in completed_run_docs]

                if completed_run_indexes:
                    self.run_indexes = list(set(self.run_indexes) - set(completed_run_indexes))

                    self.log_info("NODE RESTART", "removed completed indexes={}".format(completed_run_indexes))
                    self.log_info("new run_indexes", self.run_indexes)

                for restart_run in self.restart_list:
                    # remove corresponding entry in self.run_indexes
                    run_index = restart_run["run_index"]
                    if run_index in self.run_indexes:
                        self.log_info("restart_list: removing entry from run_indexes: {}".format(run_index))
                        self.run_indexes.remove(run_index)
                        self.log_info("new run_indexes", self.run_indexes)

        # mirrow the node-level files requested (usually just the node console log file(s))
        self.start_mirror_workers_for_node(store, context)

        # queue up first job
        self.queue_job_core(context, cmd_parts, aml_run=aml_run)

    def make_event_text(self, event_name, dd={}):
        nd = {"time": time_utils.get_arrow_now_str(), "event": event_name, "data": dd}
        text = json.dumps(nd) + "\n"
        return text

    def write_connect_info_to_job(self, store, job_id):

        if os.getenv("PHILLY_CONTAINER_PORT_RANGE_START"):
            # this is a PHILLY job
            ip = os.getenv("PHILLY_CONTAINER_IP")
            connect_info = {"controller_port": self.port, "ip_addr": ip}

            if store.database:
                store.database.update_connect_info_by_node(self.ws_name, job_id, self.node_id, connect_info)

    def send_heartbeat_if_needed(self):

        if self.node_heartbeat:
            now = time.time()
            elapsed = now - self.last_heartbeat_sent

            if elapsed >= self.node_heartbeat:

                # # send heartbeat to database
                store = self.get_store()
                # nd = {"heartbeat":  now}

                # console.print("** sending heartbeat to database **")
                # NOT YET IMPLEMENTED
                #store.database.send_heartbeat(self.ws_name, self.job_id, self.node_index, self.restart_number)

                self.last_heartbeat_sent = time.time()

    def log_time_msg(self, msg):
        # print date and time formatted nicely
        now = datetime.datetime.now()
        now_str = now.strftime("%Y-%m-%d, @%H:%M:%S")
        console.print("{}: {}".format(now_str, msg), flush=True)
        
    def bg_queue_worker(self):
        '''
        We want any exception here to be logged then force app to exit.
        '''
        self.log_info("bg_queue_worker", "background thread started")

        max_time_checks = 0
        worker_sleep_time = 2
        log_check_freq = 3600/worker_sleep_time    # every hour

        max_dur_text = self.mrc_context.max_node_duration 
        if not max_dur_text and self.mrc_context.max_minutes:
            # use legacy max-minutes
            max_dur_text = "{}m".format(self.mrc_context.max_minutes)

        if max_dur_text:
            max_secs = utils.shell_time_str_to_secs(max_dur_text)
        

        while True:
            # time.sleep(1)
            # self.queue_check(1)

            try:
                # delay between queue checks
                time.sleep(worker_sleep_time)
                self.queue_check(1)
                self.send_heartbeat_if_needed()

            except BaseException as ex:
                logger.exception("Error in controller.thread_manager, ex={}".format(ex))
                console.print("** Exception during queue_check(): ex={}".format(ex))

                # for debugging print stack track
                traceback.print_exc()

                # give dev a chance to read the error before exiting (if viewing live log)
                console.print("sleeping 15 secs before exiting...")
                self.log_time_msg("exiting XTController")
                time.sleep(15)    

                # shutdown app now
                os._exit(1)

            # limit node time to specified value
            if max_dur_text:
                node_elapsed_secs = time.time() - self.started
                exceeded_time = max_secs and (node_elapsed_secs > max_secs)
                                              
                if max_time_checks == 0:
                    console.print("max_node_duration={} translates to max_secs: {:,}".format(max_dur_text, max_secs))

                if exceeded_time or (max_time_checks % log_check_freq == 0):
                    console.print("node_elapsed_secs={:,.0f}, max_secs={:,}".format(node_elapsed_secs, max_secs))

                max_time_checks += 1

                if exceeded_time:

                    suffix = max_dur_text[-1]
                    max_actual_text = utils.secs_to_shell_time(node_elapsed_secs, suffix)
                    console.print("** Error: node's elapsed running times ({}) exceeded max-node-duration ({})".format( \
                        max_actual_text, max_dur_text))

                    # give dev a chance to read the error before exiting (if viewing live log)
                    console.print("sleeping 15 secs before exiting...", flush=True)
                    self.log_time_msg("exiting XTController")
                    time.sleep(15)    

                    # shutdown app now
                    os._exit(1)

               
    def queue_count(self):
        with queue_lock:
            return len(self.queue)

    def on_shutdown(self, context):
        #self.log_title("controller SHUTDOWN")

        if self.node_logger is not None:
            # close node logger & upload logs to storage
            self.node_logger.close()
            self.node_logger = None

        #remove the cert file
        fn_server_cert = os.path.expanduser(constants.FN_SERVER_CERT)
        if os.path.exists(fn_server_cert):
            os.remove(fn_server_cert)

        # stop logging (and free log file for deletion in below code)
        logging.shutdown()        
        store = self.get_store()

        if context:
            node_id = os.getenv("XT_NODE_ID")

            # write XT event log to job store AFTER
            fn = os.path.expanduser(constants.FN_CONTROLLER_EVENTS)
            self.log_info("controller events", fn)   
            self.log_info("exists", os.path.exists(fn))

            if os.path.exists(fn):
                fn_store = "nodes/{}/after/xt_logs/{}".format(node_id, os.path.basename(fn))

                #console.print("starting to upload CONTROLLER log: {} => {}".format(fn, fn_store))
                store.upload_file_to_job(context.ws, context.job_id, fn_store, fn)
                #console.print("finished upload of CONTROLLER log")

        if store:
            if context and context.log_db_stats:
                self.log_title("XT controller: db call stats")
                store.database.print_call_stats()

            # log end of controller to JOB
            store.log_node_event(self.ws_name, self.job_id, self.node_id, 
                "node_end", {"node_id": self.node_id, "run": self.parent_run_name})

        self.log_time_msg("exiting XTController")
        time.sleep(2)    # wait for 2 secs for any bg thread cleanup

        console.print("controller calling os._exit(0)...")

        # os._exit will exit all threads without running 'finally' blocks 
        # sys.exit will exit current thread only, but run 'finally' blocks for a cleaner exit
        os._exit(0)

    def on_idle(self):

        self.log_title("controller IDLE detected")

        if self.restarting:
            # simulate some time passing
            time.sleep(self.restart_delay)

            # reset controller's state and start processing the MRC file again
            self.reset_state()
            self.restarting = False
        else:
            # prepare to shut down
            context = None

            if self.runs:
                first_run = list(self.runs.values())[0]
                context = first_run.context

                job_id = self.running_job
                if job_id:
                    self.running_job = None

            store = self.get_store()
            job_id = self.job_id
            ws_id = self.ws_name
        
            # tell db this job node is exiting
            console.diag("calling db job_node_exit: job_id={}".format(job_id))

            # always call job_node_exit() and node_end() before exiting
            db = store.get_database()
            if db:
                db_retries, storage_retries = run_errors.count_node_errors()

                # log stats for job
                job_completed = db.job_node_exit(ws_id, job_id)

                # log stats for node 
                self.log_info("NODE db_retries", db_retries)
                self.log_info("NODE storage_retries", storage_retries)

                db.node_end(ws_id, job_id, self.node_index, db_retries, 
                    storage_retries, self.app_start_str)

                self.process_notification_events("end_node")

                if job_completed:
                    self.process_notification_events("end_job")

            else:
                context = None

            # is it time to shut down the controller?
            #if self.multi_run_context_fn and not self.multi_run_hold_open:
            if self.shutdown_requested or (self.multi_run_context_fn and not self.multi_run_hold_open):
                self.on_shutdown(context)

    def queue_check(self, max_starts=1):
        ''' see if 1 or more jobs at top of queue can be run '''

        # active_count = self.get_active_runs_count()
        # if active_count == 0:
        #     self.on_idle()

        # for responsiveness, limit # of runs can be released in a single check
        for _ in range(max_starts):       
            running_count = len(self.get_running_names())

            if not self.process_top_of_queue(running_count):
                break

        # AFTER potentially starting a run, see if we are idle
        self.idle_check()

    def idle_check(self):

        alive = self.get_alive_names()
        alive_count = len(alive)

        if self.force_restart:
            elapsed = time.time() - self.start_time
            #self.log_info("force_restart elapsed=", elapsed)
            
            if elapsed > self.force_restart:
                self.log_title("controller FORCE RESTART triggered!")
                self.force_restart = None   # only trigger this once
                self.force_restart_enabled = False
                self.restart_controller()

        if alive_count == 0:
            self.idle_check_count += 1
            self.log_info("idle_check", self.idle_check_count)

            with runs_lock:
                not_wrapped_up = [ri.run_name for ri in self.runs.values() if not ri.is_wrapped_up]
                wrapping_count = len(not_wrapped_up)

            #print("queue_check: running_count={}, names={}".format(running_count, names))
            if self.idle_check_count > MAX_IDLE_CHECK:
                console.print("idle_check: exceeded MAX_IDLE_CHECK={} checks, aborting controller".format(MAX_IDLE_CHECK))
                self.on_idle()
            elif wrapping_count:
                watch_threads = []
                #print("\nrunning threads:")
                for thread in threading.enumerate(): 
                    #print(" ", thread.name)
                    if thread.name.startswith("watcher_"):
                        watch_threads.append(thread)
                #print()

                self.log_info("waiting for wrap up", not_wrapped_up)
                self.log_info("watch_threads", watch_threads)

                if wrapping_count != len(watch_threads):
                    print("ERROR: COUNT MISMATCH between runs being wrapped up and watch_threads")
            else:
                self.log_info("idle_check", "ALL RUNS are wrapped up")
                self.on_idle()
        else:
            self.idle_check_count = 0

    def is_run_ready(self, rix):
        ready = False
        out_of_runs = (self.next_run_list_index > self.last_run_index)

        if not out_of_runs and rix.max_delay:
            if rix.delay_started:
                elapsed = time.time() - rix.delay_started
                if elapsed > rix.run_delay:
                    ready = True
                    self.log_info("run is now STARTING", rix.run_name)
            else:
                rix.run_delay = rix.max_delay * np.random.random()
                rix.delay_started = time.time()
                self.log_info("delaying {}".format(rix.run_name), "for {:.2f} secs".format(rix.run_delay))
        else:
            self.log_info("run is READY", rix.run_name)
            self.log_info("out_of_runs", out_of_runs)
            ready = True

        return ready

    def process_top_of_queue(self, running_count):
        processed_entry = False
        run_info = None

        with queue_lock:
            if len(self.queue):
                if running_count < self.concurrent or self.concurrent == -1:
                    if self.is_run_ready(self.queue[0]):

                        run_info = self.queue.pop(0)

                        # run_info is ready to run!
                        if run_info.run_as_parent and not run_info.parent_prep_needed:
                            run_info.status = "spawning"
                        else:
                            run_info.status = "running"
                            run_info.started = time.time()

        if run_info:
            # got a run from the queue that is ready to run (or spawn a child)
            self.process_queue_entry(run_info)
            processed_entry = True

        return processed_entry

    def process_queue_entry(self, run_info):
        self.log_info("process_queue_entry: run_info:", run_info)

        if run_info.parent_prep_needed:

            # run PARENT PREP script 
            self.start_local_run(run_info, cmd_parts=[])

        elif run_info.run_as_parent:
            
            # should parent spawn new child?
            context = run_info.context
            store = self.get_store()

            # get index of next run for our node storage
            #console.print("self.next_run_list_index=", self.next_run_list_index)

            if self.stop_processing_runs:
                entry = None

            elif self.restart_list:
                restart_run = self.restart_list.pop(0)
                console.print("** restarting run: {} **".format(restart_run))

                run_index = restart_run["run_index"]
                entry = {"status": "restart", "run_index": run_index, "source": "restart_list"}

            elif context.schedule == "dynamic":
                #  runs are dynamically created on each node (not a fixed count)
                # let database allocate next job-level run_index
                run_index =  store.database.get_next_run_index(context.ws, context.job_id)
                entry = {"status": "unstarted", "run_index": run_index, "source": "dynamic"}

                if self.total_run_count and run_index >= self.total_run_count:
                    # all runs completed; tell controller to exit
                    self.log_info("all runs completed for parent", run_info.run_name)
                    entry = None

            elif self.next_run_list_index < len(self.run_indexes):
                # schedule=static (runs are pre-allocated to each node)
                run_index = self.run_indexes[self.next_run_list_index]
                self.next_run_list_index += 1
                entry = {"status": "unstarted", "run_index": run_index, "source": "static"}

            else:
                entry = None

            self.log_info("entry",  entry)

            # log run index to JOB
            store.log_node_event(self.ws_name, self.job_id, self.node_id, 
                "get_index", {"node_id": self.node_id, "entry": entry})

            if entry:
                run_index = entry["run_index"]

                if context.search_type == "ccd":
                    if context.total_run_count is None:
                        limit = "unlimited"
                    else:
                        limit = context.total_run_count-1
                else:
                    limit = context.total_run_count-1

                self.log_info("==> running INDEX", "{}/{}".format(run_index, limit))

                # yes: CREATE CHILD
                self.run_template(run_info, run_index, entry)

                # insert back into queue
                with queue_lock:
                    run_info.delay_started = None
                    self.queue.append(run_info)
                    run_info.status = "queued"
            else:

                # no: parent has completed
                self.log_info("marking PARENT completed", run_info.run_name)

                with run_info.lock:
                    run_info.status = "completed"

                    # process end of parent run
                    #run_info.run_wrapup()
                    self.exit_handler(run_info, True, called_from_thread_watcher=False)

        else:
            # start NORMAL RUN
            self.start_local_run(run_info, cmd_parts=run_info.cmd_parts)

    def add_to_runs(self, run_info):
        key = run_info.workspace + "/" + run_info.run_name
        with runs_lock:
            self.runs[key] = run_info

    def run_template(self, parent_ri:RunInfo, run_index:int, entry:dict):
        parent_run_name = parent_ri.run_name

        # ensure PARENT run has a rundir (so it can log its own output)
        if not parent_ri.rundir:
            rundir, rundir_index = self.allocate_rundir(parent_run_name)
            parent_ri.rundir = rundir

            # assign a console output file to the PARENT
            console_fn = rundir + "/service_logs/stdboth.txt"
            parent_ri.set_console_fn(console_fn)

        # create a parent log event for "spawning"
        context = parent_ri.context
        store = self.get_store()
        store.log_run_event(context.ws, parent_run_name, "status-change", {"status": "spawning"}, job_id=self.job_id)  

        # spawn child run from template
        child_info, prev_run_name = self.spawn_child(parent_ri, run_index, entry)
        if child_info:

            # add to runs
            self.add_to_runs(child_info)

            # start normal run of CHILD
            self.start_local_run(child_info, cmd_parts=child_info.cmd_parts)

            if parent_ri.status == "queued":
                # create a parent log event for "spawing"
                store.log_run_event(context.ws, parent_run_name, "status-change", {"status": "queued"})  

            if prev_run_name:
                # mark our previous instance as ended with status="restarted"
                self.log_info("marking prev_run as restarted", prev_run_name)    

                store.database.run_exit(self.ws_name, prev_run_name, "restarted", -1, db_retries=None, storage_retries=None, 
                    start_time=None, error_msg=None)
        else:
            self.stop_processing_runs = True
            
    def requeue_run(self, run_info):
        with queue_lock:
            self.queue.append(run_info)
            run_info.status = "queued"

        self.log_info("run requeued", run_info.run_name)

    def schedule_controller_exit(self):
        if self.multi_run_hold_open:
            self.log_info("holding controller open", "after single run...")
        else:
            self.log_info("xt controller", "scheduling shutdown...")
            self.shutdown_requested = True

    def get_cmdline_args(self, cmd_parts, option_prefix):
        arg_dict = {}
        pending_name = None
        #print("CONTROLLER: cmd_parts=", cmd_parts)

        for part in cmd_parts:
            if option_prefix and part.startswith(option_prefix):
                # start of new option being specified

                if pending_name:
                    # assume previous option name is a flag
                    arg_dict[pending_name] = 1
                    pending_name = None

                part = part[len(option_prefix):]
                pending_name = None

                if "=" in part:
                    name, value = part.split("=", 1)
                    arg_dict[name] = value
                else:
                    # name specified but not value
                    pending_name = part

            elif pending_name:
                # found value for pending name
                arg_dict[pending_name] = part
                pending_name = None

        if pending_name:
            # assume previous option name is a flag
            arg_dict[pending_name] = 1
        
        return arg_dict

    def spawn_child(self, parent, run_index, entry):
        spawn_start = time.time()

        # create a CLONE of template as a child run
        start_child_start = time.time()

        # create a child run_info from the parent template
        context = copy.copy(parent.context)
        context.repeat = None
        context.is_parent = False

        # find cmd to use for this child run
        cmd_index = run_index % len(self.mrc_cmds)

        cmd = self.mrc_cmds[cmd_index]
        self.log_info("run_index: " + str(run_index), "cmd: {}".format(cmd))

        # update context with new cmd
        context.cmd_parts = cmd_utils.user_cmd_split(cmd)    

        store = self.get_store()

        self.log_info("spawn_child, parent", parent.run_name)
        self.log_info("child run_index", run_index)

        prev_name = None

        if context.search_style == "dynamic":
            # perform dynamic HPARAM search
            run_index_name = "run_index_" + str(run_index)
            self.log_info("doing dynamic HPARAM search for child", run_index_name)
    
            arg_dict = self.hparam_search.process_child_hparams(run_index_name, store, context, parent)
            if arg_dict:
                # now its safe to create the child name
                child_name, prev_name = store.database.create_child_name(self.ws_name, self.job_id, self.node_index, 
                    entry, self.parent_run_name)
                
                self.log_info("created dynamic sched child", child_name)
                self.log_info("prev_name", prev_name)

                cmd_parts = self.hparam_search.apply_runset(arg_dict, context.cmd_parts, context, store, child_name)
            else:
                # we should stop processing runs now
                cmd_parts = None

            hp_set = str(arg_dict)
        else:
            child_name, prev_name = store.database.create_child_name(self.ws_name, self.job_id, self.node_index,
                entry, self.parent_run_name, context.rename_restarts)

            self.log_info("created static sched child", child_name)
            self.log_info("prev_name", prev_name)

            if self.runsets:
                # select a runset and apply to run
                actual_ri = run_index % len(self.runsets)
                self.log_info("getting runset for child=" + child_name, "index=" + str(actual_ri))

                runset = self.runsets[actual_ri]
                self.log_info("runset for child", runset)

                cmd_parts = list(context.cmd_parts)
                cmd_parts = self.hparam_search.apply_runset(runset, cmd_parts, context, store, child_name)
                self.log_info("runset applied to cmd_parts", cmd_parts)

                hp_set = str(runset)
            else:
                # select the normal command for the run
                self.log_info("normal child without HPARAM search", child_name)
                cmd_parts = context.cmd_parts
                hp_dict = self.get_cmdline_args(cmd_parts, context.option_prefix)
                hp_set = str(hp_dict)

        if cmd_parts:
            # HP search succeeded
            # the logged value of search_type reflects if it was really used
            if context.search_style in ["dynamic", "static"]:
                search_type = context.search_type
            else:
                search_type = None

            # expand display_name for child runs
            display_name = utils.expand_xt_vars(context.display_name, node_index=self.node_index, 
                job_id=self.job_id, run_id=child_name)

            print("expanded child display_name from: '{}' to '{}'".format(context.display_name, display_name))

            store.start_child_run(context.ws, parent.run_name, context.exper_name,
                child_name=child_name, 
                box_name=context.box_name, app_name=context.app_name, path=context.target_file,
                from_ip=context.from_ip, from_host=context.from_host, sku=context.sku,
                job_id=context.job_id, pool=context.pool, node_index=self.node_index, 
                aggregate_dest=context.aggregate_dest,  
                compute=context.compute, service_type=context.service_type, username=context.username, 
                search_type=search_type, run_index=run_index, hp_set=hp_set, display_name=display_name, 
                cmd_line_args=str(cmd_parts), xt_cmd=context.xt_cmd)

            # must update context info
            context.run_name = child_name
            context.node_index = self.node_index

            # log run CMD
            store = self.get_store()
            store.log_run_event(context.ws, child_name, "cmd", {"cmd": cmd_parts, "xt_cmd": context.xt_cmd}, job_id=context.job_id)  

            # for now, don't log context (contain private credentials and not clear if we really need it)
            # for CHILD runs, record all "context" (from cmd line, user config, default config) in log (for audit/re-run purposes)
            #store.log_run_event(context.ws, child_name, "context", context.__dict__)

            child_info = RunInfo(child_name, context.ws, cmd_parts, context.run_script, 
                None, context, "running", True, parent_name=parent.run_name, mirror_close_func = self.stop_mirror_worker, 
                node_id=self.node_id, run_index=run_index, store=store, is_parent=False, log_info=self.log_info)

            parent.process_run_output("spawned: {}\n".format(child_name))
        else:
            child_info = None

        return child_info, prev_name
 
    def print_elapsed(self, started, title):
        elapsed = time.time() - started
        self.log_info(title, "{:.2f} secs".format(elapsed))
        
    def exit_handler(self, run_info, run_info_is_locked=False, 
        called_from_thread_watcher=False, traceback_lines=None):
        ''' be conservative here - don't assume we have even started the process.
        '''
        self.log_time_msg("ended USER SCRIPT: " + run_info.run_name)

        self.log_info("exit_handler", run_info.run_name)
        store = self.get_store()

        if not run_info.process_was_created:
            # run died during launch (likely due to Azure/dbDB errors)
            if run_info.status == "running":
                run_info.status = "error"
                run_info.exit_code = -2    # died during launch

        if run_info.parent_prep_needed:
            self.log_info("parent prep script", "exited")
            run_info.wrapup_parent_prep_run()
        else:
            if called_from_thread_watcher:
                self.log_info("app exit detected", run_info.run_name)
            else:
                self.log_info("parent app completed", run_info.run_name)

            run_info.run_wrapup()

            # send "app exited" msg to callbacks
            msg = self.log_info_to_text(constants.APP_EXIT_MSG, run_info.status) + "\n"
            run_info.process_run_output(msg, run_info_is_locked)

            # log run end to JOB
            dd = {"node_id": self.node_id, "run": run_info.run_name, "status": run_info.status, 
                "is_parent": run_info.is_parent, "exit_code": run_info.exit_code}

            store.log_node_event(self.ws_name, self.job_id, self.node_id, "end_run", dd)

            self.log_info("run_end logged", run_info.run_name)

        run_info.check_for_completed(True)

        if run_info.exit_code:
            run_errors.record_run_error("fatal", run_info.error_msg, run_info.exit_code, 
                traceback_lines, run_name=run_info.run_name)

        # release rundir
        if run_info.rundir:
            self.return_rundir(run_info.rundir)
            run_info.rundir = None

        if run_info.parent_prep_needed:
            run_info.parent_prep_needed = False

            self.log_info("run={}".format(run_info.run_name), "status={}".format(run_info.status))

            if run_info.status == "completed":
                # now that the parent prep script has successfully run we can 
                # requeue parent run to spawn child runs
                self.requeue_run(run_info)
        else:
            run_info.is_wrapped_up = True

        context = run_info.context

        if run_info.parent_name and context.search_style == "dynamic":
            stop_controller = self.hparam_search.process_end_of_run(store, context)

            if stop_controller:
                self.stop_processing_runs = True

        self.process_notification_events("end_run", run_info.run_name)

        self.log_info("end of", "exit handler")

    def on_connect(self, conn):
        # code that runs when a connection is created
        # (to init the service, if needed)
        #console.print("client attach!")
        pass

    def on_disconnect(self, conn):
        # code that runs after the connection has already closed
        # (to finalize the service, if needed)
        #console.print("client detach!")
        pass


    def fix_path(self, path):
        path = os.path.expanduser(path)

        if pc_utils.is_windows():
            console.print("FIXING UP path for WINDOWS: {}".format(path))

            path = path.replace("$HOME", "%USERPROFILE%")
            path = path.replace("/", "\\")

        return path

    def find_file_in_path(self, name):
        path_list = os.getenv('PATH', '')
        #console.print("path_list=", path_list)

        if pc_utils.is_windows():
            paths = path_list.split(";")
        else:
            paths = path_list.split(":")

        full_fn = None

        for path in paths:
            fn = path + "/" + name
            #console.print("testing fn=", fn)

            if os.path.exists(fn):
                full_fn = fn
                #console.print("match found: fn=", full_fn)
                break
        
        return full_fn

    def is_process_running(self, name):
        name = name.lower()
        found = False

        for process in psutil.process_iter():

            # this is the only allowed exception catching in controller process
            try:
                if name in process.name().lower():
                    found = True
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # ignore known OS exceptions while iterating processes
                pass

        return found

    def validate_request(self, request_token):
        #print("token={}, box_secret={}".format(request_token, self.box_secret))
        
        if request_token != self.box_secret:
            print("*** tokens do not match - validation failed ***")
            errors.service_error("Access denied")
        #print("request validated")

    def exposed_queue_user_request(self, token, request):
        self.validate_request(token)
        fn = os.path.expanduser(constants.FN_USER_REQUEST)

        with open(fn, "at") as outfile:
            outfile.write(request + "\n")

    def exposed_get_tensorboard_status(self, token):
        self.validate_request(token)

        running = self.is_process_running("tensorboard")
        status = {"running": running}
        return status

    def exposed_elapsed_time(self, token):
        self.validate_request(token)
        return time.time() - self.started

    def exposed_xt_version(self, token):
        self.validate_request(token)
        return constants.BUILD

    def exposed_controller_log(self, token):
        self.validate_request(token)
        fn = os.path.expanduser(constants.CONTROLLER_INNER_LOG)
        with open(fn, "r") as textfile:
            text = textfile.read()
        return text

    def copy_bag(self, bag):
        new_bag = Bag()
        for key,value in bag.get_dict().items():
            setattr(new_bag, key, value)

        return new_bag

    def copy_dict(self, dict):
        new_dict = {}
        for key,value in dict.items():
            new_dict[key] = value

        return new_dict

    def allocate_rundir(self, run_name, allow_retry=True):
        rundir = None
        base_name = "rundir"

        with rundir_lock:
            for dirname, rn in self.rundirs.items():
                if not rn:
                    # it's available - mark it as in-use
                    self.rundirs[dirname] = run_name
                    rundir = dirname
                    break

            if not rundir:
                # add a new name
                rundir = base_name + str(1 + len(self.rundirs))
                self.rundirs[rundir] = run_name
                self.log_info("new rundir", rundir)

            self.log_info("updated rundirs", self.rundirs)

        start = len(base_name)
        rundir_index = int(rundir[start:])
        runpath = self.rundir_parent + "/" + rundir

        # remove and recreate for a clear start for each run
        try:
            file_utils.ensure_dir_clean(runpath)
        except Exception as ex:    #  AccessDenied:
            print("Exception deleting rundir, ex=", ex)
            if allow_retry:
                #time.sleep(10)    # experiment; see if wating 10 secs helps 
                #file_utils.ensure_dir_clean(runpath)

                # try just once more (a different directory)
                self.allocate_rundir(run_name, allow_retry=False)
            else:
                raise ex

        return runpath, rundir_index

    def return_rundir(self, rundir_path):
        rundir = os.path.basename(rundir_path)

        with rundir_lock:
            # we check because "restart controller" will try to return rundirs from before restart
            if rundir in self.rundirs:
                # mark as no longer used
                self.rundirs[rundir] = None

    def exposed_queue_job(self, token, json_context, cmd_parts):
        self.validate_request(token)

        context = json.loads(json_context)
        context = utils.dict_to_object(context)

        # make a copy of cmd_parts
        cmd_parts = list(cmd_parts)
        context.cmd_parts = cmd_parts
        
        run_info = self.queue_job_core(context, cmd_parts)
        return True, run_info.status

    def queue_job_core(self, context, cmd_parts, previously_queue=False, aml_run=None):

        run_name = context.run_name
        exper_name = context.exper_name

        self.log_title("QUEUING run: {}".format(run_name))
        store = self.get_store()

        app_name = context.app_name
        run_script = context.run_script
        self.log_info("context.run_script", run_script)

        parent_script = context.parent_script
        parent_prep_needed = context.is_parent and parent_script
        if parent_prep_needed:
            self.log_info("parent_script=", parent_script)
            run_script = parent_script

        # apply concurrent of run when it is queued
        if context.concurrent is not None:
            self.concurrent = context.concurrent
            self.log_info("set concurrent", self.concurrent)

        is_parent = context.is_parent      # or context.repeat is not None
        print("context.job_id=", context.job_id)
        print("context.repeat=", context.repeat)
        print("is_parent=", is_parent)

        run_info = RunInfo(run_name, context.ws, cmd_parts, run_script, context.repeat, context, "queued", True, 
            parent_name=None, parent_prep_needed=parent_prep_needed, mirror_close_func = self.stop_mirror_worker, 
            node_id=self.node_id, run_index=None, store=store, max_delay=context.max_delay, is_parent=is_parent,
            log_info=self.log_info)

        # mark that parent run is starting
        store.database.run_start(context.ws, run_name)

        # log run QUEUED event 
        store.log_run_event(context.ws, run_name, "queued", {}, job_id=context.job_id) 

        # queue job to be run
        with queue_lock:
            self.queue.append(run_info)
            self.log_info("job queue", "{} entries".format(len(self.queue)))

        self.add_to_runs(run_info)

        self.log_info("run QUEUED", run_name)
        
        # before returning - see if this run can be started immediately
        #self.queue_check(1)

        return run_info 

    def create_default_run_script(self, cmd_parts, activate_cmd):
        ''' create a default run_script for user that specified a cmd.
        '''
        #self.log_info("create run script: cmd_parts", cmd_parts)

        flat_cmd = " ".join(cmd_parts)
        run_script = []
        
        if activate_cmd:
            if pc_utils.is_windows():
                activate_cmd = activate_cmd.replace("$call", "@call")
            else:
                activate_cmd = activate_cmd.replace("$call", "")
            run_script.append(activate_cmd)

        run_script.append(flat_cmd)
        return run_script

    def start_local_run(self, run_info, cmd_parts):
        # wrapper to catch exceptions and clean-up
        # we need to support multiple run directories (for concurrent param) - so we cannot run in originating dir

        run_name = run_info.run_name
        self.log_title("STARTING: {}".format(run_name), force_log=True)

        rundir, run_dir_index = self.allocate_rundir(run_name)
        run_info.rundir = rundir

        self.start_local_run_core(run_info, cmd_parts, rundir, run_dir_index)

    def start_local_run_core(self, child_ri:RunInfo, cmd_parts: list, rundir: str, rundir_index: int):
        '''
        Note: 
            when user did NOT specify a run script:
                - cmd_parts is the "python/docker/exe" run cmd
                - its args have been updated with HP search args for this run
            --> in this case, "wrap" cmd_parts in a default script and just run script without args

            when user DID specify a run script:
                - run script should contain a "%*" cmd to be HP-search enabled
                - cmd_parts, in this case, looks like: train.sh --epochs=3, lr=.3, etc.
            --> in this case, run "cmd_parts" (which will run the RUN SCRIPT with correct args)
        '''
        self.log_info("cmd_parts", cmd_parts)

        context = child_ri.context  
        run_name = child_ri.run_name

        # set run's current dir
        relative_cwd = context.working_dir
        if relative_cwd:
            user_script_cwd = rundir + "/" + relative_cwd
        else:
            user_script_cwd = rundir

        # download files from STORE to rundir
        store = self.get_store()
        job_id = context.job_id 

        if self.is_aml:
            # # copy contents of current dir to rundir (Azure ML copied snapshot to this dir)
            # file_utils.zap_dir(rundir)
            # file_utils.copy_tree(".", rundir)

            # write generated sweep text to a file in rundir
            if context.generated_sweep_text:
                fn = rundir + "/" + os.path.basename(context.hp_config)
                self.log_info(fn, "{:.120s}".format(context.generated_sweep_text))

                with open(fn, "wt") as outfile:
                    outfile.write(context.generated_sweep_text)

        # its better to copy user's code files from /.xt/cwd because user may have
        # run some setup commands that added to or modified the files
        side_load_files = True

        if side_load_files:
            # instead of copying code from JOB, we copy from the controller working directory so each run gets
            # the benifit on any parent parent script adjustment to the environment
            omit_list = ["rundirs", "mnt", "blobfusetmp*", "__after__", "__multi_run_context__.json", 
                "__run_controller__.py", "__xt_server_cert__.pem", "__aml_shim__.py", 
                "extract_project.success", "azureml-setup", "azureml-logs", "packages-microsoft-prod.deb", 
                "azureml_compute_logs", "__current_running_entry__.txt", "__t__", 
                constants.FN_BATCH_HELPER, constants.FN_NODE_SCRIPT, constants.FN_INNER_SCRIPT, 
                "logs", "azureml-logs", "azureml-setup"]

            copy_count = capture.make_local_snapshot(".", rundir, ".", omit_list=omit_list) 
            self.log_info("sideloaded", "{} CODE files from controller working dir".format(copy_count))
        else:   
            # code is stored in JOB BEFORE files
            files = capture.download_before_files(store, job_id, context.ws, run_name, dest_dir=rundir, silent=True)
            self.log_info("downloaded", "{} BEFORE files from JOB STORE".format(len(files)))

        if context.snapshot_dirs:
            self.log_title("RUNDIR DIR " + rundir)
            #os.system("ls -lt {} | grep -vh '^total' | head -n 30".format(rundir))
            os.system("ls -l {} | grep -vh '^total'".format(rundir))

        # HP search generated config.yaml is stored in RUN BEFORE files
        files = capture.download_before_files(store, context.job_id, context.ws, run_name, dest_dir=rundir, silent=True, source="run")
        self.log_info("downloaded", "{} BEFORE files from RUN STORE".format(len(files)))

        run_script = child_ri.run_script
        script_args = None

        if run_script:
            # user supplied a RUN SCRIPT and args in cmd_parts
            script_args = cmd_parts
            # must add rundir since our working dir is different
            fn_script = os.path.join(user_script_cwd, cmd_parts[0])
        else:
            # user supplied a run command; wrap it in a default script
            run_script = self.create_default_run_script(cmd_parts, context.activate_cmd)
            script_args = None
            fn_script = None

        exper_name = context.exper_name

        # local function
        def safe_env_value(value):
            return "" if value is None else str(value)
        
        if context.snapshot_dirs and relative_cwd:
            # show the CWD directory that user will run in (ensure needed files are present)
            self.log_title("USER_SCRIPT_CWD DIR " + user_script_cwd)
            os.system("ls -l {} | grep -vh '^total'".format(user_script_cwd))

        # copy env vars from parent environment
        child_env = os.environ.copy()

        if context.force_restart and self.force_restart_enabled:
            self.force_restart = utils.shell_time_str_to_secs(context.force_restart)
            self.log_info("force_restart", self.force_restart)

        # pass xt info to the target app (these are access thru Store "running" API's)cls

        child_env["XT_USERNAME"] = safe_env_value(context.username)
        child_env["XT_CONTROLLER"] = "1"

        child_env["XT_WORKSPACE_NAME"] = safe_env_value(context.ws)
        child_env["XT_EXPERIMENT_NAME"] = safe_env_value(exper_name)
        child_env["XT_RUN_NAME"] = safe_env_value(run_name)
        child_env["XT_JOB_ID"] = safe_env_value(job_id)
        child_env["XT_IS_RUN"] = "1"

        child_env["XT_TARGET_FILE"] = safe_env_value(context.target_file)
        child_env["XT_RESUME_NAME"] = safe_env_value(context.resume_name)
        child_env["XT_STORE_CODE_PATH"] = context.store_code_path

        safe_store_creds = dict(context.store_creds)
        if self.credential:
            del safe_store_creds["credential"]
        sc = json.dumps(safe_store_creds)
        child_env["XT_STORE_CREDS"] = utils.text_to_base64(sc)

        safe_db_creds = dict(context.db_creds)
        if self.credential:
            del safe_db_creds["credential"]
        dc = json.dumps(safe_db_creds)
        child_env["XT_DB_CREDS"] = utils.text_to_base64(dc)

        base_run_name = run_helper.get_base_run_name(run_name)
        if base_run_name != run_name:
            # this is a restarted run
            largest_step = store.database.get_largest_run_step(context.ws, run_name)
            child_env["XT_LARGEST_STEP"] = str(largest_step)
            print("setting XT_LARGEST_STEP=", largest_step)

        # update XT_OUTPUT_DIR and XT_OUTPUT_MNT for child run path
        output_path = os.getenv("XT_OUTPUT_DIR")
        self.log_info("parent output path", output_path)
        parent_name = child_ri.parent_name
        self.log_info("parent name", parent_name)

        if output_path and parent_name:
            child_output_path = output_path.replace(parent_name, run_name)
            self.log_info("child XT_OUTPUT_DIR", child_output_path)
        else:
            child_output_path = output_path

        child_env["XT_OUTPUT_DIR"] = child_output_path
        child_env["XT_OUTPUT_MNT"] = child_output_path

        # ensure dir exists and is empty (local machine)
        file_utils.ensure_dir_clean(child_output_path)

        pp = os.getenv("PYTHONPATH")
        self.log_info("PYTHONPATH", pp)
        
        self.log_info("run_script", run_script)

        # this expands symbols in the script AND removes CR chars for linux scripts
        run_script = scriptor.fixup_script(run_script, pc_utils.is_windows(), True, run_info=child_ri, concurrent=self.concurrent)  

        # write RUN SCRIPT LINES to a run_appXXX script file
        if pc_utils.is_windows():
            if not fn_script:
                fn_script = self.fix_path("{}/run_app{}.bat".format(user_script_cwd, rundir_index))
            #utils.send_cmd_as_script_to_box(self, "localhost", flat_cmd, fn_script, prep_script, False)
            scriptor.write_script_file(run_script, fn_script, for_windows=True)
            self.log_info("WINDOWS script", fn_script)
        else:
            if not fn_script:
                fn_script = self.fix_path("{}/run_app{}.sh".format(user_script_cwd, rundir_index))
            #utils.send_cmd_as_script_to_box(self, "localhost", flat_cmd, fn_script, prep_script, True)
            scriptor.write_script_file(run_script, fn_script, for_windows=False)
            self.log_info("LINUX script", fn_script)

        console_fn = rundir + "/service_logs/stdboth.txt"
        child_ri.set_console_fn(console_fn)

        self.log_info("target", child_env["XT_TARGET_FILE"])

        # use False if we want to capture TDQM output correctly (don't convert CR to NEWLINE's)
        stdout_is_text = True
        bufsize = -1 if stdout_is_text else -1     # doesn't seem to affect TDQM's turning off progress logging...

        if not script_args:
            script_args = [fn_script]

        prefix = context.shell_launch_prefix
        if not prefix and not pc_utils.is_windows():
            # probably running a linux docker container on windows
            prefix = "bash"

        parts = process_utils.make_launch_parts(prefix, script_args)

        # write run's context file, in case run needs to access additional info
        safe_context = dict(context.__dict__)
        del safe_context["store_creds"]["credential"]
        del safe_context["db_creds"]["credential"]

        json_text = json.dumps(safe_context)
        fn_context = os.path.join(user_script_cwd, constants.FN_RUN_CONTEXT)
        file_utils.write_text_file(fn_context, json_text)
        self.log_info("context written", fn_context)

        self.log_time_msg("starting USER SCRIPT: " + run_name)

        # log run start to JOB
        dd = {"node_id": self.node_id, "run": run_name, "restart": context.restart}
        store.log_node_event(self.ws_name, self.job_id, self.node_id, "start_run", dd)

        # start a MIRROR thread to copy files to grok server
        if context.mirror_request_list:
            self.start_mirror_workers_for_run(store, child_ri, rundir, run_name, context)

        # tell db JOBS that this job has a new run
        db = store.get_database()
        if db:
            # tell db RUNS that this run has started
            self.log_info("calling db.run_start", run_name)
            run_restarted = db.run_start(context.ws, run_name)
            context.restart = run_restarted

            if not run_restarted:
                # don't count this run if it has been restarted
                db.job_run_start(context.ws, job_id)
                db.node_run_start(context.ws, job_id, self.node_index)

        # log run STARTED event 
        if context.restart:
            self.log_title("CHILD RESTART detected")

        start_event_name = "restarted" if context.restart else "started"
        self.restart_number = 1     # TODO: need to compute this with odbc/node log
        store.log_run_event(context.ws, run_name, start_event_name, {"restart_number": self.restart_number}, job_id=job_id)  
        #prep_script = run_info.prep_script  

        if not self.running_job:
            # this is the first run of this job on this node
            self.running_job = job_id

        # don't start run until above logging has completed
        self.start_run_now(rundir, parts, user_script_cwd, fn_script, child_env, stdout_is_text, bufsize, child_ri)

        return True

    def start_run_now(self, rundir, parts, user_script_cwd, fn_script, child_env, stdout_is_text, bufsize, run_info):

        self.process_notification_events("start_run", run_info.run_name)

        if pc_utils.is_windows():
            # target must be a fully qualified name to work reliably
            fq = os.path.join(rundir, parts[0])
            if os.path.exists(fq):
                parts[0] = fq

            # run as dependent process with HIDDEN WINDOW
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            #console.print("startupinfo=", startupinfo)

            self.log_info("user_script_cwd", user_script_cwd)
            self.log_info("parts", parts)
            self.log_info("script", file_utils.read_text_file(fn_script))

            p = process = subprocess.Popen(parts, cwd=user_script_cwd, startupinfo=startupinfo, 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=child_env, 
                universal_newlines=stdout_is_text, bufsize=bufsize)
        else:
            self.log_info("user_script_cwd", user_script_cwd)
            self.log_info("parts", parts)
            self.log_info("script", file_utils.read_text_file(fn_script))

            p = process = subprocess.Popen(parts, cwd=user_script_cwd, 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=child_env, 
                universal_newlines=stdout_is_text, bufsize=bufsize)

        with run_info.lock:
            run_info.set_process(process)

        # start a thread to consume STDOUT and STDERR from process
        thread_name = "watcher_" + run_info.run_name
        stdout_thread = Thread(name=thread_name, target=read_from_stdout_pipe, args=(process.stdout, 
            run_info, self, stdout_is_text))
        stdout_thread.start()

        self.log_info("process created", p)

    def start_mirror_workers_for_run(self, store, run_info, rundir, run_name, context):
        self.log_info("starting MIRROR worker for run", run_name)

        mirror_requests = context.mirror_request_list
        mirror_dest: str = context.mirror_dest

        self.log_info("RUN mirror-dest", mirror_dest)
        self.log_info("RUN mirror_requests=", mirror_requests)

        workers = []

        for mr in mirror_requests:
            dest_type = mr["dest_type"]

            if dest_type == "run":

                worker = MirrorWorker(store, rundir, mirror_dest, wildcard_path=mr["local_dir"], grok_url=context.grok_server, 
                    ws_name=context.ws, run_name=run_name, node_id=None, job_id=context.job_id, mirror_delay_mins=context.mirror_delay_mins, 
                    show_calls=context.show_mirror_calls, dest_folder=mr["dest_folder"])
            
                worker.start()
                workers.append(worker)

                self.mirror_workers.append(worker)

        run_info.mirror_workers = workers

    def start_mirror_workers_for_node(self, store,  context):

        mirror_requests = context.mirror_request_list
        mirror_dest: str = context.mirror_dest

        self.log_info("NODE mirror-dest", mirror_dest)
        self.log_info("NODE mirror_requests=", mirror_requests)

        for mr in mirror_requests:
            dest_type = mr["dest_type"]

            if dest_type == "node":
                node_id = utils.node_id(context.node_index)
                cwd = os.getcwd()

                worker = MirrorWorker(store, cwd, mirror_dest, wildcard_path=mr["local_dir"], grok_url=context.grok_server, 
                    ws_name=context.ws, run_name=None, node_id=node_id, job_id=context.job_id, mirror_delay_mins=context.mirror_delay_mins, 
                    show_calls=context.show_mirror_calls, dest_folder=mr["dest_folder"])
            
                worker.start()

                self.mirror_workers.append(worker)

    def stop_mirror_worker(self, run_info):
        self.log_info("stop_mirror_worker: run_info.mirror_workers", run_info.mirror_workers)
        
        if run_info.mirror_workers:
            for worker in run_info.mirror_workers:
                worker.stop()

                if worker in self.mirror_workers:
                    self.mirror_workers.remove(worker)
            
            run_info.mirror_workers = None

    def diag(self, msg):
        console.print(msg)

    def get_run_info(self, ws_name, run_name, raise_if_missing=True):
        key = ws_name + "/" + run_name
        with runs_lock:
            if key in self.runs:
                return self.runs[key]
            elif raise_if_missing:
                raise Exception("unknown run_name: " + ws_name + "/" + run_name)
        return None

    def exposed_attach(self, token, ws_name, run_name, callback):
        print("==========> ATTACH: #1")
        self.validate_request(token)
        run_info = self.get_run_info(ws_name, run_name)

        # taking lock here hangs this thread (.attach also takes the lock)
        status = run_info.status
        if (status != "running"):
            return False, status

        run_info.attach(callback)
        return True, status

    def exposed_detach(self, token, ws_name, run_name, callback):
        self.validate_request(token)
        run_info = self.get_run_info(ws_name, run_name)
        index = run_info.detach(callback)
        return index

    def exposed_get_status_of_runs(self, token, ws_name, run_names_str):
        self.validate_request(token)
        status_dict = {}
        run_names = run_names_str.split("^")

        for run_name in run_names:
            run_info = self.get_run_info(ws_name, run_name, False)
            if run_info:
                status_dict[run_name] = run_info.status

        json_status_dict = json.dumps(status_dict)
        return json_status_dict

    def exposed_get_status_of_workers(self, token, worker_name):
        self.validate_request(token)
        status_list = []

        for worker in self.mirror_workers:
            status = worker.get_status()
            status_list.append(status)

        json_text = json.dumps(status_list)
        return json_text

    def status_matches_stage_flags(self, status, stage_flags):
        match = False

        if status in ["queued"]: 
            match = "queued" in stage_flags
        elif status in ["spawning", "running"]: 
            match = "active" in stage_flags
        else:
            match = "completed" in stage_flags

        return match

    def exposed_get_runs(self, token, stage_flags, ws_name=None, run_name=None):
        self.validate_request(token)
        if run_name:
            console.print("get_status: ws_name=", ws_name, ", run_name=", run_name)

            run_info = self.get_run_info(ws_name, run_name)
            return run_info.get_summary_stats() + "\n"

        result = ""
        with runs_lock:
            for run_info in self.runs.values():
                matches = self.status_matches_stage_flags(run_info.status, stage_flags)
                if matches:
                    result += run_info.get_summary_stats() + "\n"
        return result

    def get_matching_run_infos(self, full_run_names):
        # match all runinfos that have not finished (exact match and matching children)
        matches = []
        full_name_set = set(full_run_names)

        with runs_lock:
            running = [ri for ri in self.runs.values() if ri.status in ["running", "spawning", "queued"]] 

        for ri in running:
            base_name = ri.run_name.split(".")[0]
            if ri.workspace + "/" + base_name in full_name_set:
                # match parent to parent or child to parent
                matches.append(ri)
            elif ri.workspace + "/" + ri.run_name in full_name_set:
                # exact parent/child name match
                matches.append(ri)

        self.log_info("matches=", matches)
        return matches

    def get_property_matching_run_infos(self, prop_name, prop_value):
        # match all runinfos that have not finished (exact match and matching children)
        matches = []

        with runs_lock:
            running = [ri for ri in self.runs.values() if ri.status in ["running", "spawning", "queued"]] 

        for ri in running:
            if getattr(ri, prop_name) == prop_value:
                matches.append(ri)

        self.log_info("matches=", matches)
        return matches

    def restart_controller(self, delay_secs=.01):

        # simulate a service restart (for testing both XT and user's ML restart code)
        self.restarting = True
        self.restart_delay = delay_secs

        # cannot do wrapup for these runs (must look like box rebooted)
        self.cancel_all(True)

        return True

    def cancel_all(self, for_restart):
        with runs_lock:
            for run in self.runs.values():
                if run.status == "running":
                    run.kill(for_restart)

    def exposed_shutdown(self, token):
        self.validate_request(token)
        print("shutdown request received...")
        self.schedule_controller_exit()

    def exposed_get_ip_addr(self, token):
        self.validate_request(token)
        addr = self.my_ip_addr
        if not addr:
            addr = pc_utils.get_ip_address()
        return addr

    def exposed_get_concurrent(self, token):
        self.validate_request(token)
        return self.concurrent

    def exposed_set_concurrent(self, token, value):
        self.validate_request(token)
        self.concurrent = value

    def get_running_names(self):
        with runs_lock:
            running_names = [run.run_name for run in self.runs.values() if run.status == "running"]
        return running_names

    def get_alive_names(self):
        with runs_lock:
            running_names = [run.run_name for run in self.runs.values() if run.status in ["running", "queued", "spawning"]]
        return running_names

# flat functions

# def print_env_vars():
#     print("xt_controller - env vars:")
#     keys = list(os.environ.keys())
#     keys.sort()

#     for key in keys:
#         value = os.environ[key]
#         if len(value) > 100:
#             value = value[0:100] + "..."
#         self.log_info("  " + key, value)

def run(concurrent=1, my_ip_addr=None, multi_run_context_fn=constants.FN_MULTI_RUN_CONTEXT, multi_run_hold_open=False, 
        port=constants.CONTROLLER_PORT, is_aml=False):
    '''
    Runs the XT controller app - responsible for launch and control of all user ML apps for a
    local machine, remote machine, Azure VM, or Azure Batch VM.

    'max-runs' is the maximum number of jobs the controller will schedule to run simultaneously.

    'my_ip_addr' is the true IP address of the machine (as determined from the caller).

    'multi_run_context_fn' is used with Azure Batch - when specified, the controller
       should launch a single job, described in the context file (multi_run_context_fn), and when the job
       is finished, the controller should exit.
    '''

    box_secret = os.getenv("XT_BOX_SECRET")
    #console.print("XT_BOX_SECRET: ", box_secret)

    # create the controller
    service = XTController(concurrent, my_ip_addr, multi_run_context_fn, multi_run_hold_open, port, is_aml)

    if box_secret:
        # listen for requests from XT client

        philly_port = os.getenv("PHILLY_CONTAINER_PORT_RANGE_START")   # 14250
        if philly_port:
            port = int(philly_port) + 15

        # write server cert file JIT from env var values
        fn_server_cert = os.path.expanduser(constants.FN_SERVER_CERT)
        cert64 = os.getenv("XT_SERVER_CERT")
        server_cert_text = utils.base64_to_text(cert64)
        file_utils.write_text_file(fn_server_cert, server_cert_text)

        #print("create SSLAuthenticator with keyfile={}, certfile={}".format(fn_server_cert, fn_server_cert))
        authenticator = SSLAuthenticator(keyfile=fn_server_cert, certfile=fn_server_cert)  

        # launch the controller as an RYPC server
        t = ThreadedServer(service, port=port, authenticator=authenticator)
        t.start()

if __name__ == "__main__":      
    run()
