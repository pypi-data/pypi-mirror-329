#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# store-azure-blob-1212: Azure Blob Storage API (based on azure-storage-blob==12.18.3)
#
# ==> this is our new STORAGE DRIVER as of Dec-03-2023
#
import os
import re
import time
from pytz import NonExistentTimeError
import requests
import logging
import numpy as np
from interface import implements

from azure.storage.blob import BlobServiceClient

from xtlib import utils
from xtlib import errors
from xtlib import console
from xtlib import file_utils
from xtlib.storage.store_interface import StoreInterface

logger = logging.getLogger(__name__)

# warn user before we trip over confusing OS error for long paths
MAX_PATH = 259 if os.name == "nt" else 4096

class AzureBlobStore_12_18(implements(StoreInterface)):

    def __init__(self, storage_creds, max_retries=25, pool_connections=25, max_put_size=64):
        self.storage_id = storage_creds["name"]
        self.storage_key = storage_creds["key"] if "key" in storage_creds else None
        self.pool_connections = utils.safe_value(storage_creds, "pool_connections", pool_connections)
        self.credential = storage_creds["credential"]

        self.current_blob_etag = None
        self.max_retries = max_retries    

        # default is 64MB, but that causes network errors from home connections with slow upload speeds
        self.max_put_size = max_put_size

        self.reset_connection()

    # ---- HELPER functions ----

    def reset_connection(self):
        '''
        Use for initial connect and to recover from "connection reset" errors
        '''

        # create a custom request session with specified # of pool connections
        # this helps avoid "connection pool closed" warnings
        # ref: https://github.com/Azure/azure-storage-python/issues/413
        sess = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=self.pool_connections, 
            pool_maxsize=self.pool_connections)
        sess.mount('http://', adapter)

        max_put = int(self.max_put_size*1024*1024)    
         
        #cs = "DefaultEndpointsProtocol=https;AccountName={};AccountKey={}==;EndpointSuffix=core.windows.net".format(self.storage_id, self.storage_key)
        #self.blob_service_client  = BlobServiceClient.from_connection_string(cs, max_single_put_size=max_put, max_block_size=max_put)

        storage_url="https://{}.blob.core.windows.net".format(self.storage_id)

        # print("AzureBlobStore CTR")
        # print("  storage_url: {}".format(storage_url))
        # print("  credential: {}".format(self.credential))

        self.blob_service_client = BlobServiceClient(storage_url, credential=self.credential, max_single_put_size=max_put, max_block_size=max_put)

        #print("XT storage driver: using max_put={}".format(max_put))

        self.set_retries(self.max_retries)

    def set_retries(self, count):

        old_count = self.max_retries
        self.max_retries = count

        # bug workaround: standard Retry classes don't retry status=409 (container is being deleted)
        #import azure.storage.common.retry as retry

        self.blob_service_client.retry = utils.make_retry_func(count, self.reset_connection)
        #self.append_bs.retry = utils.make_retry_func(count, self.reset_connection)

        return old_count

    def _is_legal_container_name(self, name):

        if not name:
            return False
            
        if not bool(re.match('^[a-zA-Z0-9-]+$', name)):
           return False
        
        if len(name) < 3:
           return False

        return True

    def _call_with_retry(self, name, func):
        '''
        this replaces normal azure retry callbacks so that we can reset the azure storage connection when 
        needed and correctly retry the call.
        '''
        pass
        
    def _container_check(self, container: str, create_if_needed=False):
        '''
        Validate container name and optionally create it if it doesn't exist.
        '''
        if not container:
            errors.store_error("error: storage container name cannot be blank")

        if not self._is_legal_container_name(container):
            errors.store_error("error: illegal storage container name (must be 3-63 chars in length, only alpha, digits, or '-' allowed): {}"  \
                .format(container))

        if not self.does_container_exist(container):
            if create_if_needed:
                self.blob_service_client.create_container(container)
            else:
                errors.service_error("container not found: {}".format(container))

    # ---- MISC part of interface ----

    def get_service_name(self):
        ''' return the unique name of the storage service'''
        return self.storage_id
    
    def get_retry(self):
        return self.blob_service_client.retry

    def set_retry(self, value):
        self.blob_service_client.retry = value

    # ---- CONTAINER interface ----

    def does_container_exist(self, container: str):
        container_client = self.blob_service_client.get_container_client(container)
        result = container_client.exists()
        return result

    def create_container(self, container: str):
        container_client = self.blob_service_client.get_container_client(container)
        if container_client.exists():
            errors.service_error("container already exists: {}".format(container))

        result = container_client.create_container()
        return result

    def list_containers(self):
        containers = self.blob_service_client.list_containers()
        name_list = [contain.name for contain in containers]
        return name_list

    def delete_container(self, container: str):
        self._container_check(container, create_if_needed=False)

        self.blob_service_client.delete_container(container)
        assert not self.does_container_exist(container)

        return True     # need a non-null return value

    def get_container_properties(self, container: str):
        container_client = self.blob_service_client.get_container_client(container)
        props = container_client.get_container_properties()
        return props

    def get_container_metadata(self, container: str):
        container_client = self.blob_service_client.get_container_client(container)
        props = container_client.get_container_properties()
        return props.metadata

    # ---- BLOB interface ----

    def does_blob_exist(self, container: str, blob_path: str):
        self._container_check(container, create_if_needed=False)

        blob_client = self.blob_service_client.get_blob_client(container, blob_path)
        exists = blob_client.exists()
        return exists

    def create_blob(self, container: str, blob_path: str, text: str, fail_if_exists=False, etag=None):
        self._container_check(container, create_if_needed=True)

        if etag is not None:
            # TODO
            result = self.bs.create_blob_from_text(container, blob_path, text, if_match=etag)
        else:
           # ifn = "*" if fail_if_exists else None
            blob_client = self.blob_service_client.get_blob_client(container, blob_path)
            result = blob_client.upload_blob(text, overwrite=not fail_if_exists)

        return result

    def create_blob_from_path(self, container: str, blob_path: str, source_fn: str, progress_callback=None):
        self._container_check(container, create_if_needed=True)

        blob_client = self.blob_service_client.get_blob_client(container, blob_path)
        with open(source_fn, "rb") as infile:
            result = blob_client.upload_blob(infile, overwrite=True, progress_hook=progress_callback)
        return result

    def append_blob(self, container: str, blob_path: str, text: str, append_with_rewrite=False):
        self._container_check(container, create_if_needed=True)

        # create blob if it doesn't exist
        if not append_with_rewrite:
            # normal handling for append blob
            blob_client = self.blob_service_client.get_blob_client(container, blob_path)
            if not blob_client.exists():
                blob_client.create_append_blob()

            return blob_client.append_block(text)

        ''' 
        Appends text to a normal block blob by reading and then rewriting the entire blob.
        Correctly handles concurrency/race conditions.
        Recommended for lots of small items (like 10,000 run names).

        Note: we turn off retries on azure CALL-level so that we can retry on 
        OUR CALL-level.
        '''
        # experimental local retry loop
        # TODO
        old_retry = self.bs.get_retry()
        self.bs.set_retry(utils.make_retry_func(0))
        succeeded = False

        for i in range(20):
            
            try:
                if self.bs.does_blob_exist(container, blob_path):
                    # read prev contents
                    blob_text = self.bs.get_blob_text(container, blob_path)
                    # append our text
                    new_text = blob_text + text
                    # write blob, ensuring etag matches (no one updated since above read)
                    self.bs.create_blob(container, blob_path, new_text, if_match=blob.properties.etag)
                else:
                    # if no previous blob, just try to create it
                    self.bs.create_blob(container, blob_path, text)
            except BaseException as ex:
                logger.exception("Error in _append_blob_with_retries, ex={}".format(ex))
                sleep_time = np.random.random()*4
                console.diag("XT store received an expected azure exception; will backoff for {:.4f} secs [retry #{}]".format(sleep_time, i+1))
                time.sleep(sleep_time)
            else:
                succeeded = True
                break

        # restore retry
        self.bs.set_retry(old_retry)

        if not succeeded:
            errors.service_error("_append_blob_with_rewrite failed (too many retries)")


    def list_blobs(self, container: str, path: str=None, return_names=True, recursive=True):
        '''
        NOTE: the semantics here a tricky

        if recursive:
            - return a flat list of all full path names of all files (no directory entries)
        else: 
            - return a flat list of all files and all directory names (add "/" to end of directory names)

        if return_names:
            - return list of names
        else:
            - return a list of objects with following properties:
                .name     (file pathname)
                .properties
                    .content_length   (number)
                    .modified_ns      (time in ns)

        The delimiter trick: this is when we set the delimiter arg = "/" to tell azure to return only the blobs 
        in the specified directory - that is, don't return blobs from child directories.  In this case, azure 
        returns the effective child directory name, followed by a "/", but not its contents (which we hope is faster).
        '''
        self._container_check(container, create_if_needed=True)

        delimiter = None if recursive else "/"

        # specific Azure path rules for good results
        if path:
            if path.startswith("/"):
                path = path[1:]     # blob API wants this part of path relative to container

            # we should only add a "/" if path is a folder path
            if path.endswith("*"):
                # we just need to block the addition of "/"
                path = path[0:-1]
            elif not path.endswith("/"):
                # if self.bs.exists(container, path):
                #     # special case for "list" of a single blob
                #     pass
                # else:
                #     path += "/"         # treat as directory
                path += "/"     # treat as directory

        # blobs = self.bs.list_blobs(container, prefix=path, delimiter=delimiter)

        container_client = self.blob_service_client.get_container_client(container)

        if delimiter:
            blobs = container_client.walk_blobs(path, delimiter=delimiter)
        else:
            blobs = container_client.list_blobs(path)

        if return_names:
            blobs = [blob.name for blob in blobs]
        else:
            blobs = list(blobs)

        return blobs

    def delete_blob(self, container: str, blob_path: str, snapshot=None):
        self._container_check(container, create_if_needed=False)
        container_client = self.blob_service_client.get_container_client(container)
        result = container_client.delete_blob(blob_path, snapshot=snapshot)
        return result

    def get_blob_text(self, container: str, blob_path: str):
        self._container_check(container, create_if_needed=False)

        # # watch out for 0-length blobs - they trigger an Azure RETRY error
        # text = ""
        # # azure storage bug workaround: avoid RETRY errors for 0-length blob 
        # blob = self.bs.get_blob_properties(container, blob_path)

        # # save etag where caller can retrieve it, if needed
        # self.current_blob_etag = blob.properties.etag

        # if blob.properties.content_length:
        #     try:
        #         blob = self.bs.get_blob_to_text(container, blob_path)
        #     except BaseException as ex:
        #         if "specified using HTTP conditional header(s) is not met" in str(ex):
        #             # blob changes during read; try again using a snapshot of the blob
        #              props = self.snapshot_blob(container, blob_path)
        #              snapshot_id = props.snapshot
        #              blob = self.bs.get_blob_to_text(container, blob_path, snapshot=snapshot_id)
        #              self.delete_blob(container, blob_path, snapshot=snapshot_id)
        #         else:
        #             # re-raise the unrecognized exception
        #             raise

        #     text = blob.content
        # return text

        container_client = self.blob_service_client.get_container_client(container)
        blob_client = container_client.get_blob_client(blob_path)

        download_stream = blob_client.download_blob()
        text = download_stream.readall().decode()

        return text

    def get_blob_to_path(self, container: str, blob_path: str, dest_fn: str, snapshot=None, progress_callback=None):
        self._container_check(container, create_if_needed=False)

        # ensure path has correct slashes 
        dest_fn = os.path.abspath(dest_fn)
        dest_dir = os.path.dirname(dest_fn)
        if not dest_dir:
            dest_dir = "."
        assert os.path.exists(dest_dir)
        
        dest_fn = os.path.abspath(dest_fn)
        path_len = len(dest_fn)
        if path_len > MAX_PATH:
            console.print("warning: output file path may be too long for this OS: {}".format(path_len))

        # azure storage bug workaround: avoid RETRY errors for 0-length blob 
        # blob = self.bs.get_blob_properties(container, blob_path)
        # if blob.properties.content_length:
        #     # print("writing to dest_dir: ", dest_dir)
        #     # print("len(dest_fn)=", len(dest_fn))

        #     result = self.bs.get_blob_to_path(container, blob_path, dest_fn, snapshot=snapshot, progress_callback=progress_callback)
        #     text = result.content
        # else:
        #     md = blob.metadata
        #     if "hdi_isfolder" in md and md["hdi_isfolder"]:
        #         # its a directory marker; do NOT create a local file for it
        #         text = ""
        #     else:
        #         # 0-length text file; just write the file outselves
        #         text = ""

        #         with open(dest_fn, "wt") as outfile:
        #             outfile.write(text)
           
        container_client = self.blob_service_client.get_container_client(container)
        blob_client = container_client.get_blob_client(blob_path)

        # create local dir, if needed
        dir_name = os.path.dirname(dest_fn)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        with open(dest_fn, "wb") as outfile:
            download_stream = blob_client.download_blob()
            data = download_stream.readall()
            outfile.write(data)    

        return data

    def get_blob_properties(self, container: str, blob_path: str):
        self._container_check(container, create_if_needed=False)

        blob_client = self.blob_service_client.get_blob_client(container, blob_path)
        props = blob_client.get_blob_properties()
        return props

    def get_blob_metadata(self, container: str, blob_path: str):
        self._container_check(container, create_if_needed=False)

        blob_client = self.blob_service_client.get_blob_client(container, blob_path)
        props = blob_client.get_blob_properties()
        return props.metadata

    # def set_blob_metadata(self, container, blob_path, md_dict):
    #     return self.bs.set_blob_metadata(container, blob_path, md_dict)

    def copy_blob(self, source_container: str, source_blob_path: str, dest_container: str, dest_blob_path: str):
        sc_client = self.blob_service_client.get_container_client(source_container)
        if not sc_client.exists():
            errors.service_error("source container not found: {}".format(source_container))

        dc_client = self.blob_service_client.get_container_client(dest_container)
        if not dc_client.exists():
            errors.service_error("destination container not found: {}".format(dest_container))

        source_blob_client = self.blob_service_client.get_blob_client(source_container, source_blob_path)
        if not source_blob_client.exists():
            errors.service_error("source blob not found: {}".format(source_blob_path))

        dest_blob_client = self.blob_service_client.get_blob_client(dest_container, dest_blob_path)

        # workaournd: below call gets "Server failed to authenticate the request." error
        #dest_blob_client.upload_blob_from_url(source_blob_client.url)
        
        # download from source and upload to dest
        data = source_blob_client.download_blob().readall()
        dest_blob_client.upload_blob(data)

    def snapshot_blob(self, container: str, blob_path: str):
        self._container_check(container, create_if_needed=False)

        blob_client = self.blob_service_client.get_blob_client(container, blob_path)
        props_dict = blob_client.create_snapshot()

        return props_dict

