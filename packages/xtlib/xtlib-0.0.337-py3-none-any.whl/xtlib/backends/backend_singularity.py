# backend_singularity.py: reflects new Singularity SDK as of Jul-03-2024

import os
import json
import time
import urllib
from xtlib.backends.backend_aml import AzureML
from xtlib import utils

from azure.identity import InteractiveBrowserCredential, TokenCachePersistenceOptions, AuthenticationRecord
from azureml.core.authentication import TokenAuthentication
from azure.ai.ml import command
from azure.ai.ml.entities import Environment
from azure.ai.ml import MLClient, Input, Output
from azure.ai.ml.constants import AssetTypes, InputOutputModes
from azure.ai.ml.entities import UserIdentityConfiguration


# ignore warning messages about experimental classes
import warnings
warnings.filterwarnings("ignore", message=".*is an experimental class.*", category=FutureWarning)

# we leverage the AzureML class to handle common AzureML operations
# and only override the needed methods

class Singularity(AzureML):
    def __init__(self, compute, compute_def, core, config, username=None, arg_dict=None):
        super().__init__(compute, compute_def, core, config, username, arg_dict)

    # API call

    def collect_env_vars(self, job_id, workspace, aml_ws_name, xt_exper_name, aml_exper_name, run_name, node_index,
        node_run, compute_target, username, description, aggregate_dest, args):
        
        node_id = utils.node_id(node_index)

        env_vars = self.build_env_vars(workspace, aml_ws_name, xt_exper_name, aml_exper_name, run_name, job_id=job_id, 
            compute_target=compute_target, username=username, description=description, aggregate_dest=aggregate_dest, 
            node_id=node_id, args=args)
        
        # 2/2 calls to this (TODO: remove one)
        # this second call really updates the env_vars to be passed to singularity for this node run
        self.get_controller_env_vars(env_vars, node_run, node_index, args)

        # add env var for UAMI (User Assigned Managed Identity)
        # should look something like this: /subscriptions/41c6e824-0f66-4076-81dd-f751c70a140b/resourcegroups/xt-sandbox/providers/Microsoft.ManagedIdentity/userAssignedIdentities/xt_user_identity
        env_vars["_AZUREML_SINGULARITY_JOB_UAI"] = args["uami_id"]

        return env_vars


    def submit_node_run(self, job_id, node_run, xt_ws_name, aml_ws_name, xt_exper_name, aml_exper_name, 
        compute_def, resume_name, repeat_count, using_hp, target, runs_by_box, code_dir, node_index, 
        show_aml_run_name, nodes, args):
        '''
        Submit a node run to the specified Singularity compute target.
        Args:
            job_id: the job id (e.g., "job30")
            node_run: the node run to submit (dict of run info)
            xt_ws_name: the XT workspace name (e.g., "xlm")
            aml_ws_name: the name of workspace we will use for Singularity (e.g., "xt-sing-workspace")
            xt_exper_name: the name of the XT experiment as specified by the user (e.g., "rfernand-job55")
            aml_exper_name: unsure of purpose vs.  (e.g., "rfernand__ws5__rfernand-job345")
            compute_def: the compute definition (dict)
            resume_name: the name of the resume file (e.g., "run648.0.r1")
            repeat_count: the number of times to repeat the run (e.g., 1)
            using_hp: whether or not this is an AML hyperparameter run (e.g., False)
            target: the name of the compute target specified by the user (e.g., sing-h100)
            runs_by_box: the runs by box (dict)
            code_dir: the temp. directory containing the code to run (e.g., "C:\\Users\\roland\\appData\local\temp\\...")
            node_index: the index of the node (e.g., 0)
            show_aml_run_name: should the AML run name be displayed on the console (e.g., True)
            nodes: the number of nodes being submitted with this job (e.g., 6)
            args: the arguments for this XT run command
        '''
        credential = self.config.get_credential()

        # xt singularity workspace account info
        vm_size = compute_def["vm-size"]
        vc_name = compute_def["compute"]
        docker_name = compute_def["docker"]

        service_info = self.config.get_service(aml_ws_name)
        #vc_info_from_xt = self.config.get_service(vc_name)

        vc_config = {
            "instance_type": vm_size,
            "instance_count": 1, #Set instance 
            "properties": {
                "AISuperComputer": {
                    "interactive": True,
                    "slaTier": "Premium",            # recommended by GCR (enabled SSH to container)
                    "enableAzmlInt": False,
                    "tensorboardLogDirectory": "/scratch/tensorboard_logs",
                    "scalePolicy": {
                        "autoScaleIntervalInSec": 120,
                        "maxInstanceTypeCount": 1,
                        "minInstanceTypeCount": 1, 
                    },
                }
            },
            "sshPublicKey": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCxt7gAYS/4LvNj6zDCi0BVH3zEgi95BiPPvcbbBvpyGRMEwFAeGnO2kiDxzClKEt5x86mMt9XJl+RNObmjTG09bscSv/WyW85k3HcKHNgbwK9ECY0ck+rCZHUn9tkT57iDkGDWWkeCikQwsKKONglgPrIEmCdAPW9Dix28F0t8fIYhDk4lQgW6boNAq9WXKqo6j9jUuXlHyQeuHwhGUTSx1nwNs4mhTYxJquEy07QquC1yYS+SkrYcYYCS8ilclzHlgoeToMDKXcbCFgFbx7vLVfdUe9NlYf4WvDOPXwtaefSAVNz8un+RVcV0570CvxOVjiOZWax72eKq5RJMpZ5t v-lifli@microsoft.com",
        }

        class vc_info:
            def __init__(self, subscription_id= "156138e5-a3b1-48af-9e2e-883f4df3f457", resource_group="gcr-singularity-lab", vc="dell1"):
                self.subscription_id = subscription_id
                self.resource_group = resource_group
                self.vc = vc
                self.compute_config= "/subscriptions/"+ subscription_id +"/resourceGroups/"+ resource_group +"/providers/Microsoft.MachineLearningServices/virtualclusters/" + vc
                
        if vc_name in ["dell1", "kings01", "kings02", "kings03", "kings04", "kings05", "kings06", "kings07", "kings08", "kings09", "kings10", "kings11", "kings12", "mckinley01", "mckinley02", "mckinley03", "mckinley04", \
            "mckinley05", "mckinley06", "mckinley07", "mckinley08", "barlow01", "barlow02", "barlow03", "barlow04", "barlow05", "barlow06", "barlow07", "barlow08", "barlow09", "msrresrchlab"]:
                vc_info= vc_info(subscription_id= "156138e5-a3b1-48af-9e2e-883f4df3f457", resource_group="gcr-singularity-lab", vc=vc_name)

        elif vc_name in ["baltic01", "baltic02", "baltic03", "baltic04", "baltic05", "baltic06", "baltic07", "baltic08", "baltic09", "baltic10", "baltic11", "baltic12", "huashanvc1", "huashanvc2", "huashanvc3", "huashanvc4"]:
            vc_info= vc_info(subscription_id= "22da88f6-1210-4de2-a5a3-da4c7c2a1213", resource_group="gcr-singularity", vc=vc_name)   

        # TODO: verify new vc names
        elif vc_name in ["msrresrchvc", "msrreschlab", "msrresrchbasicvc"]:
            vc_info= vc_info(subscription_id= "22da88f6-1210-4de2-a5a3-da4c7c2a1213", resource_group="gcr-singularity-resrch", vc=vc_name)

        # TODO: verify new vc names
        elif vc_name in ["msroctovc", "msroctobasicvc"]:
            vc_info= vc_info(subscription_id= "d4404794-ab5b-48de-b7c7-ec1fefb0a04e", resource_group="gcr-singularity-octo", vc=vc_name)

        else:
            raise Exception("unknown vc: {}".format(vc_name))

        # use the connected AML datastore as output
        #output_path = "azureml://datastores/ericdatastoretest/paths/"
        #output_path = "azureml://datastores/tpx_job_output/job_output/"     # currently on tpxstoragev2 
        output_path = "azureml://subscriptions/41c6e824-0f66-4076-81dd-f751c70a140b/resourcegroups/tpx-sing/workspaces/tpx-sing-ws5/datastores/tpx_job_output/paths/job_output/"

        docker_image, login_server, docker_registry, _ = self.config.get_docker_info(target, docker_name, required=False)

        docker_image_url = f"{login_server}/{docker_image}"
        environment = Environment(image=docker_image_url)

        display_name = args["display_name"]
        run_name = node_run["run_name"]
        display_name = utils.expand_xt_vars(display_name, job_id=job_id, run_id=run_name, node_index=node_index)

        # muai_id = args["uami_id"]
        # identity = UserIdentityConfiguration()

        # /bin/bash', '--login', '__node_script__.sh'
        cmd_parts = node_run["run_specs"]["cmd_parts"]
        cmd_line = cmd_parts[-1]         # last part is the command to run (rest is __aml_shim__ stuff)                   

        username = args["username"]
        description = args["description"]
        aggregate_dest = args["aggregate_dest"]

        env_vars_dict = self.collect_env_vars(job_id, xt_ws_name, aml_ws_name, xt_exper_name, aml_exper_name, run_name, 
            node_index, node_run, target, username, description, aggregate_dest, args)

        env_vars_dict["JOB_EXECUTION_MODE"] = "basic"      # "basic"
        env_vars_dict["AZUREML_COMPUTE_USE_COMMON_RUNTIME"] = "true"

        job = command(
            # NOTE: we pass our temp dir used to upload the zipped code to XT storage (so it will already be filtered)
            code=code_dir,       
            command=cmd_line,
            outputs = {"output_data": Output(type=AssetTypes.URI_FOLDER, path=output_path, mode=InputOutputModes.RW_MOUNT)},

            environment=environment,
            environment_variables=env_vars_dict,
            experiment_name= xt_exper_name,    # rfernand_sing_testing", 
            display_name=display_name,
            compute=vc_info.compute_config,
            distribution={
                "type": "PyTorch",
                "process_count_per_instance": 1,                 # How many GPUs
            },
            #identity=identity,
            resources=vc_config)  

        subscription_id = service_info["subscription-id"]
        resource_group = service_info["resource-group"]

        # create the MLCient object, for submitting our job
        ml_client = MLClient(credential, subscription_id=subscription_id, resource_group_name=resource_group, workspace_name=aml_ws_name)
        returned_job = ml_client.jobs.create_or_update(job)      # submit the command
        print(returned_job.studio_url) 

        print("singularity job submitted: experiment={}, job={}".format(job.experiment_name, job.display_name))

        # return node_info: all info needed for this backend (singularity) to later retrieve info about this run
        run_name = node_run["run_name"]
        node_info = {"ws": xt_ws_name, "aml_ws": aml_ws_name, "run_name": run_name, "job_id": job_id, "node_id": utils.node_id(node_index)}

        node_info["aml_exper_name"] = xt_exper_name         # aml_exper_name
        node_info["aml_run_number"] = returned_job.name     # aml_run_number
        node_info["aml_run_id"] = returned_job.name         # aml_run_id

        return node_info

    