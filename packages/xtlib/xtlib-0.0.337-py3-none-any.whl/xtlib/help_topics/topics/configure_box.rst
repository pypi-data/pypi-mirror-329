.. _configure_box:

=================================================
How To Configure a PC as a Compute Node for XT
=================================================

If you have extra computers available, you can configure them to run XT jobs. This is a good way to get started with XT, and it is also useful for running large jobs that require more compute power than your local computer can provide.

Steps:
    1. If you haven't done so already, install XT on your local computer

    2. If you have never generated an SSH key using XT, run the **xt ssh-keygen** command.  This will create an SSH key pair in your ~/.ssh directory.

    3. Add an entry in your XT config file under "boxes" for the computer you want to use as a compute node.  The entry should follow this format:

            a60004x: {address: REDMOND.$username@172.31.42.133, os: "linux", box-class: "linux", max-runs: 1, docker: "pytorch-xtlib", setup: "singd"}

        - In the above example:
        - **a60004x** is your XT <box name> for the computer.  You can use any name you want, but it must be unique.  
        - **address** is the username and IP address of the computer.  The format is **<domain name>.$username@<ip address>**.  
        - **docker** is optional: it is the name of the docker configuration for this box.  There should be a matching entry in the "dockers" section of your XT config file.
        - **setup** is optional: it is the name of the setup configuration for this box.  There should be a matching entry in the "setups" section of your XT config file.

    4. Run the **xt sendkey <box name>** command to send your public key to the remote computer.  This will allow XT to log into the remote computer and run jobs.

    5. Run the **xt ssh <boxname>** command to log into the remote computer.  

    6. On the remote computer, run the following to install the **shutil** package: **python3 -m pip install shutil**

    7. use "exit" to close the remote SSH session.

    8. you can now specify your <box name> when running XT commands.  For example, you can run **xt run --target=<box name> <code file>** to run a job on the remote computer.

            
.. seealso:: 

    - :ref:`Getting Started with XT (and installing) <getting_started>`
    - :ref:`Job Submission <job_submission>`
