#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# xt_vault.py: retreives secrets from the xt vault services
''' 
it works!  "no device code" authentication in browser, just like Azure Portal and CLI.
'''
import os
import json
import time

from xtlib import utils
from xtlib import errors
from xtlib import console
from xtlib import pc_utils
from xtlib import constants
from xtlib import file_utils
from xtlib.node_creds import NodeCreds

class XTVault():

    def __init__(self, vault_url, store_name, secret_name):
        self.vault_url = vault_url
        self.store_name = store_name
        self.client = None
        self.authentication = None
        self.keys = None
        self.secret_name = secret_name
        self.credential = None
        self.node_creds = None

    def init_creds(self, authentication):
        cache_client = None    # CacheClient()
        loaded = False
        self.authentication = authentication

        loaded = self._load_grok_creds()
        if not loaded:
            loaded = self._load_node_creds()
        if not loaded:   #  and self.vault_url:
            # normal XT client
            creds = None    # cache_client.get_creds(self.store_name)
            if creds:
                self.apply_creds(creds)
            else:
                creds = self._get_creds_from_login(authentication, reason="cache not set")
                #cache_client.store_creds(self.store_name, creds)

    def _load_grok_creds(self):
        fn_keys = "keys.bin"
        loaded = False

        if not os.path.exists(fn_keys):
            fn_keys = os.path.expanduser("~/.xt/stores/{}/keys.bin".format(self.store_name))

        console.diag("looking for grok_creds: {}".format(fn_keys))

        if os.path.exists(fn_keys):
            # GROK server creds
            creds = file_utils.read_text_file(fn_keys)  
            self.apply_creds(creds)

            fn_cert = os.path.join(os.path.dirname(fn_keys), "xt_cert.pem")
            if os.path.exists(fn_cert):
                cert = file_utils.read_text_file(fn_keys) 
                self.keys["xt_server_cert"] = cert

            console.diag("init_creds: using grok server 'keys.bin' file")
            loaded = True

        return loaded

    def _load_node_creds(self):
        loaded = False

        if not self.node_creds:
            self.node_creds = NodeCreds()

        store_creds, db_creds = self.node_creds.get_store_and_db_creds_on_compute_node()
        if store_creds:
            # creds are limited in this case to just Store access [storage + db_creds]
            kv = {}
            if store_creds:
                kv[store_creds["name"]] = store_creds["key"]

            if db_creds:
                kv[db_creds["name"]] = db_creds["connection-string"]

            creds = json.dumps(kv)
            self.apply_creds(creds)

            console.print("init_creds: using compute node ENV VAR settings")
            loaded = True

        return loaded

    def get_creds_core(self, authentication):
        used_browser = False

        if not self.credential:
            from azure.identity import InteractiveBrowserCredential, TokenCachePersistenceOptions, AuthenticationRecord, ManagedIdentityCredential

            # open the serialized azure authentication record (contains no secrets)
            dir_name = file_utils.get_xthome_dir()
            fn = dir_name + "/azure_cred_cache.txt"        
            deserialized_record = None

            if os.path.exists(fn):
                with open(fn, "rt") as infile:
                    cred_json = infile.read()
                    deserialized_record = AuthenticationRecord.deserialize(cred_json)

            if authentication == "auto":
                uami_client_id = os.getenv("XT_UAMI_CLIENT_ID", None)

                if uami_client_id:
                    authentication = "managed-identity"

                elif pc_utils.has_gui():
                    authentication = "browser"

                else:
                    authentication = "device-code"

            if authentication == "browser":
                if not deserialized_record:
                    console.print("authenticating with azure thru browser... ", flush=True, end="")
                    used_browser = True
                
                cpo = TokenCachePersistenceOptions(allow_unencrypted_storage=True)

                # experiment
                client_id = "2e17b368-85c5-4b5f-b0ce-fdeb1d3d7339"
                tenant_id = "72f988bf-86f1-41af-91ab-2d7cd011db47"                      

                # do we really need all of these options?  causing problems when trying to acess TPX storage/sql
                # credential = InteractiveBrowserCredential(client_id=client_id, tenant_id=tenant_id, cache_persistence_options=cpo, 
                #     authentication_record=deserialized_record, additionally_allowed_tenants=['*'])

                # additionally_allowed_tenants=['*'] allows user to authenticate with any tenant (supports access to singularity)

                credential = InteractiveBrowserCredential(cache_persistence_options=cpo, authentication_record=deserialized_record,
                    additionally_allowed_tenants=['*'])

            elif authentication == "managed-identity":
                # this is for running on Azure VMs
                credential = ManagedIdentityCredential(client_id=uami_client_id) 

            elif authentication == "device-code":
                '''
                This apparently does NOT support caching.  We can't make user authenticate
                thru browser on separate machine every time he wants to run an XT command.
                '''
                # console.print("authenticating with azure thru device code... ", flush=True, end="")
                from azure.identity import DeviceCodeCredential

                console.print("using device-code authorization")
                credential = DeviceCodeCredential() 

            else:
                errors.user_error("unrecognized authentication type '{}'".format(authentication))

            if not deserialized_record:
                # serialize to our cred to disk
                record = credential.authenticate()        # force immediate authentication
                cred_json = record.serialize()

                file_utils.ensure_dir_exists(file=fn)
                
                with open(fn, "wt") as outfile:
                    outfile.write(cred_json)

            self.credential = credential

            # test credential (debug)
            #self.test_credential(credential)

        return self.credential, used_browser

    def test_credential(self, credential):
        from azure.storage.blob import BlobServiceClient
        
        container_name = "00-share-data"
        storage_url="https://sandboxstoragev2s.blob.core.windows.net"              # URL of storage account

        blob_service_client = BlobServiceClient(storage_url, credential=credential)
        container_client = blob_service_client.get_container_client(container_name)
        exists = container_client.exists()
        print("container exists=", exists)

    def _get_creds_from_login(self, authentication, reason=None):

        # use normal Key Value
        from azure.keyvault.secrets import SecretClient
        #from azure.identity import DefaultAzureCredential

        credential, used_browser = self.get_creds_core(authentication)

        if used_browser:
            console.print("authenticated successfully", flush=True)

        # expires = outer_token[1]
        # elapsed = expires - time.time()
        #print(" [new token expires in {:.2f} mins] ".format(elapsed/60), end="")

        # get keys from keyvault
        if self.vault_url:
            self.client = SecretClient(self.vault_url, credential=credential)
            key_text = self.get_secret_live(self.secret_name)

            #xt_client_cert = self.get_secret_live("xt-clientcert")
            xt_server_cert = self.get_secret_live("xt-servercert")

            # write all our creds to self.keys
            self.apply_creds(key_text)
            self.keys["xt_server_cert"] = xt_server_cert

            # for some reason, credentials returned from InteractiveBrowserCredential w/serialization
            # no longer works for this AAD call

        else:
            self.keys = {}

        gd = self.get_me_graph_property(credential, None)

        display_name = gd["displayName"]
        mail = gd["mail"]
        self.keys["display_name"] = display_name

        # during security chaos, ensure user knows how he has been authenticated
        print("AUTHENTICATION: {}".format(mail))

        # return creds as json string
        return json.dumps(self.keys)

    def apply_creds(self, creds_text):
        try:
            self.keys = json.loads(creds_text)
        except BaseException as ex:
            msg = "Error in parsing vault secret '{}' as JSON string: {}".format(self.secret_name, ex)
            errors.general_error(msg)

    def get_secret(self, id):
        # returned cached copy (only ever needs 1 roundtrip)
        if self.keys:
            if not id in self.keys:
                errors.creds_error("Missing key in memory vault: {}".format(id), show_stack=True)

            return self.keys[id]

        return None

    def get_secret_live(self, id):
        secret_bundle = self.client.get_secret(id)
        secret = secret_bundle.value
        return secret

    def get_me_graph_property(self, credential, property_name):
        import requests

        scope = "https://graph.microsoft.com/.default"
        outer_token = credential.get_token(scope)
        token = outer_token.token

        # The HTTP headers with the access token
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        # Example: Get the logged-in user's profile
        response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
        data = response.json()
        #rint(data)

        value = data[property_name] if property_name else data
        return value


