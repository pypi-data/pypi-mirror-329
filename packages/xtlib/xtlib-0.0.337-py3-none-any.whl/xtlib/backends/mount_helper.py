# mount_helper.py: functions related to mounting/unmounting storage (used when generating node script)
import os

from xtlib import errors
from xtlib import store_utils
from xtlib import utils
from xtlib import file_utils
from xtlib.backends.cmd_appender import CmdAppender

class MountHelper():

    def __init__(self, compute_def, sudo_available, actions, use_username, use_allow_other, nonempty, backend,
            homebase="$HOME", mountbase="$HOME", tmpbase="$HOME", config=None, args=None) -> None:

        self.compute_def = compute_def  
        self.sudo_available = sudo_available
        self.actions = actions
        self.use_username = use_username
        self.use_allow_other = use_allow_other
        self.nonempty = nonempty
        self.backend = backend
        self.homebase = homebase
        self.mountbase = mountbase
        self.tmpbase = tmpbase
        self.config = config
        self.args = args

        self.blobfuse_index = 0
        self.mounted_drives = []
        snapshot_dirs = args["snapshot_dirs"]

        add_time = config.get("logging", "add-timestamps")
        capture_setup_cmds = args["capture_setup_cmds"]
        self.install_blobfuse = utils.safe_value(compute_def, "install-blobfuse")

        setup_name = compute_def["setup"]
        setup = self.config.get_setup_from_target_def(compute_def, setup_name)
        self.mounting_enabled = utils.safe_value(setup, "mounting-enabled")

        self.ca = CmdAppender(capture_setup_cmds, add_time, snapshot_dirs)

    def gen_mount_and_download_cmds(self, cmds):

        args = self.args

        store_data_dir, data_action, data_writable, store_model_dir, model_action, model_writable,  \
            storage_name = self.get_action_args(args)

        sudo_available = self.sudo_available
        actions = self.actions
        use_username = self.use_username
        use_allow_other = self.use_allow_other
        nonempty = self.nonempty
        install_blobfuse = self.install_blobfuse
        mountbase = self.mountbase
        tmpbase = self.tmpbase

        workspace = args["workspace"]
        job_id = args["job_id"]

        # create the MNT base folder WITHOUT SUDO
        # this is required for accessing data/models as normal user
        self.ca.append(cmds, "mkdir -p {}/.xt/mnt".format(mountbase))

        # put mnt paths in user's home dir so sudo isn't needed to create/mount
        '''
        NOTE: in storage v2, the workspace container is sufficient to also access the jobs,
        so we don't need to mount the jobs container separately
        '''
        if self.mounting_enabled:
            #jobs_mount_dir = mountbase + "/.xt/mnt/jobs_container"
            workspace_mount_dir = mountbase + "/.xt/mnt/workspace_container"
            data_mount_dir = mountbase + "/.xt/mnt/data_container"
            model_mount_dir = mountbase + "/.xt/mnt/models_container"
        else:
            #jobs_mount_dir = mountbase + "/.xt/local/jobs_container"
            workspace_mount_dir = mountbase + "/.xt/local/workspace_container"
            data_mount_dir = mountbase + "/.xt/local/data_container"
            model_mount_dir = mountbase + "/.xt/local/models_container"

        # emit cmds to MOUNT WORKSPACE and export/set releated environment variables
        workspace = args["workspace"]

        if self.mounting_enabled:
            user_install_blobfuse = self.install_blobfuse    # args["install_blobfuse"]
            if install_blobfuse and user_install_blobfuse:
                self.add_install_blobfuse_cmds(cmds, sudo_available)

            # mount workspace to /mnt/xt_workspace
            self.ca.append_title(cmds, "MOUNT WORKSPACE container to path:")
            self.emit_mount_cmds(cmds, storage_name, container=workspace, 
                mnt_path=workspace_mount_dir, is_writable=True, install_blobfuse=False, 
                sudo_available=sudo_available, use_username=use_username, use_allow_other=use_allow_other, 
                nonempty=nonempty, cleanup_needed=True)

        # # on linux, always mount JOBS container
        # jobs_container = store_utils.get_jobs_container(workspace)

        # if self.mounting_enabled:

        #     # mount JOBS to /mnt/.xt/mnt/jobs_container
        #     self.ca.append_title(cmds, "MOUNT JOBS container to path:")
        #     self.emit_mount_cmds(cmds, storage_name, container=jobs_container, 
        #         mnt_path=workspace, is_writable=True, install_blobfuse=False, 
        #         sudo_available=sudo_available, use_username=use_username, use_allow_other=use_allow_other, 
        #         nonempty=nonempty, cleanup_needed=True)

        self.ca.append_title(cmds, "EXPORT related environment variables:")

        # always define XT_OUTPUT_DIR  (even if it is not mounted)
        # XT_OUTPUT_DIR
        store_path = "{}/jobs/{}/runs/$XT_RUN_NAME/output".format(workspace_mount_dir, job_id)
        self.define_xt_dir(cmds, "XT_OUTPUT_DIR", store_path)

        # always define XT_NODE_DIR  (even if it is not mounted)
        # XT_NODE_DIR
        store_path = "{}/jobs/{}/nodes/node$XT_NODE_INDEX".format(workspace_mount_dir, job_id)
        self.define_xt_dir(cmds, "XT_NODE_DIR", store_path)

        # emit cmds to MOUNT or DOWNLOAD data
        if "data" in actions and data_action != "none":
            self.ca.append_title(cmds, "MOUNT/DOWNLOAD DATA:")
            self.process_action(cmds, data_action, data_mount_dir, store_utils.DATA_STORE_ROOT, store_data_dir, "XT_DATA_DIR",
                data_writable, storage_name, sudo_available=sudo_available, cleanup_needed=True, 
                use_username=use_username, install_blobfuse=False, nonempty=nonempty,
                use_allow_other=use_allow_other, tmpbase=tmpbase, args=args)

        # emit cmds to MOUNT or DOWNLOAD model
        if "model" in actions and model_action != "none":
            self.ca.append_title(cmds, "MOUNT/DOWNLOAD MODELS:")

            self.process_action(cmds, model_action, model_mount_dir, store_utils.MODELS_STORE_ROOT, store_model_dir, "XT_MODEL_DIR",
                model_writable, storage_name, sudo_available=sudo_available, cleanup_needed=True, 
                use_username=use_username, install_blobfuse=False, nonempty=nonempty,
                use_allow_other=use_allow_other, tmpbase=tmpbase, args=args)

    def emit_mount_cmds(self, cmds, storage_name, container, mnt_path, is_writable, 
        install_blobfuse, sudo_available, use_username, use_allow_other, nonempty=False, cleanup_needed=False):

        # NOTE: OK to use SUDO here (for blobfuse dirs)

        if self.mounting_enabled:
            user_install_blobfuse = self.install_blobfuse   # self.args["install_blobfuse"]
            if install_blobfuse and user_install_blobfuse:
                self.add_install_blobfuse_cmds(cmds, sudo_available)

            if cleanup_needed:
                # on pool machines, for any action, always UNMOUNT mnt_dir 
                # also, always zap the folder in case in was used in downloading files
                sudo = "sudo " if sudo_available else ""

                # only do an unmount if dir exists
                self.ca.append(cmds, "ls {} 2>/dev/null && {}fusermount -u -q {}".format(mnt_path, sudo, mnt_path))

                # do NOT call rm as it can delete cloud data if fusermount -u failed 
                #self.ca.append(cmds,"{}rm -rf {}".format(sudo, mnt_path))

            requests = [ {"container": container, "mnt_dir": mnt_path, "readonly": not is_writable} ]
            sub_cmds = self.create_blobfuse_commands(storage_name, sudo_available, requests, install_blobfuse=install_blobfuse,
                use_username=use_username, use_allow_other=use_allow_other, nonempty=nonempty)
            cmds += sub_cmds

    def add_install_blobfuse_cmds(self, cmds, sudo_available):
        # only install it once per backend instance

        if not self.backend.blobfuse_installed:
            self.ca.append_title(cmds, "INSTALL BLOBFUSE:")
            sudo = "sudo " if sudo_available else ""

            # configure apt for microsoft products
            self.ca.append(cmds, "{}wget https://packages.microsoft.com/config/ubuntu/16.04/packages-microsoft-prod.deb".format(sudo), log="wget")
            self.ca.append(cmds, "{}dpkg -i packages-microsoft-prod.deb".format(sudo), log="dpkg")
            
            self.ca.append(cmds, "{}apt-get -y update".format(sudo), log="apt_update")

            # install blobfuse
            # without specifying version, we get version 1.2.3 on AML which breaks our code
            version = "1.0.3"         
            self.ca.append(cmds, "{}apt-get -y install blobfuse={}".format(sudo, version), log="apt_install_blobfuse")

            # #self.ca.append(cmds, "{}modprobe fuse".format(sudo))
            # self.ca.append(cmds, "apt-get -y install modprobe")
            # self.ca.append(cmds, "modprobe fuse")

            self.blobfuse_installed = True

    def create_blobfuse_commands(self, storage_name, sudo_available, mount_requests, install_blobfuse, 
            use_username=True, use_allow_other=True, nonempty=False):
        username = "$USER"
        cmds = []
        sudo = "sudo " if sudo_available else ""
        
        args = self.args
        tmpbase = self.tmpbase

        mount_retry_count = args["mount_retry_count"]
        mount_retry_interval = args["mount_retry_interval"]

        # for each mount request
        for md in mount_requests:
            mnt_dir = md["mnt_dir"]
            container_name = md["container"]
            readonly = md["readonly"]

            self.blobfuse_index += 1
            #console.print("tmpbase=", tmpbase)

            #tmp_dir = "/mnt/resource/blobfusetmp{}".format(self.blobfuse_index)
            tmp_dir = tmpbase + "/blobfusetmp{}".format(self.blobfuse_index)
            fn_config = tmpbase + "/fuse{}.cfg".format(self.blobfuse_index)
            readonly_opt = "-o ro" if readonly else ""
            nonempty_opt = "-o nonempty" if nonempty else ""

            self.mounted_drives.append(mnt_dir)

            self.ca.append(cmds, "{}mkdir {} -p".format(sudo, mnt_dir))

            if use_username:
                self.ca.append(cmds, "{}chown {} {}".format(sudo, username, mnt_dir))

            allow_other = "-o allow_other" if use_allow_other else ""

            # create temp dir (required by blobfuse)
            self.ca.append(cmds, "mkdir -p {}".format(tmp_dir))

            # create fuse config file (clunky but it works)
            # NOTE: to expand XT_STORAGE_KEY, the enclosing string must be made of DOUBLE QUOTES
            self.ca.append(cmds, "echo 'accountName {}' > {}".format(storage_name, fn_config))
            self.ca.append(cmds, 'echo "accountKey $XT_STORAGE_KEY" >> {}'.format(fn_config))
            self.ca.append(cmds, "echo 'containerName {}' >> {}".format(container_name, fn_config))
            
            # for debugging
            #self.ca.append(cmds, "cat {}".format(fn_config))

            #"echo here is the config file '{}' contents".format(fn_config),
            #"more {}".format(fn_config),

            # keep it private 
            self.ca.append(cmds, "chmod 600 {}".format(fn_config))
            self.ca.append(cmds, "blobfuse -v")

            # need to wrap this command with retry logic (similiar to docker run)
            #     pull_cmd = '''timeout {} bash -c "until {}; do '''.format(timeout, constants.FN_DOCKER_PULL_SH) + \
            #         '''echo XT: docker pull failed.  retrying...; sleep 60; done" '''

            blobfuse_cmd = "{}blobfuse {} --tmp-path={}  --config-file={} {} -o attr_timeout=240 -o entry_timeout=240 -o negative_timeout=120 {} {}" \
                .format(sudo, mnt_dir, tmp_dir, fn_config, readonly_opt, allow_other, nonempty_opt)

            if mount_retry_count:
                # retry the blobfuse command as per count/interval
                range = "{1.." + str(mount_retry_count) + "}"
                retry_cmd = "for i in {}; do {} && break || echo error in blobfuse mount: sleeping... ; sleep {}; echo retrying blobfuse mount...; done".format(range, blobfuse_cmd, mount_retry_interval)
                self.ca.append(cmds, retry_cmd)

            else:       
                # normal blobfuse cmd (no retries)     
                self.ca.append(cmds, blobfuse_cmd)

            #self.ca.append(cmds, "echo just ran blobfuse, here is ls -l on mnt_dir", echo=False)
            self.ca.append_dir(cmds, mnt_dir)

        return cmds

    def process_action(self, cmds, action, mnt_path, container, store_data_dir, env_var_name, is_writable,
        storage_name, sudo_available=True, cleanup_needed=False, is_windows=False, use_username=True, 
        install_blobfuse=False, use_allow_other=True, nonempty=False, tmpbase=None, args=None):

        if action == "mount":
            self.emit_mount_cmds(cmds, storage_name, container, mnt_path=mnt_path, 
                is_writable=is_writable, install_blobfuse=install_blobfuse, sudo_available=sudo_available, 
                use_username=use_username, use_allow_other=use_allow_other, 
                nonempty=nonempty, cleanup_needed=cleanup_needed)

            self.ca.append_export(cmds, env_var_name, "{}/{}".format(mnt_path, store_data_dir))

        elif action == "use_local":
            self.ca.append(cmds, "echo USING LOCAL path for ENV[{}]".format(env_var_name), echo=False)
            self.ca.append_export(cmds, env_var_name, store_data_dir, value_is_windows=False)

        elif action == "download":

            # keep all DOWNLOAD directories owned by normal user (not ROOT)
            sudo_available = False

            self.ca.append(cmds, "echo DOWNLOADING {} from container {}".format(mnt_path, container))

            full_mnt_path =  mnt_path + "/" + store_data_dir
            self.ca.append_export(cmds, env_var_name, full_mnt_path, value_is_windows=False)
            self.ca.append(cmds, "echo setting {}={}".format(env_var_name, full_mnt_path, value_is_windows=False))

            # make it look like this is parent dir
            dest_dir_ext = mnt_path + "/" + store_data_dir

            requests = [ {"container": container, "blob_path": store_data_dir, "dest_dir": dest_dir_ext} ]
            sub_cmds = self.create_download_commands("xt", True, sudo_available, requests, use_username=use_username)
            cmds += sub_cmds

    def create_download_commands(self, xt_path, create_dest_dirs, sudo_available, download_requests, 
            for_windows=False, use_username=True):
        '''
        Lessons learned here:
            - we want to create MNT root and subdirectories all without SUDO (so we don't create access for download process 
              or subsequent reading by normal user)
              
            - previously, we were created the MNT folder indirectly thru our blobfuse mounting code, where we create the mapping folder
              with SUDO.  This created a problem later when we create the download directory, it becomes created with ROOT and then normal
              user code cannot copy to that folder.
        '''
        cmds = []
        #username = "$USER"
        #sudo = "sudo " if (sudo_available and not for_windows) else ""
        #sudo = "sudo " if (sudo_available and not for_windows) else ""

        # for each mount request
        for md in download_requests:
            container_name = md["container"]
            blob_path = md["blob_path"]
            dest_dir = md["dest_dir"]

            if create_dest_dirs:
                if for_windows:
                    # fix slashes for windows
                    dest_dir = dest_dir.replace("/", "\\")
                    sub_cmds = \
                    [ 
                        "mkdir {} ".format(dest_dir),
                    ]
                else:
                    sub_cmds = \
                    [ 
                        # don't use SUDO here; we need dir accessible by current user
                        "mkdir -p {}".format(dest_dir),
                    ]
                    # if use_username:
                    #     sub_cmds.append("{}chown {} {}".format(sudo, username, dest_dir))

                for sc in sub_cmds:
                    self.ca.append(cmds, sc)

            # # remove old directory from previous run (singularity doesn't clean these up?)
            # mc = "{}rm -rf {} ".format(sudo, dest_dir)
            # self.ca.append(cmds, mc)

            cmd = "{} download /{}/{} {}".format(xt_path, container_name, blob_path, dest_dir)
            self.ca.append(cmds, cmd, expand=True, log="download")

            self.ca.append_dir(cmds, dest_dir)

        return cmds        

    def get_action_args(self, args):
        store_data_dir = args["data_share_path"]
        data_action = args["data_action"]
        data_writable = args["data_writable"]

        store_model_dir = args["model_share_path"]
        model_action = args["model_action"]
        model_writable = args["model_writable"]

        storage_name = args["storage"]
        storage_info = self.config.get("external-services", storage_name, default_value=None)
        if not storage_info:
            errors.config_error("storage name '{}' not defined in [external-services] in config file".format(storage_name))

        return store_data_dir, data_action, data_writable, store_model_dir, model_action, model_writable, storage_name

    def define_xt_dir(self, cmds, name, path):

        # ensure dir is empty but present
        path = file_utils.fix_slashes(path, True, protect_ws_run_name=False)
        self.ca.append_export(cmds, name, path)
        self.ca.append(cmds, "rm -rf {}".format(path))
        self.ca.append(cmds, 'mkdir -p "{}"'.format(path))

        self.ca.append_dir(cmds, path)

    def gen_unmount_all(self, cmds):    

        if self.mounted_drives:
            self.ca.append_title(cmds, "Unmount Blobfuse drives")
            
            for md in self.mounted_drives:
                self.ca.append(cmds, "fusermount -u -q {} && rm -rf {}".format(md, md))
