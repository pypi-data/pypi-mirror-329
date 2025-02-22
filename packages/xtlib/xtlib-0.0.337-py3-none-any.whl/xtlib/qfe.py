#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# qfe: a quick-front-end builder for XT (parses commands, arguments, and options & dispatches to associated code).
import enum
import os
import sys
import copy
import functools

from xtlib.console import console
from xtlib.helpers.scanner import Scanner

from xtlib import utils
from xtlib import errors
from xtlib import cmd_utils
from xtlib import run_helper
from xtlib import job_helper

'''
Definitions:
    argument - a postional, unnamed parameter; can be optional iif it last argument
    option   - a non-positional, named parameter; can be optional or required
    flag     - a non-positional, named parameter without a value, or with a 1, 0 value
    layer    - marker to start a new layer of arguments for the current command
    unknown  - option that accepts unknown options and passes them to command

Root:
    options can be added to the main() function with a "root=True" parameter.  This
    will be they can be accepted for any command.
'''

# GLOBALS
# TODO: remove these

# structure that is used for storing all cmd_info's and
# for locating a cmd_info one word at a time
commands = {}               # nested dictionary, each level index by next command keyword
commands_by_name = {}       # key = function name
current_dispatcher = None

# workaround for "commands" getting corrupted during quicktest
save_commands = None
dispatch_counter = 0

# special cmd_info's and funcs
root_cmd_info = None
current_cmd_info = None         # for command function being defined as function decorators are processed
parser_cmd_info = None          # the command being parsed or dispatched
command_help_func = None
kwgroup_help_func = None
explicit_options = {}

# debugging flags
debug_decorators = False
first_command = True

def is_xt_object(name):
    if run_helper.is_run_name(name):
        match = True
    elif job_helper.is_job_id(name):
        match = True
    else:
        match = False

    return match

def get_xt_objects_from_cmd_piping():
    objects = []

    if not os.isatty(0):
        # command line piping
        for line in sys.stdin:
            tokens = line.split()
            tokens = [tok for tok in tokens if is_xt_object(tok)]
            if tokens:
                objects.append(tokens[0])

    return objects

pipe_object_list = None   

# testing
#pipe_object_list= ['run2122', 'run2123', 'run2124']

def inner_dispatch(args, is_rerun=False):
    current_dispatcher.dispatch(args, is_rerun)

def get_dispatch_cmd():
    return current_dispatcher.get_dispatch_cmd() if current_dispatcher else None

def get_command_by_words(words):
    dd = commands
    for word in words:
        dd = dd[word]

    if not "" in dd:
        errors.general_error("command not found: " + " ".join(words))

    cmd_info = dd[""]
    return cmd_info

def get_root_command():
    return root_cmd_info

def build_commands():
    '''
    we return as a dict with key=func because:
        - it automatically eliminate the duplicate caused by keyword_optional 
        - enables caller to quickly access command by name
    '''
    func_dict = {}
    get_commands_from(commands, func_dict)

    return func_dict

# def remove_hidden_commands():
#     # remove hidden commands from commnds_by_name
#     global commands_by_name
#     commands_by_name = {name:cmd for name,cmd in commands_by_name.items() if not cmd["hidden"]}

#     # rebuild commands from commands_by_name
#     ddx = {}
#     for _, cmd in commands_by_name.items():
#         cmd_name = cmd["name"]

#         # add cmd keywords to dd
#         dd = ddx
#         for name_part in cmd_name.split(" "):
#             if name_part not in dd:
#                 dd[name_part] = {}
#             dd = dd[name_part]

#         dd[""] = cmd

#     global commands
#     commands = ddx

def get_commands_from(dd, func_dict):
    for key, value in dd.items():
        if key:
            get_commands_from(value, func_dict)
        else:
            func_name = value["func"].__name__
            func_dict[func_name] = value

def update_or_insert_argument(cmd_info, list_name, new_arg):
    new_name = new_arg["name"]
    args = cmd_info[list_name]
    names = [arg["name"] for arg in args]

    if new_name in names:
        # replace existing entry
        cmd_info[list_name] = [(new_arg if arg["name"] == new_name else arg) for arg in args ]
    else:
        # insert new entry at beginning
        args.insert(0, new_arg)

# COMMAND_HELP decorator processor
def command_help(func):
    global command_help_func
    command_help_func = func
    return func

# KWGROUP_HELP decorator processor
def kwgroup_help(func):
    global kwgroup_help_func
    kwgroup_help_func = func
    return func

# ROOT decorator processor
def root(help=""):
    '''
    builds the root_cmd_info entry, mostly to track root options.
    '''
    def decorator_root(func):
        @functools.wraps(func)
        def wrapper_root(*args, **kwargs):
            return func(*args, **kwargs)

        # begin actual decorater processing
        if debug_decorators:
            console.print("root decorator called, func=", func.__name__)

        global root_cmd_info, current_cmd_info
        root_cmd_info =  {"name": func.__name__, "func": func, "arguments": [], "options": [], "help": help}
        current_cmd_info = root_cmd_info
        # end actual decorater processing

        return wrapper_root
    return decorator_root

# COMMAND decorator processor
def command(name=None, group=None, kwgroup=None, user_filters=False, kwhelp=None, 
    options_before_args=False, keyword_optional=False, pass_by_args=False, help=""):
    '''
    builds a nested dictionary of name parts for multi-word commands 
    and their associated functions.
    '''

    def decorator_command(func):
        @functools.wraps(func)
        def wrapper_command(*args, **kwargs):
            return func(*args, **kwargs)

        # begin actual decorater processing
        global first_command
        if first_command:
            first_command = False
            #   console.diag("processing first cmd decorator")
            #console.print("first command...")

        if name:
            cmd_name = name
        else:
            cmd_name = func.__name__.replace("_", " ")

        if debug_decorators:
            console.print("command decorator called, func=", func.__name__)
        dd = commands

        for name_part in cmd_name.split(" "):
            if name_part not in dd:
                dd[name_part] = {}
            dd = dd[name_part]

        cmd_info =  {"name": cmd_name, "options_before_args": options_before_args, "keyword_optional": keyword_optional, "pass_by_args": pass_by_args, 
            "group": group, "func": func, "arguments": [], "options": [], "examples": [], "faqs": [], "hidden": False, "see_alsos": [],
            "kwgroup": kwgroup, "kwhelp": kwhelp, "help": help, "user_filters": user_filters}

        dd[""] = cmd_info

        if keyword_optional:
            # only 1 command can use this
            if "" in commands:
                errors.internal_error("processing command decoration for '{}'; only 1 command can use 'keyword_optional'".format(func.__name__))
            commands[""] = cmd_info

        global current_cmd_info
        current_cmd_info = cmd_info
        # end actual decorater processing

        return wrapper_command
    return decorator_command

    #console.print("command decorator called, func=", func.__name__)
    #return func

