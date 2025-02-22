#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# xt_cmds.py: defines the XT commands, arguments, and options
'''
This module's main() supports the parsing and execution of an XT command.  It is
usually called from xt_run, but can be called directly (as is done in the quicktest and grokserver).
'''
import os
import sys
import time
import logging
import importlib

from xtlib import qfe
from xtlib import utils
from xtlib import errors
from xtlib import cmd_utils
from xtlib import constants
from xtlib import file_utils

from xtlib.console import console
from xtlib.helpers.feedbackParts import feedback
from xtlib.impl_shared import ImplShared

logger = logging.getLogger(__name__)

# global 
orig_xt_cmd = None

def get_fn_local_config(cmd):
    '''
    gets path to local config file (specified on cmd line or defaulting to ./xt_config.yaml)
    '''
    # default value
    fn = os.path.join(".", constants.CONFIG_FN)

    # is config file specified by --config option or as a run command with .yaml file script?
    parts = cmd_utils.xt_cmd_split(cmd)
    found_run = False

    for i, part in enumerate(parts):
        # don't change the order of these checks
        if found_run:
            if part.endswith(".yaml"):
                fn = part
            else:
                # is there an XT confile file in the script dir?
                fnx = os.path.join(os.path.dirname(part), constants.CONFIG_FN)
                if os.path.exists(fnx):
                    fn = file_utils.rel_path(fnx, ".")
                    if os.path.dirname(fn):
                        # only print if its not the current directory
                        console.print("using script config file: {}".format(fn))
            break
        
        if part.startswith("--"):
            # process pre-cmd option
            subs = part[2:].split("=", 1)
            option = subs[0]
            if qfe.match(option, "config"):
                if len(subs) == 1:
                    i += 1
                    np = None
                    if i < len(parts):
                        np = parts[i]
                else:
                    np = subs[1]
                if np:
                    if not os.path.exists(np):
                        errors.config_error("--config file not found: {}".format(np))
                    return np

        else:
            if part == "run":
                found_run = True
            else:
                # some other command
                break

    return fn

def args_to_dict(args, template_formal_args):
    arg_dict = {}
    a = 0

    while a < len(args):
        arg = args[a]

        if arg.startswith("--"):
            # named arg (--foo=value)

            arg = arg[2:]
            if "=" in arg:
                name, value = arg.split("=", 1)
                part = value
            else:
                name = arg
                value = 1
                part = None

            # handle space delimited str list  (e.g., a, b, c)
            while part and part.endswith(",") and a < len(args)-1:
                a += 1
                part = args[a]
                value += " " + part

            arg_dict[name] = value

        else:
            # unnamed arg value (match with position=a)
            name = template_formal_args[a][1:]
            arg_dict[name] = arg
            
        a += 1

    return arg_dict

def expand_template(config, cmd):
    '''
    replace a template invocation and specified args with the corresponding XT command.
    '''
    args = cmd_utils.xt_cmd_split(cmd)
    template_name = args[0][1:]
    template_actual_args = args[1:]

    # retrieve template definition
    td = config.get("templates", template_name)
    if not td:
        errors.user_error("Template not found: {}".format(template_name))

    template_cmd = td["command"]
    cmd_parts = template_cmd.split()
    template_formal_args = [part for part in cmd_parts if part.startswith("@")]
    opt_arg_dict = utils.safe_value(td, "optional-args", {})

    required_arg_count = len(template_formal_args) - len(opt_arg_dict)

    if required_arg_count > len(template_actual_args):
        errors.user_error("template requires {} args, but only {} were supplied".format(len(template_formal_args), 
            len(template_actual_args)))

    # process template args from user
    arg_dict = args_to_dict(template_actual_args, template_formal_args)

    hidden = utils.safe_value(td, "hidden", False)
    if hidden:
        errors.user_error("cannot use a template that is marked as hidden: {}".format(template_name))


    for i, part in enumerate(cmd_parts):
        if part.startswith("@"):
            name = part[1:]
            if name in arg_dict:
                cmd_parts[i] = arg_dict[name]
                del arg_dict[name]
            else:
                # argument not specified by user
                if name in opt_arg_dict:
                    # use value from optional args dict
                    cmd_parts[i] = opt_arg_dict[name]
                else:
                    errors.user_error("template argument not specified: --{}".format(name))

    cmd = "xt " + " ".join(cmd_parts)

    # add any remaining args to the end of the command
    for name, value in arg_dict.items():
        cmd += " --{}={}".format(name, value)

    print("[{}]".format(cmd))
    return cmd

