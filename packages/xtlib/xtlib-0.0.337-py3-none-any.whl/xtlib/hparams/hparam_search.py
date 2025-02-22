#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# hparam_search.py: XT controller side of hparam processing: determine set of hyperparameter values for next child run
import os
import sys
import json
import time
import yaml
import importlib
import numpy as np

from hyperopt import hp
    
from xtlib import utils
from xtlib import errors
from xtlib import constants
from xtlib import run_helper
from xtlib import store_utils
from xtlib.console import console
from xtlib.hparams import hp_helper

class HParamSearch():

    def __init__(self, is_aml=False):
        self.is_aml = is_aml
        self.run_history = []
        self.end_id = 0
        self.search_provider = None
        self.hp_records = None

    # main ENTRY POINT 
    def process_child_hparams(self, child_name, store, context, parent):
        '''
        determine set of hyperparameter values for child_name, update config file, 
        and return updated cmd_parts, as appropriate for search type
        '''
        arg_dict = None

        if context.hp_config:
            # read hp config file from experiment or job
            if context.aggregate_dest == "experiment":
                text = store.read_experiment_file(context.ws, context.dest_name, context.hp_config)
            else:    
                # assume sweeps file is at the job level
                text = store.read_job_file(context.ws, context.dest_name, context.hp_config)

            arg_dict = self.generate_hparam_set(text, child_name, store, context)
            
        return arg_dict

    def apply_runset(self, arg_dict, cmd_parts, context, store, child_name):
        '''
        processing:
            - generate a yaml runset file & write to run store
            - apply runset to run_cmd, if appropriate 
        '''

        if context.option_prefix != None:
            self.apply_runset_to_cmd_parts(arg_dict, cmd_parts, context)

            # update context (critical if this run gets preempted/restarted)
            context.cmd_parts = cmd_parts

        # always write a YAML runset file
        runset = {constants.HPARAM_RUNSET: arg_dict}
        sweep_text = yaml.dump(runset)

        fn_target = context.fn_generated_config
        console.print("HP fn_target=", fn_target)

        if self.is_aml:
            # AML doesn't have a lightweight way of adding a file to the Snapshot
            # KISS and just use context to store until we start run process
            context.generated_sweep_text = sweep_text
        else:
            # upload config file for sweep args to child-specific BEFORE folder
            store.create_run_file(context.ws, child_name, "before/" + fn_target, sweep_text)

        return cmd_parts

    def generate_hparam_set(self, search_file_text, run_name, store, context):
        '''
        generate a set of hyperparameter values, based on the algorithm specified by
        context.search_type.
        '''

        # parse text into {name: text, value: text, spacefunc: space_func} records
        text = search_file_text.replace("\r", "")

        # we only support yaml format here
        import yaml
        hparams = yaml.safe_load(text)
        hparams = hparams[constants.HPARAM_DIST]

        # algorithm-specific processing
        search_type = context.search_type
        records = self.parse_hp_config_yaml(hparams, search_type)

        # get code_path for search_type from hpsearch_providers
        arg_dict = self.hp_search_core(context, search_type, store, run_name, records)
        return arg_dict

    def hp_search_core(self, context, search_type, store, run_name, space_records):
        # get code_path for search_type from hpsearch_providers
        search_ctr = utils.get_provider_class_ctr_from_context(context, "hp-search", search_type)
        impl = search_ctr()
        need_runs = impl.need_runs()
        runs = None

        utils.log_title("HP_SEARCH_CORE")

        utils.log_info("run_name", context.run_name)
        utils.log_info("primary_metric", context.primary_metric)
        utils.log_info("maximize_metric", context.maximize_metric)

        if need_runs:
            # this could be a lengthly delay
            started = time.time()
            runs = self.get_completed_runs(store, context) 
            elapsed = time.time() - started

            utils.log_info("get_completed_runs, elapsed", elapsed)
            utils.log_info("len(all_runs)", len(runs))
            utils.log_info("new_run_count", self.new_run_count)

        utils.log_title("HP SEARCH: " + search_type)

        # workaround issue for quicktest with older runs using 'seed' hparam
        if runs:
            for run in runs:
                if "hparams" in run:
                    hparams = run["hparams"]
                    if "seed" in hparams:
                        del hparams["seed"]
            
        arg_dict = impl.search(run_name, store, context, space_records, runs=runs)

        # fix up returned values 
        if arg_dict:
            for key, value in arg_dict.items():
                if isinstance(value, (np.float32, np.float64)):
                    arg_dict[key] = value.item()

            console.print("\n---- search_type={}, returned arg_dict={} ----\n".format(search_type, arg_dict))

        # save for processing end of run
        self.search_provider = impl
        self.hp_records = space_records

        return arg_dict

    def make_values_consistent(self, values):
        '''
        To try and prevent errors in hyperopt (bayesian search), if any values 
        in list are float, make them all float.
        '''
        is_float = False

        for value in values:
            if isinstance(value, float):
                is_float = True
                break

        if is_float:
            values = [float(val) for val in values]

        return values

    def parse_hp_config_yaml(self, hparams, search_type):
        # use original size=() for randint on hyperopt (bayesian) search
        hp_size = (search_type == "bayesian")

        records = []
        for prop, value in hparams.items():
            # value can be a list, a number, or a string
            fa = hp_helper.parse_hp_dist(value)
            space_func = hp_helper.build_dist_func_instance(prop, fa["func"], fa["args"], hp_size)

            # for DGD: generate a text-file compatible version of value
            if isinstance(value, str) and value.startswith("$randint"):
                # looks like "randint" is no longer processed by DGD search, so just pick a value now
                import random
                vs = str(random.randint(0, 65535))

            elif isinstance(value, str) and value.startswith("$linspace"):
                # the values generated from linspace are in "args"
                args = list(fa["args"])
                vs = str(args)

            elif isinstance(value, (list,tuple)):  
                # this is the most commonly used XT search space: a list of values
                value = self.make_values_consistent(value)

                strs = [str(v) for v in value]
                vs = (", ").join(strs)

            else:
                vs = str(value).strip()

            if isinstance(vs, str) and vs.startswith("["):
                vs = vs[1:-1]
                
            record = {"name": prop, "value": vs, "space_func": space_func}
            records.append(record)

        return records

    def update_cmd(self, cmd_parts, insert_index, option_prefix, arg, value):
        prefix = option_prefix + arg 
        prefix_eq = prefix + "="
        new_part = prefix_eq + str(value)

        if insert_index:
            cmd_parts.insert(insert_index, new_part)
            insert_index += 1
        else:
            # remove previous arg, if present
            part = None

            for i, part in enumerate(cmd_parts):
                if part == prefix or part.startswith(prefix_eq):
                    del cmd_parts[i]
                    break

            # add new arg to end
            if part:
                cmd_parts.append(part)

        return insert_index

    def get_completed_runs(self, store, context):
        if context.aggregate_dest == "job":
            filter_dict = {"job_id": context.dest_name}
        elif context.aggregate_dest == "experiment":
            filter_dict = {"exper_name": context.dest_name}
        else:
            errors.general_error("unrecognized aggregation dest: {}".format(context.aggregate_dest))
            
        # get next "end_id" to be assigned to an ending run
        next_end_id = store.database.get_next_end_id_without_update(context.ws)

        # we are using in-memory cache (self.run_history holds runs whose end_id is <= self.end_id)
        # we specify a max value for end_id so queries return consistent results (avoid dup records)
        # build a filter to find all runs where: end_id > self.end_id and end_id < next_end_id
        #filter_dict["end_id"] = {"$gt": self.end_id}

        # TODO: improve this
        # it is not ideal to have separate code here for each storge version, but v3 is not
        # yet equiped to handle the mongo implicit $and format, and this form of the "$and" operator
        # (as a field name value) is not supported by mongo (v1 format).
        if store_utils.STORAGE_FORMAT == "1":
            filter_dict["end_id"] = {"$gt": self.end_id}     # , "$lt": next_end_id} 
        else:
            filter_dict["end_id"] = {"$and": [{"$gt": self.end_id}, {"$lt": next_end_id} ] }

        # only look at runs whose status = "complete"
        filter_dict["status"] = "completed"

        # only look at runs with primary metric defined
        metric = "metrics." + context.primary_metric
        filter_dict[metric] = {"$exists": True}

        # fields needed for dgd and bayesian searches
        fields_dict = {"run_name": 1, "end_id": 1, "hparams": 1, metric: 1}

        fn_cache = "hparams_search.cache"

        # get all completed runs from DB
        new_runs = store.get_all_runs(context.aggregate_dest, context.ws, context.dest_name, filter_dict, fields_dict,
            use_cache=False)

        # merge new runs with previous
        # utils.log_info("filter_dict", filter_dict)
        # utils.log_info("fields_dict", fields_dict)
        
        # utils.log_info("get_completed_runs, self.end_id", self.end_id)
        # utils.log_info("get_completed_runs, next_end_id", next_end_id)
        # utils.log_info("get_completed_runs, run_history", len(self.run_history))
        # utils.log_info("get_completed_runs, new_runs", len(new_runs))

        runs = self.run_history + new_runs

        # update cache
        self.run_history = runs
        self.new_run_count = len(new_runs)

        if self.new_run_count:
            end_ids = [run["end_id"] for run in new_runs if "end_id" in run]
            self.end_id = max(end_ids)

        return runs

    def process_end_of_run(self, store, context):
        utils.log_title("HP SEARCH (PROCESS_END_OF_RUN): " + context.search_type)
        utils.log_info("run_name", context.run_name)
        utils.log_info("primary_metric", context.primary_metric)

        self.search_provider.process_end_of_run(store, context, self.hp_records)
        console.print("")
   
    def apply_runset_to_cmd_parts(self, arg_dict, cmd_parts, context, insert_before=False):
        # if insert_before=True, we would like to insert the new HP values BEFORE the potential override options
        # that are specified in cmd_parts, so try to set insert_index based on what we 
        # can figure out about cmd_parts
        if insert_before:
            insert_index = self.find_insert_index(cmd_parts)
        else:
            insert_index = None

        for prop, value in arg_dict.items():
            # update cmd
            if insert_before:
                insert_index = self.update_cmd(cmd_parts, insert_index, context.option_prefix, prop, value)
            else:
                new_part = "{}{}={}".format(context.option_prefix, prop, value)
                cmd_parts.append(new_part)
                
    def find_insert_index(self, cmd_parts):
        console.print("find_insert_index: cmd_parts=", cmd_parts)
        insert_index = None
        
        first = cmd_parts[0]
        count = len(cmd_parts)

        if first.endswith(".bat") or first.endswith(".sh"):
            insert_index = 1   
        elif first in ["python", "python3"]:
            for i in range(1, count):
                part = cmd_parts[i]
                if not part.startswith("-") and part.endswith(".py"):
                    insert_index = 1 + i
                    break
        elif first in ["run"]:
            insert_index = 2

        # for some cases, like "docker run <options and values> <image> <cmd> <args>",
        # we will just append at end (and lose the ability to override the generated options)

        console.print("INITIAL insert_index=", insert_index)
        return insert_index

