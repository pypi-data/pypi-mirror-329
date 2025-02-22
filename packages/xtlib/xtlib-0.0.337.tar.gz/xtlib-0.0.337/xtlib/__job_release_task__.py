# __job_release_task__.py: small module called from end of job processing by Azure Batch
# to resize & delete the associated pool.  This is needed to avoid charges for the pool.
import os
import sys
import datetime

from azure.batch import BatchServiceClient
from azure.batch import models
from azure.identity import ManagedIdentityCredential, InteractiveBrowserCredential
from msrest.authentication import BasicTokenAuthentication

if True:    # set to False to test locally
    uami_client_id = os.getenv("XT_UAMI_CLIENT_ID")
    credential = ManagedIdentityCredential(client_id=uami_client_id)   # ManagedIdentityCredential()
else:
    credential = InteractiveBrowserCredential()

pool_id = sys.argv[1]
batch_url = sys.argv[2]

 # convert the new style credential into a token that can be used by BatchServiceClient
token = credential.get_token("https://batch.core.windows.net/.default").token
token_config = {"access_token": token}
token_credential = BasicTokenAuthentication(token_config)

batch_service_client = BatchServiceClient(credentials=token_credential, batch_url=batch_url)

try:
    # must resize to 0 before deleting, or tasks will be requeued 
    resize_param = models.PoolResizeParameter(target_dedicated_nodes=0, target_low_priority_nodes=0,
       resize_timeout=datetime.timedelta(minutes=10), node_deallocation_option="terminate") 
     
    batch_service_client.pool.resize(pool_id, resize_param)
    print("pool resized to 0: ", pool_id)
except Exception as ex:
    print("error resizing pool:", ex)

try:    
    # delete the pool
    batch_service_client.pool.delete(pool_id)
    print("pool deleted: ", pool_id)
except Exception as ex:
    print("error deleting pool:", ex)
