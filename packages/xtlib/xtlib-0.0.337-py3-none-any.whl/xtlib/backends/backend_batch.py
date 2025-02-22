#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# backend_batch.py: support for running a XT job on a 1-N Azure Batch Compute boxes.
# import azure.mgmt
# from azure.mgmt import batch as mgmt_batch

import os
import io
import sys
import arrow
import shutil
import time
import datetime
import numpy as np
from interface import implements
from threading import Lock                              
from datetime import timedelta

from xtlib import utils
from xtlib import errors
from xtlib import scriptor
from xtlib import constants
from xtlib import file_utils
from xtlib import time_utils
from xtlib import store_utils
from xtlib.console import console
from xtlib.report_builder import ReportBuilder
from xtlib.helpers.feedbackParts import feedback as fb
from xtlib.backends.mount_helper import MountHelper
from xtlib.backends.node_scriptor import NodeScriptor
from xtlib.helpers.key_press_checker import KeyPressChecker

#from xtlib.backends.backend_interface import BackendInterface
from xtlib.backends.backend_base import BackendBase

# azure library, loaded on demand
BlobServiceClient = None
BlobSasPermissions = None
generate_blob_sas = None
generate_container_sas = None

batch = None   
azuremodels = None
batchmodels = None
mgmt_batch = None


