#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# reportt_builder.py: builds the report shown in "list jobs", "list runs", etc. cmds
import os
import sys
import json
import time
from xtlib.pc_utils import COLORS
import arrow
import math
import numpy as np
from fnmatch import fnmatch
from collections import OrderedDict, defaultdict

from xtlib.console import console

from xtlib import qfe
from xtlib import utils
from xtlib import errors
from xtlib import pc_utils
from xtlib import constants
from xtlib import time_utils
from xtlib.hp_set import HpSetFormatter
from xtlib.html_writer import HtmlWriter
from xtlib.html_clipboard_tables import HtmlClipboardTables
from xtlib.event_processor import get_ids_from_python_expression

def safe_format(fmt, value, col_width):
    if value is None:
        text = ""
    elif value == "":
        text = col_width*" "
    elif fmt is None:
        text = str(value)
    else:
        text = fmt.format(value)

    return text

class ReportBuilder():
    def __init__(self, config=None, store=None):
        self.config = config
        self.store = store
        self.user_col_args = {}
        self.hp_set_formatter = HpSetFormatter()
        self.col_headers = None
        self.calc_col_helper = None

        self.time_col_names = [
            # run: create_time/created, start_time/started, last_time, end_time/ended
            # node: create_time, prep_start_time, app_start_time, post_start_time, post_end_time
            # job: started, run_started, end_time
            "created", "started", "last_time", "ended",
            "create_time", "prep_start_time", "app_start_time", "post_start_time", "post_end_time",
            "run_started", "end_time",
        ]

        self.duration_col_names = [
            # run: queue_duration (aka queued), run_duration (aka duration)
            # node: queue_duration, prep_duration, app_duration, post_duration
            # job: queue_duration, run_duration
            "queued", "duration",
            "queue_duration", "prep_duration", "app_duration", "post_duration",
            "run_duration",
        ]   

        self.duration_map = {
                # RUN: queue_duration, run_duration (user names used below)
                "queued": "created", "duration": "started",
                
                # NODE
                "queue_duration": "queue_start_time", "prep_duration": "prep_start_time", 
                "app_duration": "app_start_time", "post_duration": "post_start_time",
                
                # JOB
                "queue_duration": "started",   
                "run_duration": "run_started", 
                }

    def wildcard_matches_in_list(self, wc_name, name_list, omits):
        matches = []

        if name_list:
            matches = [name for name in name_list if fnmatch(name, wc_name) and not name in omits]
            
        return matches

    def default_user_name(self, col_name):
        user_name = col_name

        if col_name.startswith("hparams."):
            user_name = col_name[8:]
        elif col_name.startswith("metrics."):
            user_name = col_name[8:]
        else:
            user_name = col_name

        return user_name

    def get_requested_cols(self, user_col_args, avail_list):
        actual_cols = []
        new_col_args = []
        
        for value in user_col_args:
            key = value["key"]
            calculated_exp = value["calculated_exp"]

            # if the requested key is available, include it
            if "*" in key:
                # wildcard match
                if key.startswith("metrics."):
                     matches = self.wildcard_matches_in_list(key, name_list=avail_list, omits=["metrics." + constants.STEP_NAME, "metrics.$step_name", "metrics._id", "metrics.ws_name"])

                elif key.startswith("hparams."):
                     matches = self.wildcard_matches_in_list(key, name_list=avail_list, omits=["hparams._id", "hparams.ws_name"])

                elif key.startswith("tags."):
                     matches = self.wildcard_matches_in_list(key, name_list=avail_list, omits=["tags._id", "tags.ws_name"])

                else:
                    errors.api_error("wildcards not allowed with this column: {}".format(key))

                actual_cols += matches

                # replace our wildcard in request_list with matches
                for match in matches:
                    user_name = self.default_user_name(match)
                    new_value = {"user_name": user_name, "user_fmt": None}
                    #new_col_args[match] = new_value
                    new_value["key"] = match
                    new_col_args.append(new_value)

            elif calculated_exp:
                # always include calculated columns
                actual_cols.append(key)
                #new_col_args[key] = value
                value["key"] = key
                new_col_args.append(value)
        
            elif key in avail_list:
                actual_cols.append(key)
                #new_col_args[key] = value
                value["key"] = key
                new_col_args.append(value)
        
        return actual_cols, new_col_args

    def sort_records(self, records, sort_col, reverse):
        if reverse is None:
            reverse = 0

        console.diag("after reportbuilder SORT")
        console.diag("sort_col={}".format(sort_col))

        # normal sort
        records.sort(key=lambda r: r[sort_col] if sort_col in r and r[sort_col] else 0, reverse=reverse)

        console.diag("after reportbuilder SORT")

    def expand_special_symbols(self, value):

        if isinstance(value, str):
            value = value.strip()

            if value == "$none":
                value = {"$type": 10}
            elif value == "empty":
                value = ""
            elif value == "$true":
                value = True
            elif value == "$false":
                value = False
            elif value == "$exists":
                value = {"$exists": True}

        return value

    def process_filter_list(self, filter_dict, filter_exp_list, report2filter):
        '''
        used to filter records for following expressions of form:
            - <prop name> <relational operator> <value>

        relation operators:
            - =, ==, <, <=, >, >=, in, not-in, contains, not-contains, exists

        special values:
            - $exists   (does property exist)
            - $none     (None, useful for matching properties with no value)
            - $empty    (empty string)
            - $true     (True)
            - $false    (False)
        '''
        for filter_exp in filter_exp_list:
            prop = filter_exp["prop"]
            op = filter_exp["op"]
            value = filter_exp["value"]
            
            # translate name, if needed
            if prop in report2filter:
                prop = report2filter[prop]

            if isinstance(value, str):
                value = self.expand_special_symbols(value)
                value = utils.make_numeric_if_possible(value)

            if op in ["=", "=="]:
                filter_dict[prop] = value
            elif op == "<":
                filter_dict[prop] = {"$lt": value}
            elif op == "<=":
                filter_dict[prop] = {"$lte": value}
            elif op == ">":
                filter_dict[prop] = {"$gt": value}
            elif op == ">=":
                filter_dict[prop] = {"$gte": value}
            elif op in ["!=", "<>"]:
                filter_dict[prop] = {"$ne": value}
            elif op == ":regex:":
                filter_dict[prop] = {"$regex" : value}
            elif op == ":exists:":
                filter_dict[prop] = {"$exists" : value}
            elif op == "in":
                value = [val.strip() for val in value.split(",")]
                filter_dict[prop] = {"$in" : value}
            elif op == "not-in":
                value = [val.strip() for val in value.split(",")]
                filter_dict[prop] = {"$nin" : value}
            elif op == "contains":
                value = [val.strip() for val in value.split(",")]
                filter_dict[prop] = {"$contains" : value}
            elif op == "not-contains":
                value = [val.strip() for val in value.split(",")]
                filter_dict[prop] = {"$ncontains" : value}
            elif op == ":database:":
                # raw filter dict, but we need to translate quotes and load as json
                value = value.replace("`", "\"")
                value = json.loads(value)
                filter_dict[prop] = value
            else:
                errors.syntax_error("filter operator not recognized/supported: {}".format(op))
        
    def available_cols_report(self, report_type, std_list, std_cols_desc, hparams_list=None, metrics_list=None, tags_list=None, avail_filter=None):
        lines = []

        if avail_filter == 1 or avail_filter == True:
            avail_filter = "all"

        if not avail_filter in ["all", "std", "hparams", "metrics", "tags"]:
            errors.general_error("invalid --available filter value: {}".format(avail_filter))

        if avail_filter in ["all", "std"]:
            lines.append("")
            lines.append("Standard {} columns:".format(report_type))
            if std_list:
                std_list.sort()
                for col in std_list:
                    if col in ["hparams", "metrics", "tags"]:
                        continue

                    if not col in std_cols_desc:
                        console.print("internal error: missing description for std col: " + col)
                        desc = ""
                    else:
                        desc = std_cols_desc[col]

                    lines.append("  {:<14s}: {}".format(col, desc))

        if avail_filter in ["all", "hparams"]:
            lines.append("")
            lines.append("Logged hyperparameters:")
            if hparams_list:
                hparams_list.sort()
                for col in hparams_list:
                    lines.append("  {}".format(col))

        if avail_filter in ["all", "metrics"]:
            if metrics_list:
                lines.append("")
                lines.append("Logged metrics:")

                metrics_list.sort()
                for col in metrics_list:
                    lines.append("  {}".format(col))
                metrics_list.sort()
                for col in metrics_list:
                    lines.append("  {}".format(col))

        if avail_filter in ["all", "tags"]:
            if tags_list:
                lines.append("")
                lines.append("Tags:")

                tags_list.sort()
                for col in tags_list:
                    lines.append("  {}".format(col))
                tags_list.sort()
                for col in tags_list:
                    lines.append("  {}".format(col))

        return lines

    def build_avail_list(self, col_dict, record, prefix=""):
        subs = ["metrics", "hparams", "tags"]

        for key in record.keys():
            if key in subs:
                value = record[key]
                if isinstance(value, dict):
                    self.build_avail_list(col_dict, value, prefix=key + ".")
            else:
                col_dict[prefix + key] = 1

    def flatten_records(self, records, sort_col, need_alive, which, user_columns=None, args=None):
        '''
        pull out the AVAILABLE or USER SPECIFIED columns, flattening nested props to their dotted names.
        '''

        # build avail col list based on final set of filtered records
        # actual_cols in the intersection of avail_cols and user_columns
        avail_cols, actual_cols, user_col_args  = self.get_avail_actual_user_cols(records, user_columns, args)

        # add often-needed cols for processing report
        for col in ["status"]:   # , "created", "started"]:
            if not col in actual_cols:
                actual_cols.append(col)

        # for each duration col in user_columns, add the corresponding start time column
        for col in self.duration_col_names:
            if user_columns and col in user_columns:
                start_col = self.get_start_col_for_duration_col(col)
                if not start_col in actual_cols:
                    actual_cols.append(start_col)

        # flatten each record's nested columns
        available = utils.safe_value(args, "available")

        add_if_missing_cols = []    # why were these being added? ["queued", "duration"]
        get_cols = avail_cols if available else actual_cols

        new_records = [self.extract_actual_cols(rec, get_cols, add_if_missing_cols) for rec in records if rec]
        return new_records

    def extract_actual_cols(self, record, actual_cols, add_if_missing_cols=None):
        '''
        pull out the cols specified in actual_cols, flattening nested props to their dotted names.
        '''
        new_record = {}

        for actual_key in actual_cols:
            if not actual_key:
                continue

            empty_value = constants.EMPTY_TAG_CHAR if actual_key.startswith("tags.") else None

            if "." in actual_key:
                # its a NESTED reference
                outer_key, inner_key = actual_key.split(".", 1)

                if outer_key in record:
                    inner_record = record[outer_key]
                    if inner_record and inner_key in inner_record:
                        value = inner_record[inner_key]
                        new_record[actual_key] = value if value is not None else empty_value
            else:
                # its a FLAT reference
                if actual_key in record:
                    value = record[actual_key]
                    new_record[actual_key] = value if value is not None else empty_value
    
        if add_if_missing_cols:
            for col in add_if_missing_cols:
                if not col in new_record:
                    new_record[col] = None

        return new_record

    def translate_record(self, record, actual_to_user):
        '''
        pull out the cols specified in actual_to_user, translating from storage names to user names.
        '''
        new_record = {}

        for actual_key, user_key in actual_to_user.items():
            if not actual_key:
                continue

            if actual_key in record:
                value = record[actual_key]
                new_record[user_key] = value 
    
        return new_record

    def get_first_last_all(self, args):

        def apply_fla(which, value, args):

            args[which] = value
            
            if value:
                if which == "first":
                    args["last"] = None
                    args["all"] = None

                elif which == "last":
                    args["first"] = None
                    args["all"] = None

                elif which == "all":
                    args["first"] = None
                    args["last"] = None

        # apply any default values from config file
        first = utils.safe_value(args, "first")
        last = utils.safe_value(args, "last")
        all = utils.safe_value(args, "all")

        apply_fla("first", first, args)
        apply_fla("last", last, args)
        apply_fla("all", all, args)
        
        # apply any explicit values from command line in the order specified on the command line
        explict = qfe.get_explicit_options()
        for which, value in explict.items():
            if which in ["first", "last", "all"]:
                apply_fla(which, value, args)  

        first = utils.safe_value(args, "first")
        last = utils.safe_value(args, "last")
        show_all = utils.safe_value(args, "all")

        return first, last, show_all

    def get_user_col_info(self, user_cols, col_name):

        for col in user_cols:

            name = col
            user_name = None
            fmt = None

            if "=" in name:
                name, user_name = col.split("=", 1)

            if ":" in name:
                name, fmt = name.split(":", 1)

            if name == col_name:
                return name, fmt, user_name
            
        return None, None, None

    def get_db_records(self, database, filter_dict, workspace, which, actual_to_user,
            col_dict=None, col_names_are_external=True, flatten_records=True, need_alive=False, 
            user_columns=None, hide_empty_cols=None, args=None):

        started = time.time()

        first, last, all = self.get_first_last_all(args)
        skip = utils.safe_value(args, "skip")

        list_nodes = utils.safe_value(args, "list_nodes")
        if list_nodes:
            which = "nodes"

        reverse = utils.safe_value(args, "reverse")
        # use database to do all of the work (query, sort, first/last)
        sort_col = utils.safe_value(args, "sort")   
        group_sort_col = utils.safe_value(args, "group_sort")   
        group_col = utils.safe_value(args, "group")   
        mean_cols = utils.safe_value(args, "mean")   
        add_cols = utils.safe_value(args, "add_columns")   

        if first:
            limiter = "first"
            limiter_value = first
        elif last:
            limiter = "last"
            limiter_value = last
        else:
            limiter = None
            limiter_value = 0

        sort_dir = 1
        hp_set_display = utils.safe_value(args, "hp_set_display")

        # if mean_col and not group_col:
        #     errors.syntax_error("cannot use --mean without setting the grouping column (--group)")

        user_to_actual = {value: key for key, value in actual_to_user.items()}

        if hp_set_display and hp_set_display != "hidden":
            # add to user_columns, if not already there
            name, _, _ = self.get_user_col_info(user_columns, "hp_set")
            if not name:
                user_columns.append("hp_set")

        if group_col == "hp_set" and hp_set_display == "hidden":
            # nice default for grouping
            hp_set_display = "changed"
            args["hp_set_display"] = hp_set_display

        if group_col:
            # add to user_columns, if not already there
            name, _, _ = self.get_user_col_info(user_columns, group_col)
            if not name:
                user_columns.append(group_col)

            # zap first/last/reverse flags for grouping phase
            first = None
            last = None
            reverse = False

        if group_sort_col:
            # add to user_columns, if not already there
            name, _, _ = self.get_user_col_info(user_columns, group_sort_col)
            if not name:
                user_columns.append(group_sort_col)
                
            if mean_cols:
                # fully qualify the group_sort_col name
                group_sort_col += "-mean"
                args["group_sort"] = group_sort_col

        if not sort_col:
            sort_col = "name"
        
        if sort_col:
            if sort_col == "name":

                # special sorting needed; we have created "xxx_num" fields just for this purpose
                if which == "runs":
                    sort_col = "run_num"
                elif which == "jobs":
                    sort_col = "job_num"
                elif which == "nodes":
                    sort_col = "node_num"

            elif not "." in sort_col:
                # translate name of std col from user-friendly version to logged version

                # if not sort_col in user_to_actual:
                #     errors.general_error("unknown standard property: {} (did you mean metrics.{}, hparams.{}, or tags.{}?)". \
                #         format(sort_col, sort_col, sort_col, sort_col))

                sort_col = user_to_actual[sort_col]

            # this is a TRICK to avoid having to call for the exists_count for calculation of skip count
            # it works fine, since we re-sort records on the xt client anyway
            sort_dir = -1 if reverse else 1
            if last:
                sort_dir = -sort_dir
                first = last

            # ensure we only ask for records where sort_col exists, or else we MIGHT end up with less than LIMIT records
            # don't think we need this anymore (rfernand, Nov-11-2022)
            # if sort_col != "run_num" and not sort_col in filter_dict:
            #     filter_dict[sort_col] = { "$exists": True}

        # validate specified col names
        self.validate_col(which, "--sort", sort_col)
        self.validate_col(which, "--group", group_col)

        if mean_cols:
            for mc in mean_cols:
                self.validate_col(which, "--mean", mc)

        if add_cols:
            for ac in add_cols:
                self.validate_col(which, "--add-columns", ac)
        else:
            add_cols = []
            args["add_columns"] = add_cols

        title = utils.safe_value(args, "title")
        if title:
            title_cols = self.get_cols_from_title(title)

            # validate and add cols from title to add_cols
            for col in title_cols:
                if not col in add_cols:
                    self.validate_col(which, "title cols", col)
                    add_cols.append(col)

        # always include ws_name (for now)
        if workspace and not "ws_name" in filter_dict:
            filter_dict["ws_name"] = workspace

        container = "run_info" if which == "runs" else "job_info"

        orig_col_dict =  col_dict
        # if not col_dict:
        #     col_dict = {"log_records": 0}

        console.diag("get_db_records: first={}, last={}, ws: {}, filter_dict: {}, col_dict: {}". \
            format(first, last, workspace, filter_dict, col_dict))

        count_runs = utils.safe_value(args, "count")
        buffer_size = utils.safe_value(args, "buffer_size", 50)

        started = time.time()

        if hide_empty_cols:
            for col in hide_empty_cols:
                if not col in user_to_actual:
                    errors.user_error("unknown column name in hide_empty_cols: {}".format(col))

            hide_empty_cols = [user_to_actual[col] for col in hide_empty_cols]

        # here is where DATABASE SERVICE does all the hard work for us
        if which == "runs":
            records = database.get_filtered_sorted_run_info(workspace, filter_dict, col_dict, sort_col, sort_dir, skip, first, 
                count_runs, buffer_size, hide_empty_cols=hide_empty_cols)

        elif which == "jobs":
            records = database.get_filtered_sorted_job_info(workspace, filter_dict, col_dict, sort_col, sort_dir, skip, first, 
                count_runs, buffer_size, hide_empty_cols=hide_empty_cols)

        elif which == "nodes":
            records = database.get_filtered_sorted_node_info(workspace, filter_dict, col_dict, sort_col, sort_dir, skip, first, 
                count_runs, buffer_size, hide_empty_cols=hide_empty_cols)

        elif which == "requests":
            records = database.get_filtered_sorted_request_info(workspace, filter_dict, col_dict, sort_col, sort_dir, skip, first, 
                count_runs, buffer_size, hide_empty_cols=hide_empty_cols)
        else:
            errors.internal_error("unrecognized value for which: {}".format(which))

        elapsed = time.time() - started
        console.diag("  query elapsed: {:.2f} secs".format(elapsed))

        console.diag("after full records retreival, len(records)={}".format(len(records)))

        if col_names_are_external:    # not orig_col_dict:
            # pull out standard cols, translating from actual to user-friendly names
            records = [self.translate_record(rec, actual_to_user) for rec in records if rec]

        exclude_from_hp_set = utils.safe_value(args, "exclude_from_hp_set") 

        # fixup null hp_set values using all logged hparams (don't filter by user_columns)
        if group_col == "hp_set" or (hp_set_display and hp_set_display != "hidden"):
            self.fixup_legacy_hp_set_nulls(records, exclude_from_hp_set)

        if flatten_records:
            # pull out requested cols, flattening nested values to their dotted names
            records = self.flatten_records(records, sort_col, need_alive, which, user_columns=user_columns, args=args)

        if last:
            # we had to reverse the sort done by database, so correct it here
            records.reverse()
            #self.sort_records(records, sort_col, reverse)

        elapsed = time.time() - started
        #console.print("  query stats: round trips={}, elapsed: {:.2f} secs".format(round_trip_count, elapsed))

        return records, limiter, limiter_value

    def validate_col(self, which, name, col_name):
        '''
        col_name could be in either user or actual names,
        depending on the caller.  we check for both.
        '''
        # prevent circular imports with JIT usage
        from xtlib import run_helper
        from xtlib import job_helper
        from xtlib import node_helper
        from xtlib import request_helper

        found = False

        if not col_name:
            found = True
        elif col_name.startswith("hparams."):
            found = True
        elif col_name.startswith("metrics."):
            found = True
        elif col_name.startswith("tags."):
            found = True
        elif which == "runs":
            found = col_name in run_helper.user_to_actual or col_name in run_helper.all_run_props
        elif which == "jobs":
            found = col_name in job_helper.user_to_actual or col_name in job_helper.all_job_props
        elif which == "requests":
            found = col_name in request_helper.user_to_actual or col_name in request_helper.all_job_props
        elif which == "nodes":
            found = col_name in node_helper.user_to_actual or col_name in node_helper.all_node_props
        else:
            errors.internal_error("validate_col(): 'which' value not yet supported: {}".format(which))

        if not found:
            errors.user_error("unknown standard column specified for {}: {} (did you mean metrics.{}, hparams.{}, or tags.{}?)". \
                format(name, col_name, col_name, col_name, col_name))

    def get_user_columns(self, requested_list, args):
        if requested_list is None:
            requested_list = args["columns"]
            
        add_cols = utils.safe_value(args, "add_columns")
        if add_cols:
            for ac in add_cols:
                if not ac in requested_list:
                    requested_list.append(ac)

        return requested_list

    def get_avail_actual_user_cols(self, records, user_columns, args):
        col_dict = OrderedDict()
        for sr in records:
            if "metric_names" in sr:
                # seed col_dict with ordered list of metrics reported
                names = sr["metric_names"]
                if names:
                    for name in names:
                        col_dict["metrics." + name] = 1

            # build from log records
            self.build_avail_list(col_dict, sr)

        avail_list = list(col_dict.keys())

        # if we are computing averages of column(s), ensure the base name of those columns ar in user_columns 
        # user only needs to specify the xxx-mean or xxx-err names, so include the base name to ensure metrics are carried thru
        mean_cols = utils.safe_value(args, "mean")
        if mean_cols:
            user_columns += mean_cols

        # get list of user-requested columns
        all_user_columns = self.get_user_columns(user_columns, args)

        # parse out the custom column NAMES and FORMATS provided by the user
        user_col_args_raw = self.build_user_col_args(all_user_columns)

        actual_cols, user_col_args = self.get_requested_cols(user_col_args_raw, avail_list)
        return avail_list, actual_cols, user_col_args

    def build_report(self, records, user_columns, report_type, args):
        ''' build a tabular report of the records, or export to a table, as per args.  
        values in each record must have been flattened with a dotted key (e.g., hparams.lr).
        records must be in final sort order.
        '''
        row_count = 0
        was_exported = False
        max_column_width = utils.safe_value(args, "max_width")

        hp_set_display = utils.safe_value(args, "hp_set_display")
        mean_cols = utils.safe_value(args, "mean")
        group_by = utils.safe_value(args, "group")
        sort_by = utils.safe_value(args, "sort")
        reverse = utils.safe_value(args, "reverse")
        first = utils.safe_value(args, "first")
        last = utils.safe_value(args, "last")
        all = utils.safe_value(args, "all")
        total_cols = utils.safe_value(args, "total_columns")
        copy_to_clipboard = utils.safe_value(args, "clipboard")

        if all:
            first = None
            last = None

        # fixup hp_set cols in records, as per hp_set_display
        self.format_hp_set_values(records, user_columns, hp_set_display)

        if mean_cols:
            # produce new mean-calculated columns (new records)
            records = self.create_mean_records(user_columns, records, mean_cols, group_by, sort_by, reverse, first, last)
            if args["flat"]:
                group_by = None

        # NOTE: user_col_args is a list here, so that we can support multiple instances of same col in long report lines
        avail_list, actual_cols, user_col_args  = self.get_avail_actual_user_cols(records, user_columns, args)

        # store for later use
        self.user_col_args = user_col_args

        actual_cols = [value["key"] for value in user_col_args]

        fn_export = utils.safe_value(args, "export")
        if fn_export:
            fn_ext = os.path.splitext(fn_export)[1]
            if not fn_ext:
                fn_ext = ".txt"
                fn_export += fn_ext

            sep_char = "," if fn_ext == ".csv" else "\t"

            count = self.export_records(fn_export, records, actual_cols, sep_char)
            row_count = count - 1
            line = "report exported to: {} ({} rows)".format(fn_export, row_count)
            lines = [line]
            was_exported = True
        else:
            number_groups =  utils.safe_value(args, "number_groups")

            group_by_fmt = None
            if group_by:
                _, group_by_fmt, _ = self.get_user_col_info(user_columns, group_by)

                if group_by_fmt:
                    group_by_fmt = "{:" + group_by_fmt + "}" 

            group_hdrs = utils.safe_value(args, "group_hdrs")
            group_sort = utils.safe_value(args, "group_sort")
            group_reverse = utils.safe_value(args, "group_reverse")
            group_first = utils.safe_value(args, "group_first")
            group_last = utils.safe_value(args, "group_last")
            group_all = utils.safe_value(args, "group_all")

            if group_all:
                group_first = None
                group_last = None

            title = utils.safe_value(args, "title")

            text, row_count = self.build_formatted_table(records, avail_cols=avail_list, col_list=actual_cols, 
                report_type=report_type, group_by=group_by, number_groups=number_groups, title=title,
                max_col_width=max_column_width, group_by_fmt=group_by_fmt, group_hdrs=group_hdrs, first=first, last=last, 
                group_sort=group_sort, group_reverse=group_reverse, group_first=group_first, group_last=group_last, total_cols=total_cols, 
                copy_to_clipboard=copy_to_clipboard)

            lines = text.split("\n")

        if self.calc_col_helper:
            self.calc_col_helper.get_error_report(lines)

        return lines, row_count, was_exported

    def format_hp_set_values(self, records, user_columns, hp_set_display):
        '''
        The hp_set column is part of the run_info table record created for each run.  hp_set is a string     
        version of a dictionary containing all of the hyperparameters (and their associated values), that were
        a result of the hyperparameter search, the cmdline arguments for your script, or the logged hyperparameters 
        for your run.

        The --hp-set-display option controls how hp_set is used and formatted in the list runs report:
        
            changed:                hp_set is transformed to only include hp names/values unique to this run
            full:                   hp_set is unchanged
            simple:                 hp_set is changed to a simple name for its unique set of values (e.g., hp_set_1)
            columns:                adds a new column to the report for each changed hparam
            user-columns:           adds a new column for changed hparam if column has been specified by user (run-reports, named-columns, etc.)
            simple_plus_columns:    adds a column for each changed hparam, and a column for the hp_set name
        '''

        # from the current set of records, calculate the set of hyperparameters that change between runs
        self.hp_set_formatter.build_hp_set_names(records)
        hp_set_index = user_columns.index("hp_set") if "hp_set" in user_columns else -1

        def _set_or_append(values, value, index): 
            if index > -1:
                values[index] = value
            else:
                values.append(value)

        if hp_set_display == "changed":
            _set_or_append(user_columns, "hp_set:$hpset_changed", hp_set_index)

        if hp_set_display == "simple" or hp_set_display == "simple_plus_columns":
            # "simpl"
            _set_or_append(user_columns, "hp_set:$hpset_simple", hp_set_index)

        if hp_set_display == "full":
            _set_or_append(user_columns, "hp_set", hp_set_index)

        # add new HP columns to each record
        if hp_set_display == "columns" or hp_set_display == "simple_plus_columns":
            if self.hp_set_formatter.hp_sets_processed:

                # add each hparam col that has changed to user_columns
                for col in self.hp_set_formatter.hp_changed_keys:
                    self.add_to_user_columns_if_needed(user_columns, "hparams." + col)

                for record in records:
                    # for each changed hparam, add to run record
                    if "hp_set" in record:
                        hp_set_str = record["hp_set"]
                        hp_set = self.hp_set_formatter.format_hpset_changed(hp_set_str)

                        for hp, value in hp_set.items():
                            full_hp_name = "hparams." + hp

                            # don't overwrite existing col (record values are typed but the hp_set values are strings)
                            if not full_hp_name in record:
                                record[full_hp_name] = value

                        if hp_set_display == "columns":
                            del record["hp_set"]

        # add new HP columns to each record
        if hp_set_display == "user-columns":
            if self.hp_set_formatter.hp_sets_processed:
                # for each run record, add new columns for each changed hparam that is found in user_columns
                for record in records:
                    if "hp_set" in record:
                        hp_set_str = record["hp_set"]
                        hp_set = self.hp_set_formatter.parse_and_sort_hp_set(hp_set_str)

                        for hp, value in hp_set.items():
                            full_hp_name = "hparams." + hp
                            if full_hp_name in user_columns:
                                record[full_hp_name] = value

                        del record["hp_set"]

    def add_to_user_columns_if_needed(self, user_columns, col_name):
        name, _, _ = self.get_user_col_info(user_columns, col_name)
        if not name:
            user_columns.append(col_name)

    def export_records(self, fn_report, records, col_list, sep_char):

        lines = []

        # write column header
        header = ""
        for col in col_list:
            if header == "":
                header = col
            else:
                header += sep_char + col
        lines.append(header)

        # write value rows
        for record in records:
            line = ""

            for col in col_list:
                value = record[col] if col in record else ""
                if value is None:
                    value = ""
                else:
                    value = str(value)

                if line == "":
                    line = value
                else:
                    line += sep_char + value
    
            lines.append(line)

        with open(fn_report, "wt") as outfile:
            text = "\n".join(lines)
            outfile.write(text)

        return len(lines)

    def build_user_col_args(self, requested_list):

        user_col_args = []

        for col_spec in requested_list:
            col_name = col_spec
            user_fmt = None
            user_name = None
            calculated_exp = None

            if "=" in col_name:
                # CUSTOM NAME
                col_name, user_name = col_name.split("=", 1)
                if ":" in user_name:
                    # CUSTOM FORMAT
                    user_name, user_fmt = user_name.split(":", 1)
                    user_fmt = "{:" + user_fmt + "}"
            else:
                if ":" in col_name:
                    # CUSTOM FORMAT
                    col_name, user_fmt = col_name.split(":", 1)
                    
                    user_fmt = "{:" + user_fmt + "}"

            if user_name and user_name.startswith("+"):
                # user_name specified a caclulated column
                calculated_exp = user_name[1:]
                user_name = col_name

            # only look for "." after we have isolated the actual col_name (from the formatting info)
            if "." in col_name:
                prefix, col_name = col_name.split(".", 1)
            else:
                prefix = None

            if not user_name:
                user_name = col_name

            # rebuild prefix_name (must be prefix + col_name)
            prefix_name = prefix + "." + col_name if prefix else col_name

            user_col_args.append( {"key": prefix_name, "user_name": user_name, "user_fmt": user_fmt, "calculated_exp": calculated_exp} )

        return user_col_args

    def xt_custom_format(self, fmt, value):
        blank_zero_fmt = "{:$bz}"
        date_only = "{:$do}"
        time_only = "{:$to}"
        hpset_simple = "{:$hpset_simple}"
        hpset_changed = "{:$hpset_changed}"
        right_trim = "{:$rt."
        align = ">"

        if value:
            if fmt == blank_zero_fmt:
                # blank if zero
                value = "" if value == 0 else str(value)

            elif fmt == date_only:
                # extract date portion of datetime string
                delim = " " if " " in value else "T"
                value, _ = value.split(delim)

            elif fmt == time_only:
                # extract time portion of datetime string
                delim = " " if " " in value else "T"
                _, value = value.split(delim)
                value = value.split(".")[0]    # extract hh:mm:ss part of fractional time

            elif fmt == hpset_simple:
                value = str(self.hp_set_formatter.format_hpset_simple(value))
                align = "<"

            elif fmt == hpset_changed:
                value = str(self.hp_set_formatter.format_hpset_changed(value))
                align = "<"

            elif fmt.startswith(right_trim):
                int_part = fmt[6:].split("}")[0]
                trim_len = int(int_part)
                value = str(value)[-trim_len:]

        else:
            value = str(value)
        
        return value, align

    def needed_precision(self, value, max_sig_digits):
        '''
        precision: 3                   # number of fractional digits to display for float values, so "3.23" has precision 2.
        significance: 2                # number of significant digits to display (by increasing precision, when needed).  So "3.23" has significance 3.

        Determine how much precision is required for the specified significant digits.  
            - For example, if the value is 0.0001234, and the significance is 2, then the value should be displayed as 0.00012, which requires 5 digits of precision.
            - For example, if the value is 0.0001234, and the significance is 5, then the value should be displayed as 0.0001234, which requires 7 digits of precision.
            - For example, if the value is 323.430, and the significance is 4, then the value should be displayed as 323.4, which requires 1 digits of precision.
            - For example, if the value is 3348348348348348.34, and the significance is 4, then the value should be displayed as 3.348e+15, which requires 4 digits of precision.

        See also: tryOut/calc_needed_precision.py test app.
        '''
        # written by ChatGPT-4 (with slight mods by me)
        if value == 0:
            decimal_places = 1

        else:
            value = abs(value)     # don't care about sign

            # first, format number as a float (not scientific notation)
            # "f" format defaults to 6 decimal places, so we specify out to where noise starts
            text = f'{value:.15f}'

            # now, zap the decimal point and strip zeros from both sides
            text_stripped = text.replace('.', '').strip('0')
            actual_sig_digits = len(text_stripped)

            # use the smallest of the max and the actual
            sig_digits = min(max_sig_digits, actual_sig_digits)

            if value >= 1:
                # now, determine the magnitude of the number (number of digits to left of text)
                ivalue = int(value)
                whole_places = len(f'{ivalue:d}') if ivalue != 0 else 0
                decimal_places = max(0, sig_digits - whole_places)

            else:
                # if value is less than 1, then we need to count the leading zeros
                exponent = int(math.floor(math.log10(value)))
                #mantissa = value/10**exponent

                leading_zeros = -(exponent + 1)
                decimal_places = leading_zeros + sig_digits

        return decimal_places
    
    def smart_float_format(self, value, significance, max_precision, max_fixed_length):
        if max_precision <= max_fixed_length:
            # FIXED POINT formatting
            text = "%.*f" % (max_precision, value)
        else:
            # SCIENTIFIC NOTATION formatting
            text = "%.*e" % (significance-1, value)
        return text

    def get_user_col_arg(self, col_name):
        cdx = None

        for cd in self.user_col_args:
            if cd["key"] == col_name:
                cdx = cd
                break

        return cdx

    def eval_calculated_exp(self, calculated_exp, record, dest_col):
        # prevent circular imports
        from xtlib.calc_col_helper import CalcColHelper
        
        if not self.calc_col_helper:
            self.calc_col_helper = CalcColHelper()

        result = self.calc_col_helper.eval_calculated_exp(calculated_exp, record)

        # propogate the ONGOING flag from dependent columns
        cols = get_ids_from_python_expression(calculated_exp)
        for col in cols:

            # if col == "sku_cost_per_hour":
            #     col = "run_duration"     # sku_cost_per_hour's dependent duration col

            if (constants.ONGOING_PREFIX + col) in record:
                record[constants.ONGOING_PREFIX + dest_col] = 1
                break

        return result

    def get_cols_from_title(self, title):
        cols = []

        if "$" in title:
            # look for named columns in title (@hparams.foo@) 
            parts = title.split("$")

            if len(parts) > 2:        
                # contains 1 or more @xxx@ entries
                while len(parts) >= 2:
                    left = parts.pop(0)
                    col_name = parts.pop(0)

                    cols.append(col_name)

        return cols

    def expand_title(self, records, title):
        if not title:
            text = ""

        else:
            text = title + "\n\n"
            record = records[0] if records else {}

            if "$" in text:
                # look for a named column (@hparams.foo@) and replace it with its value
                parts = text.split("$")
                if len(parts) > 2:        
                    # contains 1 or more @xxx@ entries
                    new_text = ""

                    while len(parts) >= 2:
                        left = parts.pop(0)
                        col_name = parts.pop(0)
                        
                        # update @N@ with value of arg   
                        if record and col_name in record:
                            value = record[col_name]
                        else:
                            value = ""

                        new_text += "{}{}".format(left, value)

                    new_text += parts.pop()
                    text = new_text

        return text

    def build_formatted_table(self, records, avail_cols=None, col_list=None, max_col_width=None, 
        report_type="run-reports", group_by=None, number_groups=False, indent=None, print_report=False, 
        copy_as_html=False, skip_lines=None, group_by_fmt=None, group_hdrs=True, first=None, last=None, 
        group_sort=None, group_reverse=False, group_first=None, group_last=None, total_cols=None, 
        title=None, copy_to_clipboard=False):

        '''
        Args:
            records:        a list of dict entries containing data to format
            avail_cols:     list of columns (unique dict keys found in records)
            col_list:       list of columns to be used for report (strict subset of 'avail_cols')
            report_type:    a dotted path to the report definition in the XT config file

        Processing:
            Builds a nicely formatted text table from a set of records.
        '''

        if not avail_cols:
            avail_cols = list(records[0].keys()) if records else []
        #console.print("self.user_col_args=", self.user_col_args)

        if self.config:
            if not max_col_width:
                max_col_width = utils.to_int_or_none(self.config.get(report_type, "max-width"))     
                
            precision = self.config.get(report_type, "precision")
            significance = self.config.get(report_type, "significance")
            max_fixed_length = self.config.get(report_type, "max-fixed-length")
            
            uppercase_hdr_cols = self.config.get(report_type, "uppercase-hdr")
            right_align_num_cols = self.config.get(report_type, "right-align-numeric")
            truncate_with_ellipses = self.config.get(report_type, "truncate-with-ellipses")
            skip_lines = self.config.get(report_type, "skip-lines")
        else:
            # default when running without config file
            if not max_col_width:
                max_col_width = 35
            precision = 3
            significance = 2
            max_fixed_length = 7
            uppercase_hdr_cols = True
            right_align_num_cols = True
            truncate_with_ellipses = True

        if not col_list:
            col_list = avail_cols

        if group_by and group_by in col_list:
            # remove group_by columns from those display in group records
            col_list.remove(group_by)

        col_infos = self.build_column_info(col_list, precision, significance, max_fixed_length, max_col_width, records, avail_cols)

        col_space = 2               # spacing between columns
        header_line = None

        text = self.expand_title(records, title)

        if group_by:
            # GROUPED REPORT
            row_count = 0
            group_count = 0

            if not group_hdrs:
                text += "$HDRS\n"     # will be replaced at end

            grouped_recs_dict = self.group_by(records, group_by, group_by_fmt, inner_first=first, inner_last=last)
            sorting_output = False
            output_tuple_list = []

            if group_sort == group_by:
                # sort by group value
                grouped_recs_dict = utils.sort_dict_by_keys(grouped_recs_dict, reverse=group_reverse, first=group_first, last=group_last)

            elif group_sort:
                sorting_output = True

            for i, (group, grecords) in enumerate(grouped_recs_dict.items()):

                by = self.remove_col_prefix(group_by)
                fmt_group, need_newline = self.format_group_value(group)

                if need_newline:
                    text += "\n"

                if number_groups:
                    #text += "\n{}. {}:\n".format(i+1, group)
                    text += "\ngroup #{}: [{}: {}]\n".format(i+1, by, fmt_group)
                else:
                    #text += "\n{} {}:\n".format(group_by, group)
                    text += "\ngroup: [{}: {}]\n".format(by, fmt_group)

                if need_newline:
                    text += "\n"

                txt, rc, group_sort_value = self.generate_report(col_infos, grecords, right_align_num_cols, uppercase_hdr_cols, truncate_with_ellipses, 
                    col_space, significance, max_fixed_length, precision, skip_lines=skip_lines, 
                    add_hdrs=group_hdrs, group_sort_col=group_sort, total_cols=total_cols)

                # indent report
                txt = "  " + txt.replace("\n", "\n  ")
                text += txt
                row_count += rc
                group_count += 1

                if sorting_output:
                    output_tuple_list.append((group_sort_value, text))
                    text = ""

            if sorting_output:
                # sort output
                output_tuple_list = utils.sort_tuple_list_by_key(output_tuple_list, reverse=group_reverse, first=group_first, last=group_last)

                for group, txt in output_tuple_list:
                    text += txt

            if not group_hdrs:
                text = text.replace("$HDRS", self.col_headers)
                text += "\n" + self.col_headers + "\n"

            text += "\ntotal groups: {}\n".format(group_count)
        else:
            # UNGROUPED REPORT
            text_report, row_count, _ = self.generate_report(col_infos, records, right_align_num_cols, uppercase_hdr_cols, truncate_with_ellipses, 
                col_space, significance, max_fixed_length, precision, skip_lines=skip_lines, total_cols=total_cols, copy_to_clipboard=copy_to_clipboard)
            
            text += text_report

        if indent:
            text = "\n".join([indent + line for line in text.split("\n")])

        if print_report:
            console.print(text)

        if copy_as_html:
            writer = HtmlWriter()
            html = writer.write(text)
            
            from xtlib.helpers import clipboard
            with clipboard.Clipboard() as cb:
                cb.set_contents("HTML Format", html)

        return text, row_count

    def build_column_info(self, col_list, precision, significance, max_fixed_length, max_col_width, records, avail_cols):

        col_infos = []              # {width: xxx, value_type: int/float/str, is_numeric: true/false}

        # formatting strings with unspecified width and alignment
        int_fmt = "{:d}"
        str_fmt = "{:s}"
        #console.print("float_fmt=", float_fmt)
        plus_minus_format = None

        # build COL_INFO for each col (will calcuate col WIDTH, formatting, etc.)
        for i, col in enumerate(col_list):

            if plus_minus_format:
                # don't process this column (it was consumed by previous col formatting)
                plus_minus_format = False
                continue

            if col.startswith("hparams.beta1"):
                aa = 9

            next_col = col_list[i+1] if i+1 < len(col_list) else None

            if next_col and col.endswith("-mean") and next_col.endswith("-err"):
                plus_minus_format = True

            # largest precision needed for this col
            max_precision = 0 

            # examine all records for determining max col_widths
            user_col = col
            user_fmt = None
            calculated_exp = None

            if col.startswith("metrics.dev-seq_acc"):
                aa = 9

            if self.user_col_args:
                user_args = self.get_user_col_arg(col)
                if user_args:
                    user_col = user_args["user_name"]
                    user_fmt = user_args["user_fmt"] 
                    calculated_exp = utils.safe_value(user_args, "calculated_exp")

                    if user_fmt and user_fmt == "{:$hidden}":
                        # skip this column
                        continue

            float_fmt = "{:." + str(precision) + "f}"

            col_width = len(user_col)
            #console.print("col=", col, ", col_width=", col_width)
            value_type = None
            is_numeric = False
            first_value = True
            force_string = False

            for record in records:

                self.compute_dynamic_duration_cols(record, col_list)

                if calculated_exp:
                    value = self.eval_calculated_exp(calculated_exp, record, col)

                    # also add to record for use by other calculated columns
                    record[col] = value

                else:
                    if not col in record:
                        # not all columns are defined in all records
                        continue

                    value = record[col]

                try:
                    # special formatting for time values
                    if col in self.duration_col_names:
                        value = self.format_duration(value, col, record)
                        #record[col] = value

                    elif col in self.time_col_names:
                        # workaround some bad job data that has time as '0' instead of None
                        if value is None or value == '0':
                            value = ""
                        else:
                            if isinstance(value, str):
                                # convert to PST (local Redmond time zone)
                                value = arrow.get(value).to('local')
                            value = value.format('YYYY-MM-DD @HH:mm:ss')

                    # for sql, convert float types that are really integer values to int types
                    if isinstance(value, float) and value == int(value) and user_fmt is None and value_type in [None, str, int]:
                        value = int(value)
                    # elif isinstance(value, float) and value_type is int:
                    #     value = int(value)

                    elif value_type is None and isinstance(value, str) and value.isnumeric():
                        # handle cases where int was logged incorrectly as a string
                        value = int(value)

                    elif value_type in [None, float] and isinstance(value, str) and utils.str_is_float(value):
                        # handle cases where int was logged incorrectly as a string
                        value = float(value)

                    if user_fmt:
                        # user provided explict format for this column
                        value_str, align = self.format_value(user_fmt, value, col_width)
                        is_numeric = self.is_user_fmt_numeric(user_fmt)

                    elif isinstance(value, float):
                        if col == "metrics.best-eval-acc":
                            dummy = 33
                        # default (smart) FLOAT formatting
                        needed = self.needed_precision(value, significance)
                        max_precision = max(max_precision, needed)
                        value_str = self.smart_float_format(value, significance, max_precision, max_fixed_length)
                        
                        if user_fmt is None and value_type in [None, int, str]:
                            value_type = float
                            is_numeric = True

                    elif isinstance(value, bool):
                        value_str = str(value)
                        value_type = bool
                        is_numeric = False

                    elif isinstance(value, int):
                        value_str = int_fmt.format(value)
                        if value_type in [str, None] and not force_string:
                            value_type = int
                            is_numeric = True

                    elif value is not None:
                        # don't let None values influence the type of field
                        # assume value found is string-like
                        
                        # ensure value is a string
                        value = str(value)

                        value_str = str_fmt.format(value) if value else ""
                        if first_value:
                            is_numeric = utils.str_is_float(value)

                        if len(value):
                            force_string = True

                    else:
                        value_str = ""

                    if (constants.ONGOING_PREFIX + col) in record:
                        value_str = "+" + value_str

                    # set width as max of all column values seen so far
                    col_width = max(col_width, len(value_str))
                    #console.print("name=", record["name"], ", col=", col, ", value_str=", value_str, ", col_width=", col_width)
                except BaseException as ex:
                    console.print("Exception formatting col={}: {}".format(col, ex))
                    console.print("  Exception record: {}".format(record))

                    # debug
                    raise ex

            # finish this col
            if is_numeric and not max_precision:
                max_precision = 3

            if col == "hp_set":
                dummy = col
                
            if not user_fmt:
                col_width = min(max_col_width, col_width)

            if plus_minus_format:
                if user_fmt:
                    user_fmt += " ± " + user_fmt
                else:
                    user_fmt = "{:.4f} ± {:.4f}"

            col_info = {"name": col, "user_name": user_col, "col_width": col_width, "value_type": value_type, 
                "is_numeric": is_numeric, "precision": max_precision, "user_fmt": user_fmt, 
                "value_padding": None}

            col_infos.append(col_info)
            #console.print(col_info)

        return col_infos

    def compute_dynamic_duration_cols(self, record, col_list):
        # support for dynamic duration columns on this record
        status = utils.safe_value(record, "status")

        # create a list from intersection of col_list and self.duration_col_names
        cols = list(set(col_list) & set(self.duration_col_names))

        for col in cols:
            value = utils.safe_value(record, col)

            if not value:
                value = self.calc_duration_col(col, status, record)
                if value:
                    record[col] = value
                    record[constants.ONGOING_PREFIX + col] = 1

    def format_group_value(self, value):

        def simple_fmt(v):
            if isinstance(v, str):
                v = utils.make_numeric_if_possible(v)
            if isinstance(v, float) and v == int(v):
                v = str(int(v))
            else:
                v = str(v)
            return v

        need_newline = False

        if isinstance(value, str) and value.startswith("{"):
            # try an easier to read format of group dict 
            newlines = False

            import ast 
            value = ast.literal_eval(value)
            
            max_name_len = max([len(key) for key in value])

            if newlines:
                value = "".join(["\n    " + str.ljust(key+":", max_name_len+2) + simple_fmt(value) for key, value in value.items()])
            else:
                value = ", ".join([key + ": " + simple_fmt(value) for key, value in value.items()])
                need_newline = True
        else:
            value = simple_fmt(value)

        return value, need_newline

    def create_mean_records_core(self, new_col_dict, records, mean_cols, group_by):
        values = {}

        for col in mean_cols:
            values[col] = []
            for record in records:
                if col in record:
                    value = record[col]
                    if value is not None:
                        values[col].append(float(value))

        mean_records = []
        using_single_record = True
        
        if using_single_record:
            mr = {}
            mr["item_count"] = len(records)
            if group_by:
                mr[group_by] = record[group_by]

            for col in mean_cols:
                data = values[col]

                mean_val = np.mean(data) if data else None
                std_err = np.std(data) / np.sqrt(len(data)) if data else None

                col_name = col + "-mean" 
                mr[col_name] = mean_val

                err_col_name = col + "-err"
                mr[err_col_name] = std_err

                new_col_dict[col + "-mean"] = 1
                new_col_dict[col + "-err"] = 1

            mean_records.append(mr)
            new_col_dict["item_count"] = 1

        else:
            for col in mean_cols:
                data = values[col]
                mr = {}
                mr["column"] = self.default_user_name(col)
                mr["mean"] = np.mean(data) if data else None
                mr["stderr"] = np.std(data) / np.sqrt(len(data)) if data else None

                if group_by:
                    mr[group_by] = record[group_by]

                mean_records.append(mr)

        return mean_records

    def remove_col_prefix(self, name: str):
        if name.startswith("hparams."):
            name = name[8:]
        elif name.startswith("metrics."):
            name = name[7:]
        elif name.startswith("tags."):
            name = name[5:]

        return name

    def create_mean_records(self, user_cols, records, mean_cols, group_by, sort_by, reverse, first, last):

        new_col_dict = {}

        if group_by:
            # get user-specified formatting for group_by
            _, fmt, _ = self.get_user_col_info(user_cols, group_by)
            if fmt:
                fmt = "{:" + fmt + "}" 

            # calc mean over each groups of records
            grouped_records = self.group_by(records, group_by, fmt)
            mean_records = []

            for i, (group_name, group_records) in enumerate(grouped_records.items()):
                recs = self.create_mean_records_core(new_col_dict, group_records, mean_cols, group_by)
                mean_records += recs

        else:
            # calc mean over all records
            mean_records = self.create_mean_records_core(new_col_dict, records, mean_cols, group_by)

        # add new cols to user_cols
        for nc in new_col_dict:
            self.add_to_user_columns_if_needed(user_cols, nc)

        # apply sort, reverse, first, last
        self.sort_records(mean_records, sort_by, reverse)

        # if first:
        #     mean_records = mean_records[:first]
        # elif last:
        #     mean_records = mean_records[-last:]
        
        return mean_records

    def should_highlight_row(self, highlight_exp, rd):
        should = False

        if highlight_exp == "$alive":
            status = utils.safe_value(rd, "status")
            should = status in ["submitted", "queued", "running"]

        return should

    def fixup_legacy_hp_set_nulls(self, records, exclude_from_hp_set):
        for record in records:
            hp_set = utils.safe_value(record, "hp_set", None)
            if hp_set is None and "hparams" in record:

                arg_dict = record["hparams"]
                if exclude_from_hp_set:
                    arg_dict = {key:value for key, value in arg_dict.items() if not key in exclude_from_hp_set}
                record["hp_set"] = str(arg_dict)

    def get_start_col_for_duration_col(self, col):
        start_col = None

        if col in self.duration_map:
            start_col = self.duration_map[col]

        return start_col

    def calc_duration_col(self, col, status, record):
        '''
        for jobs/nodes/runs that are still alive, we compute a dynamic value for duration
        columns that are in-progress.
        '''
        value = 0

        if status not in ["error", "cancelled", "completed", "restarted"]:
            start = None

            if col in self.duration_map:
                start_str = self.duration_map[col]
                start = utils.safe_value(record, start_str) 

                if start:                
                    start_value = time_utils.get_time_from_arrow_str(start)
                    value = time.time() - start_value

        return value

    def format_duration(self, value, col, record):
        '''
        formats duration column values.
        '''
        value = utils.friendly_duration_format(value, False)
        return value

    def get_report_color(self, config_section, config_name):
        color_name = self.config.get(config_section, config_name).upper()
        color = getattr(pc_utils, color_name) if color_name else pc_utils.NORMAL

        return color

    def generate_report(self, col_infos, records, right_align_num_cols, uppercase_hdr_cols, truncate_with_ellipses, 
        col_space, significance, max_fixed_length, float_precision, skip_lines=None, 
        add_hdrs=True, group_sort_col=None, total_cols=None, copy_to_clipboard=False):

        # process COLUMN HEADERS
        headers = ""
        group_sort_value = None

        first_col = True
        if self.config:
            color_highlight = self.get_report_color("run-reports", "color-highlight")
            color_hdr = self.get_report_color("run-reports", "color-hdr")
            highlight_exp = self.config.get("run-reports", "highlight")
        else:
            color_highlight = None
            highlight_exp = None
            color_hdr = None

        if color_highlight or color_hdr:
            pc_utils.enable_ansi_escape_chars_on_windows_10()

        if color_hdr:
            headers += color_hdr

        for i, col_info in enumerate(col_infos):
            if first_col:
                first_col = False
            else:
                headers += " " * col_space

            user_fmt = col_info["user_fmt"] 
            col_width = col_info["col_width"]
            col_name = col_info["user_name"].upper() if uppercase_hdr_cols else col_info["user_name"]

            #right_align = right_align_num_cols and (col_info["is_numeric"] or user_fmt) or \
            right_align = right_align_num_cols and (col_info["is_numeric"]) or \
                col_info["name"] in self.duration_col_names

            if truncate_with_ellipses and len(col_name) > col_width:
                col_text = col_name[0:col_width-3] + "..."
            elif right_align:
                fmt = ":>{}.{}s".format(col_width, col_width)
                fmt = "{" + fmt + "}"
                col_text = fmt.format(col_name)
            else:
                fmt = ":<{}.{}s".format(col_width, col_width)
                fmt = "{" + fmt + "}"
                col_text = fmt.format(col_name)

            headers += col_text

        if color_hdr:
            headers += pc_utils.NORMAL

        self.col_headers = headers
        text = ""

        if add_hdrs:
            text = headers
            if len(records) > 1:
                text += "\n\n"
            else:
                text += "\n"

        row_count = 0
        totals_record = defaultdict(float)

        # process VALUE ROWS
        # collect each row of values, for copy_to_clipboard
        rows = []

        for row_num, record in enumerate(records):
            row_values = []

            first_col = True
            highlighted = False

            if highlight_exp and color_highlight:
                if self.should_highlight_row(highlight_exp, record):
                    text += color_highlight
                    highlighted = True

            if row_num % 500 == 0:
                console.diag("build_formatted_table: processing row: {}".format(row_num))

            col = None
            catch_exception = False

            if catch_exception:
                try:
                    for col_info in col_infos:

                        first_col, col_text = self.format_col_to_text(record, col_info, first_col, max_fixed_length, 
                            float_precision, significance, col_space, right_align_num_cols, 
                            total_cols, totals_record)
                        
                        text += col_text

                        if copy_to_clipboard:
                            row_values.append(col_text.strip())

                except BaseException as ex:
                    console.print("Exception formatting col={}: {}".format(col, ex))
                    console.print("  Exception record: {}".format(record))

                    # debug
                    raise ex

            else:

                for col_info in col_infos:

                    if group_sort_col == col_info["name"]:
                        group_sort_value = record[col_info["name"]]

                    in_debugger = bool(sys.gettrace())

                    if in_debugger:
                        # throw exception directly to debugger
                        first_col, col_text = self.format_col_to_text(record, col_info, first_col, max_fixed_length, 
                            float_precision, significance, col_space, right_align_num_cols, 
                            total_cols, totals_record)

                        text += col_text
                        if copy_to_clipboard:
                            row_values.append(col_text.strip())

                    else:
                        # wrap exception with context info for end user
                        try:
                            first_col, col_text = self.format_col_to_text(record, col_info, first_col, max_fixed_length, 
                                float_precision, significance, col_space, right_align_num_cols, 
                                total_cols, totals_record)

                            text += col_text

                            if copy_to_clipboard:
                                row_values.append(col_text.strip())

                        except BaseException as ex:
                            # wrap the exception with context (column name, value, value type))
                            col = col_info["name"]
                            value = record[col] if col in record else ""
                            value_type = type(record[col]).__name__ if col in record else "<empty string>"
                            msg = "formatting col={}, value={}, value_type={}: {}".format(col, value, value_type, ex)
                            errors.general_error(msg)

            if highlighted:
                text += pc_utils.NORMAL

            text += "\n"
            row_count += 1

            if copy_to_clipboard:
                rows.append(row_values)

            if skip_lines and (row_count % skip_lines == 0):
                text += "\n"

        if copy_to_clipboard:
            hct = HtmlClipboardTables()

            col_headers = [col_info["user_name"] for col_info in col_infos]
            hct.add_table(col_headers, rows)
            hct.copy_to_clipboard()
        
        # all records processed
        if add_hdrs and row_count > 5:
            # console.print header and run count
            text += "\n" + self.col_headers + "\n"

        if totals_record:
            text += "\nTotals:\n"

            for i, col_info in enumerate(col_infos):
                col_name = col_info["name"]
                if col_name in totals_record:

                    _, text_value = self.format_col_to_text(totals_record, col_info, True, max_fixed_length, 
                        float_precision, significance, col_space, right_align_num_cols, 
                        apply_col_width=False)
                    
                    text_value = text_value.strip()
                    text += "  {}: \t{}\n".format(col_name, text_value)

            text += "\n"

        return text, row_count, group_sort_value

    def format_col_to_text(self, record, col_info, first_col, max_fixed_length, 
        float_precision, significance, col_space, right_align_num_cols, 
        total_cols=None, totals_record=None, apply_col_width=True):

        text = ""

        if first_col:
            first_col = False
        else:
            text += " " * col_space

        user_fmt = col_info["user_fmt"] 
        if user_fmt == "{:s}":
            # don't need this anymore (was used to remove column width restriction)
            user_fmt = None

        col = col_info["name"]
        value_type = col_info["value_type"]

        if col.startswith("hparams.beta1"):
            aa = 9

        right_align = right_align_num_cols and (col_info["is_numeric"] or user_fmt or \
            value_type == bool) or col in self.duration_col_names

        col_width = col_info["col_width"]
        align = ">" if right_align else "<"

        if not col in record:
            # not all records define all columns
            str_fmt = "{:" + align + str(col_width)  + "." + str(col_width) + "s}"
            text += str_fmt.format("")
        else:
            value = record[col]

            # apply inferred type if differernt than current type
            if value_type is not None and value_type != type(value):
                if value != None:
                    value = value_type(value)

            # special handling for int values that were logged as floats
            # if isinstance(value, float) and value_type is int:
            #     value = int(value)
            if value_type is int and value is not None:
                # handle cases where int was logged incorrectly as a string
                value = int(value)

            if total_cols and col in total_cols:
                if value is not None:
                    totals_record[col] += value

            #console.print("col=", col, ", value=", value, ", type(value)=", type(value))

            is_duration_col = (col in self.duration_col_names)
            # special formatting for time values
            if (value is None) and (not is_duration_col):
                value = ""

            else:
                if is_duration_col:
                    value = self.format_duration(value, col, record)
                elif col in self.time_col_names:
                    if value is None or value == "0":
                        value = ""
                    else:
                        if isinstance(value, str):
                            value = arrow.get(value).to("local")
                        value = value.format('YYYY-MM-DD @HH:mm:ss')

            if user_fmt:
                # user provided explict format for this column
                if "±" in user_fmt:
                    left_fmt, right_fmt = user_fmt.split("±")

                    left, align = self.format_value(left_fmt, value, col_width)
                    col2 = col.replace("-mean", "-err")
                    value2 = record[col2]

                    right, align = self.format_value(right_fmt, value2, col_width)
                    value = left + "±" + right

                else:
                    value, align = self.format_value(user_fmt, value, col_width)

                # now treat as string that must fit into col_width
                str_fmt = "{:" + align + str(col_width)  + "." + str(col_width) + "s}"
                #value = value if value else ""
                value = "" if value is None else value
                text += safe_format(str_fmt, value, col_width)

            elif isinstance(value, float):

                # default (smart) FLOAT formatting
                precision = col_info["precision"] if "precision" in col_info else float_precision
                if precision > max_fixed_length:
                    # use SCIENTIFIC NOTATION
                    float_fmt = "{:" + align + str(col_width) + "." + str(significance-1) + "e}"
                else:
                    # use FIXED POINT formatting
                    float_fmt = "{:" + align + str(col_width) + "." + str(precision) + "f}"

                text += safe_format(float_fmt, value, col_width)

            elif isinstance(value, bool):
                bool_fmt = "{!r:" + align + str(col_width) + "}"
                text += safe_format(bool_fmt, value, col_width)

            elif isinstance(value, int):
                int_fmt = "{:" + align + str(col_width) + "d}"
                text += safe_format(int_fmt, value, col_width)
            else:
                if col == "sku":
                    dummy = 3
                # ensure value is a string
                value = "" if value is None else str(value)

                if apply_col_width:
                    str_fmt = "{:" + align + str(col_width)  + "." + str(col_width) + "s}"
                    text += safe_format(str_fmt, value, col_width)
                else:
                    text += value

        if (constants.ONGOING_PREFIX + col) in record:
            # insert a "+" in text to replace right-most leading space
            ns_text = text.lstrip()
            lead_space_count = len(text) - len(ns_text)
            text = " " * (lead_space_count-1) + "+" + ns_text

        return first_col, text

    def is_user_fmt_numeric(self, fmt):
        # for now, assume all user formatting is numeric
        is_numeric = False

        if "i" in fmt or "f" in fmt or "," in fmt:
            is_numeric = True

        return is_numeric

    def format_value(self, user_fmt, value, col_width):
        align = "<"
        prefix = ""

        if user_fmt and user_fmt.startswith("{:$$"):
            user_fmt = user_fmt[0:2] + user_fmt[4:]
            prefix = "$"

        if user_fmt and "$" in user_fmt:
            value_str, align = self.xt_custom_format(user_fmt, value)
        else:
            value_str = safe_format(user_fmt, value, col_width)
            if user_fmt and self.is_user_fmt_numeric(user_fmt):
                align = ">"   

            if prefix:
                value_str = prefix + value_str

        return value_str, align

    def group_by(self, records, group_col, fmt, inner_first=None, inner_last=None):
        groups = {}
        for rec in records:
            if not group_col in rec:
                continue

            group_value = rec[group_col]
            group, _ = self.format_value(fmt, group_value, 0)

            if not group in groups:
                groups[group] = []

            groups[group].append(rec)

        # apply first/last to each group
        for group in groups.keys():
            group_records = groups[group]
            if inner_first:
                groups[group] = group_records[:inner_first]
            elif inner_last:
                groups[group] = group_records[-inner_last:]

        return groups

