# node_creds.py: handles getting credentials on compute node using Azure Managed Identity
import os
import json
from azure.identity import ManagedIdentityCredential

from xtlib import utils

class NodeCreds():
    def __init__(self) -> None:
        self.node_credential = None

        # # print all env var names/values
        # print("============ defined env vars: ===============")
        
        # key_list = list(os.environ.keys())
        # key_list.sort()

        # for key in key_list:
        #     if key.startswith("XT_"):
        #         print(key, "=", os.getenv(key))

        # print("===============================================")
        
        if os.getenv("XT_STORE_CREDS"):
            # we are running on a compute node (in controller.py, user script, node_post_wrapup.py, etc.)
            uami_client_id = os.getenv("XT_UAMI_CLIENT_ID")
            self.node_credential = ManagedIdentityCredential(client_id=uami_client_id)  

    def get_store_and_db_creds_on_compute_node(self):
        # TODO: remove this (now obsolete) method 

        store_creds = None
        db_creds = None

        store_creds64 = os.getenv("XT_STORE_CREDS")

        if store_creds64:
            store_creds_json = utils.base64_to_text(store_creds64)
            store_creds = json.loads(store_creds_json)

        db_creds64 = os.getenv("XT_DB_CREDS")
        if db_creds64:
            db_creds_json = utils.base64_to_text(db_creds64)
            db_creds = json.loads(db_creds_json)

        if self.node_credential:
            store_creds["credential"] = self.node_credential
            db_creds["credential"] = self.node_credential

        # print("get_store_and_db_creds_on_compute_node: node_credential=", self.node_credential)
        # print("store_creds=", store_creds)
        # print("db_creds=", db_creds)

        return store_creds, db_creds        