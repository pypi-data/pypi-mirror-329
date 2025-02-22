#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# backend_singularity.py: support for running jobs under the Microsoft Singularity platform (similiar to AML and ITP)

import os
import time
import urllib.request

from azureml.core import Environment, Experiment, ScriptRunConfig, Workspace
from azureml.core.authentication import InteractiveLoginAuthentication
from azureml.contrib.aisc.aiscrunconfig import AISuperComputerConfiguration
import azureml.core

from xtlib import utils
from xtlib import errors
from xtlib import constants
from xtlib import file_utils
from xtlib.backends.backend_aml import AzureML
from xtlib.console import console

class Singularity(AzureML):

    def __init__(self, compute, compute_def, core, config, username=None, arg_dict=None, disable_warnings=True):
        super(Singularity, self).__init__(compute, compute_def, core, config, username, arg_dict, disable_warnings)

        # blobfuse is still busted if we are using their default docker images
        # for now, let's assume we are using latest good pytorch-xtlib docker image
        self.mounting_enabled = True   # False
        self.request = None
        self.last_node_started_msg = None

    # API call
    def get_name(self):
        return "singularity"

    # API call
    def provides_container_support(self):
        '''
        Returns:
            returns True if docker run command is handled by the backend.
        Description:
            For Singularity, they only support containers we can cannot run native to launch our own docker.
        '''
        return True   
        
    def update_env_vars(self, env_vars, args):

        # move long/secret env vars into a file
        text = ""
        #for key in ["XT_BOX_SECRET", "XT_SERVER_CERT", "XT_STORE_CREDS", "XT_DB_CREDS"]:
        for key in ["XT_STORE_CREDS", "XT_DB_CREDS"]:
            value = env_vars[key]
            text += "{}={}\n".format(key, value)

            # remove from environt_variables
            del env_vars[key]

        # write text to set_env file in bootstrap dir
        bootstrap_dir = args["bootstrap_dir"]
        fn = bootstrap_dir + "/" + constants.FN_SET_ENV_VARS
        with open(fn, "wt") as outfile:
            outfile.write(text)

    def configure_rc_for_docker(self, rc, trainer, args):
        use_docker = trainer.run_config.docker.use_docker

        if use_docker:
            # old idea: this tells Singularity to use my docker image "as is" (don't build a new image with it as the base)
            # new idea: I don't know what this does anymore
            rc.environment.python.user_managed_dependencies = True

            rc.docker = trainer.run_config.docker  
            rc.docker.use_docker = True
            docker = rc.environment.docker

            old_env = trainer.run_config.environment
            old_registry = old_env.docker.base_image_registry  

            container_registry, image_url, sing_dict = self.get_docker_container_registry(args)
            sing_wrap = utils.safe_value(sing_dict, "sing_wrap")

            if sing_wrap:
                # wrap our docker image with a singularity-compliant image
                docker.base_image = None
                docker.base_image_registry = None

                sha256 = sing_dict["sha256"]
                post_sing_steps = sing_dict["post_sing_steps"]

                if sha256:
                    image_url2 = image_url.split(":")[0] + "@sha256:" + sha256
                else:
                    image_url2 = image_url
                registry_url = old_registry.address

                # tell singularity to upgrade my docker image to be singularity-compliant
                fn = file_utils.get_xtlib_dir() + "/backends/" + constants.FN_BUILD_STEPS_TEMPLATE
                with open(fn, "rt") as infile:
                    build_steps_template = infile.read()
                
                build_steps = build_steps_template.format(registry_url, image_url, registry_url, image_url2)

                # add singularity cleanup commands to docker build steps
                if post_sing_steps:
                    for step in post_sing_steps:
                        build_steps += "\n" + step

                docker.base_dockerfile = build_steps
            
            else:
                # use our docker image directly (no wrapping)
                #docker.base_image = image_url
                docker.base_image = old_registry.address + "/" + image_url
                docker.base_dockerfile = None

                registry = azureml.core.ContainerRegistry()
                docker.base_image_registry = registry
                registry.address = old_registry.address
                registry.username = old_registry.username
                registry.password = old_registry.password


    def update_estimator(self, estimator, gpu_count, preemption_allowed):
        # when submitting an ITP job, we do a JIT install of weird AML K8S dependency
        # (doing it here helps keep pip install for XT working correctly, on client
        # machine as well as ITP compute node).
        cmd = "pip install --upgrade --disable-pip-version-check --extra-index-url " + \
            "https://azuremlsdktestpypi.azureedge.net/K8s-Compute/D58E86006C65 azureml_contrib_k8s"

        fn_log = os.path.expanduser("~/.xt/k8s_install.log")
        cmd += " > {} 2>&1".format(fn_log)
        os.system(cmd)


    def run_job_on_singularity(self, experiment, trainer, arg_parts, run_name, node_index, args):
        ws = experiment.workspace

        armid = (
            f"/subscriptions/{ws.subscription_id}/"
            f"resourceGroups/{ws.resource_group}/"
            "providers/Microsoft.MachineLearningServices/"
            f"virtualclusters/{trainer._compute_target}"
        )

        src = ScriptRunConfig(source_directory=trainer.source_directory, command=arg_parts)

        rc = src.run_config 
        rc.target = "aisupercomputer"
        rc.node_count = 1
        
        # add env vars from trainer
        for name, value in trainer.run_config.environment.environment_variables.items():
            rc.environment_variables[name] = value

        # Neither of these settings will be required once this task is marked Done:
        # https://dev.azure.com/msdata/Vienna/_workitems/edit/1644223
        rc.environment_variables['AZUREML_COMPUTE_USE_COMMON_RUNTIME'] = 'true'
        rc.environment_variables['JOB_EXECUTION_MODE'] = 'basic'
        rc.environment_variables['OMPI_COMM_WORLD_SIZE'] = '1' # SKU=G1
        
        rc.environment = Environment(name="xt_env")

        # enforce Singualrity's max run duration
        # always set "rc.max_run_duration_seconds" since its default of 30 days > singularity max of 14 days
        max_singularity_secs = 1209600       # 14 days
        max_secs = args["max_seconds"]
        if not max_secs:
            max_secs = max_singularity_secs
        if max_secs and max_secs > max_singularity_secs:
            errors.user_error("specified max_seconds={:,} exceeds the singularity maximum={:,}".format(max_secs, max_singularity_secs))

        rc.max_run_duration_seconds = max_secs

        self.configure_rc_for_docker(rc, trainer, args)

        location = utils.safe_value(self.compute_def, "location", None)
        vm_size = utils.safe_value(self.compute_def, "vm-size", None)
        sla_tier = utils.safe_value(self.compute_def, "sla", "basic").capitalize()
        
        experiment = args["experiment"]

        ai = AISuperComputerConfiguration()
        rc.aisupercomputer = ai
        ai.instance_type = vm_size       # "NC6_v3"   
        
        if isinstance(location, list):  
            ai.location = location
        else:
            ai.locations = location

        ai.sla_tier = sla_tier
        ai.image_version = '' 
        ai.scale_policy.auto_scale_interval_in_sec = 47
        ai.scale_policy.max_instance_type_count = 1
        ai.scale_policy.min_instance_type_count = 1
        ai.virtual_cluster_arm_id = armid
        ai.enable_azml_int = False
        ai.interactive = False
        ai.ssh_public_key = None

        # submit the job
        exper = Experiment(workspace=ws, name=experiment)
        run = exper.submit(src)

        display_name = args["display_name"]
        display_name = utils.expand_xt_vars(display_name, run_id=run_name, node_index=node_index, args=args)

        run.display_name = display_name

        #run.wait_for_completion(show_output=True)
        return run
            
    # API call
    def run_job_on_service(self, job_id, workspace, sing_ws_name, trainer, experiment, xt_exper_name, sing_exper_name, compute_target, cwd, run_name, box_name, 
            node_index, repeat, fake_submit, arg_parts, args):
        monitor_cmd = None

        console.diag("before AML experiment.submit(trainer)")

        # SUBMIT the run and return an AML run object
        if fake_submit:
            sing_run = None 
            sing_run_id = "fake_sing_id"
            sing_run_number = 999
        else:
            sing_run = self.run_job_on_singularity(experiment, trainer, arg_parts, run_name, node_index, args)
            sing_run_id = sing_run.id
            sing_run_number = sing_run.number

        # copy to submit-logs
        utils.copy_data_to_submit_logs(args, self.serializable_trainer, "sing_submit.json")

        console.diag("after AML experiment.submit(trainer)")

        jupyter_monitor = args["jupyter_monitor"]
        sing_run_name = sing_exper_name + ".{}".format(run_name)

        # set "xt_run_name" property for fast access to run in future
        if not fake_submit:
            sing_run.add_properties({"xt_run_name": sing_run_name})
            sing_run.set_tags({"xt_run_name": sing_run_name})

        #console.print("  display_name:", sing_run.display_name)
        #console.print("  experiment_url:", sing_run._experiment_url)
        #run_url = sing_run._run_details_url
        #console.print("  run url:", run_url)

        run_url = sing_run.portal_url + "/runs/" + sing_run.id
        console.print("   node {}: {}, {}".format(node_index, sing_run.display_name, run_url))

        if jupyter_monitor:
            fn = self.make_monitor_notebook(sing_ws_name, sing_run_name)
            dir = os.path.dirname(fn)
            #console.print("jupyter notebook written to: " + fn)
            monitor_cmd = "jupyter notebook --notebook-dir=" + dir
        
        return run_name, monitor_cmd, sing_run_name, sing_run_number, sing_run_id

       
    # API call
    def read_log_file(self, service_node_info, log_name, start_offset=0, end_offset=None, 
        encoding='utf-8', use_best_log=True, log_source=None):
        '''
        used by the "xt montior" command to read the log file for a Singularity running job
        '''
        # FN_STDOUT_LOG = "azureml-logs/00_stdout.txt"
        # FN_STDOUT2_LOG = "azureml-logs/70_driver_log.txt"
        # FN_STD_OUT_TXT = "user_logs/std_out.txt"
        # FN_STD_LOG_TXT = "user_logs/std_log.txt"

        from_storage = True
        run = None

        for r in range(3):
            # try 3 times, then just bail
            try:
                run = self.get_node_run(service_node_info)
                break
            except BaseException as ex:
                print("error during get_node_run(): {}".format(ex))
                time.sleep(2)

        if not run:
            errors.env_error(msg="unable to get run for node: {}".format(service_node_info))

        job_id = utils.safe_value(service_node_info, "job_id", service_node_info["aml_exper_name"].split("__")[3])
        node_id =  utils.safe_value(service_node_info, "node_id", "node0")
        workspace = service_node_info["ws"]

        new_text = None
        node_status = "queued"
        next_offset = None
        found_file = False
        
        if start_offset == None:
            start_offset = 0

        if log_name is None:
            file_path = "std_log.txt"
        else:
            file_path = log_name

        if log_source != "live":
            # try to read log from job storage (task has completed)
            node_index = utils.node_index(node_id) 

            job_path = "nodes/node{}/after/service_logs/{}".format(node_index, file_path)
            if self.store.does_job_file_exist(workspace, job_id, job_path):
                new_text = self.store.read_job_file(workspace, job_id, job_path)
                aml_status = "completed"
                simple_status = "completed"
                found_file = True
                log_source = "after_logs"

        if not found_file:
            # read URL of log file from singularity service
            current_details = run.get_details() 
            aml_status = current_details["status"] 
            simple_status = self.get_simple_status(aml_status)
            
            available_logs = None
            next_log = None
            log_name = file_path
            from_storage = False
            log_source = "live"

            if log_name:
                # reuse request for better perf (hopefully)
                log_files = current_details["logFiles"]
                aml_log_path = "user_logs/" + log_name

                # try to read one of Singularity-hosted service logs
                for log_path in [log_name, aml_log_path]:
                    if log_path in log_files:
                        url = log_files[log_path]

                        # create the request object to read the URL
                        if not self.request:
                            self.request = urllib.request.Request(url)
                        elif self.request.full_url != url:
                            #self.request.close()
                            range_hdr = {"Range": f"bytes={start_offset}-"}
                            self.request = urllib.request.Request(url=url, headers=range_hdr)

                        try:
                            # read the URL
                            with urllib.request.urlopen(self.request) as response:
                                all_bytes = response.read()
                        except BaseException as ex:
                            # note: we get exception "invalid range" if no new data is available
                            # treat any error as "no new data"
                            all_bytes = b""

                        if end_offset:
                            new_bytes = all_bytes[start_offset:1+end_offset]
                        else:
                            # since we are now reading with range header, we only get new bytes
                            new_bytes = all_bytes[0:]   #    [start_offset:]

                        new_count = len(new_bytes)

                        # not sure if we have new acceptable text yet, so default to "none found"
                        next_offset = start_offset

                        if new_count:
                            # found some new text
                            text = new_bytes.decode(encoding)
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
                                next_offset = start_offset + new_count
                                new_text = text

                            # debug
                            #print("url:", url)
                        break

        return {"new_text": new_text, "simple_status": simple_status, "log_name": log_name, "next_offset": next_offset, 
            "service_status": aml_status, "from_storage": from_storage, "log_source": log_source}

    # API call
    def add_service_log_copy_cmds(self, ca, cmds, dest_dir, args):

        ca.append(cmds, "mkdir -p {}".format(dest_dir))

        # copy known singularity log directories 
        for log_dir in ["user_logs"]:    # "azureml-logs", "logs",
            from_dir = "$AZUREML_CR_EXECUTION_WORKING_DIR_PATH/{}".format(log_dir)

            ca.append(cmds, "ls -R -lt {}/*".format(from_dir), echo=True)
            ca.append(cmds, "cp -r -v {}/* {}".format(from_dir, dest_dir))

        # this is now copy in user_logs above
        #self.append(cmds, "cp -r -v $AZUREML_CR_EXECUTION_WORKING_DIR_PATH/user_logs/std_log.txt {}".format(dest_dir))

    # API call
    def get_log_files_dir(self, args):
        # singularity adds the "userlogs" at the end
        return "$AZUREML_CR_EXECUTION_WORKING_DIR_PATH/user_logs"