# ARGUMENT decorator processor
def argument(name, required=True, type=str, help="", default=None):
    def decorator_argument(func):
        @functools.wraps(func)
        def wrapper_argument(*args, **kwargs):
            return func(*args, **kwargs)

        if debug_decorators:
            console.print("argument decorator called, name=", name, ", func=", func.__name__)

        global current_cmd_info
        if not current_cmd_info:
            errors.internal_error("@argument decorators must be followed by a single @command decorator")

        type_name = type if isinstance(type, str) else type.__name__
        arg_info = {"name": name, "required": required, "type": type_name, "help": help, "default": default}

        #current_cmd_info["arguments"].insert(0, arg_info)
        update_or_insert_argument(current_cmd_info, "arguments", arg_info)

        return wrapper_argument

    return decorator_argument

# ARGUMENT decorator processor
def keyword_arg(name, keywords, required=True, type=str, help="", default=None):
    def decorator_keyword_arg(func):
        @functools.wraps(func)
        def wrapper_keyword_arg(*args, **kwargs):
            return func(*args, **kwargs)

        if debug_decorators:
            console.print("keyword_arg decorator called, name=", name, ", func=", func.__name__)

        global current_cmd_info
        if not current_cmd_info:
            errors.internal_error("@keyword_arg decorators must be followed by a single @command decorator")

        type_name = type if isinstance(type, str) else type.__name__
        arg_info = {"name": name, "keywords": keywords, "required": required, "type": type_name, "help": help, "default": default}

        #current_cmd_info["keyword_args"].insert(0, arg_info)
        update_or_insert_argument(current_cmd_info, "arguments", arg_info)

        return wrapper_keyword_arg

    return decorator_keyword_arg

# OPTION decorator processor
def option(name, arg_name=None, default=None, required=None, multiple=False, type=str, values=None, help=""):
    '''
    params:
        multiple: when True, user can specify this option multiple times and values will accumulate (list of strings)
        values: if values are specified, the value of this option must be set to one of these keyword values
    '''
    def decorator_option(func):
        @functools.wraps(func)
        def wrapper_option(*args, **kwargs):
            return func(*args, **kwargs)

        if debug_decorators:
            console.print("option decorator called, name=", name, ", func=", func.__name__)

        global current_cmd_info
        if not current_cmd_info:
            errors.internal_error("@option decorators must be followed by a single @command decorator")

        type_name = type if isinstance(type, str) else type.__name__
        actual_arg_name = arg_name if arg_name else name

        option_info = {"name": name, "arg_name": actual_arg_name, "hidden": False, "required": required, "type": type_name, "multiple": multiple, 
            "default": default, "values": values, "help": help}
        
        #current_cmd_info["options"].append(option_info)
        update_or_insert_argument(current_cmd_info, "options", option_info)

        return wrapper_option

    return decorator_option
 
def hidden(name, default=None, type=str, help=""):
    def decorator_hidden(func):
        @functools.wraps(func)
        def wrapper_hidden(*args, **kwargs):
            return func(*args, **kwargs)

        if debug_decorators:
            console.print("hidden decorator called, name=", name, ", func=", func.__name__)

        global current_cmd_info
        if not current_cmd_info:
            errors.internal_error("@hidden decorators must be followed by a single @command decorator")

        # a hidden is really just a hidden option
        type_name = type if isinstance(type, str) else type.__name__
        option_info = {"name": name, "hidden": True, "type": type_name, "default": default, "help": help}
        
        #current_cmd_info["hiddens"].append(hidden_info)
        update_or_insert_argument(current_cmd_info, "options", option_info)

        return wrapper_hidden

    return decorator_hidden

# FLAG decorator processor  
def flag(name, default=None, help=""):
    def decorator_flag(func):
        @functools.wraps(func)
        def wrapper_flag(*args, **kwargs):
            return func(*args, **kwargs)

        if debug_decorators:
            console.print("flag decorator called, name=", name, ", func=", func.__name__)

        global current_cmd_info, root_cmd_info

        # a flag is really just a type=flag option
        option_info = {"name": name, "hidden": False, "type": "flag", "multiple": False, "default": default, "help": help}
        if not current_cmd_info:
            errors.internal_error("@flag decorators must be followed by a single @command or @root decorator")

        update_or_insert_argument(current_cmd_info, "options", option_info)

        return wrapper_flag

    return decorator_flag

# LAYER decorator processor  
def layer(name, dest, help=""):
    def decorator_layer(func):
        @functools.wraps(func)
        def wrapper_layer(*args, **kwargs):
            return func(*args, **kwargs)

        if debug_decorators:
            console.print("layer decorator called, name=", name, ", func=", func.__name__)

        global current_cmd_info, root_cmd_info

        if not current_cmd_info:
            errors.internal_error("@layer decorators must be followed by a single @command or @root decorator")

        option_info = {"name": name, "hidden": False, "type": "layer", "multiple": False, "help": help, "dest": dest}
        update_or_insert_argument(current_cmd_info, "options", option_info)

        return wrapper_layer

    return decorator_layer

# UNKNOWN decorator processor  
def unknown(dest, type, help=""):
    def decorator_unknown(func):
        @functools.wraps(func)
        def wrapper_unknown(*args, **kwargs):
            return func(*args, **kwargs)

        if debug_decorators:
            console.print("unknown decorator called, name=", name, ", func=", func.__name__)

        global current_cmd_info, root_cmd_info

        if not current_cmd_info:
            errors.internal_error("@unknown decorators must be followed by a single @command or @root decorator")

        option_info = {"name": "_unknown_", "hidden": False, "type": type, "multiple": False, "help": help, "dest": dest}
        update_or_insert_argument(current_cmd_info, "options", option_info)

        return wrapper_unknown

    return decorator_unknown