def build_xt_cmds(config, store, basic_mode=False):
    # import azure.mgmt
    # from azure.mgmt import batch as mgmt_batch

    cmd_providers = config.get("providers", "command")
    impl_dict = {}

    for name, code_path in cmd_providers.items():
        package, class_name = code_path.rsplit(".", 1)
        #console.print("importing package=", package)
        module = importlib.import_module(package)
        impl_class = getattr(module, class_name)

        impl = impl_class(config, store)
        impl_dict[package] = impl

        if name == "help":
            impl.set_basic_mode(basic_mode)

    return impl_dict

def hide_commands(dispatcher, basic_mode=False):
    if basic_mode:
        # a dict of commands + arg/options to be surfaced (None means use all args/options)
        show_commands = {
            "cancel_all": ["target"],
            "cancel_job": ["job-id"], 
            "cancel_run": ["run-names"],
            "clear_credentials": [],
            "config_cmd": ["which", "create"],
            "create_demo": ["destination", "response"],
            "create_services_template": [],
            "download": ["store-path", "local-path", "share", "workspace", "experiment", "job", "run", "feedback", "snapshot", "show_output"],
            "extract": ["runs", "dest-dir", "browse", "workspace"], 
            "help": ["command", "about", "browse", "version"],
            "help_topics": ["topic", "browse"],
            "list_blobs": ["path"],
            "list_jobs": ["job-list", "experiment", "all", "first", "last", "filter", "sort", "reverse", "status", 
                "available", "tags-all", "tags-any"],
            "list_runs": ["run-list", "job", "experiment", "all", "first", "last", "filter", "sort", "reverse", "status", 
                "available", "tags-all", "tags-any"],
            "monitor": ["name", "workspace"],
            "run": ["script", "script-args", "experiment", "hp-config", "max-runs", "monitor", "nodes", 
                "runs", "search-type", "target", "data-action", "model-action"],
            "upload": ["local-path", "store-path", "share", "workspace", "experiment", "job", "run", "feedback", "show_output"],
            "view_console": ["name", "target", "workspace", "node-index"],
            "view_metrics": ["runs", "metrics"],
            "view_run": ["run-name"]
            }

        dispatcher.show_commands(show_commands)

        #qfe.remove_hidden_commands()
    
    # hide under-development commands
    hide_commands  = ["collect_logs", "start_tensorboard", "stop_tensorboard"]

    # hide internal cmds (for xt development use only)
    hide_commands.append("generate_help")
    dispatcher.hide_commands(hide_commands)

def main(cmd, new_start_time=None, capture_output=False, basic_mode=False, raise_syntax_exception=True):
    '''
    Parse and execute the specified cmd.
    '''
    # when executing multiple commands, reset the feedback for each command
    feedback.reset_feedback()

    global orig_xt_cmd
    orig_xt_cmd = cmd

    #console.print("cmd=", cmd, ", args=", args)
    console.diag("in xt_cmds.main")

    #console.print("config=", config)
    fn_local_config = get_fn_local_config(cmd)

    impl_shared = ImplShared()
    config = impl_shared.init_config(fn_local_config)
    store = impl_shared.store
    basic_mode = not config.get("general", "advanced-mode")

    if cmd and cmd.startswith("xt "):
        cmd = cmd[3:].strip()

    # process template invocations
    if cmd.startswith("@"):
        cmd = expand_template(config, cmd)
        if cmd and cmd.startswith("xt "):
            cmd = cmd[3:].strip()

    impl_dict = build_xt_cmds(config, store, basic_mode)

    # this parses args and calls the correct command function with its args and options correctly set.
    # the config object supplies the default value for most options and flags.
    dispatcher = qfe.Dispatcher(impl_dict, config, preprocessor=impl_shared.pre_dispatch_processing)

    hide_commands(dispatcher, basic_mode)

    # expand symbols like $lastjob, $lastrun
    cmd = impl_shared.expand_xt_symbols(cmd)

    # this is the NORMAL outer exeception handling block, but
    # also see the client/server exception handling in xt_run.py
    try:
        text = dispatcher.dispatch(cmd, capture_output=capture_output, raise_syntax_exception=raise_syntax_exception)  
    except BaseException as ex:
        #console.print("in Exception Handler: utils.show_stack_trace=", utils.show_stack_trace)
        # does user want a stack-trace?
        logger.exception("Error during displatcher.dispatch, cmd={}".format(cmd))

        exc_type, exc_value, exc_traceback = sys.exc_info()
        errors.process_exception(exc_type, exc_value, exc_traceback)

    return text

if __name__ == "__main__":
    main()