class AzureBatch(BackendBase):
    ''' 
    This class submits and controls Azure Batch jobs.  Submit process consists of:
        - building a "node_record" that describes how to launch each node
        - call the appropriate Batch SDK API's to build a batch job and launch it.

    Features:
        - Build the node script (shared by all nodes of the job)
        - Building a node record:
            - create a Batch ResourceFile for each input file and the expected output files
            - include the node script 
    '''

    def __init__(self, compute, compute_def, core, config, username=None, arg_dict=None):
        super(AzureBatch, self).__init__(compute, compute_def, core, config, username, arg_dict)

        # import azure libraries on demand
        global BlobServiceClient, batchmodels, batch, BlobSasPermissions, generate_blob_sas, generate_container_sas
        from azure.storage.blob import BlobServiceClient, BlobSasPermissions, generate_blob_sas, generate_container_sas
        import azure.batch.models as batchmodels
        import azure.batch as batch

        # CAUTION: "batchmodels" is NOT the same as batch.models

        if not compute_def:
            compute_def = config.get_target_def(compute)

        self.compute = compute
        self.compute_def = compute_def
        self.core = core
        self.config = config
        self.username = username
        self.custom_image_name = None

        # first, ensure we have a config file
        if config:
            self.config = config
        else:
            self.config = self.core.config

        self.store = self.core.store if core else None
        self.batch_job = None

        store_creds = self.config.get_storage_creds()
        store_name = store_creds["name"]
        store_key = store_creds["key"] if "key" in store_creds else None

        self.store_name = store_name
        self.store_key = store_key

        expire_days = self.config.get("general", "storage-cert-days")
        self.cert_now =  datetime.datetime.now(datetime.timezone.utc)

        if not isinstance(expire_days, int):
            errors.user_error(("'general.storage-cert-days' in config file must be an integer"))

        if expire_days <= 0:
            errors.user_error(("'general.storage-cert-days' in config file must be > 0"))

        if expire_days > 7:
            # why is this so low??  this seems to limit batch jobs to 7 days
            errors.user_error(("'general.storage-cert-days' in config file must be <= 7"))

        self.cert_expiration = self.cert_now + datetime.timedelta(hours=expire_days*24)

        if store_key:
            # old style (not Entra)
            blob_service_client =  BlobServiceClient(account_url=f"https://{store_name}.blob.core.windows.net/",
                credential=store_key)

            self.sas_account_key = store_key
            self.credential = store_key
            
        else:
            # new style (Entra)
            credential = store_creds["credential"]

            blob_service_client = BlobServiceClient(account_url=f"https://{store_name}.blob.core.windows.net/", 
                credential=credential)

            self.sas_account_key = self.request_user_delegation_key(blob_service_client)
            self.credentials = credential

        blob_service_client.retry = utils.make_retry_func()
        self.blob_service_client = blob_service_client
        self.batch_client = None

    def get_name(self):
        return "batch"

    def request_user_delegation_key(self, blob_service_client):
        # Get a user delegation key that's valid for 1 day
        user_delegation_key = blob_service_client.get_user_delegation_key(key_start_time=self.cert_now,
            key_expiry_time=self.cert_expiration)

        return user_delegation_key

    # API call
    def provides_container_support(self):
        '''
        Returns:
            returns True if docker run command is handled by the backend.
        Description:
            For Azure Batch, we use the XT-level container support. We had problems getting the Azure Batch container support to work.
        '''
        return False

    def build_node_script_and_adjust_runs(self, job_id, job_runs, using_hp, experiment, service_type, snapshot_dir, env_vars, args, cmds=None):
        '''
        This method is called to allow the backend to inject needed shell commands before the user cmd.  At the
        time this is called, files can still be added to snapshot_dir.
        '''

        nowrap = args["nowrap"]
        is_direct_run = args["direct_run"]

        if nowrap:
            # user script is the node script
            fn_script = args["script"]
            fn_inner = None
        else:
            # build the node script
            first_run = job_runs[0]
            fn_script, fn_inner = self.build_node_script(first_run, args)

        # adjust each job run to run fn_script
        for i, box_run in enumerate(job_runs):
            run_name = box_run["run_name"]

            run_specs = box_run["run_specs"]
            #cmd_parts = run_specs["cmd_parts"]

            if nowrap:
                # run user's script directly
                fn_direct = os.path.basename(fn_script)
                #run_specs["cmd_parts"] = ["echo i was here; ls -lt; echo bye now"]   # [fn_direct]
                cmd = "/bin/bash --login -c 'echo starting script: {}; {}; echo script ended'".format(fn_direct, fn_direct)
                run_specs["cmd_parts"] = [cmd]
            
            else:
                # NOTE: we pass the NODE_INDEX, RUN_NAME, and DIRECT_CMD as environment variables
                # so that we can share a single script among all nodes
                if is_direct_run:
                    direct_cmd = cmds[i] if i < len(cmds) else cmds[0]
                    run_specs["run_cmd"] = direct_cmd

                bash_parts = [ '/bin/bash', '--login', '{}'.format(os.path.basename(fn_script)) ]
                run_specs["cmd_parts"] = bash_parts

                merge_batch_logs = args["merge_batch_logs"]
                if merge_batch_logs:
                    # recompose this command to pass along all script arguments
                    bash_parts = ['/bin/bash', '--login', '{} $*'.format(os.path.basename(fn_script))]
        
                    # create a STDBOTH.txt that merged stdout and stderr
                    node_cmd = "{} > ../stdboth.txt 2>&1".format(" ".join(bash_parts))

                    # create a helper file to call our node cmd
                    fn_helper = snapshot_dir + "/" + constants.FN_BATCH_HELPER
                    file_utils.write_text_file(fn_helper, node_cmd)

                    outer_bash_parts = ["bash", constants.FN_BATCH_HELPER, str(i), run_name]
                    run_specs["cmd_parts"] = outer_bash_parts

                    console.diag(run_specs)

        # copy node_id to snapshot dir
        fn_from = file_utils.get_xtlib_dir() + "/backends/batch_node_id.py" 
        fn_to = snapshot_dir + "/" + constants.FN_BATCH_NODE_ID
        shutil.copyfile(fn_from, fn_to)

        # copy job_release_task to snapshot dir
        fn_from = file_utils.get_xtlib_dir() + "/" + constants.FN_JOB_RELEASE_TASK
        fn_to = snapshot_dir + "/" + constants.FN_JOB_RELEASE_TASK
        shutil.copyfile(fn_from, fn_to)

    def build_node_script(self, first_run, args):

        run_specs = first_run["run_specs"]
        box_secret = first_run["box_secret"]

        # username = args["username"]
        # cwd = "$HOME/.xt/cwd"

        cmd_parts = run_specs["cmd_parts"]
        node_cmd = " ".join(cmd_parts)
        homebase = "$HOME"
        actions = ["data", "model"]
        manual_docker = bool(args["docker_cmd"]) 

        # sudo is available, but causes problems with subsequent MNT directory access
        sudo_available = False     

        mount_helper = MountHelper(compute_def=self.compute_def, homebase=homebase, sudo_available=sudo_available, actions=actions,
            use_username=False, use_allow_other=False, nonempty=True, backend=self, config=self.config, args=args)
        
        cwd="$HOME/.xt/cwd"
        default_docker_image = None

        node_scriptor = NodeScriptor(homebase=homebase, cwd=cwd, controller_cmd=node_cmd, 
            manual_docker=manual_docker, mount_helper=mount_helper, backend=self, compute_def=self.compute_def, default_docker_image=default_docker_image,
            config=self.config, args=args)
        
        fn_script, fn_inner = node_scriptor.generate_script()
        return fn_script, fn_inner
    
    def gen_code_prep_cmds(self, ca, cmds, cwd, using_docker):
        code_dir = "/usr/src" if using_docker else "."
        code_fn = code_dir + "/" + constants.CODE_ZIP_FN

        ca.append_title(cmds, "CODE PREP: UNZIP code files to cwd:")
        ca.append_unzip(cmds, code_fn, cwd)

        if not using_docker:
            ca.append(cmds, "rm {}".format(constants.CODE_ZIP_FN))

        # move to CWD
        ca.append(cmds, "cd {}".format(cwd))

    def print_things(self, things, columns):
        
        if not things:
            print("no matches found\n")
            return
            
        # convert to a list of dict items
        things = [thing.__dict__ for thing in things]

        for thing in things:
            created = thing["creation_time"]
            now = datetime.datetime.now(tz=created.tzinfo)
            elapsed = now - created
            thing["created"] = str(created)
            thing["elapsed"] = str(elapsed)

        lb = ReportBuilder(self.config, self.store)
        text, rows = lb.build_formatted_table(things, columns)
        console.print(text)

    def match_stage(self, job, stage_flags):
        
        state = job.state
        if state == "active":  # this means 'queued' for batch
            match = "queued" in stage_flags
        elif state == "completed":
            match = "completed" in stage_flags
        else:
            match = "active" in stage_flags

        return match

    def view_status(self, run_name, workspace, job, monitor, escape_secs, auto_start, 
            stage_flags, status, max_finished):

        if not self.batch_client:
            self.create_batch_client()

        # get/report JOBS
        jobs = self.batch_client.job.list()

        # filter jobs by stage
        jobs = [job for job in jobs if self.match_stage(job, stage_flags)]

        console.print("\ntarget={} jobs:".format(self.compute))

        self.print_things(jobs, ["id", "state", "created", "elapsed"])

        # get/report POOLS

        if "active" in stage_flags:
            pools = self.batch_client.pool.list()
            console.print("\ntarget={} pools:".format(self.compute))

            self.print_things(pools, ["id", "state", "created", "elapsed"])

    def make_batch_job_id(self, ws_name, job_id):
        # qualify job_id with store_name and ws_name to minimize duplicate job names
        store_name = self.config.get("store")
        name = "{}__{}__{}".format(store_name, ws_name, job_id)
        return name
        
    def submit_job(self, job_id, job_runs, workspace, compute_def, resume_name, 
            repeat_count, using_hp, runs_by_box, experiment, snapshot_dir, controller_scripts, args):
        '''
        This runs the controller on one or more boxes within an Azure Batch pool.
        '''
        #console.print("pool_info=", pool_info)

        #import azure.storage.blob as azureblob
        global mgmt_batch
        from azure.mgmt import batch as mgmt_batch

        vm_size = compute_def["vm-size"]
        vm_image = utils.safe_value(compute_def, "azure-image")
        num_nodes = compute_def["nodes"]
        use_low_pri = compute_def["low-pri"]

        if num_nodes is None:
            num_nodes = 0

        if num_nodes <= 0:
            errors.config_error("nodes must be > 0")
        
        search_type = args["search_type"]
        multi_commands = args["multi_commands"]
        
        static_run_cmds = (search_type == "grid" or multi_commands)

        # fb.feedback("azure-batch (vm_size={}, vm_image={}, num_nodes={}, use_low_pri={})".format(vm_size, vm_image, 
        #     num_nodes, use_low_pri), is_final=static_run_cmds)

        ws_name = args["workspace"]
        is_distributed = args["distributed"]
        merge_batch_logs = args["merge_batch_logs"]

        # first, build a list of runs for each node in our azure batch pool
        node_records = []
        service_info_by_node = {}

        self.prep_all_nodes(job_id, job_runs, num_nodes, use_low_pri, using_hp, experiment, 
            static_run_cmds, node_records, workspace, service_info_by_node, merge_batch_logs, args)

        # "hold" is used to hold open the created pool
        auto_pool = not args["hold"]

        fb.feedback("submitting job to batch")

        # finally, launch the job on AZURE BATCH
        pool_id = self.launch(job_id, node_records, auto_pool=auto_pool, ws_name=ws_name, vm_size=vm_size, 
            vm_image=vm_image, num_nodes=num_nodes, use_low_pri=use_low_pri, is_distributed=is_distributed, job_runs=job_runs, args=args)

        service_job_info = {"batch_job_id": self.batch_job_id, "pool_id": pool_id}

        return service_job_info, service_info_by_node    

    def prep_all_nodes(self, job_id, job_runs_list, num_nodes, use_low_pri, using_hp, exper_name, 
        static_run_cmds, node_records, workspace, service_info_by_node, merge_batch_logs, args):

        # create each run on a worker thread
        next_progress_num = 1
        job_count = len(job_runs_list)
        thread_lock = Lock()

        def thread_worker(job_runs, job_id, num_nodes, use_low_pri, 
                using_hp, exper_name, static_run_cmds, args):

            # process a subset of all job_runs (nodes) on this thread
            for i, node_run in enumerate(job_runs):
                
                # if this is a direct run (no controller), use "box_index" instead of "node_index"
                node_index = node_run["node_index"] if "node_index" in node_run else node_run["box_index"]

                node_record = self.prep_node(job_id, node_index, node_run, num_nodes, use_low_pri, 
                    using_hp=using_hp, exper_name=exper_name, static_run_cmds=static_run_cmds, args=args)

                with thread_lock:
                    nonlocal next_progress_num

                    node_records.append(node_record)

                    node_msg = "building nodes: {}/{}".format(next_progress_num, job_count)

                    fb.feedback(node_msg, id="node_msg")  # , add_seperator=is_last)
                    next_progress_num += 1

                    node_id = "node" + str(node_index)
                    batch_job_id = self.make_batch_job_id(workspace, job_id)
                    run_name = "run_{}".format(node_index)

                    node_info = {"workspace": workspace, "job_id": job_id, "batch_job_id": batch_job_id, 
                        "node_id": node_id, "task_index": node_index, "merge_batch_logs": merge_batch_logs,
                        "run_name": run_name}

                    service_info_by_node[node_id] = node_info

                # update node_info record in database with service_info
                self.store.database.update_node_info_with_service_info(workspace, job_id, node_index, node_info)
                #print("updated node_info: job_id='{}', node_index='{}'".format(job_id, node_index))

        # create each Batch Task on a worker thread
        max_run_workers = args["max_workers"]
        utils.run_on_threads(thread_worker, job_runs_list, max_run_workers, [job_id, num_nodes, use_low_pri, 
                using_hp, exper_name, static_run_cmds, args])

        # sort node_records to normal order
        node_records.sort(key=lambda r: r["node_index"])

    def prep_node(self, job_id, node_index, node_run, num_nodes, use_low_pri, using_hp,  
            exper_name, static_run_cmds, args):
        '''prepare runs for node node_index'''

        # box_info = node_run["box_info"]
        # box_name = "{}-{}-{}".format(job_id, "batch", node_index)
        
        # target_sh, node_cmd, fn_context, fn_sh, run_names = self.prep_for_controller_run(run_data_list, node_index, job_id, tmp_dir, using_hp, 
        #     box_info, exper_name, args=args)
        run_name = node_run["run_name"]

        # build RESOURCE FILES for each file we have uploaded into "before"  directory
        before_path = "before/code"      # job store
        after_path = "nodes/node{}/after/service_logs".format(node_index)         # run store

        # use blob service from store 
        store_provider = self.store.helper.provider

        # get list of BEFORE blobs (captured by runner, with controller adjustments)
        before_blob_path = file_utils.path_join(constants.JOBS_DIR, job_id, before_path)

        workspace = args["workspace"]
        jobs_container = store_utils.get_jobs_container(workspace)

        fake_submit = utils.safe_value(args, "fake_submit")

        # BATCH BUG WORKAROUND: tried to create a resource file for FOLDER instead of enumerating all blobs
        # but always get "blob not found" error (before, before/, before/** - no form works)
        #blob_names = [before_blob_path + "/**"]
        blob_names = store_provider.list_blobs(jobs_container, before_blob_path, recursive=True)

        if not fake_submit:
            assert len(blob_names) > 0

        # for the DEST FILENAME on the node, strip off the blob path prefix
        bbp_len = 1 + len(before_blob_path)    # +1 to remove the trailing "/"
        node_file_names = [ bn[bbp_len:] for bn in blob_names ]

        #console.diag("  local_file_names=" + str(local_file_names))
        console.diag("  files uploaded to blobs: " + str(blob_names))
        console.diag("  node_file_names=" + str(node_file_names))

        # use our helper to convert blobs and filenames to resource files
        node_res_files = self.convert_blobs_to_resource_files(jobs_container, blob_names, node_file_names)

        # build list of output files that Batch will automatically upload at end of node run (aka Batch Task)
        # XT files always uploaded:
        #   controller.log - this seems to be obsolete
        #   ../*.txt       - we run in the batch "wd" directory initially and the stdboth.txt is created in the parent directory
        #output_file_list = ["controller.log", "../*.txt"]
        output_file_list = ["../std*.txt"]

        # convert to a list of ResourceFile objects
        after_blob_path = constants.JOBS_DIR + "/" + job_id + "/" + after_path
        job_container = workspace if store_utils.STORAGE_FORMAT == "2" else constants.INFO_CONTAINER_V1
        node_output_files = self.build_output_files(job_container, after_blob_path, output_file_list)

        # if static_run_cmds:
        #     fb.feedback("  adding node: {}, run(s): {}".format(box_name.upper(), run_names.upper()), is_final=True)

        node_specs = node_run["run_specs"]
        box_secret = node_run["box_secret"]
        cmd_parts = node_specs["cmd_parts"]
        node_cmd = " ".join(cmd_parts)

        return {"node_cmd": node_cmd, "node_res_files": node_res_files, "node_output_files": node_output_files, 
            "box_secret": box_secret, "node_index": node_index, "run_name": run_name}

    def launch(self, job_id, node_records, auto_pool=True, description=None, ws_name=None, 
            vm_size=None, vm_image=None, num_nodes=1, use_low_pri=True, is_distributed=False, job_runs=None, args=None):
        
        fake_submit = utils.safe_value(args, "fake_submit")

        self.auto_pool = auto_pool
        self.description = description

        workspace = args["workspace"]
        batch_job_id = self.make_batch_job_id(workspace, job_id)

        self.batch_job_id = batch_job_id
        self.pool_id = "_pool_{}_{}_".format(workspace, job_id)
        self.xt_job_id = job_id

        self.vm_size = vm_size
        self.azure_image = vm_image 
        self.num_nodes = num_nodes 
        self.use_low_pri = use_low_pri 

        self.start_time = datetime.datetime.now().replace(microsecond=0)

        self.create_batch_client(args)

        if not fake_submit:
            # create our pool and job together 
            pool = self.create_pool_and_job(is_distributed, node_records, args)
        else:
            pool = None
            
        # add the specified tasks (commands) to our job
        self.add_tasks_to_job(node_records, job_runs=job_runs, args=args)

        # job is now launched (usually remained queued for 2-4 minutes, then starts running)
        return self.pool_id      # may have changed (for auto_pool=True, the default)

    def resize_pool(self, batch_service_client, node_count, pool_id):
        resize_param = batch.models.PoolResizeParameter(target_dedicated_nodes=0, target_low_priority_nodes=node_count,
            resize_timeout=datetime.timedelta(minutes=10), node_deallocation_option="requeue") 
        
        resized = False

        for i in range(1000):
            try:
                batch_service_client.pool.resize(pool_id, resize_param)
                resized = True
                break
            except:
                if i and i % 10 == 0:
                    print("retrying pool resize, target={}".format(node_count))
                time.sleep(1)

        if not resized:
            raise Exception("initial pool resize failed")

    def create_batch_client(self, args=None):
        # create a batch_client to handle most of our azure needs
        if args:
            target = args["target"]
            target_def = args["compute_def"]
        else:
            target = self.compute
            target_def = self.compute_def
            
        service_name = utils.safe_value(target_def, "service")
        if not service_name:
            errors.config_error("{} '{}' missing 'service' property in [compute-targets] of XT config file".format("target", target))

        # validate BATCH credentials
        batch_creds = self.config.get_service(service_name)

        batch_name = service_name
        batch_key = batch_creds["key"] if "key" in batch_creds else ""
        batch_url = batch_creds["url"]

        # import azure libraries on demand
        import azure.batch.batch_auth as batch_auth

        #console.print("batch_name={}, batch_key={}, batch_url={}".format(batch_name, batch_key, batch_url))

        if batch_key:
            # old style
            credentials = batch_auth.SharedKeyCredentials(batch_name, batch_key)
            batch_client = batch.BatchServiceClient(credentials, batch_url=batch_url)

        else:
            # new style: use Entra authentication
            from msrest.authentication import BasicTokenAuthentication

            creds = self.config.vault.credential
            #tenant_id = "72f988bf-86f1-41af-91ab-2d7cd011db47"
            #creds = InteractiveBrowserCredential(logging_enable=True, tenant_id=tenant_id)
            token = creds.get_token("https://batch.core.windows.net/.default").token
            token_config = {"access_token": token}
            token_credential = BasicTokenAuthentication(token_config)
            batch_client = batch.BatchServiceClient(credentials=token_credential, batch_url=batch_url)

            # debug
            token_sample = token[:10] + "..." + token[-10:]
            #console.print("new batch_client created using token: {}".format(token_sample))

        #self.test_batch_client(batch_client)

        batch_client.retry = utils.make_retry_func()
        self.batch_client = batch_client

    def test_batch_client(self, batch_client):
        # test the batch client by getting the account info
        print("testing batch client...")

        jobs = batch_client.job.list()
        for j, job in enumerate(jobs):
            print(  job.id)
            break

        print("test complete.")

    # API
    def supports_setting_location(self):
        # not currently supported
        return False
    
    # API 
    def get_location(self, service):
        if not self.batch_client:
           self.create_batch_client()

        # cannot find a proper API for this, so just parse the URL
        url = self.batch_client.config.batch_url
        parts = url.split(".")
        location = parts[1]

        return location

    def get_external_port(self, port_name, node):
        port = None
        ip_addr = None

        for ep in node.endpoint_configuration.inbound_endpoints:
            if ep.name.startswith(port_name):
                # found our address for the specified node_index
                ip_addr = ep.public_ip_address
                port = ep.frontend_port
                break

        return ip_addr, port

    def get_client_cs(self, service_node_info):
        '''
        Args:
            service_node_info: info that service maps to a compute node for a job
        Returns:
            {"ip": value, "port": value, "box_name": value}
        '''
        cs = None

        job_id = service_node_info["job_id"]
        node_id = service_node_info["node_id"]
        node_index = utils.node_index(node_id)
        workspace = service_node_info["workspace"]

        state, ip_addr, controller_port, tensorboard_port = \
            self.get_azure_box_addr(workspace, job_id, node_index)

        if not (ip_addr and controller_port):
            errors.service_error("Node not available (node state: {})".format(state))

        if ip_addr and controller_port:
            cs = {"ip": ip_addr, "port": controller_port, "box_name": node_id}

        return cs

    def get_azure_box_addr(self, ws_name, job_id, node_index):
        ip_addr = None
        port = None
        state = None
        controller_port = None
        tensorboard_port = None

        if not self.batch_client:
            self.create_batch_client()

        # XT always has exactly 1 task running on each node (xt controller), so
        # we can reply on task[x] running on node index x
        batch_job_name = self.make_batch_job_id(ws_name, job_id)
        task_id = "task" + str(node_index)
        task = self.batch_client.task.get(batch_job_name, task_id)

        state = task.state
        if state in ["running", "completed"]:
            node_info = task.node_info
            pool_id = node_info.pool_id
            node_id = node_info.node_id

            try:
                #console.print("job_id=", job_id, ", pool_id=", pool_id, ", mode_id=", node_id)
                node = self.batch_client.compute_node.get(pool_id, node_id)
                #console.print("node.ip_address=", node.ip_address)

                ip_addr, controller_port = self.get_external_port("xt-controller", node)
                ip_addr, tensorboard_port = self.get_external_port("xt-tensorboard", node)
            except BaseException as ex:
                # treat any exception here as the pool being deallocated
                state = "deallocated"

        return state, ip_addr, controller_port, tensorboard_port

    def wait_for_job_completion(self, max_wait_minutes=60):
        # Pause execution until tasks reach Completed state.
        completed = self.wait_for_tasks_to_complete()

    def port_request(self, port_num, port_name, base_offset, rules):
        pr = batchmodels.InboundNATPool(
            name=port_name, 
            protocol='tcp', 
            # NOTE: client machine should connect to the Azure Batch app using the port that is dynamically ASSIGNED 
            # to the node (node_index + AZURE_BATCH_BASE_CONTROLLER_PORT).
            # Note: Azure Batch node should listen via the CONTROLLER_PORT
            backend_port=port_num,   
            frontend_port_range_start=base_offset + constants.AZURE_BATCH_BASE_CONTROLLER_PORT, 
            frontend_port_range_end=base_offset + 500 + constants.AZURE_BATCH_BASE_CONTROLLER_PORT,
            network_security_group_rules=rules)

        return pr

    def create_network_config(self):
        '''open port CONTROLLER_PORT for incoming traffic on all nodes in pool '''
        rules = network_security_group_rules=[
            # for CONTROLLER PORT
            batchmodels.NetworkSecurityGroupRule(priority=179, access=batchmodels.NetworkSecurityGroupRuleAccess.allow,
                source_address_prefix='*'),
            
            # for TENSORBOARD PORT
            batchmodels.NetworkSecurityGroupRule(priority=181, access=batchmodels.NetworkSecurityGroupRuleAccess.allow,
                source_address_prefix='*')
        ]

        nat_pools = []
        nat_pools.append(self.port_request(constants.CONTROLLER_PORT, "xt-controller-rpc", 0, [rules[0]]))
        nat_pools.append(self.port_request(constants.TENSORBOARD_PORT, "xt-tensorboard-run", 600, [rules[1]]))

        pep_config = batchmodels.PoolEndpointConfiguration(inbound_nat_pools=nat_pools)
        network_config = batchmodels.NetworkConfiguration(endpoint_configuration=pep_config)

        return network_config

    def create_mgmt_pool(self, vm_config, vm_size, network_config, is_distributed, args):
        # NOTE: we use the mgmt_batch package to create the pool so that we can specify the user_assigned_managed_identity.
        # the usual batch.models.Pool object does not yet support this feature (known issue going on 2 years now).

        # CAUTION: be sure to use all *mgmt_batch* objects being passed to bmc.pool.create()
        # because the batch_models objects are incompatible with the mgmt_batch objects

        deployment_config = mgmt_batch.models.DeploymentConfiguration(virtual_machine_configuration=vm_config)

        # here is where we specify our UAMI (with a funky API)
        uai_url = args["uami_id"]

        user_assigned_identities = mgmt_batch.models.UserAssignedIdentities()
        batch_pool_identity = mgmt_batch.models.BatchPoolIdentity(type="UserAssigned", user_assigned_identities={uai_url: user_assigned_identities})
        
        # we specify starting with 0 dedicated and 0 low priority nodes (will resize soon)
        # this prevents our submit script from waiting for the pool to resize (which can take a quite a while)
        
        fixed_scale = mgmt_batch.models.FixedScaleSettings(target_dedicated_nodes=0, target_low_priority_nodes=0)
        fixed_scale_settings = mgmt_batch.models.ScaleSettings(fixed_scale=fixed_scale)

        # auto scale takes way too long to start the job (15 minutes to start!)
        # auto_formula = "$TargetLowPriorityNodes = $ActiveTasks.GetSample(1) + $RunningTasks.GetSample(1);"
        # auto_scale = mgmt_batch.models.AutoScaleSettings(auto_scale_evaluation_interval=timedelta(minutes=5), formula=auto_formula)
        # auto_scale_settings = mgmt_batch.models.ScaleSettings(auto_scale=auto_scale)

        # TODO: how should "is_distributed" be used here?

        pool_params = mgmt_batch.models.Pool(
            identity=batch_pool_identity, 
            display_name=self.pool_id,                                   
            deployment_configuration=deployment_config,
            scale_settings=fixed_scale_settings,
            #scale_settings=auto_scale_settings,
            #network_configuration=network_config,
            vm_size=vm_size)
        
        service_name = utils.safe_value(self.compute_def, "service")
        batch_creds = self.config.get_service(service_name)
        subscription_id = batch_creds["subscription-id"]
        resource_group = batch_creds["resource-group"]

        bmc = mgmt_batch.BatchManagementClient(self.credentials, subscription_id)
        pool = bmc.pool.create(resource_group, service_name, self.pool_id, pool_params)

        # resize pool to specified number of nodes
        self.resize_pool(self.batch_client, self.num_nodes, self.pool_id)

        return pool

    def old_create_pool(self, vmc, vm_size, network_config, is_distributed):
        '''
        This old approach to create a pool uses the azure.batch.models classes:
            - PoolSpecification
            - PoolAddParameter

            - AutoPoolSpecification
            - PoolInformation
            
        This approach was working fine until we needed to add a user-assigned managed identity to the pool, 
        and due to a bug in the Azure Batch SDK, they omitted support for this feature in the PoolSpecification and 
        PoolAddParameter classes.
        '''
        if self.auto_pool:    # hold==0

            # create a dynamically allocated pool  (name will be GUID assigned by Azure Batch)
            #dynamic_resize = True
            dynamic_resize = False
            #max_tasks_per_node = None
            enable_inter_node_communication = is_distributed

            if dynamic_resize:
                target_name = "$TargetLowPriorityNodes" if self.use_low_pri else "$TargetDedicatedNodes"
                target_count = self.num_nodes

                # lots of work here to specify: release nodes when their only task has completed
                formula = ""
                formula += "pending = max(0, $PendingTasks.GetSample(1)); "
                formula += "succeeded = max(0, $SucceededTasks.GetSample(1)); "
                formula += "failed = max(0, $FailedTasks.GetSample(1)); "
                formula += "{} = (pending + succeeded + failed) ? pending : {}; ".format("target_name", target_count)
                formula += "$NodeDeallocationOption = taskcompletion; "
            else:
                formula = None

            pool_spec = batch.models.PoolSpecification(
                #id=self.pool_id,
                virtual_machine_configuration=vmc,
                vm_size=vm_size,
                network_configuration=network_config,
                enable_auto_scale=(formula is not None),
                auto_scale_formula=formula,
                #identity=pool_identity,          # NOT IMPLEMENTED YET
                #max_tasks_per_node = max_tasks_per_node,
                target_dedicated_nodes=0 if self.use_low_pri else self.num_nodes,
                enable_inter_node_communication=enable_inter_node_communication)

            # else:
            #     pool_spec = batch.models.PoolSpecification(
            #         #id=self.pool_id,
            #         virtual_machine_configuration=vmc,
            #         vm_size=self.vm_size,
            #         network_configuration=network_config,
            #         target_low_priority_nodes=self.num_nodes if self.use_low_pri else 0,
            #         #identity=pool_identity,          # NOT IMPLEMENTED YET
            #         #max_tasks_per_node = max_tasks_per_node,
            #         enable_inter_node_communication=enable_inter_node_communication)

            auto_pool = batch.models.AutoPoolSpecification(pool_lifetime_option="job", keep_alive=False, pool=pool_spec, 
                auto_pool_id_prefix=self.xt_job_id)

            pool_info = batch.models.PoolInformation(auto_pool_specification= auto_pool)
            
        else:            # hold==1
            # create a staticly allocated pool that must be released by the user
            # for this pool, we can provide a name to easily associate it with the job
            new_pool = batch.models.PoolAddParameter(id=self.pool_id,
                virtual_machine_configuration=vmc,
                vm_size=self.vm_size,
                network_configuration=network_config,
                target_dedicated_nodes=0 if self.use_low_pri else self.num_nodes,
                target_low_priority_nodes=self.num_nodes if self.use_low_pri else 0,
                #max_tasks_per_node = max_tasks_per_node,
                enable_auto_scale=False,                # don't resize to 0 or we won't be able to connect to node
                resize_timeout=timedelta(minutes=30),                      # allow 30 mins to allocate all needed VMs
                enable_inter_node_communication=enable_inter_node_communication)

            self.batch_client.pool.add(new_pool)
            pool_info = batch.models.PoolInformation(pool_id=self.pool_id)  # , auto_pool_specification= auto_pool)

        return pool_info

    def create_pool_and_job(self, is_distributed, node_records, args):
        # get the required Azure VM image 
        props = self.config.get("azure-batch-images", self.azure_image)
        if not props:
            errors.config_error("No config file entry found in [azure-batch-images] section for azure-image=" + self.azure_image)

        publisher =  utils.safe_value(props, "publisher")
        offer =  utils.safe_value(props, "offer")
        sku =  utils.safe_value(props, "sku")
        version =  utils.safe_value(props, "version")
        node_agent_sku_id =  utils.safe_value(props, "node-agent-sku-id")
        custom_image_id = utils.safe_value(props, "custom-image-id")

        # # this approach uses batchmodels.xxx
        # if custom_image_id:
        #     # supply a custom OS image for each node in the pool
        #     img_ref = batchmodels.ImageReference(virtual_machine_image_id=custom_image_id)
        #     vmc = batchmodels.VirtualMachineConfiguration(image_reference=img_ref, node_agent_sku_id=node_agent_sku_id)

        # else:
        #     # use a Microsoft published image
        #     img_ref = batchmodels.ImageReference(publisher=publisher, offer=offer, sku=sku, version=version)
        #     vmc = batchmodels.VirtualMachineConfiguration(image_reference=img_ref, node_agent_sku_id=node_agent_sku_id)

        # this approach uses batch.mgmt.xxx
        if custom_image_id:
            # supply a custom OS image for each node in the pool
            img_ref = mgmt_batch.models.ImageReference(virtual_machine_image_id=custom_image_id)
            vmc = mgmt_batch.models.VirtualMachineConfiguration(image_reference=img_ref, node_agent_sku_id=node_agent_sku_id)

        else:
            # use a Microsoft published image
            img_ref = mgmt_batch.models.ImageReference(publisher=publisher, offer=offer, sku=sku, version=version)
            vmc = mgmt_batch.models.VirtualMachineConfiguration(image_reference=img_ref, node_agent_sku_id=node_agent_sku_id)            

        target = self.compute

        # TODO: support for running a user-specified custom container
        
        # TODO: how should this network_config be used?
        network_config = self.create_network_config()

        #pool_info = self.old_create_pool(vmc, self.vm_size, network_config, is_distributed)
        pool_info = self.create_mgmt_pool(vmc, self.vm_size, network_config, is_distributed, args)

        hold = args["hold"]
        job_release_task, job_prep_task = self.make_job_release_task(hold, self.pool_id, node_records)
        
        pool_info = batch.models.PoolInformation(pool_id = self.pool_id)

        batch_job = batch.models.JobAddParameter(id=self.batch_job_id, pool_info=pool_info, 
            job_preparation_task=job_prep_task, job_release_task=job_release_task,
            on_all_tasks_complete="terminateJob")

        self.batch_client.job.add(batch_job)
        self.batch_job = batch_job

        return pool_info

    def make_job_release_task(self, hold, pool_id, node_records):
        if hold:
            job_prep_task = None
            job_release_task = None
            
        else:
            service_name = utils.safe_value(self.compute_def, "service")
            batch_creds = self.config.get_service(service_name)
            batch_url = batch_creds["url"]

            from azure.batch.models import JobReleaseTask, JobSpecification, JobPreparationTask

            # cmd to delete our pool after job completes (to save money)
            # couldn't get az version to work so using python version
            #cmd_delete_pool = "az batch pool delete --account-name {} --resource-group {} --pool-id {} --yes".format(service_name, resource_group, self.pool_id)
            cmd_delete_pool = "pip install --target=. azure-batch azure-identity; python3 {} {} {}".format(constants.FN_JOB_RELEASE_TASK, self.pool_id, batch_url)

            # must specify a (dummy) job preparation task to be able to specify a job release task
            job_prep_task = JobPreparationTask(command_line="echo 'job prep task'", wait_for_success=True)
            user_identity =  {'auto_user': {'scope': 'task', 'elevation_level': 'admin'}}
            resource_files = node_records[0]["node_res_files"]

            job_release_task = JobReleaseTask(command_line=f'/bin/bash -c "{cmd_delete_pool}"',   
                wait_for_success=True, user_identity=user_identity, resource_files=resource_files)
        
        return job_release_task, job_prep_task

    def get_elevated_user_identify(self):
        aus = batchmodels.AutoUserSpecification(elevation_level=batchmodels.ElevationLevel.admin, 
            scope=batchmodels.AutoUserScope.task)
        user = batchmodels.UserIdentity(auto_user=aus)
        return user

    def delete_container_if_exists(self, name):
        if self.blob_service_client.exists(name):
            self.blob_service_client.delete_container(name)

    def get_container_sas_url(self, dest_container_name):
        # create container (workspace) to hold output files (usually already exists)
        from azure.core.exceptions import ResourceExistsError

        try:
            self.blob_service_client.create_container(dest_container_name)
        except ResourceExistsError as err:
            #print("OUTPUT container already exists: {}".format(dest_container_name))
            pass

        account_name = self.blob_service_client.account_name

        # important: use BLOB permissions here (not container)
        sas_token = generate_container_sas(account_name=account_name, container_name=dest_container_name, 
            account_key=self.sas_account_key, permission=BlobSasPermissions(read=True, write=True, create=True), 
            expiry=self.cert_expiration, start=self.cert_now)    

        # secret trick: construct SAS URL for the container
        container_sas = "https://{}.blob.core.windows.net/{}?{}".format(self.store_name, dest_container_name, sas_token)
        return container_sas

    def add_tasks_to_job(self, node_records, job_runs, args):

        # we always use exactly 1 task per node (xt controller)
        tasks = []
        for idx, node_record in enumerate(node_records):
            node_cmd = node_record["node_cmd"]
            node_res_files = node_record["node_res_files"]
            node_output_files = node_record["node_output_files"]
            run_name = node_record["run_name"]

            #env_vars = dict(args["env_vars"])
            # env_vars["XT_NODE_ID"] = "node" + str(idx)
            # env_vars["XT_BOX_SECRET"] = node_record["box_secret"]

            # user's env vars
            node_env_vars = dict(args["env_vars"])

            # add NODE-SPECIFIC (and shared) XT env vars 
            service_name = utils.safe_value(self.compute_def, "service")
            batch_creds = self.config.get_service(service_name)
            batch_key = batch_creds["key"] if "key" in batch_creds else ""
            direct_cmd = None
            
            if args["direct_run"]:
                job_run = job_runs[idx]
                direct_cmd = job_run["run_specs"]["run_cmd"]

            scriptor.add_controller_env_vars(node_env_vars, self.config, node_index=idx, run_name=run_name, 
                batch_key=batch_key, direct_cmd=direct_cmd, args=args)

            task_id = "task{}".format(idx)
            #console.print("add task: id=", task_id, ", node_cmd=", node_cmd)

            # this is so that we can run SUDO on our cmd line (related to bug in "conda create" that requires SUDO)
            elevated_user = self.get_elevated_user_identify()

            # add user-specified environment variables
            env_var_list = []
            for key, value in node_env_vars.items():
                # wierd API; need to specify params by name or get wierd errors
                es = batchmodels.EnvironmentSetting(name=key, value=str(value))
                env_var_list.append(es)

            if self.custom_image_name:
                tcs = batch.models.TaskContainerSettings(image_name=self.custom_image_name)
            else:
                tcs = None

            task_param = batch.models.TaskAddParameter(id=task_id, command_line=node_cmd, environment_settings=env_var_list,
                resource_files=node_res_files, user_identity=elevated_user, output_files=node_output_files, 
                container_settings=tcs)

            tasks.append(task_param)

        fake_submit = args["fake_submit"]

        if not fake_submit:
            # this statement launches the job
            self.batch_client.task.add_collection(self.batch_job_id, tasks)

        # copy to submit-logs
        tasks_data = self.make_submit_data_serializable(tasks)
        dd = {"job_id": self.batch_job_id, "tasks": tasks_data}
        utils.copy_data_to_submit_logs(args, dd, "batch_submit.json")

        ### bug workaround: setting "on_all_tasks_complete" below doesn't seem to work so
        ### we set it on job creation (above)

        # now that we have added all our tasks, terminate the job as soon as all tasks complete (with or without error)
        #self.self.on_all_tasks_complete = "terminatejob"
        #console.print("self.self.on_all_tasks_complete=", self.self.on_all_tasks_complete)

    def make_submit_data_serializable(self, tasks):
        import json
        task_datas = []

        for task in tasks:
            command_line = task.command_line
            id = task.id
            
            env_vars = {}
            es = task.environment_settings
            for ev in es:
                env_vars[ev.name] = ev.value

            res_files = []
            for rf in task.resource_files:
                file_path = rf.file_path
                url = rf.http_url
                res_file = {"file_path": file_path, "url": url}
                res_files.append(res_file)

            out_files = []
            for of in task.output_files:
                dest_url = of.destination.container.container_url
                dest_path = of.destination.container.path

                file_pattern = of.file_pattern
                upload_condition = str(of.upload_options.upload_condition)

                out_file = {"dest_url": dest_url, "dest_path": dest_path, "file_pattern": file_pattern, "upload_condition": upload_condition}
                out_files.append(out_file)                

            td = {"command_line": command_line, "id": id, "env_vars": env_vars, "res_files": res_files, "out_files": out_files}

            #json.dumps(td)     # ensure its serializable
            task_datas.append(td)

        return task_datas

    def build_output_files(self, dest_container_name, blob_path, wildcard_names):
        '''
        For each wildcard string in wildcard_names, build an OutputFile instance that specifies:
            - the source files on the node (specified by the wildcard)
            - the blob destination in the dest_container_name 

        Return the list of OutputFiles built.
        '''
        container_sas = self.get_container_sas_url(dest_container_name)
        output_files = []

        for pattern in wildcard_names:
            # CAUTION: "batchmodels" is NOT the same as batch.models
            upopts = batchmodels.OutputFileUploadOptions(upload_condition="taskCompletion")

            if utils.has_azure_wildcards(pattern):
                dest_blob_path = blob_path
            else:
                # single file names require adjust to blob_path
                dest_blob_path = blob_path + "/" + os.path.basename(pattern)

            dest = batchmodels.OutputFileBlobContainerDestination(container_url=container_sas, path=dest_blob_path)
            dest2 = batchmodels.OutputFileDestination(container=dest)

            output_file = batchmodels.OutputFile(file_pattern=pattern, destination=dest2, upload_options=upopts)
            #console.print("built output_file: pattern=", pattern, ", dest_container=", out_container_url, ", blob_path=", blob_path)
            output_files.append(output_file)

        return output_files

    def print_status_text(self, task_counts, wait_steps):
        # console.print out status codes as we wait
        #console.print("task_counts=", task_counts)

        status = ""
        for _ in range(task_counts.active):
            status += "q"
        for _ in range(task_counts.running):
            status += "r"
        for _ in range(task_counts.failed):
            status += "f"
        for _ in range(task_counts.succeeded):
            status += "s"

        if len(status) == 0:
            # something went wrong
            status = "."
        elif len(status) > 1:
            # more than one task, separate each sample by a space
            status += " "

        console.print(status, end="")
        if wait_steps > 0 and wait_steps % 60 == 0:
            console.print("")
            
        sys.stdout.flush()

    def wrapup_parent_run(self, store, ws, run_name):
        '''
        wrap up a run from an azure self.  run may have spawned child runs, which also need to be cleaned up.
        '''
        records = self.wrapup_target_run(store, ws, run_name)
        child_records = [rec for rec in records if rec["event"] == "child_created"]
        child_names = [rec["data"]["child_name"] for rec in child_records]

        for child_name in child_names:
            self.wrapup_target_run(store, ws, child_name)

    def wrapup_target_run(self, store, ws, run_name):
        '''
        wrap up a run from azure batch.  run may have started, or may have completed.  
        '''
        # get some needed info from run log
        records = store.get_run_log(ws, run_name)

        if records:
            # is a wrapup needed?
            end_record = [rec for rec in records if rec["event"] == "ended"]
            
            if not end_record:
                dd = records[0]["data"]
                exper_name = dd["exper_name"]
                job_id = dd["job_id"]
                status = "cancelled"
                exit_code = None
                rundir = None      # since job has not started
                log = self.config.get("logging", "log")
                capture = self.config.get("after-files", "after-upload")

                # should we be getting these 3 values from the run itself (its context or logged values for these)?
                primary_metric = self.config.get("general", "primary-metric")
                maximize_metric = self.config.get("general", "maximize-metric")
                report_rollup = self.config.get("run-reports", "report-rollup")

                after_files_list = self.config.get("after-files", "after-dirs")
                after_files_list = utils.parse_list_option_value(after_files_list)

                aggregate_dest = self.config.get("hyperparameter-search", "aggregate-dest")
                dest_name = exper_name if aggregate_dest == "experiment" else job_id

                node_id = utils.node_id(dd["node_index"])
                run_index = dd["run_index"] if "run_index" in dd else None

                store.wrapup_run(ws, run_name, aggregate_dest, dest_name, status, exit_code, 
                    primary_metric, maximize_metric, report_rollup, rundir, after_files_list, log, capture, 
                    job_id=job_id, node_id=node_id)

        return records

    def cancel_job_node(self, store, ws_name, job_id, node_index, run_datas):
        pool_id = None
        node_id = None
        task_killed = False

        if not self.batch_client:
            self.create_batch_client()

        # terminate the TASK
        #console.print("canceling: job={}, node_index={}, run_names={}".format(job_id, node_index, full_run_names))

        batch_job_name = self.make_batch_job_id(ws_name, job_id)
        task = self.batch_client.task.get(batch_job_name, "task" + str(node_index))
        before_status = str(task.state)
        #console.print("task.state=", task.state)

        if task.node_info:
            pool_id = task.node_info.pool_id
            node_id = task.node_info.node_id

        if task.state != "completed":
            try:
                self.batch_client.task.terminate(batch_job_name, task.id)     
                console.print("azure-batch task terminated: {}.{}".format(job_id, task.id))
                task_killed = True
            except BaseException as ex:
                print("exception trying to cancel job '{}', task: '{}': {}".format(job_id, task.id, ex.message))

        # kill the NODE itself
        # TODO: we need the resource_group to make this call
        #self.batch_client.node.delete(resource_group, node_id)

        # wrap-up each run (logging, capture)
        cancel_results = []

        if run_datas:
            for run_data in run_datas:    
                ws = run_data["ws_name"]
                run_name = run_data["run_name"]

                # watch out for fully-qualified run names
                if "/" in run_name:
                    ws, run_name = run_name.split("/")
                    
                # now, wrapup all runs for the specified azure batch box

                self.wrapup_parent_run(store, ws, run_name)
                kr = {"workspace": ws, "run_name": run_name, "cancelled": True, "status": "cancelled", "before_status": before_status}
                #console.print("kr=", kr)
                cancel_results.append(kr)
 
        #console.print("cancel_results=", cancel_results)
        return cancel_results, pool_id

    def get_job_status(self, job_id):
        if not job_id:
            job_id = self.batch_job_id

        console.print("get_job_status (azure): job_id=", job_id)

        if not self.batch_client:
            self.create_batch_client()
        
        try:
            status = "running"
            task_counts = self.batch_client.job.get_task_counts(job_id)
            if task_counts.active:
                # if any tasks are waiting for a node, consider the job status as allocating
                status = "allocating"    
            elif task_counts.running == 0:
                status = "completed"
        except:
            # job deleted/unknown/corrput
            status = "unknown"
        
        return status

    def attach_task_to_console(self, job_id, run_name):
        self.batch_job_id = job_id

        self.create_batch_client()

        all_tasks_complete = False
        start = datetime.datetime.now()
        detach_requested = False
        console.print()

        with KeyPressChecker() as checker:
            # wait until job starts
            while True:   
                
                # get a dict of the stats for each task
                task_counts = self.batch_client.job.get_task_counts(self.batch_job_id)

                elapsed = time_utils.elapsed_time(start)
                console.print("waiting for queued job to start... (elapsed time: {}).format(elapsed)", end="\r")

                all_tasks_complete = task_counts.running or task_counts.failed or task_counts.succeeded
                if all_tasks_complete:
                    break

                # check every .5 secs for keypress to be more responsive (but every 1 sec for task counts)
                ch = checker.getch_nowait()
                if ch == constants.ESCAPE:
                    detach_requested = True
                    break
                time.sleep(.5)

                ch = checker.getch_nowait()
                if ch == constants.ESCAPE:
                    detach_requested = True
                    break
                time.sleep(.5)

        console.print()     # end the status line of "..."
        sys.stdout.flush()

        if detach_requested:
            console.print("\n--> experiment detached from console.  to reattach, run:")
            console.print("\txt attach " + run_name)
        else:
            #----- stream output to console ----
            self.print_task_output(self.batch_job_id, 0)

    def print_task_output(self, job_id, task_index):

        # get task_id
        tasks = self.batch_client.task.list(self.batch_job_id)
        console.print("task.list len=", len(tasks))
        
        task = next(iter(tasks), None)
        if not task:
            console.print("error - job has no tasks")
        else:
            task_info = self.batch_client.task.get(self.batch_job_id, task.id)
            node_info = task_info.node_info

            if node_info:
                # node has been allocated and not yet released
                stream = self.batch_client.file.get_from_task(self.batch_job_id, task.id, "stdout.txt")

                while True:
                    for data in stream:
                        text = data.decode("utf-8")
                        console.print(text)

                    task_counts = self.batch_client.job.get_task_counts(self.batch_job_id)
                    if task_counts.running == 0:
                        console.print("<task terminated>")
                        break

                    time.sleep(1)

                #console.print(file_textt)
            else:
                console.print("error - task has no node")


    def print_output_for_tasks(self):
        """Prints the stdout.txt file for each task in the self.
        """
        console.print('Printing task output...')

        tasks = self.batch_client.task.list(self.batch_job_id)

        for task in tasks:
            console.print("getting output for job={}, task={}".format(self.batch_job_id, task.id))
            
            task_info = self.batch_client.task.get(self.batch_job_id, task.id)
            node_info = task_info.node_info

            if node_info:
                node_id = node_info.node_id
                stream = self.batch_client.file.get_from_task(self.batch_job_id, task.id, "stdout.txt")
                file_text = self._stream_to_text(stream)

                console.print("\nTask: {}, Node: {}, Standard output:".format(task.id, node_id))
                console.print(file_text)

    def _stream_to_text(self, stream, encoding='utf-8'):
        output = io.BytesIO()

        try:
            for data in stream:
                output.write(data)
            return output.getvalue().decode(encoding)
        finally:
            output.close()

        raise RuntimeError('could not read task data from stream')

    def convert_blobs_to_resource_files(self, container_name, blob_names, file_names, writable=False):

        if writable:
            permission = BlobSasPermissions(write=True)
        else:
            permission = BlobSasPermissions(read=True)

        resource_files = []
        account_name = self.blob_service_client.account_name

        #for blob_name, file_name in zip(blob_names, file_names):
        for i, blob_name in enumerate(blob_names):
            # create a security token to allow anonymous access to blob

            sas_token = generate_blob_sas(account_name=account_name, container_name=container_name,
                blob_name=blob_name, account_key=self.sas_account_key, permission=BlobSasPermissions(read=True),
                expiry=self.cert_expiration)

            # convert SAS to URL
            STORAGE_ACCOUNT_DOMAIN = 'blob.core.windows.net' 
            sas_url = f"https://{account_name}.{STORAGE_ACCOUNT_DOMAIN}/{container_name}/{blob_name}?{sas_token}"

            # support OPTIONAL file_names
            file_name = file_names[i] if file_names and file_names[i] else "./"

            # finally, create the ResourceFile
            resource_file = batchmodels.ResourceFile(http_url=sas_url, file_path=file_name)
            resource_files.append(resource_file)

        return resource_files

    def upload_files_to_blobs(self, container_name, blob_path, files):
        # create container if needed
        self.blob_service_client.create_container(container_name, fail_on_exist=False)
        #console.print("result from create_container=", result)

        blob_names = []
        for fn in files:
            blob_dest = os.path.basename(fn)
            if blob_path:
                blob_dest = blob_path + "/" + blob_dest
            self.blob_service_client.create_blob_from_path(container_name, blob_dest, fn)
            blob_names.append(blob_dest)

        return blob_names

    def close_resources(self, batch_client):

        if self.pool_id:
            console.print("deleting pool...")
            batch_client.pool.delete(self.pool_id)
            self.pool_id = None

        if self.batch_job_id:
            console.print("deleting self...")
            batch_client.self.delete(self.batch_job_id)
            self.batch_job_id = None

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
        node_index = int(node_index)
        cancelled_by_controller = False
        cancel_results = None

        # is the controller available?
        azure_batch_state, ip_addr, controller_port, tensorboard_port = \
            self.get_azure_box_addr(workspace, job_id, node_index)

        if ip_addr and controller_port:
            # add workspace to run_names
            first_run_name = run_names[0]
            run_names = [workspace + "/" + run_name for run_name in run_names]

            try:
                # from xtlib.client import Client

                # client = Client(self.config, self.store, self.core)
                # if client.connect_to_controller(ip_addr=ip_addr, port=controller_port):
                #     # send request to controller via the client service
                #     cancel_results = client.cancel_runs(run_names)
                #     cancelled_by_controller = True

                from xtlib.xt_client import XTClient
                from xtlib import run_helper

                cs, box_secret = run_helper.get_client_cs(self.core, workspace, first_run_name)
                if not cs:
                    console.print("could not find info for run: {}/{}".format(workspace, first_run_name))
                else:
                    with XTClient(self.config, cs, box_secret) as xtc:
                        if xtc.connect():
                            result = xtc.cancel_runs(run_names)

            except BaseException as ex:
                #errors.report_exception(ex)
                pass

        if not cancelled_by_controller:
            # run is in a node that waiting for a pool or has left pool; just kill the whole node
            run_datas = [ {"ws_name": workspace, "run_name": run_name} for run_name in run_names ]
            cancel_results, pool_id = self.cancel_job_node(self.store, workspace, job_id, node_index, run_datas)

        return cancel_results        

    def cancel_runs_by_job(self, job_id, runs_by_box, workspace=None):
        '''
        Args:
            job_id: the name of the job containing the run_names
            runs_by_box: a dict of box_name/run lists
        Returns:
            cancel_results_by box: a dict of box_name, cancel_result records
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''
        pool_id = None
        cancel_results_by_box = {}
        workspace = None

        for node_index, box_name in enumerate(runs_by_box.keys()):

            run_datas = runs_by_box[box_name]
            run_names = [rd["run_name"] for rd in run_datas]

            if not workspace:
                # set workspace from first run of job
                workspace = run_datas[0]["ws_name"]

            self.cancel_runs_by_names(workspace, run_names, box_name)

        # for now, do both of these to ensure the job has completed shut down
        terminate_job_explictly = True
        delete_pool = True

        if terminate_job_explictly:
            # terminate the JOB
            try:
                self.batch_client.job.terminate(job_id, terminate_reason="cancelled by user")
                #console.print("job terminated: " + str(job_id))
            except BaseException as ex:
                # avoid rasing errors here (could be a quicktest workspace re-creation issue)
                pass

        if delete_pool and pool_id:
            # delete the POOL (to ensure job charges terminate)
            try:
                self.batch_client.pool.delete(pool_id)
                console.print("pool deleted: " + str(pool_id))
            except:
                pass

        return cancel_results_by_box

    def get_active_jobs(self, ws_name):
        ''' return a list of job_id's running on this instance of Azure Batch '''
        if not self.batch_client:
            self.create_batch_client()

        jobs = self.batch_client.job.list()

        # state values can be one of: 'active', 'disabling', 'disabled', 'enabling', 'terminating', 'completed', 'deleting'
        active_states = ["active", "disabling", "disabled", "enabling"]

        job_ids = [job.id for job in jobs if job.state in active_states]
        return job_ids


    def cancel_runs_by_user(self, ws_name, box_name):
        '''
        Args:
            box_name: the name of the box the runs ran on (pool service)
        Returns:
            cancel_results: a list of kill results records 
                (keys: workspace, run_name, exper_name, killed, status, before_status)
        '''
        cancel_results_by_box = {}

        # get list of active jobs from batch
        job_ids = self.get_active_jobs(ws_name)
        console.diag("after get_active_jobs()")

        if job_ids:
            # get runs_by_job data from MONGO
            db = self.store.get_database()

            filter_dict = {}
            filter_dict["job_id"] = {"$in": job_ids}
            filter_dict["username"] = self.username

            fields_dict = {"runs_by_box": 1}

            job_records = db.get_info_for_jobs(ws_name, filter_dict, fields_dict)
            console.diag("after get_info_for_jobs()")

            # cancel each ACTIVE job
            for job in job_records:
                job_id = job["_id"]
                runs_by_box = job["runs_by_box"]

                kr_by_box = self.cancel_runs_by_job(job_id, runs_by_box)

                cancel_results_by_box.update(kr_by_box)

        return cancel_results_by_box

    def get_node_task(self, service_node_info):
        # get task_id
        if not self.batch_client:
            self.create_batch_client()
        
        batch_job_id = service_node_info["batch_job_id"]
        task_index = service_node_info["task_index"]

        task_id = "task" + str(task_index)
        task = self.batch_client.task.get(batch_job_id, task_id)

        return task

    # BACKEND API
    def get_node_status(self, service_node_info):

        task = self.get_node_task(service_node_info)
        return task.state.value

    # BACKEND API
    def get_log_reader(self, service_node_info):
        self.create_batch_client()

        log_reader = BatchLogReader(self.store, self.batch_client, self, service_node_info)
        return log_reader

    # API call
    def get_simple_status(self, status):
        # translates an BATCH status to a simple status (queued, running, completed)

        queued = ["active", "preparing"]
        running = ["running"]
        completed = ["completed"]

        if status in queued:
            ss = "queued"
        elif status in running:
            ss = "running"
        elif status in completed:
            ss = "completed"
        else:
            errors.warning("unexpected Azure Batch status value: {}".format(status))

        return ss

    # API call
    def cancel_job(self, service_job_info, service_info_by_node):
        result_by_node = {}
        node_end_times = {}

        for node_id, node_info in service_info_by_node.items():
            result, node_end_time = self.cancel_node(node_info)

            result_by_node[node_id] = result
            node_end_times[node_id] = node_end_time

        # NOTE: we currently don't explictly cancel the job (since it is cancelled when all tasks are cancelled)

        return result_by_node, node_end_times

    # API call
    def cancel_node(self, service_node_info):
        task = self.get_node_task(service_node_info)

        service_status = task.state.value
        simple_status = self.get_simple_status(service_status)
        cancelled = False
        node_end_time = None

        if simple_status in ["error", "completed", "cancelled"]:
            # node already ended
            node_end_time = task.state_transition_time.timestamp()
            
        else:
            # node is alive - cancel it
            batch_job_id = service_node_info["batch_job_id"]
            self.batch_client.task.terminate(batch_job_id, task.id)

            # refresh the task for updated status
            task = self.get_node_task(service_node_info)

            service_status = task.state.value
            simple_status = self.get_simple_status(service_status)
            cancelled = (simple_status == "completed")   
            node_end_time = time.time()  

        result = {"cancelled": cancelled, "service_status": service_status, "simple_status": simple_status}
        return result, node_end_time

    # API call
    def add_service_log_copy_cmds(self, ca, cmds, dest_dir, args):
        # this used to be done by the batch service but that stopped working with insufficient diagnostics
        # so now we do it as part of our end-of-script upload
        ca.append(cmds, "mkdir -p {}".format(dest_dir))
        
        cmd1 = "cp /usr/logs/std*.txt {}".format(dest_dir)
        cmd2 = "cp $XT_ORIG_WORKDIR/../std*.txt {}".format(dest_dir)

        if_cmd = 'if [ $XT_IN_DOCKER -eq 1 ]; then {}; else {}; fi'.format(cmd1, cmd2)
        ca.append(cmds, if_cmd)
        pass


    def get_ssh_creds(self, config, job_id, node_index, workspace_id):
        import azure.batch as batch
        import azure.batch.batch_auth as batch_auth

        # get batch credentials
        service_name = "xtsandboxbatch"
        batch_creds = config.get_service(service_name)
        batch_name = service_name
        batch_key = batch_creds["key"]
        batch_url = batch_creds["url"]

        credentials = batch_auth.SharedKeyCredentials(batch_name, batch_key)
        batch_client = batch.BatchServiceClient(credentials, batch_url= batch_url)
        compute_node_ops = batch_client.compute_node

        # get compute node
        store_id = config.get("store")
        batch_job_id = "{}__{}__{}".format(store_id, workspace_id, job_id)

        node_index = 0
        task_id = "task" + str(node_index)
        task = batch_client.task.get(batch_job_id, task_id)

        node_info = task.node_info
        if not node_info:
            errors.user_error("node information for job is not available (job is not yet or no longer active)")
            
        pool_id = node_info.pool_id
        node_id = node_info.node_id

        node = batch_client.compute_node.get(pool_id, node_id)
        #ip_address = node.ip_address

        result = compute_node_ops.get_remote_login_settings(pool_id, node_id)
        ip_addr = result.remote_login_ip_address
        port = result.remote_login_port

        # create the xt-user for this node
        user_name = "xt-user"
        pw = "kt#abc!@XTwasHere"
        is_admin = True
        user = compute_node_ops.models.ComputeNodeUser(name=user_name, password=pw, is_admin=is_admin)

        try:
            compute_node_ops.add_user(pool_id, node_id, user)
        except:
            # ignore if user already exists
            pass

        return {"user": user_name, "pw": pw, "ip_addr": ip_addr, "port": port}

    # API call
    def get_log_files_dir(self, args):
        docker_cmd = args["docker_cmd"]

        path = "/usr/logs" if docker_cmd else "$XT_ORIG_WORKDIR/.."
        return path

    # API call
    def get_timestamped_status_of_nodes(self, service_name, service_info_list):
        sd = {}

        if self.batch_client is None:
            self.create_batch_client()
    
        missing_tasks = 0

        for si in service_info_list:
            if not si:
                sd[node_id] = (None, None)

            else:
                batch_job_id = si["batch_job_id"]
                task_index = si["task_index"]

                task_id = "task" + str(task_index)
                node_id = si["node_id"]

                try:
                    task = self.batch_client.task.get(batch_job_id, task_id)
                    status = self.get_simple_status(task.state)
                    #print("    id: {}, status: {}".format(task.id, status))
                    dt_end = task.state_transition_time
                    end_time = arrow.get(dt_end)
                    sd[node_id] = (status, end_time)
                except BaseException as ex:
                    #print("error trying to access batch task_id: {}, {}".format(task_id, ex.error.code))
                    sd[node_id] = (None, None)

        return sd

    # API call
    def get_status_of_nodes(self, service_name, experiment_name, service_info_list):
        sd = {}

        started = time.time()
        print("  getting {:,} specified BATCH tasks".format(len(service_info_list)))

        if self.batch_client is None:
            self.create_batch_client()
    
        missing_tasks = 0

        for si in service_info_list:
            batch_job_id = si["batch_job_id"]
            task_index = si["task_index"]

            task_id = "task" + str(task_index)
            node_id = si["node_id"]

            try:
                task = self.batch_client.task.get(batch_job_id, task_id)
            except BaseException as ex:
                #print("error trying to access batch task_id: {}, {}".format(task_id, ex.error.code))
                sd[node_id] = None
                missing_tasks += 1
            else:
                status = str(task.state)
                print("    id: {}, status: {}".format(task.id, status))
                sd[node_id] = status

        elapsed = time.time() - started
        print("  missing batch tasks: {:,}".format(missing_tasks))
        print("  enumerated {:,} desired runs ({:.2f} secs)".format(len(service_info_list), elapsed))

        return sd

    # API call
    def get_status_of_jobs(self, workspace, jobs):
        sd = {}

        if self.batch_client is None:
            self.create_batch_client()

        job_error_count = 0

        for job in jobs:
            job_id = job["job_id"]

            try:
                job_obj = self.batch_client.job.get(job_id)
            except BaseException as ex:
                #print("error getting Batch JOB for: {}, ex: {}".format(job_id, ex.error.code))
                sd[job_id] = None        # user deleted job from Batch Explorer; which would have cancelled it if it was running
                job_error_count += 1
            else:
                status = job_obj.status
                print("job: {}, status: {}".format(job_id, status))
                sd[job_id] = job_obj.status

        if job_error_count:
            print("Batch jobs not found: {:,}".format(job_error_count))

        return sd