# EXAMPLE decorator processor  
def example(text, task="", image=None, alt=None):
    def decorator_example(func):
        @functools.wraps(func)
        def wrapper_example(*args, **kwargs):
            return func(*args, **kwargs)

        if debug_decorators:
            console.print("example decorator called, text={}, func={}".format(text, func.__name__))

        global current_cmd_info, root_cmd_info

        example_info = {"text": text, "task": task, "image": image, "alt": alt}
        if not current_cmd_info:
            errors.internal_error("@example decorators must be followed by a single @command or @root decorator")

        #console.print("setting example name=", name)
         
        current_cmd_info["examples"].insert(0, example_info)
        return wrapper_example

    return decorator_example

# SEE ALSO decorator processor  
def see_also(text, page_path=""):
    def decorator_see_also(func):
        @functools.wraps(func)
        def wrapper_see_also(*args, **kwargs):
            return func(*args, **kwargs)

        if debug_decorators:
            console.print("see_also decorator called, text={}, func=".format(text, func.__name__))

        global current_cmd_info, root_cmd_info

        see_also_info = {"text": text, "page_path": page_path}
        if not current_cmd_info:
            errors.internal_error("@see_also decorators must be followed by a single @command or @root decorator")

        #console.print("setting see_also name=", name)
         
        current_cmd_info["see_alsos"].insert(0, see_also_info)
        return wrapper_see_also

    return decorator_see_also

# FAW decorator processor  
def faq(question, answer):
    def decorator_faq(func):
        @functools.wraps(func)
        def wrapper_faq(*args, **kwargs):
            return func(*args, **kwargs)

        if debug_decorators:
            console.print("faq decorator called, question={}, func={}".format(question, func.__name__))

        global current_cmd_info, root_cmd_info

        faq_info = {"question": question, "answer": answer}
        if not current_cmd_info:
            errors.internal_error("@faq decorators must be followed by a single @command or @root decorator")

        #console.print("setting faq name=", name)
         
        current_cmd_info["faqs"].insert(0, faq_info)
        return wrapper_faq

    return decorator_faq

# CLONE decorator processor  
def clone(source, arguments=True, options=True):
    def decorator_clone(func):
        @functools.wraps(func)
        def wrapper_clone(*args, **kwargs):
            return func(*args, **kwargs)

        if debug_decorators:
            console.print("clone decorator called, source=", source, ", func=", func.__name__)

        global current_cmd_info, root_cmd_info

        if not current_cmd_info:
            errors.internal_error("@clone decorators must be followed by a single @command or @root decorator")

        source_cmd_info = get_command_by_words(source.split("_"))

        if arguments:
            current_cmd_info["arguments"] += source_cmd_info["arguments"]

        if options:
            current_cmd_info["options"] += source_cmd_info["options"]

        return wrapper_clone

    return decorator_clone

def get_commands():
    cmd_list = list(commands_by_name.values())
    return cmd_list

def get_command(name):
    return commands_by_name[name]

def get_explicit_options():
    '''
    return dict of options explicitly set for this command (dash-style names)
    '''
    return explicit_options

def set_explicit_options(options, additive=True):
    global explicit_options
    
    if additive:
        explicit_options.update(options)
    else:
        explicit_options = options