def test():
    builder = ReportBuilder()

    records = []
    for i in range(1, 11):
        age = np.random.randint(2*i)
        income = np.random.randint(10000*i)
        record = {"name": "roland" + str(i), "age": age, "income": income}
        records.append(record)

    text, _ = builder.build_formatted_table(records)
    print(text)

def test_needed_precision():
#   precision: 3                   # number of fractional digits to display for float values, so "3.23" has precision 2.
#   significance: 2                # number of significant digits to display (by increasing precision, when needed).  So "3.23" has significance 3.

# see also: tryOut/calc_needed_precision.py

    builder = ReportBuilder()

    precision = builder.needed_precision(value=.9, max_sig_digits=2)
    assert precision == 1            # .9

    precision = builder.needed_precision(value=.95, max_sig_digits=2)
    assert precision == 2           # .95

    precision = builder.needed_precision(value=.95, max_sig_digits=3)
    assert precision == 2           # .95

    precision = builder.needed_precision(value=.958, max_sig_digits=2)
    assert precision == 2           # .95

    precision = builder.needed_precision(value=.9584, max_sig_digits=2)
    assert precision == 2

    print("all needed_precision tests passed")

if __name__ == "__main__":
    # test out simple use of ReportBuilder
    #test()

    test_needed_precision()


