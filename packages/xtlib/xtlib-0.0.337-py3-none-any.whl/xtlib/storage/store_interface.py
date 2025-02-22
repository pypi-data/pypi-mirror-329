#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# store_interface.py: specifies the interface for storge providers
from interface import Interface

class StoreInterface(Interface):
    # def __init__(self, storage_creds_dict, *args):
    #     pass

    # ---- MISC part of interface ----
    def get_service_name(self):
        ''' return the unique name of the storage service'''
        pass

    def get_retry(self):
        ''' return the error return count'''
        pass

    def set_retry(self, value): 
        ''' set the error return count'''
        pass

    # ---- CONTAINER interface ----

    def does_container_exist(self, container: str):
        pass

    def create_container(self, container: str):
        pass

    def list_containers(self):
        pass

    def delete_container(self, container: str):
        pass

    def get_container_properties(self, container: str):
        pass

    def get_container_metadata(self, container: str):
        pass

    # ---- BLOB interface ----

    def does_blob_exist(self, container: str, blob_path: str):
        pass

    def create_blob(self, container: str, blob_path: str, text: str, fail_if_exists=False):
        pass

    def create_blob_from_path(self, container: str, blob_path: str, source_fn: str, progress_callback=None):
        pass

    def append_blob(self, container: str, blob_path: str, text: str, append_with_rewrite=False):
        pass

    def list_blobs(self, container: str, path: str=None, return_names=True, recursive=True):
        '''
        NOTE: the semantics here are a bit tricky

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
        '''
        pass

    def delete_blob(self, container: str, blob_path: str, snapshot=None):
        pass

    def get_blob_text(self, container: str, blob_path: str):
        pass

    def get_blob_to_path(self, container: str, blob_path: str, dest_fn: str, snapshot=None, progress_callback=None):
        pass

    def get_blob_properties(self, container: str, blob_path: str):
        pass

    def get_blob_metadata(self, container: str, blob_path: str):
        pass

    def copy_blob(self, source_container: str, source_blob_path: str, dest_container: str, dest_blob_path: str):
        pass

    def snapshot_blob(self, container: str, blob_path: str):
        pass
        