class Dispatcher():
    def __init__(self, impl_dict, config, preprocessor=None):
        self.impl_dict = impl_dict
        self.config = config
        self.preprocessor = preprocessor
        self.cmd_words = None
        self.dispatch_cmd = None
        self.cmd_info = None
        self.user_filters = self.config.data["user-filters"]
        self.unknown_dict = {}
        self.unknown_dest = None
        self.layers = []
        self.unknown_option = None

        global commands_by_name, current_dispatcher, dispatch_counter, commands, save_commands

        commands_by_name = build_commands()
        current_dispatcher = self
        dispatch_counter += 1

        if dispatch_counter > 2:
            if not save_commands:
                # first time thru, save a copy of the commands
                save_commands = copy.deepcopy(commands)
            else:
                # restore from saved copy
                commands = copy.deepcopy(save_commands)

    def build_xt_cmd_from_dict(self, cmd, arguments, options, arg_dict):
        xt_cmd = cmd
        args = ""
        opts = ""

        for arg in arguments:
            arg_name = arg["name"]
            if arg_name in arg_dict:
                args += " " + str(arg_dict[arg_name])

        for opt in options:
            opt_name = opt["name"]
            if opt_name in arg_dict:
                opts += " --{}={}".format(opt_name, arg_dict[opt_name])
        
        if cmd == "run":
            xt_cmd += opts + args
        else:
            xt_cmd += args + opts

        return xt_cmd

    def validate_and_add_defaults_for_cmd(self, cmd, arg_dict):
        cmd_info = get_command("run")
        options = cmd_info["options"]
        arguments = cmd_info["arguments"]

        # build xt_cmd for logging purposes
        self.dispatch_cmd = self.build_xt_cmd_from_dict(cmd, arguments, options, arg_dict)

        return self.validate_and_add_defaults(arguments, options, arg_dict)

    def show_current_command_syntax(self):
        console.print()

        if self.cmd_info:
            help_impl = self.impl_dict["xtlib.impl_help"]
            help_impl.command_help(self.cmd_info, True, False)

    def hide_commands(self, cmds_to_hide):
        for cmd in cmds_to_hide:
            if cmd in commands_by_name:
                cmd_info = commands_by_name[cmd]
                cmd_info["hidden"] = True

    def show_commands(self, show_dict):
        # start by hiding all commands
        for name, cmd_info in commands_by_name.items():
            cmd_info["hidden"] = True

        # show specified commands
        for cmd, args_to_show in show_dict.items():
            if cmd in commands_by_name:
                cmd_info = commands_by_name[cmd]
                cmd_info["hidden"] = False
                self.show_cmd_options(cmd_info, args_to_show)

    def show_cmd_options(self, cmd_info, args_to_show):
        for arg in cmd_info["arguments"]:
            arg["hidden"] = not (arg["name"] in args_to_show)

        for opt in cmd_info["options"]:
            opt["hidden"] = not (opt["name"] in args_to_show)

    def match_keyword(self, value, keywords):
        found = None

        for kw in keywords:
            if match(value, kw):
                found = kw
                break
        
        return found

    def get_cmd_info(self, tok, scanner, for_help=False):
        '''
        given a command line (without the program name), parses it and calls the associated
        cmd_info.
        '''
        dd = commands 
        words_seen = ""

        if not tok:
            # no input defaults to help command
            tok = "help"

        while tok:
            if tok.startswith("-"):
                break

            name = tok
            key = self.list_item_by_value(name, dd.keys())
            if not key:
                #error("command part={} not found in dd={}".format(arg, dd))
                break

            dd = dd[key]    
            tok = scanner.scan()        # skip over name
            if words_seen:
                words_seen += " " + key
            else:
                words_seen = key

        # process OUTER LEVEL match (some special cases)
        if dd == command:
            if not words_seen:
                self.syntax_error("unrecognized start of command: " + tok)

        # if not "" in dd and not for_help:
        #     errors.user_error("incomplete command: " + words_seen)

        if "" in dd:
            cmd_info = dd[""]
        else:
            # return a dict of commands (for "list", "view", etc.)
            cmds = {"kwgroup_name": words_seen}   # mark as kwgroup of cmds
            get_commands_from(dd, cmds)
            cmd_info = cmds

        return cmd_info, tok

    def parse_string_list(self, tok, scanner, pipe_objects_enabled=True):
        global pipe_object_list
        #print("parse_string_list, tok=", tok)
    
        if not tok:
            # empty string specified
            value = []
            tok = scanner.scan()   # skip over the empty string
        elif tok == "$":
            if pipe_objects_enabled:
                global pipe_object_list
                pipe_object_list =  get_xt_objects_from_cmd_piping()
                console.diag("pipe_object_list: {}".format(pipe_object_list))

            if pipe_objects_enabled and pipe_object_list:
                #print("found '*', pipe_object_list=", pipe_object_list)
                value =  pipe_object_list
                console.print("replacing '$' with: ", value)
            else:
                errors.combo_error("'$' can only be used for piping the output of a previous XT command into this run")

            # mark pipe objects as having been consumed by this parsing
            pipe_object_list = None

            tok = scanner.scan()   # skip over the $
        else:
            # scan a comma separated list of tokens (some of which can be single quoted strings)
            value = []
    
            while tok != None:
                if value and tok.startswith("--"):
                    break
                    
                ev = self.expand_system_values(tok)
                value.append(ev)

                tok = scanner.scan()
                if tok != ",":
                    break

                tok = scanner.scan()   # skip over the comma

        return value, tok

    def expand_system_values(self, value):
        if value in ["$null", "$none"]:
            value = None
        elif value == "$empty":
            value = ""

        return value

    def parse_num_list(self, tok, scanner, pipe_objects_enabled=True):
        global pipe_object_list
    
        if "," in tok and not tok.startswith("--"):
            # str_list in an option string
            values = tok.split(",")
            value = [float(v) for v in values]

            tok = scanner.scan()        # skip over the whole string
        else:
            # normal list of comma-separated tokens
            value = []
    
            while tok != None:
                if tok.startswith("--"):
                    break
                    
                value.append(float(tok))

                tok = scanner.scan()
                if tok != ",":
                    break

                tok = scanner.scan()   # skip over the comma

        return value, tok

    def parse_prop_op_value_list(self, tok, scanner):
        # normal list of comma-separated tokens
        values = []

        while tok != None:
            if tok.startswith("--"):
                break
                
            value = self.process_prop_op_value(tok)
            values.append(value)

            tok = scanner.scan()
            if tok != ",":
                break

            tok = scanner.scan()   # skip over the comma

        return values, tok

    def parse_int_list(self, tok, scanner, pipe_objects_enabled=True):
        global pipe_object_list
    
        if "," in tok and not tok.startswith("--"):
            # str_list in an option string
            values = tok.split(",")
            value = [int(v) for v in values]

            tok = scanner.scan()        # skip over the whole string
        else:
            # normal list of comma-separated tokens
            value = []
    
            while tok != None:
                if tok.startswith("--"):
                    break
                    
                value.append(int(tok))

                tok = scanner.scan()
                if tok != ",":
                    break

                tok = scanner.scan()   # skip over the comma

        return value, tok

    def parse_tag_list(self, tok, scanner):
        tag_list = []

        while tok != None:
            if tok.startswith("--"):
                break

            # tagname
            tag = tok
            tok = scanner.scan()    # skip over tagname

            if tok == "=":
                # optional assignment
                tok = scanner.scan()    # skip over =
                tag += "=" + tok
                tok = scanner.scan()    # skip over value

            tag_list.append(tag)
            
            if tok != ",":
                break
            tok = scanner.scan()   # skip over the comma

        return tag_list, tok

    def list_item_by_name(self, name, values, key="name"):
        # first, look for an exact match (takes priority)
        matches = [value for value in values if name == value[key]]
        if not matches:
            # look for abbreviated matches
            matches = [value for value in values if match(name, value["name"])]
            if len(matches) > 1:
                match_names = [m["name"] for m in matches]
                errors.syntax_error("abbreviated name '{}' results in multiple matches: {}" \
                    .format(name, ", ".join(match_names)))

        found = matches[0] if matches else None

        if not found:
            # check for presence of @unknown for this command
           if self.unknown_option:
                # make this looks like a actual match, but with an 'unknown' flag
                found = dict(self.unknown_option)
                found["name"] =  name
                found["unknown"] = True

        return found

    def list_item_by_value(self, value, values):
        matches = [val for val in values if match(value, val)]
        if len(matches) > 1:
            errors.syntax_error("abbreviated value '{}' results in multiple matches: {}".format(value, ", ".join(matches)))
        found = matches[0] if matches else None
        return found

    def get_default_from_config(self, value):
        if value and isinstance(value, str) and value.startswith("$"):
            if "." in value:
                group, prop = value[1:].split(".")
                value = self.config.get(group, prop)
            else:
                group = value[1:]
                value = self.config.get(group)
                
        return value

    def process_root_options(self, scanner, tok):
        options_processed = {}

        root_options = root_cmd_info["options"]
        root_func = root_cmd_info["func"]
        #console.print("root_options=", root_options)

        while tok and tok.startswith("--"):
            name = tok[2:]    # remove dashes
            match = self.list_item_by_name(name, root_options)
            if not match:
                break

            name = match["name"]        # full name
            tok = scanner.scan()        # skip over name
            value = True

            if tok == "=":
                tok = scanner.scan()        # skip over equals
                value = tok
                tok = scanner.scan()        # skip over value

            values = match["values"] if "values" in match else None
            value = self.process_option_value(name, match["type"], value, values)

            arg_dict =  {"name": name, "value": value}
            caller = self.impl_dict[root_func.__module__]

            # call func for root flag procesing
            if self.preprocessor:
                self.preprocessor("root_flag", caller, arg_dict)

            root_func(caller, **arg_dict)
            options_processed[name] = 1

        # ensure all root options have been processed
        for info in root_cmd_info["options"]:
            name = info["name"]
            required = info["required"] if "required" in info else None

            if not name in options_processed:
                #console.print("opt_info=", opt_info)
                if required:
                    self.syntax_error("value for required option={} not found".format(name))

                default_prop_name = info["default"] if "default" in info else None
                default_value = self.get_default_from_config(default_prop_name)
                arg_dict =  {"name": name, "value": default_value}
                caller = self.impl_dict[root_func.__module__]
        
                if self.preprocessor:
                    self.preprocessor("root flag", caller, arg_dict)

                # call func for root flag procesing
                root_func(caller, **arg_dict)
        return tok

    def process_arguments(self, scanner, tok, arguments, arg_dict):
        for arg_info in arguments:
            if utils.safe_value(arg_info, "hidden"):
                continue

            arg_name = arg_info["name"]
            arg_type = arg_info["type"]
            required = arg_info["required"]
            keywords = arg_info["keywords"] if "keywords" in arg_info else None
            current_arg = None

            #print("processing arg=", arg_name, arg_type, tok)

            if arg_type == "cmd" and tok and not tok.startswith("-"):
                # convert remaining tokens to a cmd_info
                if tok:
                    # if match(tok, "topics"):
                    #     cmd_info = {"name": "topics"}
                    #     tok = scanner.scan()
                    # else:
                    cmd_info, tok = self.get_cmd_info(tok, scanner, for_help=True)
                    current_arg = cmd_info
            elif arg_type == "text":
                # convert remaining tokens to a string
                if tok:
                    text = scanner.get_rest_of_text(include_current_token=True)
                    tok = None
                else:
                    text = ""
                current_arg = text
            else:
                if tok and not tok.startswith("-"):
                    current_arg = tok

            if required and not current_arg:
                self.syntax_error("cmd '{}' missing required argument: {}".format(self.cmd_words, arg_name))

            if current_arg:
                if arg_type == "str_list":
                    value, tok = self.parse_string_list(tok, scanner)
                    if len(value)==0 and required:
                        self.syntax_error("missing value for required argument: " + arg_name)
                elif arg_type == "num_list":
                    value, tok = self.parse_num_list(tok, scanner)
                    if len(value)==0 and required:
                        self.syntax_error("missing value for required argument: " + arg_name)
                elif arg_type == "int_list":
                    value, tok = self.parse_int_list(tok, scanner)
                    if len(value)==0 and required:
                        self.syntax_error("missing value for required argument: " + arg_name)
                elif arg_type == "tag_list":
                    value, tok = self.parse_tag_list(tok, scanner)
                    if len(value)==0 and required:
                        self.syntax_error("missing value for required argument: " + arg_name)
                else:
                    value = current_arg
                    if keywords:
                        found = self.match_keyword(value, keywords)
                        if not found:
                            self.syntax_error("Keyword argument {} has unrecognized value: {}".format(arg_name, value))
                        value = found
                    tok = scanner.scan()

                # store value to be passed 
                arg_dict[arg_name] = value

        if tok and not tok.startswith("--"):
            errors.argument_error("unrecognized argument", tok)
        return tok

    def scan_raw_value(self, scanner, tok):
        # assume it is a str list
        value, tok = self.parse_string_list(tok, scanner)
        if len(value)==0:
            value = None
        elif len(value)==1:
            value = value[0]
        return value, tok

    def parse_flag_value(self, name, value):
        value = str(value).lower()
        flag_values = ["true", "false", "on", "off", "0", "1"]

        if not value in flag_values:
            self.syntax_error("flag option '{}' value is not one of these recognized values: {}".format(name, ", ".join(flag_values)))
        
        # set to True/False so that it can filter boolean properties correctly
        #value = 1 if value in ["true", "on", "1"] else 0
        value = True if value in ["true", "on", "1"] else False
        return value

    def scan_relational_op(self, scanner):
        op = scanner.scan()

        if scanner.token_type != "special":
            if op not in ["in", "not-in", "contains", "not-contains"]:
                self.syntax_error("expected relational operator in filter expression: " + op)

        return op

    def process_prop_op_value(self, value):
        
        # mini parse of the value: <prop> <op> <value>
        scanner = Scanner(value)
        prop = scanner.scan(False)
        if scanner.token_type != "id":
            self.syntax_error("expected property name in filter expression: " + prop)

        op = self.scan_relational_op(scanner)

        # expressions can be complicated; we want the rest of the string containing the filter
        value = scanner.get_rest_of_text()

        # adjust for for :id: operators
        if op == ":" and ":" in value:
            op2, value = value.split(":", 1)
            op += op2 + ":"

        value = {"prop": prop, "op": op, "value": value}
        #print("process_prop_op_value: value=", value)
        return value

    def process_option_value(self, opt_name, opt_type, value, values):

        if values:
            found = self.match_keyword(value, values)
            if not found:
                self.syntax_error("Value for option {} not recognized: {}, must be one of: {}".format(opt_name, value, ", ".join(values)))
            value = found

        elif opt_type == "flag":
             value = self.parse_flag_value(opt_name, value)

        elif opt_type == "int":
            value = int(value)

        elif opt_type == "float":
            value = float(value)

        elif opt_type == "bool":
            value = value.lower()
            if value in ["true", "1"]:
                value = True
            elif value in ["false", "0"]:
                value = False
            else:
                self.syntax_error("Illegal value for boolean option: " + str(value))

        elif opt_type == "prop_op_value":
            value = self.process_prop_op_value(value)

        elif opt_type == "str_list":
            if not isinstance(value, list):
                value = [value]

        elif opt_type == "named_arg_list":
            if not isinstance(value, list):
                value = [value]
            value = self.convert_str_list_to_arg_dict(value)

        elif opt_type == "int_list":
            if not isinstance(value, list):
                value = [value]

        elif opt_type == "num_list":
            if not isinstance(value, list):
                value = [value]

        elif opt_type == "str":
            value = self.expand_system_values(value)

        else:
            errors.internal_error("unrecognized option type: {}".format(opt_type))

        return value

    def convert_str_list_to_arg_dict(self, values):
        ad = {}
        for value in values:
            if not "=" in value:
                self.syntax_error("named arg value must contain an equals sign ('='): {}".format(value))

            name, val = value.split("=")
            name = name.strip()
            val = val.strip()

            ad[name] = val

        return ad
        
    def get_dispatch_cmd(self):
        return self.dispatch_cmd

    def is_single_token(self, text):
            ms = Scanner(text)

            # scan first token
            tok = ms.scan()

            # try to get second token
            tok = ms.scan()
            tok2 = ms.scan()

            single = (tok is None)
            single_with_comma = (tok == "," and tok2 is None)
            return single, single_with_comma

    # def add_quotes_to_string_args(self, args):
    #     #console.print("BEFORE: self.args=", self.args)

    #     for i, arg in enumerate(args):

    #         # we currently process our options and those of ML app

    #         #if arg.startswith("-"):
    #         # parse option or tag: name=text
    #         if "=" in arg:
    #             # --option=value  (we only care about FIRST '=')
    #             name, text = arg.split("=", 1)
    #             single, single_with_comma = self.is_single_token(text)

    #             if not single and not single_with_comma:
    #                 # add back quotes that were string by the shell/command processor
    #                 arg = name + '="' + text + '"'
    #                 args[i] = arg
    #         elif arg != "=":
    #             # parse target or option value
    #             if not self.is_single_token(arg):
    #                 arg = '"' + arg + '"'
    #                 args[i] = arg


    def validate_and_add_defaults(self, arguments, options, arg_dict):
        '''
        args:
            - arguments: list of the arguments for the current cmd 
            - options: list of options for the current cmd
            - arg_dict: dict of name/value pairs for user-specified args and options

        processing:
            - copy arg_dict to "explicit_options"
            - validate all names in arg_dict (against arguments & options)
            - flag as error if any required arguments/options are not specified in arg_dict
            - add default values for all arguments/options not yet specified inarg_dict

        return:
            - fullly populated copy of arg_dict
        '''
        # ensure all names in arg_dict are dash style (for validation)
        full_arg_dict = { key.replace("_", "-"):value for key, value in arg_dict.items() }

        # remember options that were set explicitly (dash-style)
        global explicit_options
        explicit_options = dict(full_arg_dict)

        # process all aguments, options, and flags; ensure each has a value in arg_dict
        all_args = arguments + options
        all_arg_dict = {aa["name"]: aa for aa in all_args}

        # process user args in arg_dict 
        # caution: this loop may update full_arg_dict so capture keys up front
        keys = list(full_arg_dict.keys())

        for name in keys:
            value = full_arg_dict[name]

            # validate arg name
            if not name in all_arg_dict:
                errors.api_error("unknown args name: {}".format(name))

            # does name need to be replaced by arg_name of option/argument?
            info = all_arg_dict[name]
            if "arg_name" in info:
                arg_name = info["arg_name"]
                if name != arg_name:
                    # update the name to arg_name
                    full_arg_dict[arg_name] = value
                    del full_arg_dict[name]

        # now add default values for all other args
        for info in all_args:
            # don't add layer marker to args
            if info["type"] == "layer":
                continue

            name = info["arg_name"] if "arg_name" in info else info["name"]
            
            required = info["required"] if "required" in info else None

            if not name in full_arg_dict:
                if required:
                    self.syntax_error("cmd '{}' missing value for required option: --{}".format(self.cmd_words, name))

                default_value = utils.safe_value(info, "default")

                # expand "$group.value" type values
                default_value = self.get_default_from_config(default_value)

                # add to user's arg dict
                full_arg_dict[name] = default_value

        # finally, convert all names to underscore style
        full_arg_dict = { key.replace("-", "_"): value for key, value in full_arg_dict.items() }

        console.diag("full_arg_dict=", full_arg_dict)
        return full_arg_dict

    def syntax_error(self, msg):
        console.print(msg)
        self.show_current_command_syntax()

        if self.raise_syntax_exception:
            errors.syntax_error("syntax error")
        
        errors.syntax_error_exit()

    def replace_curlies_with_quotes(self, text):
        '''
        replace any {} that appear outside of quotes with single quotes UNLESS
        they are part of a --template option value.
        '''

        new_text = ""
        protector = None
        inside_template = False

        for ch in text:
            if ch == protector:

                # end of a quoted string
                protector = None
                if ch == "}":
                    ch = "'"
            elif not protector:

                # outside of a quoted string
                if ch in ["'", '"', "{"]:
                    # start of a quoted string
                    if ch == "{":
                        protector = "}"
                        ch = "'"
                    else:
                        protector = ch

            new_text += ch

        return new_text

    def extract_template_option(self, cmd):
        '''
        parse the --template option for the "xt view tensorboard" cmd
        '''
        template_option = None
        new_args = []
        parsing_template = False
        args = cmd_utils.xt_cmd_split(cmd)

        for arg in args:

            if arg.startswith("--"):
                # start of an option
                left = arg.split("=")[0]
                opt_name = left[2:].strip()

                if match(opt_name, "template"):
                    parsing_template = True
                    template_option = arg
                else:
                    parsing_template = False
                    new_args.append(arg)

            elif parsing_template:
                # another value of template
                template_option += " " + arg

            else:
                new_args.append(arg)

        new_cmd = cmd_utils.join_args(new_args)

        return template_option, new_cmd
        
    def get_layers_dest(self, options):
        dest = None

        for opt in options:
            if opt["type"] == "layer":
                dest = opt["dest"]
                break

        return dest

    def dispatch(self, text, is_rerun=False, capture_output=False, raise_syntax_exception=False):
        self.raise_syntax_exception = raise_syntax_exception
        
        # be sure to reset this for each parse (for multi-command XT sessions)
        global explicit_options
        explicit_options = {}

        if "--tem" in text:
            # extract the --template option (xt view tensorboard) since it has curly brackets that are not converted to quotes
            template_option, text = self.extract_template_option(text)

            # NOTE: Windows/Linux command line parsers typically strip away quotes found in cmd
            # XT allows allows the user to use {} as a 2nd set of quotes around complex values (that won't get stripped away)
            text = self.replace_curlies_with_quotes(text)

            # add back template option
            if template_option:
                text += " " + template_option

            console.diag("\nADJUSTED cmd={}".format(text))
        elif "{" in text:
            # replace curly brackets with quotes
            text = text.replace("{", "\"").replace("}", "\"")

        self.dispatch_cmd = text


        scanner = Scanner(text)
        tok = scanner.scan()

        # process any ROOT FLAGS
        if root_cmd_info:
            tok = self.process_root_options(scanner, tok)
        else:
            # there is no command to process --console, so set it explictly now
            console.set_level("normal")

        console.diag("start of command parsing: {}".format(text))

        # process any options before the cmd as RAW options
        # raw_options = []
        # tok = self.collect_raw_options(raw_options, scanner, tok)

        # process COMMAND keywords
        cmd_info, tok = self.get_cmd_info(tok, scanner)
        self.cmd_info = cmd_info

        if "kwgroup_name" in cmd_info:
            cmd_info = get_command("help")

        self.cmd_info = cmd_info

        # does this command use an @unknown option?
        options = cmd_info["options"]
        self.unknown_option = None
        for opt in options:
            if opt["name"] == "_unknown_":
                self.unknown_option = opt
                break

        cmd_name = cmd_info["name"]
        self.cmd_words = cmd_name.replace("_", " ")
        func = cmd_info["func"]
        options = cmd_info["options"]
        arguments = cmd_info["arguments"]
        options_before_args = cmd_info["options_before_args"]

        # command-specific help?
        # if "help" in raw_options:
        #     help_value = raw_options["help"]
        #     if help_value != None:
        #         self.syntax_error("unexpected text after '--help': " + help_value)
        if tok == "--help":
            help_value = scanner.scan()

            if help_value != None:
                self.syntax_error("unexpected text after '--help': " + help_value)

            caller = self.impl_dict[command_help_func.__module__]
            if self.preprocessor:
                self.preprocessor(caller, arguments)

            command_help_func("help", caller, cmd_info)
            return

        # build a dictionary of arguments and options to be passed
        arg_dict = {}

        if options_before_args:
            # options come before arguments
            tok = self.parse_options(arg_dict, options, scanner, tok)
            tok = self.process_arguments(scanner, tok, arguments, arg_dict)
        else:
            # arguments come before options
            tok = self.process_arguments(scanner, tok, arguments, arg_dict)
            tok = self.parse_options(arg_dict, options, scanner, tok)

        # there should be no remaining tokens
        if tok:
            errors.argument_error("end of input", tok)

        # add unknown options, if found
        if self.unknown_option:
            self.add_unknown_to_layer(arg_dict, layer_seen=False)

        full_arg_dict = self.validate_and_add_defaults(arguments, options, arg_dict)

        dest = self.get_layers_dest(options)
        if dest: 
            full_arg_dict[dest] = self.layers

        console.diag("dispatching to command func")

        # select the caller using function's module name
        caller = self.impl_dict[func.__module__]
        if capture_output:
            caller.set_capture_output(True)
 
        if is_rerun:
            full_arg_dict["is_rerun"] = 1

        if "_unknown_" in full_arg_dict:
            del full_arg_dict["_unknown_"]

        # call the matching command function with collected func args
        if self.preprocessor:
            self.preprocessor("command", caller, full_arg_dict)

        if cmd_info["pass_by_args"]:
            func(caller, args=full_arg_dict)
        else:
            func(caller, **full_arg_dict)

        console.diag("end of command processing")
        output = None

        if capture_output:
            output = caller.set_capture_output(False)

        return output

    def parse_options(self, arg_dict, options, scanner, tok):
        '''
        TODO: parse scanned option according to the *options* argument, 
        not as "raw options".  
        '''
        raw_options = []

        #tok = self.collect_raw_options(raw_options, scanner, tok)
        #self.process_raw_options(options, raw_options, arg_dict)
        tok = self.process_cmd_options(arg_dict, options, scanner, tok)

        return tok

    def process_cmd_options(self, arg_dict, options, scanner, tok):

        while tok and tok.startswith("--"):
            name = tok[2:]    # remove dashes
            match = self.list_item_by_name(name, options)
            if match:
                tok = self.parse_cmd_option(match, scanner, tok, arg_dict)
            else:
                if self.cmd_info["user_filters"]:
                    # see if option name is the name of a user-defined filter
                    match_name = self.list_item_by_value(name, self.user_filters.keys())
                    if match_name:
                        match = self.user_filters[match_name]
                        tok = self.parse_user_filter(match, scanner, tok, arg_dict)

            if not match:
                self.syntax_error("cmd '{}' doesn't have an option named: {}".format(self.cmd_words, tok))
 
        return tok

    def parse_user_filter(self, match, scanner, tok, arg_dict):            

        tok = scanner.scan()        # skip over name
        
        match_prop = match["prop"]
        match_type = match["type"]
        match_op = utils.safe_value(match, "op")
        match_value = utils.safe_value(match, "value")

        if match_op and match_value:
            # user filter is a complete filter
            filter = {"prop": match_prop, "op": match_op, "value": match_value}
        else:
            filter = {"prop": match_prop}

            ops = ["=", "<", "<=", ">", ">=", "==", "!=", "<>"]
            if tok in ["=", "<", "<=", ">", ">=", "==", "!=", "<>"]:
                compare_op = tok
                tok = scanner.scan()        # skip over comparison op
            else:
                compare_op = "="

            filter["op"] = compare_op

            values = None
            required = False

            value, tok = self.parse_option_value(match_prop, match_type, values, compare_op, tok, scanner, 
                required)

            filter["value"] = value

        # add filter to filter list in arg_dict
        if not "filter" in arg_dict:
            arg_dict["filter"] = []

        arg_dict["filter"].append(filter)
        return tok

    def arguments_contain(self, arguments, name):
        found = False
        for arg in arguments:
            if arg["name"] == name:
                found = True
                break

        return found

    def remove_optional_args(self, arg_dict):
        arguments = self.cmd_info["arguments"]

        for key in list(arg_dict):
            if not self.arguments_contain(arguments, key):
                del arg_dict[key]

    def add_unknown_to_layer(self, arg_dict, layer_seen:bool):
        # this part is hard-coded to get seaborn working with multiple layers
        # TODO: make use of --type more generalized
        # add current --type from arg dict
        if not "type" in arg_dict:
            if layer_seen:
                errors.syntax_error("required --type option not specified in previous layer")
            else:
                errors.syntax_error("required --type option not specified")

        self.unknown_dict["type"] = arg_dict["type"]
        self.layers.append(dict(self.unknown_dict))

        del arg_dict["type"]
        self.unknown_dict = {}

    def parse_cmd_option(self, match, scanner, tok, arg_dict):            

        option_type = match["type"]
        force_string = option_type in ["str"]

        value = True
        found_equals = False
        name = match["name"]        # full name

        # need to peek here to set force_string correctly
        next_tok = scanner.peek()

        if next_tok == "=":
            tok = scanner.scan()
            found_equals = True
            tok = scanner.scan(force_string=force_string)        # skip over equals
        else:
            tok = scanner.scan(force_string=force_string)        # skip over name

        value = tok
        if value and value.startswith("--"):
            # this is a new option, not a value
            value = None

        # special handling for options with no value
        required = utils.safe_value(match, "required")
        if value is None and not required:
            value = 1

        if name == "layer":
            # layer's job is to accumulate all previous args into a layer dict, and append to self.layers
            if self.unknown_option:
                self.add_unknown_to_layer(arg_dict, layer_seen=True)

            elif arg_dict:
                self.layers.append(dict(arg_dict))
                self.remove_optional_args(arg_dict)

        else:
            values = match["values"] if "values" in match else None
            #value = self.process_option_value(name, match["type"], value, values)

            value, tok = self.parse_option_value(name, match["type"], values, found_equals, tok, scanner, 
                required)

            if "unknown" in match:
                # place in special argdict
                self.unknown_dict[name] = value
                self.unknown_dest = match["dest"]

            else:
                self.add_to_arg_dict(arg_dict, name, value)
                arg_dict[name] = value

        return tok
    
    def add_to_arg_dict(self, arg_dict, name, value):
        # preserve order of arguments: if duplicate, del first occurance and append to dict
        if name in arg_dict:
            del arg_dict[name]

        arg_dict[name] = value

    def parse_option_value(self, name, opt_type, keywords, found_equals, tok, scanner, required=False):

        if keywords:
            if required is None:
                # when keywords are specified, the default is that the value is required
                required = True

            user_value = self.expand_system_values(tok)
            if user_value is None:
                user_value = ""

            tok = scanner.scan()
            value = self.match_keyword(user_value, keywords)
            if value is None:
                if required:
                    self.syntax_error("value specified for option --{} ({}) is not one of required values: {}".\
                        format(name, user_value, ", ".join(keywords)))
                else:
                    value = user_value            

        elif opt_type == "str_list":
            value, tok = self.parse_string_list(tok, scanner)
            if len(value)==0 and required:
                self.syntax_error("missing value for required option: " + name)

        elif opt_type == "num_list":
            value, tok = self.parse_num_list(tok, scanner)
            if len(value)==0 and required:
                self.syntax_error("missing value for required option: " + name)

        elif opt_type == "int_list":
            value, tok = self.parse_int_list(tok, scanner)
            if len(value)==0 and required:
                self.syntax_error("missing value for required option: " + name)

        elif opt_type == "tag_list":
            value, tok = self.parse_tag_list(tok, scanner)
            if len(value)==0 and required:
                self.syntax_error("missing value for required option: " + name)

        elif opt_type == "prop_op_value":
            value, tok = self.parse_prop_op_value_list(tok, scanner)
            if len(value)==0 and required:
                self.syntax_error("missing value for required option: " + name)

        elif opt_type == "named_arg_list":
            value, tok = self.parse_string_list(tok, scanner)
            if not isinstance(value, list):
                value = [value]
            value = self.convert_str_list_to_arg_dict(value)

        elif opt_type == "flag":
            if found_equals:
                value = tok
                tok = scanner.scan()
                value = self.parse_flag_value(name, value)
            else:
                value = True

        elif opt_type == "template_value":
            # get rest of str (any chars except a space)
            value = tok + scanner.get_rest_of_token_until_space()
            tok = scanner.scan()

        else:
            # its a simple value type
            value = tok
            tok = scanner.scan()

            if opt_type == "int":
                value = int(value)

            elif opt_type == "float":
                value = float(value)

            elif opt_type == "bool":
                value = value.lower()
                if value in ["true", "1"]:
                    value = True
                elif value in ["false", "0"]:
                    value = False
                else:
                    self.syntax_error("Illegal value for boolean option: " + str(value))
            elif opt_type == "str":
                if value is None:
                    # to distinguish between unspecified option and one specified with no value
                    value = ""
                value = self.expand_system_values(value)

            else:
                errors.internal_error("Unsupported opt_type={}".format(opt_type))
        
        return value, tok

# flat functions
def match(text, cmd):
    '''
    user can abbreviate down to 3 letters, but text must unambiguosly select
    an keyword.
    '''
    return cmd == text or (len(text) >= 3 and cmd.startswith(text))