class BatchLogReader():
    def __init__(self, store, batch_client, batch_backend, service_node_info, encoding='utf-8'):
        self.store = store
        self.batch_client = batch_client
        self.batch_backend = batch_backend
        self.service_node_info = service_node_info
        self.encoding = encoding

        self.log_source = None
        self.start_offset = 0
        self.use_best_log=True
        self.task = None
        self.end_offset = 1024*1024*1024*16     # 16 GB should be big enough for a log file
        self.file_not_found_count = 0
        self.refreshed_cred_count = 0

        self.job_id = service_node_info["job_id"]
        self.batch_job_id = service_node_info["batch_job_id"]
        self.node_id = service_node_info["node_id"]
        self.workspace = service_node_info["workspace"]

    def get_task(self, force=False):
        # this is done JIT since we may not need it (if we are reading from storage)
        # should be done only initially or when auth cert expires
        # this call can take up to 15 secs (used to, but seems faster in Jul-2024)

        if force:
            self.batch_backend.create_batch_client()  # force this to be recreated

        # sometimes this fails with "Request date headers too old" error
        for i in range(5):
            try:
                task = self.batch_backend.get_node_task(self.service_node_info)
                #print("new task object created: task.state: {}".format(task.state))
                break

            except BaseException as ex:
                console.print("monitor exception: {}".format(ex))
                time.sleep(3)

        if not task:
            errors.service_error("fatal Azure Batch communication failure")

        return task

    def find_log_on_storage(self):
        from_storage = False
        new_text = None
        batch_status = None
        simple_status = None

        for log_name in ["stdboth.txt", "stdout.txt"]:

            # try to first read from job storage (if task has completed)
            node_index = utils.node_index(self.node_id)

            # look under "service_logs"
            job_path = "nodes/node{}/after/service_logs/{}".format(node_index, log_name)
            if self.store.does_job_file_exist(self.workspace, self.job_id, job_path):
                new_text = self.store.read_job_file(self.workspace, self.job_id, job_path)
                batch_status = "completed"
                simple_status = "completed"
                from_storage = True
                self.log_source = "after_logs"
                break

            # look under "xt_logs"  (legacy?)
            job_path = "nodes/node{}/after/xt_logs/{}".format(node_index, log_name)
            if self.store.does_job_file_exist(self.workspace, self.job_id, job_path):
                new_text = self.store.read_job_file(self.workspace, self.job_id, job_path)
                batch_status = "completed"
                simple_status = "completed"
                from_storage = True
                self.log_source = "after_logs"
                break

        return from_storage, new_text, batch_status, simple_status, log_name

    def refresh_creds(self):
        self.batch_backend.config.refresh_credentials()

        # must update our batch_client
        self.batch_client = self.batch_backend.batch_client

        # create a new task object
        self.task = self.get_task(force=True)

    def read(self):
        '''
        returns a node's log information from:
            - live log (if task is still running)
            - log file node storage (if task has completed)
        '''
        new_text = None
        batch_status = None
        simple_status = None
        from_storage = False
        log_name = None

        if self.log_source != "live":
            # only check this one per monitor session
            from_storage, new_text, batch_status, simple_status, log_name = self.find_log_on_storage()

        if not from_storage:
            self.log_source = "live"

            if self.task is None:
                # only do this once per monitor session
                self.task = self.get_task()

            node_info = self.task.node_info
            batch_status = self.task.state.value
            simple_status = self.batch_backend.get_simple_status(batch_status)

            gft_opts = batchmodels.FileGetFromTaskOptions(ocp_range='bytes={}-{}'.format(self.start_offset, self.end_offset))

            try:
                # stdboth is a .TMP file when it is read live
                log_name = "stdboth.txt" 

                stream = self.batch_client.file.get_from_task(self.batch_job_id, self.task.id, file_path=log_name, 
                    file_get_from_task_options=gft_opts)

                # put streamed output into "output"
                output = io.BytesIO()

                for data in stream:
                    output.write(data)

                new_bytes = output.getvalue()
                new_text = new_bytes.decode(self.encoding)
                self.start_offset += len(new_bytes)

            except BaseException as ex:
                # interpret this error as task has terminated
                ex_text = str(ex)

                ex_code = ex.error.code if hasattr(ex, "error") else None
                ex_message = ex.message.value if hasattr(ex, "message") else None
                ex_lines = ex_text.split("\n")
                ex_reason = [ex_line for ex_line in ex_lines if ex_line.startswith("Reason: ")]
                ex_reason = ex_reason[0] if ex_reason else None

                if ex_reason and "cannot be accessed as the task state is still active" in ex_reason:   
                    # task not yet started
                    #console.print("==> task not yet started; will retry read after delay.")
                    time.sleep(10)

                else:
                    # display full exception
                    time_of_day_str = datetime.datetime.now().strftime("%H:%M:%S")
                    console.print("==> @{}: Exception reading batch log file (LIVE): {}".format(time_of_day_str, ex))

                    if "Code: PoolNotFound" in ex_text or "Code: NodeNotReady" in ex_text or "Code: NodeNotFound" in ex_text:
                        # pool has been deleted (task is terminated)
                        console.print("==> pool has been deleted (task is terminated); forcing status to 'completed'")
                        batch_status = "completed"
                        simple_status = "completed"
                    
                    elif "ConnectionError" in ex_text:
                        # print & retry it after a delay
                        console.print("connection error; will retry read after delay.")
                        time.sleep(3)
                    
                    elif "Code: FileNotFound" in ex_text:
                        # we are running but the log file is not yet created
                        # allow this to happen a few times, then log it after that
                        self.file_not_found_count += 1
                        
                        # if self.file_not_found_count > 3:
                        #     console.print("Exception reading batch log file (LIVE): {}".format(ex))
                    
                    elif "Code: AuthenticationFailed" in ex_text:
                        # our authentification has expired; we need to re-authenticate
                        print("authentication failed; will refresh credentials and retry read after delay.")
                        # if self.refreshed_cred_count > 1:
                        #     # during debug phase, we don't want to get stuck in a loop
                        #     raise ex

                        self.refresh_creds()
                        self.refreshed_cred_count += 1 

                    else:
                        console.print("Unexpected exception; will retry read after delay")

        return {"new_text": new_text, "simple_status": simple_status, "log_name": log_name, 
            "service_status": batch_status, "file_path": log_name,  "found_file": from_storage, 
            "log_source": self.log_source, "from_storage": from_storage}

