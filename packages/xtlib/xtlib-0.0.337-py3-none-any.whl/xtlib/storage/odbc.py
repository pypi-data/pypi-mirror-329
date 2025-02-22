#
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.
#
# odbc.py: implementation of our database API for SQL Server / ODBC database
import os
import json
import math
import time
import arrow
import pyodbc
import struct
import numpy as np
from threading import Lock, RLock
from interface import implements

import azure.identity as identity

from xtlib import utils
from xtlib import errors
from xtlib import console
from xtlib import pc_utils
from xtlib import constants
from xtlib import time_utils
from xtlib import run_helper
from xtlib import job_helper
from xtlib import run_errors
from xtlib import node_helper
from xtlib import request_helper
from xtlib import report_builder
from xtlib.storage.db_interface import DbInterface
from xtlib.helpers.feedbackParts import feedback as fb

DB_INFO = "__db_info__"
WORKSPACES = "__workspaces__"

# column types
#TINYCHAR = "VARCHAR(5)"
SMALLCHAR = "VARCHAR(20)"
VARCHAR = "VARCHAR(255)"
BIGCHAR = "VARCHAR(4096)"

TIME = "VARCHAR(100)"
DURATION = "FLOAT"

INT = "INT"
BIGINT = "BIGINT"
FLOAT = "FLOAT"
BOOL = "BIT"

MAX_BUFFERING_SECS = 30   # don't buffer inserted records for longer than this

class OdbcDatabase(implements(DbInterface)):
    '''
    For now, we only support putting all workspaces in a single database (the one specified in the 
    connection-string).  We may support multiple db's in the future, but we will need to 
    avoid expensive connect calls (1+ sec for each).
    '''
    def __init__(self, db_creds, store, db_options):
        self.service_name = db_creds["name"]
        self.store = store

        # options
        self.force_reset_database = False
        self.update_run_stats_enabled = True
        self.update_job_stats_enabled = True
        self.update_node_stats_enabled = True
        self.buffer_metrics = 0
        self.cols_by_table = {}
        self.max_retries = 25
        self.max_backoff = 60
        self.reset_connection_on_retry = True
        self.extended_logging = False
        self.credential = db_creds["credential"]

        # for breaking query results into parallel chunks
        self.chunk_size = 50

        # manage buffered inserts
        self.insert_buffering = False
        self.insert_buffers = {}
        self.insert_buffer_lock = Lock()
        self.insert_buffering_started = None

        self.connection_lock = RLock()

        self.call_stats = {}
        self.max_query_workers = 25  # TODO: make a config param
        self.client_session = not os.getenv("XT_RUN_NAME")
        self.fake_error_percent = 0

        # manage buffered metrics
        self.last_metrics_write = time.time()
        self.metrics = {}
        self.metrics_dirty = False
        self.is_xt_run = pc_utils.is_xt_run()

        if db_options:
            self._set_db_options(db_options)

        #console.print("self.fake_error_percent=", self.fake_error_percent)

        # grab/substitute name of database
        cs = db_creds["connection-string"]
        new_db = None # "xt_db2"  
        parts = cs.split(";")

        for i, part in enumerate(parts):
            if part and "=" in part:
                key, value = part.split("=")
                if key.lower() == "database":
                    if new_db:
                        parts[i] = "database=" + new_db
                        cs = "; ".join(parts)
                        self.default_db = new_db
                    else:
                        self.default_db = value

        # allow for multithreaded requests with single connection
        cs += "; MARS_Connection=Yes"
        self.cs = cs
        console.diag("before pyodbc.connect")
        
        self._create_connection()

        # this is used to return row_count of available records for first/last queries
        self.avail_row_count = None

        self._init_core_tables(self.db, False)        

    def _create_connection_ex(self):
        # some voodoo from Azure website: 
        # https://learn.microsoft.com/en-us/azure/azure-sql/database/azure-sql-passwordless-migration-python?view=azuresql&tabs=sign-in-azure-cli%2Cazure-portal-create%2Cazure-portal-assign%2Capp-service-identity   
                                                     
        token_bytes = self.credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
        token_struct = struct.pack(f'<I{len(token_bytes)}s', len(token_bytes), token_bytes)
        SQL_COPT_SS_ACCESS_TOKEN = 1256  # This connection option is defined by microsoft in msodbcsql.h

        dbx = pyodbc.connect(self.cs, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})
        return dbx

    def _create_connection(self):

        # only let 1 thread at a time in here since we are changing self.db
        with self.connection_lock:

            self.db = None

            try:
                if self.is_xt_run:
                    console.print("attempting to create to ODBC connection...", flush=True)

                # for now, we keep a persistent connection until our session ends

                # # TEMP TEMP TEMP: try odbc 18
                # self.cs = self.cs.replace("17", "18")

                #self.db = pyodbc.connect(self.cs)
                self.db = self._create_connection_ex()
                console.diag("after pyodbc.connect")

                # we always commit after any update
                self.db.autocommit = True 

                if self.is_xt_run:
                    console.print("new ODBC connection created", flush=True)

                # validate connection
                vcursor = self.db.cursor()
                vcmd = "SELECT * from [__db_info__]"
                vcursor.execute(vcmd)
                result = vcursor.fetchone()

                if self.is_xt_run:
                    console.print("new connection validated; result={}".format(result), flush=True)

            except BaseException as ex:
                console.print("_create_connection: exception={}".format(ex), flush=True)

        return self.db

    def _reset_connection(self, cursor, dbx):

        # only let 1 thread at a time enter this block
        with self.connection_lock:        
            if self.is_xt_run:
                console.print("\n============== START of reset_connection ==================", flush=True)
            # try to close cursor

            if cursor:
                try:
                    cursor.close()
                    cursor = None
                except BaseException as ex:
                    console.print("_reset_connection: cursor.close() exception={}".format(ex), flush=True)

            if self.db:
                # try to close connection 
                try:
                    self.db.close()
                    if self.is_xt_run:
                        console.print("current ODBC connection successfully closed", flush=True)
                except BaseException as ex:
                    console.print("_reset_connection: self.db.close() exception={}".format(ex), flush=True)

            self.db = None

            # new connection
            dbx = self._create_connection()

            if self.is_xt_run:
                console.print("=============== END of reset_connection =================\n", flush=True)
        return dbx

    def _set_db_options(self, md):
        self.update_job_stats_enabled = md["update-job-stats"]
        self.update_run_stats_enabled = md["update-run-stats"]
        self.update_node_stats_enabled = md["update-node-stats"]
        self.add_log_records = md["add-log-records"]
        self.buffer_metrics = md["buffer-metrics"]
        self.max_retries = md["max-retries"]
        self.max_backoff = md["max-backoff"]
        self.fake_error_percent = md["fake-error-percent"]
        self.chunk_size = md["chunk-size"]
        self.reset_connection_on_retry = md["reset-connection"]
        self.extended_logging = md["extended-logging"]

        # internal option for dev/debug of database features
        self.force_reset_database = utils.safe_value(md, "reset-database")

    def set_insert_buffering(self, value):
        '''
        Support the buffering of multiple insert_record() calls before
        the result is written in a single backend database call.
        '''

        # flush any buffers from previous usage
        self._flush_insert_buffers()

        # 15 records seems to be a good balance (override the specified value)
        self.insert_buffering = 15 if value else 0

    # def _flush_insert_buffer(self, cmd):

    #     dbx = self.db    # TODO: remember ws_name for each cmd

    #     with self.insert_buffer_lock:
    #         values = self.insert_buffers[cmd]
    #         del self.insert_buffers[cmd]

    #     #console.print("(single) flushing buffer for cmd: {}".format(cmd))
    #     self._execute_with_retry("_flush_insert_buffers", cmd=cmd, dbx=dbx, values=values, executemany=True)

    def _flush_insert_buffers(self):

        dbx = self.db    # TODO: remember ws_name for each cmd

        with self.insert_buffer_lock:
            buffers = dict(self.insert_buffers)
            self.insert_buffers = {}
            self.insert_buffering_started = None

        for cmd, values in buffers.items():
            #console.print("(all) flushing buffer for cmd: {}".format(cmd))
            self._execute_with_retry("_flush_insert_buffers", cmd=cmd, dbx=dbx, values=values, executemany=True)

    def _make_id(self, ws_name, job_or_run_name):
        return ws_name + "/" + job_or_run_name

    def _add_id(self, dd, ws_name, job_or_run_name):
        _id = ws_name + "/" + job_or_run_name
        dd["_id"] = _id

    def _node_id_from_id(self, rd):
        return utils.node_id(rd["_id"].split("/")[-1])

    def _make_data_by_node(self, node_recs):
        by_node = {}
        for nr in node_recs:
            node_id = self._node_id_from_id(nr)
            del nr["_id"]
            by_node[node_id] = nr
        return by_node

    def _field_from_records(self, records, name):
        value = None
        if records:
            value = utils.safe_value(records[0], name)

        return value

    def _flatten_prop(self, pd, name):
        if name in pd:
            value = pd[name]
            if value:
                pd[name] = json.dumps(value)
            else:
                pd[name] = None

    def _inflate_prop(self, pd, name, merge=False):
        # convert property values from json to actual data
        if pd and name in pd:
            value = pd[name]
            if value:
                vd = json.loads(value)
                if merge:
                    pd.update(vd)
                else:
                    pd[name] = vd

        return pd

    def _record_to_doc(self, record, group_markers=None):
        if not group_markers:
            group_markers = {}

        rd = {}
        group_name = None
        group = {}

        cols_desc = record.cursor_description
        for i, col_desc_tuple in enumerate(cols_desc):
            col_name = col_desc_tuple[0]    # first entry is col name

            if col_name in group_markers:
                # all columns after this one will be qualified by the group_name
                group_name = group_markers[col_name]
                group = {}
                rd[group_name] = group
                continue

            if group_name:
                # qualify column name with specified group name
                group[col_name] = record[i]
            else:
                # DANGER: first col takes priority over others with same name
                if not col_name in rd:
                    rd[col_name] = record[i]

        return rd

    def _docs_from_records(self, records, group_markers=None):

        console.diag("calling _record_to_doc on {:,} records".format(len(records)))
        docs = [self._record_to_doc(r, group_markers=group_markers) for r in records]
        return docs

    def _dict_from_row(self, record):
        rd = None
        if record:
            rd = self._record_to_doc(record)
        return rd

    def _execute_with_retry(self, caller, cmd=None, values=None, executemany=False, dbx=None, 
        fetch_type=None, expect_dup=False, verbose=False):
        '''
        Azure SQL Server has a number of errors that need to be retried when encountered:
            https://docs.microsoft.com/en-us/azure/azure-sql/database/troubleshoot-common-errors-issues

        This function centralizes all calls to Azure SQL server, retrying errors, and logging call stats.
        '''
        cmd_succeeded = False
        last_error = None
        started = time.time()
        retry_count = 0
        actual_call_time = 0
        retry_count = 2 if self.client_session  else self.max_retries
        result = None
        cursor = None

        if self.extended_logging:
            # for debugging connection-related hang error, always print this 
            console.print("odbc._execute_with_retry, cmd: {}".format(cmd), flush=True)

        for i in range(retry_count):

            if not dbx:
                dbx = self._reset_connection(cursor, dbx)
                
            try:
                actual_started = time.time()

                # control fake errors (debugging/testing)
                # this must be done before the actual cmd is executed
                if self.fake_error_percent and self.is_xt_run:
                    rand_val = np.random.random()
                    if rand_val < self.fake_error_percent:
                        self.max_backoff = 5
                        raise Exception("Fake DBX error")

                cursor = dbx.cursor()

                if verbose:
                    console.print("cursor: {}".format(cursor))
    
                if cursor:

                    if executemany:
                        # a multi-record insert
                        result0 = cursor.executemany(cmd, values)

                    elif values:
                        # a single record insert
                        result0 = cursor.execute(cmd, values)

                    else:
                        # a query or update with no extra data
                        result0 = cursor.execute(cmd)

                    if verbose:
                        console.print("result0: {}".format(result0))

                    if fetch_type == "fetchone":
                        result = cursor.fetchone()

                    elif fetch_type == "fetchall":
                        result = cursor.fetchall()

                    else:
                        # use best practice for getting rowcount
                        #result = cursor.rowcount
                        cursor.execute("select @@rowcount")
                        result = cursor.fetchall()[0][0]

                    if verbose:
                        console.print("fetch_type: {}, result0: {}".format(fetch_type, result0))

                else:
                    # execute command without returning results
                    if executemany:
                        # a multi-record insert
                        result = dbx.executemany(cmd, values)

                    elif values:
                        # a single record insert
                        result = dbx.execute(cmd, values)

                    else:
                        result = dbx.execute(cmd)

                    if verbose:
                        console.print("fetch_type: {}, result0: {}".format(fetch_type, result0))

                # cmd executed without error
                cmd_succeeded = True
                actual_call_time = time.time() - actual_started
                retry_count = i

                if i > 0:
                    # for debugging connection-related hang error, always print this 
                    console.print("==> ODBC: after {} retries, cmd executed SUCCESSFULLY: {}".format(i, cmd), flush=True)

                break
            except BaseException as ex:
                error_msg = str(ex)

                if verbose:
                    print("odbc exception: {}".format(error_msg))

                # fast fail errors (don't retry)
                INVALID_OBJECT = '42S02'
                INVALID_COL_NAME = '42S22'
                INVALID_NEXT_USAGE = '42000'
                PRIMARY_KEY_DUP = '23000'

                # errors that need new connection
                CONNECTION_BROKEN = "IMC06"
                CONNECTION_BROKEN2 = "10054"
                INTERNAL_ERROR = "08S01"
                CONNECTION_NOT_USABLE = "08S02"
                INVALID_CURSOR_STATE = "24000"
                CLOSED_CONNECTION = "HY000"

                CLOSED_CONNECTION_TEXT = "Attempt to use a closed connection"

                if isinstance(ex, pyodbc.Error):
                    error_code = ex.args[0]
                else:
                    error_code = None

                if i==0:
                    # don't log an error for this since it is expected
                    if expect_dup and error_code == PRIMARY_KEY_DUP:
                        # immediately to caller (normal expected error)
                        raise ex

                if i == 0:
                    # on first retryable error, print the cmd
                    console.print("\nodbc ERROR: \n  cmd: {}".format(cmd))
                    console.print("  values: {}".format(values))
                    console.print("  error_code: {}, exception: {}\n".format(cmd, error_code, ex))
                    # fast fail on known exceptions that shouldn't be retried

                else:
                    console.print("\nODBC retry {}/{} failed: cmd: {}, \n  error_code: {}, exception: {}\n".format(i, 
                        retry_count, cmd, error_code, ex))

                if i==0:
                    if error_code in [INVALID_OBJECT, INVALID_COL_NAME, INVALID_NEXT_USAGE, PRIMARY_KEY_DUP]:
                        console.print("FAST FAIL on pyodbc.Error error_code: {}".format(error_code))
                        raise ex

                connection_errors = [CLOSED_CONNECTION, CONNECTION_NOT_USABLE, CONNECTION_BROKEN, 
                    CONNECTION_BROKEN2, INTERNAL_ERROR, INVALID_CURSOR_STATE]

                if self.reset_connection_on_retry or error_code in connection_errors or CLOSED_CONNECTION_TEXT in error_msg:
                    console.print("RESETTING ODBC CONNECTION... (before retry of error_code: {})".format(error_code))
                    dbx = self._reset_connection(cursor, dbx)
                    cursor = None
                
                tb_lines = utils.get_stack_lines()
                run_errors.record_run_error("db", ex, cmd, tb_lines)

                if self.client_session:
                    backoff = 5
                else:
                    backoff = self.max_backoff*np.random.random()

                console.print("_execute_with_retry: retry={}, max_retries={}, backoff={}".\
                    format(i, self.max_retries, backoff))

                time.sleep(backoff)
                last_error = ex

        if not cmd_succeeded:
            errors.service_error("ODBC max retries exceeded={}, error={}".format(self.max_retries, last_error))

        # track all DATABASE call stats
        elapsed = time.time() - started

        if not caller in self.call_stats:
            self.call_stats[caller] = []

        entry = {"elapsed": elapsed, "actual_call_time": actual_call_time, "retry_count": retry_count}
        self.call_stats[caller].append(entry)

        console.diag("odbc stats entry:", entry)

        if cursor:
            cursor.close()

        return result

    def _create_table(self, dbx, name, col_dict):
        # build list of columns
        cd = {}
        cols = ""

        for col, ctype in col_dict.items():
            if cols == "":
                # firt col (primary key)
                cols = "[{}] {} PRIMARY KEY".format(col, ctype)
                cd[col] = ctype
            else:
                # subsequent key
                cols += ", [{}] {}".format(col, ctype)
                cd[col] = ctype

        if self.force_reset_database:
            cmd = "DROP TABLE IF EXISTS {}".format(name)
            self._execute_with_retry("_create_table", cmd=cmd, dbx=dbx)

        cmd = "CREATE TABLE [{}] ({})".format(name, cols)
        self._execute_with_retry("_create_table", cmd=cmd, dbx=dbx)

        console.print("  table created: {}".format(name))

        return cd

    def _make_node_id(self, ws_name, job_id, node_index):
        _id = "{}/{}/{}".format(ws_name, job_id, node_index)
        return _id

    def _validate_columns(self, vd, col_dict, table_name):
        for col_name in vd:
            if not col_name in col_dict:
                errors.internal_error("Unknown column being updated: table={}, col={}". \
                    format(table_name, col_name))

    def _build_col_str_in_groups(self, fields_dict, groups):
        cols = list(fields_dict)
        cols.sort()

        for group in groups:
            gdot = group + "."

            # insert __group__ separator cols
            for i in range(len(cols)):
                col = cols[i]
                if col.startswith(gdot):
                    # insert _g_ separator
                    cols.insert(i, "'' as _{}_".format(group))
                    break

        col_str = ", ".join(cols)
        return col_str

    def _dict_to_record(self, rd, col_dict):
        '''
        convert a dict of cols/values to a list of values, ordered by cols
        '''
        record = [rd[col] if col in rd else None for col in col_dict]
        return record

    def _expand_doc_as_tuple(self, dbx, table_name, doc, col_dict, force_vchar=False):
        '''
        This is where new cols are added for METRICS, HPARAMS, TAGS tables
        '''
        # any new cols being created?
        actual_cols = list(doc)
        new_cols = [col for col in actual_cols if not col in col_dict]
        exist_cols = [col for col in actual_cols if col in col_dict]

        if new_cols:        
            self._add_new_cols_to_table(dbx, table_name, new_cols, doc, col_dict, force_vchar=force_vchar)

        if exist_cols:
            self.validate_existing_bag_col_types(exist_cols, col_dict, doc)
                
        trec = [ self._safe_col_value(col_dict[key], doc[key]) for key in actual_cols ]
        return trec, actual_cols
        
    def validate_existing_bag_col_types(self, exist_cols, col_dict, doc):

        def is_float(text):
            try:
                value = float(text)
            except:
                return False
 
            return True

        # validate that existing cols have not changed type
        for col in exist_cols:
            exist_type = col_dict[col]
            value = self._safe_col_value(col_dict[col], doc[col])
            new_type =  self._get_col_type(value).lower()

            # matching rules somewhat complicated
            # NOTE: we only write values as VCHARxxx or FLOAT to SQL
            # SQL allows caller to write to a FLOAT column value from a string
            # SQL allows caller to write any type of value to a VARCHAR column 
            match = (exist_type == new_type) or (exist_type == "varchar")
            if not match and exist_type == "float" and is_float(value):
                match = True

            if not match:
                msg = "cannot change type of existing tag, hyperparameter, or metric (name: {}, existing type: {}, new type: {})".format(col, 
                     exist_type, new_type)
                raise Exception(msg)
                #print(msg)

    def _safe_col_value(self, col_type, value):
        if col_type == "BIT":
            value = 1 if value else 0
        elif isinstance(value, str) or value is None or math.isfinite(value):
            pass
        else:
            value = None
        return value

    def ensure_cols_are_present(self, dbx, table_name, values, col_dict):
        '''
        For use on normal tables (not tag/hparam/metrics)
        '''
        new_cols = [col for col in values if not col in col_dict]
        if new_cols:
            # build new_col_types from declared table columns
            new_col_types = {}
            cd = self.col_dict[table_name]

            for col_name in new_cols:
                new_col_types[col_name] = cd[col_name]

            self._add_new_cols_to_table(dbx, table_name, new_cols, values, col_dict, force_vchar=False, is_for_bag=False, new_col_types=new_col_types)

        return values

    def _update_record(self, dbx, table_name, ws_name, id, values, col_dict=None, actual_cols=None, ensure_record_found=True):
        '''
        if writing to table hparams, metrics, or tags:
            - use "col_dict" to detect new cols (and add them dynamicaly to table)
        else:
            - use "col_dict" to validate cols being updated

        ALWAYS: only update cols/values specified in values
        '''

        if not values:
            errors.internal_error("value dictionary/list cannot be empty")

        if not col_dict:
            col_dict = self._get_table_columns(dbx, table_name)

        table_is_bag = (table_name in ["hparams", "metrics", "run_tags", "job_tags", "node_tags"])
        force_vchar = (table_name in ["run_tags", "job_tags", "node_tags"])

        assert isinstance(values, dict)

        # prepare values for an update operation
        utils.safe_delete(values, "ws_name")
        utils.safe_delete(values, "_id")
        filter = {"_id": id}

        if table_is_bag:
            values, actual_cols = self._expand_doc_as_tuple(dbx, table_name, values, col_dict, force_vchar=force_vchar)
        else:
            vd = self.ensure_cols_are_present(dbx, table_name, values, col_dict)
            values = list(vd.values())   # self._dict_to_record(value_dict)
            actual_cols = list(vd)

        where_str = self._build_where_from_filter(filter)
        set_str = self._build_set_from_cols(actual_cols)
        cmd = "UPDATE [{}] {} {}".format(table_name, set_str, where_str)

        my_name = "_update_record__" + table_name

        rowcount = self._execute_with_retry(my_name, cmd=cmd, dbx=dbx, values=values)

        if ensure_record_found:
            # ensure we found exactly 1 record to update
            if rowcount != 1:
                print("WARNING: _update_record may have failed; rowcount={}, cmd={}".format(rowcount, cmd), flush=True)
                print("values for update: {}".format(values))
                print("attempting retry of update...")
                rowcount = self._execute_with_retry(my_name, cmd=cmd, dbx=dbx, values=values, verbose=True)
                assert rowcount == 1

    def _insert_record(self, dbx, table_name, ws_name, id, values, col_dict=None, filter=None, expect_dup=False):
        '''
        "values": an iterator of values, or a key/value dict
        '''

        if not values:
            errors.internal_error("value dictionary/list cannot be empty")

        if not col_dict:
            col_dict = self._get_table_columns(dbx, table_name)

        table_is_bag = (table_name in ["hparams", "metrics", "run_tags", "job_tags", "node_tags"])
        force_vchar = (table_name in ["run_tags", "job_tags", "node_tags"])

        assert isinstance(values, dict)
        if ws_name:
            values["ws_name"] = ws_name
        values["_id"] = id

        if table_is_bag:
            values, actual_cols = self._expand_doc_as_tuple(dbx, table_name, values, col_dict)
        else:
            vd = self.ensure_cols_are_present(dbx, table_name, values, col_dict)
            actual_cols = list(vd)
            values = self._dict_to_record(values, actual_cols)

        format_str = ", ".join("?" for col in actual_cols)
        col_str = self._build_col_list_from_cols(actual_cols)
        cmd = "INSERT INTO [{}] ({}) VALUES ({})".format(table_name, col_str, format_str)

        if self.insert_buffering:
            #console.print("BUFFERING cmd: {}".format(cmd))

            with self.insert_buffer_lock:

                if not self.insert_buffering_started:
                    # on first insert, note starting time
                    self.insert_buffering_started = time.time()

                if not cmd in self.insert_buffers:
                    self.insert_buffers[cmd] = []

                self.insert_buffers[cmd].append(values)
                count = len(self.insert_buffers[cmd])

                buffering_elapsed = time.time() - self.insert_buffering_started

            # flush buffers when max records collected or if max time in buffering has been exceeded
            if count >= self.insert_buffering or buffering_elapsed >= MAX_BUFFERING_SECS:
                #console.print("** flushing insert buffers: elapsed: {} secs **".format(buffering_elapsed))
                self._flush_insert_buffers()

        else:
            my_name = "_insert_record__" + table_name
            self._execute_with_retry(my_name, cmd=cmd, dbx=dbx, values=values, expect_dup=expect_dup)

    def _insert_many(self, dbx, table_name, rd_list):

        console.diag("_insert_many: inserting {:,} records for table '{}'".format(
            len(rd_list), table_name))

        cols = self._get_table_columns(dbx, table_name)
        actual_cols = list(rd_list[0])

        format_str = ", ".join("?" for col in actual_cols)
        col_str = self._build_col_list_from_cols(actual_cols)
        cmd = "INSERT INTO [{}] ({}) VALUES ({})".format(table_name, col_str, format_str)

        # convert dicts to records
        records = [self._dict_to_record(rd, actual_cols) for rd in rd_list]

        self._execute_with_retry("_insert_many", cmd=cmd, dbx=dbx, values=records, executemany=True)

    def _build_col_list_from_cols(self, actual_cols):
        text = ""
        for i, col in enumerate(actual_cols):
            if i:
                text += ", "
            text += "[{}]".format(col)

        return text

    def _build_set_from_cols(self, actual_cols):
        text = "SET "
        for i, col in enumerate(actual_cols):
            if i:
                text += ", "
            text += "[{}] = ?".format(col)

        return text

    def _build_value_str(self, value_list):
        text = ""
        for value in value_list:
            if text:
                text += ", "
            if isinstance(value, str):
                text += "'{}'".format(value)
            else:
                text += "{}".format(value)
        return text

    def _build_contains_str(self, value_list):
        text = ""
        for value in value_list:
            if text:
                text += " OR "
            if isinstance(value, str):
                text += '"{}"'.format(value)
            else:
                text += "{}".format(value)

        return text

    def _build_where_from_filter(self, filter, add_brackets=True, separator=" AND ", recursive=False):
        if filter:
            where = "" if recursive else "where " 
            
            for i, (key, value) in enumerate(filter.items()):
                if i:
                    where += separator

                if add_brackets:
                    key = "[{}]".format(key)

                if isinstance(value, str):
                    value = "'{}'".format(value)

                elif isinstance(value, bool):
                    value = 1 if value else 0

                elif isinstance(value, (int, float)) or (value is None):
                    # value is already OK
                    pass
                
                elif key == "$or":
                    # recursive call (value is list of elements)
                    w_str = ""
                    for elem in value:
                        ws = self._build_where_from_filter(elem, add_brackets=add_brackets, recursive=True)
                        if w_str:
                            w_str += " OR "
                        w_str += ws

                    where += "({})".format(w_str)
                    continue

                elif key == "$and":
                    # recursive call (value is list of elements)
                    w_str = ""
                    for elem in value:
                        ws = self._build_where_from_filter(elem, add_brackets=add_brackets, recursive=True)
                        if w_str:
                            w_str += " AND "
                        w_str += ws

                    where += "({})".format(w_str)
                    continue

                elif isinstance(value, dict):
                    for prop, val in value.items():
                        if prop == "$in":
                            where += "{} in ({})".format(key, self._build_value_str(val))

                        elif prop == "$nin":
                            where += "NOT ({} in ({}))".format(key, self._build_value_str(val))

                        elif prop == "$contains":
                            where += "CONTAINS({}, '{}')".format(key, self._build_contains_str(val))

                        elif prop == "$ncontains":
                            where += "NOT CONTAINS({}, '{}')".format(key, self._build_contains_str(val))

                        elif prop == "$exists":
                            if val:
                                where += "{} is NOT NULL".format(key)
                            else:
                                where += "{} is NULL".format(key)

                        elif prop == "$regex":
                            # SQL Server doesn't support regex, but we can try to map to its subset expression language
                            like_val = val.replace(".*", "%")
                            where += "{} LIKE '{}'".format(key, like_val)
                        
                        elif prop == "$gt":
                            where += "{} > {}".format(key, val)
                        
                        elif prop == "$gte":
                            where += "{} >= {}".format(key, val)
                        
                        elif prop == "$lt":
                            where += "{} < {}".format(key, val)
                        
                        elif prop == "$lte":
                            where += "{} <= {}".format(key, val)

                        elif prop == "$ne":
                            # recursive call
                            r_filter = {key: val}
                            w_str = self._build_where_from_filter(r_filter, add_brackets=add_brackets, separator=None, recursive=True)
                            where += "NOT ({})".format(w_str)

                        elif prop == "$or":
                            # recursive call on each element in list
                            assert isinstance(val, list)
                            for v, vd in enumerate(val):

                                r_filter = {key: vd}
                                w_str = self._build_where_from_filter(r_filter, add_brackets=add_brackets, separator=None, recursive=True)

                                if v == 0:
                                    where += " ({})".format(w_str)
                                else:
                                    where += " OR  ({})".format(w_str)

                        elif prop == "$and":
                            # recursive call on each element in list
                            assert isinstance(val, list)
                            for v, vd in enumerate(val):

                                r_filter = {key: vd}
                                w_str = self._build_where_from_filter(r_filter, add_brackets=add_brackets, separator=None, recursive=True)

                                if v == 0:
                                    where += " ({})".format(w_str)
                                else:
                                    where += " AND  ({})".format(w_str)

                        else:
                            errors.internal_error("unsupported filter value: {}".format(value))
                    continue

                else:
                    errors.internal_error("unsupported filter part: key={}, value={}".format(key, value))

                if value is None:
                    where += "{} is NULL".format(key)
                else:   
                    where += "{} = {}".format(key, value)
        else:
            where = ""

        return where

    def _query(self, dbx, table_name, filter, fields=None, sort_col=None, sort_dir=1, skip=None, 
        first=None, add_brackets=True):

        if fields:
            col_str = ", ".join(["[{}]".format(col) for col in fields])
        else:
            col_str = "*"

        where = self._build_where_from_filter(filter, add_brackets=add_brackets)

        # build cmd
        cmd = "select {} from [{}] {}".format(col_str, table_name, where)

        if sort_col:
            cmd += " ORDER BY {}".format(sort_col)
            if sort_dir == -1:
                cmd += " DESC"

        if skip:
            cmd += " OFFSET {} ROWS".format(skip)
            if first:
                cmd += " FETCH NEXT {} rows only".format(first)

        my_name = "_query__" + table_name
        records = self._execute_with_retry(my_name, cmd=cmd, dbx=dbx, fetch_type="fetchall")

        docs = [self._dict_from_row(record) for record in records]

        # if value and fields and len(fields) == 1:
        #     key = list(fields)[0]
        #     value = value[key]

        return docs

    def _get_table_columns(self, dbx, table_name):
        if table_name in self.cols_by_table:
            # cache HIT
            col_dict = self.cols_by_table[table_name]
        else:
            # cache MISS
            cmd = "select COLUMN_NAME, DATA_TYPE from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{}'".format(table_name)
            records = self._execute_with_retry("_get_table_columns", cmd=cmd, dbx=dbx, fetch_type="fetchall")
            col_dict = {col[0]: col[1] for col in records}

            self.cols_by_table[table_name] = col_dict
            
        return col_dict

    def _get_col_type(self, value, is_for_bag=True):
        if isinstance(value, str):
            return VARCHAR

        if not is_for_bag:
            if isinstance(value, int):
                return INT

        return FLOAT
        
    def _adjust_job_record(self, dbx, record, need_service_info, need_connect_info, need_secrets_by_node, need_runs_by_box):

        # inflate json props, if found
        self._inflate_prop(record, "pool_info")
        self._inflate_prop(record, "service_job_info")

        _id = record["_id"]
        ws_name, job_id = _id.split("/")
        filter_dict = {"ws_name": ws_name, "job_id": job_id}

        if need_service_info:
            # separate query
            fields = {"_id": 1, "service_info": 1}
            si_docs = self._query(dbx, "node_info", filter_dict, fields, add_brackets=False)

            # build service_info_by_node from si_docs
            service_info_by_node = {}
            for doc in si_docs:
                node_index = doc["_id"].split("/")[-1]
                node_id = utils.node_id(node_index)
                service_info_json = doc["service_info"]
                if service_info_json:
                    service_info_by_node[node_id] = json.loads(service_info_json)

            record["service_info_by_node"] = service_info_by_node

        if need_connect_info:
            # separate query
            fields = {"ip_addr": 1, "controller_port": 1, "_id": 1}
            ci_records = self._query(dbx, "node_info", filter_dict, fields)
            if ci_records:
                record["connect_info_by_node"] = self._make_data_by_node(ci_records)

        if need_secrets_by_node:
            # separate query
            fields = {"secret": 1, "_id": 1}
            ci_records = self._query(dbx, "node_info", filter_dict, fields)
            if ci_records:
                record["secrets_by_node"] = self._make_data_by_node(ci_records)

        if need_runs_by_box:
            # separate query
            fields = {"box_name": 1, "run_name": 1, "node_index": 1, "node_id": 1}
            ci_records = self._query(dbx, "node_info", filter_dict, fields)
            if ci_records:
                # convert into runs_by_box records
                runs_by_box = {}
                for cr in ci_records:
                    rb = {"box_index": cr["node_index"], "run_name": cr["run_name"], "ws_name": ws_name}
                    node_id = cr["node_id"]
                    runs_by_box[node_id] = rb

                record["runs_by_box"] = runs_by_box

        return record

    def _add_new_cols_to_table(self, dbx, table_name, new_cols, record, cols_dict, force_vchar=False, is_for_bag=True, new_col_types=None):
        # determine type of new cols
        if new_col_types:
            for col_name, col_type in new_col_types.items():
                cols_dict[col_name] = col_type

        elif force_vchar:
            for col_name in new_cols:
                cols_dict[col_name] = VARCHAR

        else:
            for col_name in new_cols:
                cols_dict[col_name] = self._get_col_type(record[col_name], is_for_bag=is_for_bag)

        # build cmd to add new_cols to table 
        # protect each add with a "if not exists" clause (other jobs could add our col at any time)
        cmd = ""
        for i, key in enumerate(new_cols):
            col_type = cols_dict[key]
            if i:
                cmd += "; "

            cmd += "IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS where TABLE_NAME='{}' AND COLUMN_NAME='{}') \
                ALTER TABLE [{}] ADD [{}] {}".format(table_name, key, table_name, key, col_type)

        # execute the alter table cmd
        self._execute_with_retry("_add_new_cols_to_table", cmd=cmd, dbx=dbx)

        # invalidate our CACHE
        if table_name in self.cols_by_table:
            del self.cols_by_table[table_name]

    def _does_table_exists(self, dbx, table_name):
        cmd = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{}'".format(table_name)
        record = self._execute_with_retry("_does_table_exists", cmd=cmd, dbx=dbx, fetch_type="fetchone")
        return bool(record)
    
    def _does_workspace_exist(self, ws_name):
        dbx = self._get_db(None)
        records = self._query(dbx, WORKSPACES, {"ws_name": ws_name}, {"db_name": 1})
        db_name = self._field_from_records(records, "db_name")
        return bool(db_name)

    # API call
    def get_db_type(self):
        return "odbc"

    # API call
    def get_service_name(self):
        return "sqldb"

    # API call
    def get_db_info(self):
        '''
        example: {_id: 1, paired_storage: "sandboxstoragev2", storage_format: "2"}
        '''
        rd = None
        started = time.time()

        if not self.force_reset_database:
            # now we can rely on DEFAULT database
            dbx = self._get_db(None)
            if self._does_table_exists(dbx, DB_INFO):

                cmd = "select * from [{}]".format(DB_INFO)
                record = self._execute_with_retry("get_db_info", cmd=cmd, dbx=dbx, fetch_type="fetchone")
    
                rd = self._dict_from_row(record)

        # elapsed = time.time() - started
        # console.print("get_db_info elapsed: {:.2f} secs".format(elapsed))

        return rd

    # API call
    def set_db_info(self, db_info):

        dbx = self._get_db(None)

        # create DB_INFO table
        keys = {"_id": INT, "paired_storage": VARCHAR, "storage_format": VARCHAR}
        self._create_table(dbx, DB_INFO, keys)
        #vd = {"paired_storage": db_info["paired_storage"], "storage_format": db_info["storage_format"]}
        self._insert_record(dbx, DB_INFO, ws_name=None, id=1, values=db_info, col_dict=keys)

        # create WORKSPACES table
        keys = {"_id": VARCHAR, "db_name": VARCHAR, "next_job_number": INT, "next_end_id": INT, 
            "next_request_number": INT, "ws_name": VARCHAR}
        self._create_table(dbx, WORKSPACES, keys)

        self._init_core_tables(dbx, create=True)

    # API call
    def create_workspace_if_needed(self, ws_name, db_name=None):
        '''
        Processing:
            - using the specified db_name, add ws_name to our __workspaces__ table
            - create core tables if needed:
                - run_info, run_stats, hparams, metrics, tags
                - job_info, job_stats, node_info, node_stats
                - requests
        '''
        started = time.time()

        exists = self._does_workspace_exist(ws_name)
        if self.force_reset_database or not exists:

            # add to WORKSPACES
            dbx = self._get_db(None)
            vd = {"db_name": self.default_db, "next_job_number": 1, "next_end_id": 1, "next_request_number": 1}
            self._insert_record(dbx, WORKSPACES, ws_name=ws_name, id=ws_name, values=vd)

        # elapsed = time.time() - started
        # console.print("create workspace elapsed: {:.2f}".format(elapsed))

    # API call
    def set_column_type(self, ws_name, table_name, col_name, col_type):
        dbx = self._get_db(ws_name)
        
        cmd = "ALTER TABLE [{}] ALTER COLUMN [{}] {}".format(table_name, col_name, col_type)
        self._execute_with_retry("set_column_type", cmd=cmd, dbx=dbx)

    # API call
    def get_column_type(self, ws_name, table_name, col_name):
        dbx = self._get_db(ws_name)
        records = []
        
        if col_name:
            cmd = "SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = '{}'" \
                "and COLUMN_NAME = '{}'".format(table_name, col_name)

        else:
            cmd = "SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = '{}'" \
                .format(table_name)

        cols = self._execute_with_retry("get_column_type", cmd=cmd, dbx=dbx, fetch_type="fetchall")
        for col in cols:
            name = col[0]
            type = col[1]
            len = col[2]

            if len is not None:
                type = "{}-{}".format(type, len)

            cd = {"column": name, "type": type}
            records.append(cd)

        return records

    # API call
    def delete_workspace_if_needed(self, ws_name):
        '''
        Processing:
            - remove all data for this workspace from core tables
            - remove ws_name from list of specified workspaces
        '''
        started = time.time()

        exists = self._does_workspace_exist(ws_name)
        if exists:
            dbx = self._get_db(ws_name)
            filter = {"ws_name": ws_name}

            self._delete_from_table(dbx, "run_info", filter)
            self._delete_from_table(dbx, "run_stats", filter)
            self._delete_from_table(dbx, "run_steps", filter)
            self._delete_from_table(dbx, "run_tags", filter)

            self._delete_from_table(dbx, "job_info", filter)
            self._delete_from_table(dbx, "job_stats", filter)
            self._delete_from_table(dbx, "job_tags", filter)

            self._delete_from_table(dbx, "node_info", filter)
            self._delete_from_table(dbx, "node_stats", filter)
            self._delete_from_table(dbx, "node_tags", filter)

            self._delete_from_table(dbx, "hparams", filter)
            self._delete_from_table(dbx, "metrics", filter)
            self._delete_from_table(dbx, "requests", filter)

            dbx.commit()

            dbx = self._get_db(None)
            self._delete_from_table(dbx, WORKSPACES, filter)
            dbx.commit()
        
        # elapsed = time.time() - started
        # console.print("delete workspace elapsed: {:.2f}".format(elapsed))

        return exists

    def _create_index(self, dbx, table_name, index_name, col_list):
        with dbx:
            bracket_cols = ["[{}]".format(col) for col in col_list]
            col_str = ", ".join(bracket_cols)

            cmd = "CREATE INDEX {} ON {} ({});".format(index_name, 
                table_name, col_str)

    def _init_core_tables(self, dbx, create=False):
        '''
        NOTE: every table should include the col 'ws_name'.
        '''
        col_dict = {}
        self.col_dict = col_dict

        # WORKSPACES
        col_dict[WORKSPACES] = {"_id": VARCHAR, 'db_name': VARCHAR, 'next_job_number': INT, "next_end_id": INT, 
            "ws_name": VARCHAR, "next_request_number": INT}
        if create and not self._does_table_exists(dbx, WORKSPACES):
            self._create_table(dbx, "WORKSPACES", col_dict["WORKSPACES"] )

        # RUN_INFO
        col_dict["run_info"] = {"_id": VARCHAR, 'app_name': VARCHAR, 'box_name': VARCHAR, 'cmd_line_args': BIGCHAR,
            'compute': VARCHAR, 'create_time': TIME, 'description': VARCHAR, 'display_name': VARCHAR, 'exper_name': VARCHAR, 
            'from_ip': VARCHAR, 'from_computer_name': VARCHAR, 'job_id': VARCHAR, 'path': VARCHAR,
            'run_name': VARCHAR, 'run_guid': VARCHAR, 'script': VARCHAR, 'search_style': VARCHAR,
            'search_type': VARCHAR, 'service_type': VARCHAR, 'sku': VARCHAR, 'username': VARCHAR,
            'ws_name': VARCHAR, 'xt_build': VARCHAR, 'xt_version': VARCHAR, 'xt_cmd': BIGCHAR,
            'is_child': BOOL, 'is_outer': BOOL, 'is_parent': BOOL,
            'node_index': INT, 'repeat': INT, "run_index": INT, "hp_set": BIGCHAR,
            'run_num': BIGINT,
            # added post-submit by philly backend
            'cluster': VARCHAR, 'vc': VARCHAR, 'service_run_id': VARCHAR}
        if create:
            self._create_table(dbx, "run_info", col_dict["run_info"] )
            self._create_index(dbx, "run_info", "run_num", ["run_num"])
            self._create_index(dbx, "run_info", "ws_name", ["ws_name"])

        # RUN_STATS
        col_dict["run_stats"] = {"_id": VARCHAR, 'status': VARCHAR, 'ws_name': VARCHAR, 'job_id': VARCHAR, 'start_time': TIME, 
            'last_time': TIME, 'end_time': TIME, 'queue_duration': DURATION, 'run_duration': DURATION,
            'metric_names': BIGCHAR, 'error_msg': BIGCHAR, 'exit_code': INT, 'end_id': INT, 'restarts': INT,
            'db_retries': INT, 'storage_retries': INT}
        if create:
            self._create_table(dbx, "run_stats", col_dict["run_stats"])
            self._create_index(dbx, "run_stats", "status", ["status"])

        # RUN_STEPS
        col_dict["run_steps"] = {"_id": VARCHAR, 'ws_name': VARCHAR, 'job_id': VARCHAR, 'node_id': VARCHAR,
            "base_run_name": VARCHAR, "run_name": VARCHAR, "step_num": INT, 'time': TIME}

        if create or not self._does_table_exists(dbx, "run_steps"):
            self._create_table(dbx, "run_steps", col_dict["run_steps"])

        # we don't need to know the required columns for these tables
        if create:
            # HPARAMS
            cols = {"_id": VARCHAR, "ws_name": VARCHAR}
            self._create_table(dbx, "hparams", cols)

            # METRICS
            cols = {"_id": VARCHAR, "ws_name": VARCHAR}
            self._create_table(dbx, "metrics", cols)

            # RUN_TAGS
            cols = {"_id": VARCHAR, "ws_name": VARCHAR, "run_name": SMALLCHAR}
            self._create_table(dbx, "run_tags", cols)

            # JOB_TAGS
            cols = {"_id": VARCHAR, "ws_name": VARCHAR, "job_id": SMALLCHAR}
            self._create_table(dbx, "job_tags", cols)

            # NODE_TAGS
            cols = {"_id": VARCHAR, "ws_name": VARCHAR, "job_id": SMALLCHAR}
            self._create_table(dbx, "node_tags", cols)

        # JOB_INFO
        # NEW COLS: sla, low_pri, vm_size, sku, service_name, service_type, aml_compute, compute_target, num_dgd_seeds
        col_dict["job_info"] =  {"_id": VARCHAR, "aml_compute": VARCHAR, "compute_target": VARCHAR, 
            "concurrent": BOOL, "exper_name": VARCHAR, "hold": BOOL, "job_id": VARCHAR, 
            "job_num": BIGINT, "job_guid": VARCHAR, "job_secret": VARCHAR, "low_pri": VARCHAR,
            "node_count": INT, "num_dgd_seeds": INT, "location": BIGCHAR, "primary_metric": VARCHAR, "run_count": INT, "repeat": INT,
            "schedule": VARCHAR, "search_type": VARCHAR, "search_style": VARCHAR, "service_name": VARCHAR, 
            "service_type": VARCHAR, "sku": VARCHAR, "sla": VARCHAR, "username": VARCHAR, 
            "xt_cmd": BIGCHAR, "started": TIME, "pool_info": BIGCHAR, "service_job_info": VARCHAR, 
            "ws_name": VARCHAR, "sleep_on_exit": SMALLCHAR, "vm_size": VARCHAR}
        if create:
            self._create_table(dbx, "job_info", col_dict["job_info"])
            self._create_index(dbx, "job_info", "ws_name", ["ws_name"])

        # JOB_STATS
        col_dict["job_stats"] = {"_id": VARCHAR, "job_status": VARCHAR, "completed_runs": INT, "error_runs": INT, 
            "running_nodes": INT, "running_runs": INT, "total_runs": INT, 'ws_name': VARCHAR, "run_started": TIME,
            'queue_duration': DURATION, 'run_duration': DURATION, 'heartbeat': INT,
            "end_time": TIME, 
            'restarts': INT, 'db_retries': INT, 'storage_retries': INT, 'next_run_index': INT}
        if create:
            self._create_table(dbx, "job_stats", col_dict["job_stats"])
            self._create_index(dbx, "job_stats", "status", ["status"])

        # NODE_INFO
        col_dict["node_info"] = {
            "_id": VARCHAR, 'ws_name': VARCHAR, "job_id": VARCHAR, "exper_name": VARCHAR, 
            "node_name": SMALLCHAR, "aml_compute": VARCHAR, "compute_target": VARCHAR,
            "node_id": SMALLCHAR, "node_index": INT, "node_num": BIGINT, 
            "total_runs": INT, "box_name": VARCHAR, "run_name": VARCHAR, 
            "controller_port": INT, "ip_addr": VARCHAR,
            "secret": VARCHAR, "service_info": BIGCHAR}
        if create:
            self._create_table(dbx, "node_info", col_dict["node_info"])

        # NODE_STATS
        col_dict["node_stats"] = {
            "_id": VARCHAR, 'ws_name': VARCHAR, "node_status": VARCHAR, 
            'create_time': TIME, 'prep_start_time': TIME, "app_start_time": TIME, 
            "post_start_time": TIME, "post_end_time": TIME, 'heartbeat': INT,
            'queue_duration': DURATION, 'prep_duration': DURATION, 
            "app_duration": DURATION, "post_duration": DURATION,
            "completed_runs": INT, "error_runs": INT, "running_runs": INT,  
            'restarts': INT, 'db_retries': INT, 'storage_retries': INT}
        if create:
            self._create_table(dbx, "node_stats", col_dict["node_stats"])
            self._create_index(dbx, "node_stats", "node_status", ["node_status"])

        # REQUESTS  (must be last to be processed)
        col_dict["requests"] = {"_id": VARCHAR, "ws_name": VARCHAR, "request_id": VARCHAR, "status": VARCHAR,
            "target": VARCHAR, "nodes": INT, "runs": INT, "cmd": BIGCHAR, "env_vars": BIGCHAR,
            "requested_by": VARCHAR, "action_by": VARCHAR, "create_time": TIME, "action_time": TIME, 
            "job_id": VARCHAR, "description": VARCHAR,"takeaway": VARCHAR}

        if not create:
            # ensure this late-added table exists in this database
            if not self._does_table_exists(dbx, "requests"):
                create = True

        if create:
            self._create_table(dbx, "requests", col_dict["requests"])
            self._create_index(dbx, "requests", "status", ["request_id"])            
        else:
            # add new columns here (required if it appears in a query before being auto-added on an update/insert)
            self._add_column_if_needed(dbx, "requests", "env_vars", BIGCHAR)
            self._add_column_if_needed(dbx, "job_info", "location", BIGCHAR)
            self._add_column_if_needed(dbx, "job_stats", "run_started", TIME)

    def _add_column_if_needed(self, dbx, table_name, col_name, col_type):
        cmd = "IF COL_LENGTH('{}', '{}') IS NULL BEGIN ALTER TABLE [{}] ADD [{}] {} END".format(\
            table_name, col_name, table_name, col_name, col_type)
            
        self._execute_with_retry("set_column_type", cmd=cmd, dbx=dbx)

    def _delete_from_table(self, dbx, table_name, filter):


        filter_str = self._build_where_from_filter(filter)
        cmd = "delete from [{}] {}".format(table_name, filter_str)

        # table doesn't have to exist
        if self._does_table_exists(dbx, table_name):
            self._execute_with_retry("_delete_from_table", cmd=cmd, dbx=dbx)
        else:
            console.print("warning: XT database table not found: {}".format(table_name))

    def _get_db(self, ws_name=None):
        '''
        get a connection to the database associated with the ws_name.
        '''

        # if not ws_name:
        #     db_name = self.default_db
        # elif ws_name in self.db_from_ws:
        #     db_name = self.db_from_ws[ws_name]
        # else:
        #     # get db_name from WORKSPACES
        #     dbx = self._make_connection(self.default_db)

        #     db_name = self._query(dbx, WORKSPACES, {"ws_name": ws_name}, {"db_name": 1})
        #     if not db_name:
        #         errors.service_error("workspace not found: {}".format(ws_name))

        #     self.db_from_ws[ws_name] = db_name

        # return self._make_connection(db_name)
        return self.db

    def get_next_run_index(self, ws_name, job_id):
        dbx = self._get_db(None)
        id = self._make_id(ws_name, job_id)

        cmd = "UPDATE [job_stats] SET [next_run_index] = [next_run_index] + 1 OUTPUT INSERTED.[next_run_index] WHERE [_id] = '{}'". \
            format(id)

        record = self._execute_with_retry("get_next_run_index", cmd=cmd, dbx=dbx, fetch_type="fetchone")
        next_id = record[0]
        next_id -= 1        # get value before increment

        return next_id

    def get_next_id_from_workspace(self, ws_name, id_name):

        dbx = self._get_db(None)

        # ensure this late-added id_name exists in WORKSPACES
        if id_name == "next_request_number":

            # add column to table, if missing, and set initial value = 1
            col_cmd = "IF COL_LENGTH('{}', '{}') IS NULL BEGIN ALTER TABLE [{}] ADD [{}] INT CONSTRAINT ONE DEFAULT 1 WITH VALUES; END".format(\
                WORKSPACES, id_name, WORKSPACES, id_name)
            self._execute_with_retry("get_next_id_from_workspace", cmd=col_cmd, dbx=dbx, fetch_type=None)

        cmd = "UPDATE [{}] SET [{}] = [{}] + 1 OUTPUT INSERTED.[{}] WHERE [ws_name] = '{}' ". \
            format(WORKSPACES, id_name, id_name, id_name, ws_name)

        # update the count and return its value
        record = self._execute_with_retry("get_next_id_from_workspace", cmd=cmd, dbx=dbx, fetch_type="fetchone")
        next_id = record[0]
        next_id -= 1        # get value before increment

        return next_id

    def get_next_end_id_without_update(self, ws_name):

        dbx = self._get_db(None)
        cmd = "SELECT [next_end_id] from [{}] WHERE [ws_name] = '{}' ".format(WORKSPACES, ws_name)

        record = self._execute_with_retry("get_next_end_id_without_update", cmd=cmd, dbx=dbx, fetch_type="fetchone")
        next_id = record[0]

        return next_id

    # API call
    def get_next_run_name(self, ws_name, job_id, is_parent, total_run_count, node_index):
        # v2 run name takes its base from the job_id
        job_num = job_helper.get_job_number(job_id)
        run_name = "run" + str(job_num)

        if total_run_count > 1:
            run_name += constants.NODE_PREFIX + str(node_index)

        return run_name

    def process_run_event(self, ws_name, run_name, event, orig_dd, record_dict):
        '''
        We have turned off some updates to run_stats to avoid redundant db updates.
        '''
        dbx = self._get_db(ws_name)
        _id = self._make_id(ws_name, run_name)

        run_stats = {}
        completed = False
        dd = dict(orig_dd)

        if event == "created":
            job_id = dd["job_id"]

            # add RUN_TAGS record
            tag_list = utils.safe_delete(dd, "tags")
            td = utils.tag_dict_from_list(tag_list)

            td["job_id"] = job_id
            self._upsert_record(dbx, "run_tags", ws_name, _id, td)

            # add RUN_INFO record
            self._upsert_record(dbx, "run_info", ws_name, _id, dd)

            # add RUN_STATS record
            if self.update_run_stats_enabled:
                rs = {"status": "created", "job_id": job_id, "storage_retries": 0, "db_retries": 0}
                self._upsert_record(dbx, "run_stats", ws_name, _id, rs)

        elif event == "status-change":
            #run_stats.update(dd)
            pass

        elif event == "ended":
            # dd = dict(dd)    # make local copy that we can update
            # del dd["metrics_rollup"]
            # run_stats.update(dd)
            completed = True

        elif event == "queued":
            #run_stats["status"] = event
            # we explictly set status to "queued" in runner.py (all runs at once)
            pass

        elif event in ["started"]:
            #run_stats["status"] = "running"
            pass

        elif event == "hparams":
            if not dd:
                errors.argument_error("hyperparameter dictionary cannot be empty")

            self._upsert_record(dbx, "hparams", ws_name, _id, dd)

        elif event == "metrics":
            self.metrics.update(dd)

            if not "_id" in self.metrics:
                self._add_id(self.metrics, ws_name, run_name)

            diff = time.time() - self.last_metrics_write

            if diff/60 >= self.buffer_metrics:

                # time to write metrics to database
                #console.print("WRITING metrics: {}".format(dd))
                self._upsert_record(dbx, "metrics", ws_name, _id, self.metrics)
                self.last_metrics_write = time.time()

                self.metrics_dirty = False
            else:
                self.metrics_dirty = True

        # if self.add_log_records:
        #     self.add_log_record(ws_name, run_name, record_dict)

        return completed

    # API call
    def update_collection(self, collection_name, ws_name, dd, is_flat=True, flat_exceptions=[]):
        dbx = self._get_db(ws_name)
        _id = dd["_id"]
        self._upsert_record(dbx, collection_name, ws_name, _id, dd)

    def _upsert_record(self, dbx, table_name: str, ws_name: str, id: str, vd: dict, skip_insert=False):
        '''
        Args:
            dbx: the database connection (matching the specified ws_name)
            ws_name: the name of the workspace
            id: the unique id for the record being inserted or updated
            vd: a dictionary of name/value pairs for the columns of the record
        Processing:
            update or insert a single record ("upsert") in the specified table. 
        '''
        DUP_RECORD = "Violation of PRIMARY KEY constraint"
        DUP_RECORD_NUM = 23000
        update_needed = True

        if not skip_insert:
            # try to first insert record
            try:
                self._insert_record(dbx, table_name, ws_name, id, vd, expect_dup=True)
                update_needed = False

            except BaseException as ex:
                error_msg = str(ex)
                #console.print("_insert_record: ex={}".format(error_msg))
                if not DUP_RECORD in error_msg:
                    raise

        if update_needed:
            # existing record; just update it
            self._update_record(dbx, table_name, ws_name, id, vd)

    # API call
    def create_db_job(self, jd, update_job_stats=True):
        ws_name = jd["ws_name"]
        job_id = jd["job_id"]

        self.update_job_info(ws_name, job_id, jd, update_primary=True, new_job=True, update_job_stats=update_job_stats, zero_counts=False)

    # API call
    def update_job_info(self, ws_name, job_id, orig_dd, update_primary=False, new_job=False, update_job_stats=True, zero_counts=True):
        '''
        Args:
            - ws_name: name of the associated workspace
            - job_id: name of the job being updated
            - orig_dd: a dictionary of name/value pairs.  Can include nested: service_info_by_node,
                connect_info, child_runs, and hparams.  Other props split between job_info and job_stats.
            - update_primary: specifies if the job_info collection be updated

        Processing:
            This is the CORE function for updating job related information.  The following 
            collections may be updated: job_info, job_stats, and hparams.

            In order for the job_info collection to be updated, update_primary must = True.
        '''
        dbx = self._get_db(ws_name)
        _id = self._make_id(ws_name, job_id)

        jd = dict(orig_dd)    # make a copy to operate on
        total_runs = utils.safe_value(jd, "run_count")

        # delete low-priority embedded info
        utils.safe_delete(jd, "runs_by_box")

        # delete obsolete embedded info
        utils.safe_delete(jd, "active_runs")
        utils.safe_delete(jd, "dynamic_runs_remaining")

        # extract embedded info
        service_info_by_node = utils.safe_delete(jd, "service_info_by_node")
        runs_by_box = utils.safe_delete(jd, "runs_by_box")
        connect_info_by_node = utils.safe_delete(jd, "connect_info_by_node")
        secrets_by_node = utils.safe_delete(jd, "secrets_by_node")
        child_runs_by_node = utils.safe_delete(jd, "child_runs_by_node")

        hparams = utils.safe_delete(jd, "hparams")

        tags = {"job_id": job_id}
        tag_list = utils.safe_delete(jd, "tags")
        td = utils.tag_dict_from_list(tag_list)
        tags.update(td)

        # extract job stats properties
        job_stats = {}
        for prop in job_helper.job_stats_props:
            utils.safe_move(job_stats, jd, prop)

        if self.update_job_stats_enabled and update_job_stats:
            # hardcode any missing stats so that when processing job log, counts are correct
            # (v1 job stats are a subset of v2)
            for prop in job_helper.job_stats_props:
                if not prop in job_stats:
                    if prop == "total_runs":
                        job_stats[prop] = total_runs
                    elif zero_counts:
                        job_stats[prop] = 0

            self._upsert_record(dbx, "job_stats", ws_name, _id, job_stats)

        # add to HPARAMS
        if hparams:
            self._upsert_record(dbx, "hparams", ws_name, _id, hparams)

        # add to JOB_INFO
        if update_primary:

            self._flatten_prop(jd, "service_job_info")
            self._flatten_prop(jd, "pool_info")

            self._upsert_record(dbx, "job_info", ws_name, _id, jd)

        # add to TAGS
        if tags or new_job:
            self._upsert_record(dbx, "job_tags", ws_name, _id, tags)

    def update_job_info_only(self, ws_name, job_id, jd):
        dbx = self._get_db(ws_name)
        _id = self._make_id(ws_name, job_id)

        self._upsert_record(dbx, "job_info", ws_name, _id, jd)

    # API call
    def create_request(self, ws_name, request_id, request_dict):
        dbx = self._get_db(ws_name)
        _id = self._make_id(ws_name, request_id)

        request_dict["create_time"] = time_utils.get_arrow_now_str()
        self._upsert_record(dbx, "requests", ws_name, _id, request_dict)
    
    def create_job_stats(self, ws_name, job_id):
        dbx = self._get_db(ws_name)
        _id = self._make_id(ws_name, job_id)

        job_stats = {"next_run_index": 0, "job_status": "created"}
        self._upsert_record(dbx, "job_stats", ws_name, _id, job_stats)
    
    # API call
    def get_info_for_nodes(self, ws_name, filter_dict, fields_dict, hide_empty_cols=None):
        # call common function
        records = self._get_info_for_nodes(ws_name, filter_dict, fields_dict, hide_empty_cols=hide_empty_cols)
        return records

    # API call
    def get_filtered_sorted_node_info(self, ws_name, filter_dict, fields_dict, sort_col=None, sort_dir=1, skip=None, 
            first=None, count_jobs=False, buffer_size=50, hide_empty_cols=None):

        # call common function
        records = self._get_info_for_nodes(ws_name, filter_dict, fields_dict, sort_col, sort_dir, skip, 
            first, count_jobs, buffer_size, hide_empty_cols=hide_empty_cols)
        return records

    # API call
    def get_filtered_sorted_request_info(self, ws_name, filter_dict, fields_dict, sort_col=None, sort_dir=1, skip=None, 
            first=None, count_jobs=False, buffer_size=50, hide_empty_cols=None):

        # call common function
        records = self._get_info_for_requests(ws_name, filter_dict, fields_dict, sort_col, sort_dir, skip, 
            first, count_jobs, buffer_size, hide_empty_cols=hide_empty_cols)
        return records

    def _get_info_for_nodes(self, ws_name, filter_dict, fields_dict, sort_col=None, sort_dir=1, skip=None, 
            first=None, count_jobs=False, buffer_size=50, hide_empty_cols=None):
        ''' 
        Processing:
            - this support queries on "node_info" with join to "node_stats" when needed.
        '''
        # make copies so we can modify them
        filter = dict(filter_dict) if filter_dict else None
        fields = dict(fields_dict) if fields_dict else None

        dbx = self._get_db(ws_name)
        need_dict = {}

        if not "ws_name" in filter:
            filter["ws_name"] = ws_name

        new_tags = {}
        tags = self._get_table_columns(dbx, "job_tags")

        self._add_node_info_col_aliases(filter, need_dict, tags, new_tags)
        self._add_node_info_col_aliases(fields, need_dict, tags, new_tags)
        
        if sort_col:
            sort_col = self._qualify_node_info_col(sort_col, need_dict, tags, new_tags)

        if fields:
            # add _id for easy of matching to service_info/connect_info 
            fields["A._id"] = 1

            col_list = self._build_col_str_in_groups(fields, [])   
        else:
            col_list = "A.*, B.*, '' as _T_, T.*"
            need_dict = {"A": 1, "B": 1, "T": 1}

        # need to add to cols to NODE_TAGS?
        if new_tags:
            self._add_new_cols_to_table(dbx, "node_tags", list(new_tags), new_tags, tags, force_vchar=True)

        middle = "FROM [dbo].[node_info] as A"

        if "B" in need_dict:
            middle += " LEFT JOIN [node_stats] as B ON A.[_id]=B.[_id]"

        if "T" in need_dict:
            middle += " LEFT JOIN [node_tags] as T ON A.[_id]=T.[_id]"

        if filter:
            where_str = self._build_where_from_filter(filter, add_brackets=False)
            middle += " " + where_str

        row_count = self.calc_row_count(dbx, middle)

        # build cmd
        top_str = "TOP {} ".format(first) if (first and not skip) else ""
        cmd = "SELECT {}{} {}".format(top_str, col_list, middle)

        if sort_col:
            cmd += " ORDER BY {}".format(sort_col)
            if sort_dir == -1:
                cmd += " DESC"

        if skip:
            cmd += " OFFSET {} ROWS".format(skip)

            if first:
                cmd += " FETCH NEXT {} rows only".format(first)

        records = self._execute_with_retry("_get_info_for_nodes", cmd=cmd, dbx=dbx, fetch_type="fetchall")

        grouping_dict = {"_T_": "tags"}
        docs = self._docs_from_records(records, group_markers=grouping_dict)

        if docs:
            # remove null columns from hparams, metrics, and tags
            self._remove_null_columns(docs, groups_only=True, hide_empty_cols=hide_empty_cols)

            # self._group_cols(docs, "_T_", None, "tags", ["job_id", "ws_name"], include_none=False)
                    
        return docs

    # API call
    def get_filtered_sorted_job_info(self, ws_name, filter_dict, fields_dict, sort_col=None, sort_dir=1, skip=None, 
            first=None, count_jobs=False, buffer_size=50, hide_empty_cols=None):
        '''
        Processing:
            1. get filtered and sorted job_id's, with support for filter and sort cols in related collections
            2. get specified fields for job_id's, with support for fields in related collections
        '''

        # call common function
        records = self._get_info_for_jobs(ws_name, filter_dict, fields_dict, sort_col, sort_dir, skip, 
            first, count_jobs, buffer_size, hide_empty_cols=hide_empty_cols)

        return records

    def get_info_for_requests(self, ws_name, filter_dict, fields_dict=None, hide_empty_cols=None):
        '''
        performs a query on single table "requests", using specified filter and fields.
        '''

        # call common function
        records = self._get_info_for_requests(ws_name, filter_dict, fields_dict, hide_empty_cols=hide_empty_cols)

        return records

    def _get_info_for_requests(self, ws_name, filter_dict, fields_dict, sort_col=None, sort_dir=1, skip=None, 
            first=None, count_jobs=False, buffer_size=50, hide_empty_cols=None):
        ''' 
        Processing:
            - this support queries on "requests".
        '''

        # make copies so we can modify them
        filter = dict(filter_dict) if filter_dict else None
        fields = dict(fields_dict) if fields_dict else None

        dbx = self._get_db(ws_name)
        need_dict = {}

        # xt expects that _id will always be returned
        if fields and not "_id" in fields:
            fields["_id"] = 1

        if not "ws_name" in filter:
            filter["ws_name"] = ws_name

        tags = self._get_table_columns(dbx, "requests_tags")
        new_tags = {}

        if sort_col:
            sort_col = self._qualify_requests_info_col(sort_col, None, need_dict, tags, new_tags)

        # need to add to cols to JOB_TAGS?
        if new_tags:
            self._add_new_cols_to_table(dbx, "job_tags", list(new_tags), new_tags, tags, force_vchar=True)

        if fields:
            # should look like: A.[run_name], B.[queue_duration], C.[lr], D.[test-acc]
            col_list = self._build_col_str_in_groups(fields, ["T"])   
        else:
            col_list = "*"
            # col_list = "'' as _T_, T.*"
            # need_dict = {"T": 1}

        top_str = "TOP {} ".format(first) if (first and not skip) else ""

        # build cmd
        cmd = "SELECT {}{} FROM [dbo].[requests] as A".format(top_str, col_list)

        if "T" in need_dict:
            cmd += " LEFT JOIN [requests_tags] as T ON A.[_id]=T.[_id]"

        if filter:
            where_str = self._build_where_from_filter(filter, add_brackets=False)
            cmd += " " + where_str

        if sort_col:
            cmd += " ORDER BY {}".format(sort_col)
            if sort_dir == -1:
                cmd += " DESC"

        if skip:
            cmd += " OFFSET {} ROWS".format(skip)

            if first:
                cmd += " FETCH NEXT {} rows only".format(first)

        #row_count = self.calc_row_count(dbx, middle)

        records = self._execute_with_retry("_get_info_for_requests", cmd=cmd, dbx=dbx, fetch_type="fetchall")

        grouping_dict = {"_T_": "tags"}
        docs = self._docs_from_records(records, group_markers=grouping_dict)

        if docs:
            # remove null columns from tags
            self._remove_null_columns(docs, groups_only=True, hide_empty_cols=hide_empty_cols)

        return docs

    def get_info_for_jobs(self, ws_name, filter_dict, fields_dict=None, hide_empty_cols=None):
        '''
        performs a query on single table "job_info", using specified filter and fields.
        '''

        # call common function
        records = self._get_info_for_jobs(ws_name, filter_dict, fields_dict, hide_empty_cols=hide_empty_cols)

        return records

    def _get_info_for_jobs(self, ws_name, filter_dict, fields_dict, sort_col=None, sort_dir=1, skip=None, 
            first=None, count_jobs=False, buffer_size=50, hide_empty_cols=None):
        ''' 
        Processing:
            - this support queries on "job_info" with join to "job_stats" when needed.
            
            - we do separate queries for "service_info" and "connect_info" because:
                - they are 1:many relation (avoid JOIN that duplicates repeated job_info data)
                - they are not involved in job filtering or sorting
        '''

        # make copies so we can modify them
        filter = dict(filter_dict) if filter_dict else None
        fields = dict(fields_dict) if fields_dict else None

        # split fields "service_info" and "connect_info" into their own queries
        # since they are 1:many AND we never filter/sort on their contents
        need_service_info = utils.safe_delete(fields, "service_info_by_node")
        need_connect_info = utils.safe_delete(fields, "connect_info_by_node")
        need_secrets_by_node = utils.safe_delete(fields, "secrets_by_node")
        need_runs_by_box = utils.safe_delete(fields, "runs_by_box")

        dbx = self._get_db(ws_name)
        need_dict = {}

        # xt expects that _id will always be returned
        if fields and not "_id" in fields:
            fields["_id"] = 1

        if not "ws_name" in filter:
            filter["ws_name"] = ws_name

        hparams = self._get_table_columns(dbx, "hparams")
        tags = self._get_table_columns(dbx, "job_tags")

        new_hparams = {}
        new_tags = {}

        self._add_job_info_col_aliases(filter, need_dict, hparams, tags, new_hparams, new_tags)
        self._add_job_info_col_aliases(fields, need_dict, hparams, tags, new_hparams, new_tags)
        
        if sort_col:
            sort_col = self._qualify_job_info_col(sort_col, None, need_dict, hparams, tags, new_hparams, new_tags)

        # need to add to cols to HPARAMS?
        if new_hparams:
            self._add_new_cols_to_table(dbx, "hparams", list(new_hparams), new_hparams, hparams, force_vchar=False)

        # need to add to cols to JOB_TAGS?
        if new_tags:
            self._add_new_cols_to_table(dbx, "job_tags", list(new_tags), new_tags, tags, force_vchar=True)

        if fields:
            # should look like: A.[run_name], B.[queue_duration], C.[lr], D.[test-acc]
            col_list = self._build_col_str_in_groups(fields, ["H", "T"])   
        else:
            col_list = "A.*, B.*, '' as _T_, T.*"
            need_dict = {"A": 1, "B": 1, "T": 1}


        # build cmd
        middle = "FROM [dbo].[job_info] as A"

        if "B" in need_dict:
            middle += " LEFT JOIN [job_stats] as B ON A.[_id]=B.[_id]"

        if "H" in need_dict:
            middle += " LEFT JOIN [hparams] as H ON A.[_id]=H.[_id]"

        if "T" in need_dict:
            middle += " LEFT JOIN [job_tags] as T ON A.[_id]=T.[_id]"

        if filter:
            where_str = self._build_where_from_filter(filter, add_brackets=False)
            middle += " " + where_str

        row_count = self.calc_row_count(dbx, middle)

        top_str = "TOP {} ".format(first) if (first and not skip) else ""
        cmd = "SELECT {}{} {}".format(top_str, col_list, middle)

        if sort_col:
            cmd += " ORDER BY {}".format(sort_col)
            if sort_dir == -1:
                cmd += " DESC"

        if skip:
            cmd += " OFFSET {} ROWS".format(skip)

            if first:
                cmd += " FETCH NEXT {} rows only".format(first)

        records = self._execute_with_retry("_get_info_for_jobs", cmd=cmd, dbx=dbx, fetch_type="fetchall")

        grouping_dict = {"_H_": "hparams", "_T_": "tags"}
        docs = self._docs_from_records(records, group_markers=grouping_dict)

        if docs:
            # self._group_cols(docs, "_H_", "_T_", "hparams", ["job_id", "ws_name"], include_none=False)
            # self._group_cols(docs, "_T_", None, "tags", ["job_id", "ws_name"], include_none=False)

            # remove null columns from hparams, metrics, and tags
            self._remove_null_columns(docs, groups_only=True, hide_empty_cols=hide_empty_cols)

            for doc in docs:
                self._adjust_job_record(dbx, doc, need_service_info, need_connect_info, 
                    need_secrets_by_node, need_runs_by_box) 

        return docs

    # API call
    def run_start(self, ws_name, run_name):
        '''
        A run has started running.  We need to:
            - set the run "start_time" property to NOW
            - set the run "queue_duration" property to NOW - created_time
        '''
        dbx = self._get_db(ws_name)
        run_restarted = False

        if self.update_run_stats_enabled:
            now = arrow.now()
            now_str = str(now)

            # fetch create_time of run
            _id = self._make_id(ws_name, run_name)
            records = self.get_info_for_runs(ws_name, {"_id": _id}, 
                {"create_time": 1, "queue_duration": 1, "restarts": 1, "end_id": 1})

            doc = records[0] if records else None
            create_time_str = utils.safe_value(doc, "create_time")
            queue_duration = utils.safe_value(doc, "queue_duration")
            restarts = utils.safe_value(doc, "restarts")
            end_id = utils.safe_value(doc, "end_id")

            # if queue_duration is non-zero, we have started this run previously
            run_restarted = (end_id is None) and (bool(queue_duration) or bool(restarts))
            if run_restarted:
                # increment the "restarts" field of run_stats
                restarts = 1 if restarts is None else restarts + 1
                console.print("===> RUN restart #{} detected: {} <======".format(restarts, run_name))

            if create_time_str:
                create_time = arrow.get(create_time_str)

                # compute time in "queue" 
                queue_duration = time_utils.time_diff(now, create_time)

            # update: start_time, queue_duration, restarts
            vd = {"start_time": now_str, "queue_duration": queue_duration, 
                "restarts": restarts, "status": "running", "db_retries": 0, 
                "storage_retries": 0} 

            # use upsert to be safe
            self._upsert_record(dbx, "run_stats", ws_name, _id, vd)

        return run_restarted

    # API call
    def get_restart_list(self, ws_name, job_id, node_index):
        '''
        The specified node has been restarted after being preempted.  Retrieve the list of run_indexes
        for the runs that were running on this node.  These runs will need to be restarted by the caller (XT Controller).
        '''
        filter = {"job_id": job_id, "node_index": node_index, "is_child": 1, "status": {"$nin": ["error", "cancelled", "completed", "restarted"]}}
        fields = {"run_index": 1, "ws_name": ws_name, "job_id": 1, "node_index": 1, "restarts": 1}

        runs = self.get_info_for_runs(ws_name, filter, fields)
        if runs:
            # ensure we got the correct runs
            for run in runs:
                assert run["job_id"] == job_id
                assert run["node_index"] == node_index
                assert run["ws_name"] == ws_name

        return runs

    # API call
    def update_run_stats_only(self, ws_name, run_name, rd):
        dbx = self._get_db(ws_name)
        _id = self._make_id(ws_name, run_name)

        self._upsert_record(dbx, "run_stats", ws_name, _id, rd)
            
    def update_run_steps(self, ws_name, run_name, step_dict):
        dbx = self._get_db(ws_name)
        _id = self._make_id(ws_name, run_name)

        self._upsert_record(dbx, "run_steps", ws_name, _id, step_dict)

    def get_largest_run_step(self, ws_name, run_name):
        dbx = self._get_db(ws_name)
        base_run_name = run_helper.get_base_run_name(run_name)

        query = "select max(step_num) from run_steps where ws_name = '{}' and base_run_name = '{}'".format(ws_name, base_run_name)

        record = self._execute_with_retry("get_run_steps", cmd=query, dbx=dbx, fetch_type="fetchone")
        run_steps = record[0]

        return run_steps

    def get_restarts_for_run(self, ws_name, base_run_name):
        dbx = self._get_db(ws_name)

        query = "select run_name from run_steps where ws_name = '{}' and base_run_name = '{}' and run_name != '{}'".   \
            format(ws_name, base_run_name, base_run_name)

        records = self._execute_with_retry("get_restarts_for_run", cmd=query, dbx=dbx, fetch_type="fetchall")
        restarts = [record[0] for record in records]
        
        return restarts

    def get_latest_activity_by_node(self, ws_name, job_id):
        '''
        gets the latest activity time for each run in the job (using run_name, not base_run_name).  Returns a dict of dicts.
        Outer dict key=node_index.  Inner dict key/value is run_name/last_time (as arrow object).
        '''
        dbx = self._get_db(ws_name)

        # pretty sure we cannot correctly find MAX(time) correctly in their arrow string forms, so do that in python
        query = "select run_name, time, node_id from run_steps where ws_name = '{}' and job_id = '{}'".format(ws_name, job_id)

        records = self._execute_with_retry("get_run_steps", cmd=query, dbx=dbx, fetch_type="fetchall")

        # group by node_id
        node_dict = {}
        for record in records:
            run_name, time_str, node_id = record
            node_index = utils.node_index(node_id)
            
            if not node_index in node_dict:
                node_dict[node_index] = {}

            inner_dict = node_dict[node_index]

            # convert time to an arrow object
            arrow_obj = time_utils.get_arrow_from_arrow_str(time_str)
            inner_dict[run_name] = arrow_obj

        return node_dict

    # API call
    def get_info_for_runs(self, ws_name, filter_dict, fields_dict=None, include_log_records=False):

        # call common method to handle
        records = self._get_info_for_runs(ws_name, filter_dict, fields_dict=fields_dict, 
            include_log_records=include_log_records)

        return records

    # API call
    def get_filtered_sorted_run_info(self, ws_name, filter_dict, fields_dict, sort_col=None, sort_dir=1, skip=None, 
        first=None, count_runs=False, buffer_size=50, hide_empty_cols=None):

        started = time.time()

        # call common method to handle
        records = self._get_info_for_runs(ws_name, filter_dict, fields_dict, sort_col=sort_col, sort_dir=sort_dir,
            skip=skip, first=first, count_runs=count_runs, buffer_size=buffer_size, hide_empty_cols=hide_empty_cols)

        elapsed = time.time() - started
        #console.print("  query elapsed: {:.2f} secs".format(elapsed))

        return records

    def _group_cols(self, docs, marker, stop_marker, nesting_name, cols_to_remove=[], include_none=False):

        # all_null_cols = {}

        for i, doc in enumerate(docs):
            if marker in doc:
                new_doc = {}
                nest_doc = {}
                found_marker = False

                for key, value in doc.items():
                    if key == marker:
                        found_marker = True
                        new_doc[nesting_name] = nest_doc
                        continue
                    elif key == stop_marker:
                        found_marker = False

                    if not found_marker or not key in cols_to_remove:
                        if value is None and not include_none:
                            continue

                        if found_marker and key != "_id":
                            # transfer col from target group to new doc
                            nest_doc[key] = value
                        else:
                            # transfer normal key/value to new doc
                            new_doc[key] = value

                # update doc with nd
                docs[i] = new_doc

        # # remove any col with all NULL values (this col was most likely never defined for this set of records)
        # # not knowing for sure is a limitation of the way we represent TAGS, HPARAMS, and METRICS
        # if all_null_cols:
        #     for i, doc in enumerate(docs):
        #         for key in all_null_cols:
        #             del doc[key]

    def _find_null_columns(self, docs, groups_only=True, hide_empty_cols=None):
        # find columns with all NULL values (at top level, and in dicts)
        # "groups_only" means we only consider columns in that appear in dictionary values 
        # or after # "_C_", "_D_", or "_T_" markers (hparams, metrics, tags)
        all_null_cols = {}
        in_group = False

        for doc in docs:
            for col, value in doc.items():
                if col in ["_C_", "_D_", "_T_"]:
                    # start of a group set of columns
                    in_group = True
                elif len(col) == 3 and col[0] == "_" and col[2] == "_":
                    # start of a non-group set of columns
                    in_group = False

                if isinstance(value, dict):
                    # DICT (group) of values
                    for c,v in value.items():
                        cname = col + "." + c
                        if v is None:
                            if cname not in all_null_cols:
                                all_null_cols[cname] = 1
                        else:
                            # overwrite the all_null flag for this column
                            all_null_cols[cname] = 0

                elif not groups_only or in_group or (hide_empty_cols and col in hide_empty_cols):
                    # top level value
                    if value is None:
                        if col not in all_null_cols:
                            all_null_cols[col] = 1
                    else:
                        # overwrite the all_null flag for this column
                        all_null_cols[col] = 0

        return all_null_cols

    def _remove_null_columns(self, docs, groups_only=True, hide_empty_cols=None):
        # remove any col with all NULL values (this col was most likely never defined for this set of records)
        # not knowing for sure is a limitation of the way we represent TAGS, HPARAMS, and METRICS
        all_null_cols = self._find_null_columns(docs, groups_only, hide_empty_cols=hide_empty_cols)

        for i, doc in enumerate(docs):
            for key, value in all_null_cols.items():
                if value:

                    if "." in key:
                        group, col = key.split(".", 1)
                        del doc[group][col]

                    else:
                        del doc[key]

    def _get_info_for_runs(self, ws_name, filter_dict, fields_dict, sort_col=None, sort_dir=1, skip=None, 
        first=None, count_runs=False, buffer_size=50, include_log_records=False, hide_empty_cols=None):
        '''
        Processing:
            - query run_info as primary table.  use LEFT JOIN to include fields from other tables:
                - run_stats, hparams, metrics, tags
            - optionally, read related log_records from Azure storage.

            NOTE: to allow us to gather metrics, hpaams, and tags cols from returned results, group all cols
            in the SELECT clause by their annotation (A/B/C/D) and then we add _C_, _D_, and _E_  
            separator cols to the query 
        '''

        dbx = self._get_db(ws_name)
        need_dict = {}

        # this is used to return row_count of available records for first/last queries
        self.avail_row_count = None

        # make copies so we can modify them
        filter = dict(filter_dict) if filter_dict else None
        fields = dict(fields_dict) if fields_dict else None

        # xt expects that _id will always be returned
        if fields and not "_id" in fields:
            fields["_id"] = 1

        # we limit all queries to a single ws_name (for now)
        if not "ws_name" in filter:
            filter["ws_name"] = ws_name

        hparams = self._get_table_columns(dbx, "hparams")
        metrics = self._get_table_columns(dbx, "metrics")
        tags = self._get_table_columns(dbx, "run_tags")
        
        new_hparams = {}
        new_metrics = {}
        new_tags = {}

        # process cols in FILTER
        self._add_run_info_col_aliases(filter, need_dict, hparams, metrics, tags, new_hparams, new_metrics, new_tags)

        # process cols in FIELDS
        self._add_run_info_col_aliases(fields, need_dict, hparams, metrics, tags, new_hparams, new_metrics, new_tags)
        
        if sort_col:
            sort_col = self._qualify_run_info_col(sort_col, None, need_dict, hparams, metrics, tags, new_hparams, new_metrics, new_tags)

        # need to add to cols to HPARAMS?
        if new_hparams:
            self._add_new_cols_to_table(dbx, "hparams", list(new_hparams), new_hparams, hparams, force_vchar=False)

        # need to add to cols to METRICS?
        if new_metrics:
            self._add_new_cols_to_table(dbx, "metrics", list(new_metrics), new_metrics, metrics, force_vchar=False)

        # need to add to cols to RUN_TAGS?
        if new_tags:
            self._add_new_cols_to_table(dbx, "run_tags", list(new_tags), new_tags, tags, force_vchar=True)

        if fields:
            # should look like: A.[run_name], B.[queue_duration], C.[lr], D.[test-acc]
            col_list = self._build_col_str_in_groups(fields, ["C", "D", "T"])   
        else:
            col_list = "A.*, B.*, '' as _C_, C.*, '' as _D_, D.*, '' as _T_, T.*"
            need_dict = {"A": 1, "B": 1, "C": 1, "D": 1, "T": 1}

        # use TOP when possible (doesn't require ORDER BY)
        top_str = ""
        offset_part = ""

        if skip:
            if not sort_col:
                errors.internal_error("SKIP option cannot be used with SORT for odbc database")

            offset_part += " OFFSET {} ROWS".format(skip)
            if first:
                offset_part += " FETCH NEXT {} rows only".format(first)
        elif first:
            top_str = "TOP {} ".format(first)

        # build cmd
        middle = " FROM [dbo].[run_info] as A"

        if "B" in need_dict:
            middle += " LEFT JOIN [run_stats] as B ON A.[_id]=B.[_id]"

        if "C" in need_dict:
            middle += " LEFT JOIN [hparams] as C ON A.[_id]=C.[_id]"

        if "D" in need_dict:
            middle += " LEFT JOIN [metrics] as D ON A.[_id]=D.[_id]"

        if "T" in need_dict:
            middle += " LEFT JOIN [run_tags] as T ON A.[_id]=T.[_id]"

        if filter:
            where_str = self._build_where_from_filter(filter, add_brackets=False)
            middle += " " + where_str

        if sort_col:
            end = " ORDER BY {}".format(sort_col)
            if sort_dir == -1:
                end += " DESC"
        else:
            end = ""

        select = "SELECT {}{}".format(top_str, col_list)
        query = select + middle + end
        sync_query = pc_utils.is_compute_node() or ("A.[_id]" in filter or (first and first <= self.chunk_size))

        row_count = self.calc_row_count(dbx, middle)

        if not sync_query:
            if row_count is None:
                row_count = self._get_row_count(dbx, middle, first)
            elif first:
                row_count = min(row_count, first)

        if not sync_query:
            if row_count <= self.chunk_size:
                sync_query = True

        if sync_query:
            query += offset_part

            records = self._execute_with_retry("_get_info_for_runs", cmd=query, dbx=dbx, fetch_type="fetchall")
            
            grouping_dict = {"_C_": "hparams", "_D_": "metrics", "_T_": "tags"}
            docs = self._docs_from_records(records, group_markers=grouping_dict)

        else:
            if top_str:
                # cannot use TOP in async/chunking query
                top_str = ""
                select = "SELECT {}{}".format(top_str, col_list)
                query = select + middle + end
                
            # for use of SQL "OFFSET" clause, we must have an "order by" clause
            if not sort_col:
                query += " order by A.[run_num]"
            docs = self._run_query_workers(dbx, row_count, query, skip)

        # pull flattened cols into nested dict's
        # self._group_cols(docs, "_C_", "_D_", "hparams")
        # self._group_cols(docs, "_D_", "_T_", "metrics")
        # self._group_cols(docs, "_T_", None, "tags", ["run_name", "ws_name"], include_none=False)
        
        # remove null columns from hparams, metrics, and tags
        self._remove_null_columns(docs, groups_only=True, hide_empty_cols=hide_empty_cols)

        if "E" in need_dict or include_log_records:
            console.diag("reading log records...")

            id_list = [doc["_id"] for doc in docs]
            log_records = self.store.get_log_records_for_runs(ws_name, id_list)

            console.diag("calling _join_log_records")
            self._join_log_records(docs, log_records)

        for doc in docs:
            self._inflate_prop(doc, "metric_names")

        return docs

    def calc_row_count(self, dbx, middle):
        return_row_count = True
        row_count = None

        if return_row_count:
            row_count = self._get_row_count(dbx, middle)
            self.avail_row_count = row_count        # for later access by caller (don't want change API to pass to this)

        return row_count

    def _get_row_count(self, dbx, middle, first=None):
        # get query row count
        count_query = "select count(*) " + middle
        rc_started = time.time()

        record = self._execute_with_retry("_get_info_for_runs", cmd=count_query, dbx=dbx, fetch_type="fetchone")
        row_count = record[0]
        if first:
            row_count = min(row_count, first)
        rc_elapsed = time.time() - rc_started
        console.diag("  row_count query: {:.2f} secs".format(rc_elapsed))

        return row_count

    def _run_query_workers(self, dbx, row_count, query, skip):

        # run small queries on bg threads for max speed
        worker_lock = Lock()
        next_progress_num = 1
        results_by_chunk = []
        fb.feedback("  retrieving {:,} rows from database".format(row_count))

        # build offset_list
        if skip is None:
            skip = 0

        offset = skip
        last_offset = skip + row_count - 1

        offset_list = []
        while offset <= last_offset:
            count = min(last_offset-offset+1, self.chunk_size)
            offset_list.append([offset, count])
            offset += count

        def thread_worker(offsets, query):

            for offset, count in offsets:

                cmd = query
                cmd += " OFFSET {} ROWS".format(offset)
                cmd += " FETCH NEXT {} rows only".format(count)

                records = self._execute_with_retry("_run_query_workers__b", cmd=cmd, dbx=dbx, fetch_type="fetchall")

                grouping_dict = {"_C_": "hparams", "_D_": "metrics", "_T_": "tags"}
                docs = self._docs_from_records(records, grouping_dict)

                with worker_lock:
                    nonlocal results_by_chunk, next_progress_num

                    chunk_num = offset//self.chunk_size
                    tup = (chunk_num, docs)
                    results_by_chunk.append(tup)

                    worker_msg = "gathering query chunks: {}/{}".format(next_progress_num, len(offset_list))
                    fb.feedback(worker_msg, id="gather_msg")  
                    next_progress_num += 1

        utils.run_on_threads(thread_worker, offset_list, self.max_query_workers, [query])
        fb.feedback("done", is_final=True)

        # sort results by ascending chunk number (restore user-specified order)
        results_by_chunk.sort(key=lambda tup: tup[0])

        # flatten results_by_check into a single list
        all_docs = [doc for tup in results_by_chunk for doc in tup[1]]
        return all_docs

    def _qualify_run_info_col(self, col, value, need_dict, hparams, metrics, tags, new_hparams, new_metrics, new_tags):
        '''
        Processing:
            qualify run_info col with one of the following prefixes:
                A.  (for run_info table)
                B.  (for run_stats table)
                C.  (for hparams table)
                D.  (for metrics table)
                E.  (for log records)
                T.  (for tags)
        '''
        if col in run_helper.run_info_props:
            col = "A.[{}]".format(col)
            need_dict["A"] = 1
        elif col == "run_info":
            col = "A.*"
            need_dict["A"] = 1

        elif col in run_helper.run_stats_props:
            col = "B.[{}]".format(col)
            need_dict["B"] = 1
        elif col == "run_stats":
            col = "B.*"
            need_dict["B"] = 1

        elif col.startswith("hparams."):
            raw_col = col[8:]   # strip off "hparams."
            col = "C.[{}]".format(raw_col)

            if not raw_col in hparams:
                new_hparams[raw_col] = FLOAT
            need_dict["C"] = 1

        elif col == "hparams":
            col = "C.*".format(col)
            need_dict["C"] = 1

        elif col.startswith("metrics."):
            raw_col = col[8:]   # strip off "metrics."
            col = "D.[{}]".format(raw_col)

            if not raw_col in metrics:
                new_metrics[raw_col] = FLOAT
            need_dict["D"] = 1

        elif col == "metrics":
            col = "D.*".format(col)
            need_dict["D"] = 1

        elif col == "log_records":
            col = None
            need_dict["E"] = 1

        elif col.startswith("tags."):
            raw_col = col[5:]   # strip off "tags."
            col = "T.[{}]".format(raw_col)

            if not raw_col in tags:
                new_tags[raw_col] = VARCHAR
            need_dict["T"] = 1

        elif col == "tags":
            col = "T.*".format(col)
            need_dict["T"] = 1

        elif col == "$or":
            # value is a list of dict
            # recusively call on each col/value of element dict
            for elem_dict in value:
                ed = dict(elem_dict)    # make a copy to iterate with as orig is changed
                for key, value in ed.items():
                    qcol = self._qualify_job_info_col(key, value, need_dict, hparams, tags, new_hparams, new_tags)
                    utils.rename_dict_key(elem_dict, key, qcol)

        elif col == "$and":
            # value is a list of dict
            # recusively call on each col/value of element dict
            for elem_dict in value:
                ed = dict(elem_dict)    # make a copy to iterate with as orig is changed
                for key, value in ed.items():
                    qcol = self._qualify_job_info_col(key, value, need_dict, hparams, tags, new_hparams, new_tags)
                    utils.rename_dict_key(elem_dict, key, qcol)

        else:
            errors.internal_error("unrecognized column name for run_info (or related table): {}".format(col))
        
        return col

    def _add_run_info_col_aliases(self, fd, need_dict, hparams, metrics, tags, new_hparams, new_metrics, new_tags):
        '''
        "fd" can be either a fields dict or a filter dict.  Find each 
        col name and replace it with the qualified alias name.
        '''

        if fd:
            keys = list(fd)   # capture full list before modifying dict
            for key in keys:
                value = fd[key]
                qkey = self._qualify_run_info_col(key, value, need_dict, hparams, metrics, tags, new_hparams, new_metrics, new_tags)
                del fd[key]
                if qkey:
                    fd[qkey] = value

    def _add_node_info_col_aliases(self, fd, need_dict, tags, new_tags):
        '''
        "fd" can be either a fields dict or a filter dict.  Find each 
        col name and replace it with the qualified alias name.
        '''

        if fd:
            keys = list(fd)   # capture full list before modifying dict
            for key in keys:
                value = fd[key]
                qkey = self._qualify_node_info_col(key, need_dict, tags, new_tags)
                del fd[key]
                if qkey:
                    fd[qkey] = value

    def _qualify_node_info_col(self, col, need_dict, tags, new_tags):
        '''
        Processing:
            qualify node_info col with one of the following prefixes:
                A.  (for node_info table)
                B.  (for node_stats table)
                T.  (for node_tags table)
        '''
        if col in node_helper.node_info_props:
            col = "A.[{}]".format(col)
            need_dict["A"] = 1

        elif col in node_helper.node_stats_props:
            col = "B.[{}]".format(col)
            need_dict["B"] = 1

        elif col == "tags":
            col = "T.*"
            need_dict["T"] = 1

        elif col.startswith("tags."):
            raw_col = col[5:]   # strip off the "tags."
            col = "T.[{}]".format(raw_col)
            if not raw_col in tags:
                new_tags[raw_col] = VARCHAR
            need_dict["T"] = 1

        else:
            errors.internal_error("unrecognized node_info (or related table) col: {}".format(col))
        
        return col

    def _qualify_requests_info_col(self, col, value, need_dict, tags, new_tags):
        '''
        Args:
            - col: the name of the column being qualfied
            - value: if col was found in a filter_dict, this is the value associated with the col
            - need_dict: possible keys are "T" (track if associated table is needed in query)
            - tags: dict of existing col names in tags table
            - new_tags: dict of col names to be added to tags table

        Processing:
            qualify job_info col with one of the following prefixes:
                T.  (for job_tags table)
        '''

        if col == "tags":
            col = "T.*"
            need_dict["T"] = 1

        elif col in request_helper.request_info_props:
            col = "A.[{}]".format(col)
            need_dict["A"] = 1

        elif col.startswith("tags."):
            raw_col = col[5:]   # strip off the "tags."
            col = "T.[{}]".format(raw_col)
            if not raw_col in tags:
                new_tags[raw_col] = VARCHAR
            need_dict["T"] = 1

        elif col == "$or":
            # value is a list of dict
            # recusively call on each col/value of element dict
            for elem_dict in value:
                ed = dict(elem_dict)    # make a copy to iterate with as orig is changed
                for key, value in ed.items():
                    qcol = self._qualify_requests_info_col(key, value, need_dict, tags, new_tags)
                    utils.rename_dict_key(elem_dict, key, qcol)

        elif col == "$and":
            # value is a list of dict
            # recusively call on each col/value of element dict
            for elem_dict in value:
                ed = dict(elem_dict)    # make a copy to iterate with as orig is changed
                for key, value in ed.items():
                    qcol = self._qualify_requests_info_col(key, value, need_dict, tags, new_tags)
                    utils.rename_dict_key(elem_dict, key, qcol)

        else:
            errors.internal_error("unrecognized requests col: {}".format(col))
        
        return col

    def _qualify_job_info_col(self, col, value, need_dict, hparams, tags, new_hparams, new_tags):
        '''
        Args:
            - col: the name of the column being qualfied
            - value: if col was found in a filter_dict, this is the value associated with the col
            - need_dict: possible keys are "A", "B", "H", "T" (track if associated table is needed in query)
            - hparams: dict of existing col names in hparams table
            - tags: dict of existing col names in tags table
            - new_hparams: dict of col names to be added to hparams table
            - new_tags: dict of col names to be added to tags table

        Processing:
            qualify job_info col with one of the following prefixes:
                A.  (for job_info table)
                B.  (for job_stats table)
                H.  (for hparams table)
                T.  (for job_tags table)
        '''
        if col == "job_info":
            col = "A.*"
            need_dict["A"] = 1

        elif col in job_helper.job_info_props:
            col = "A.[{}]".format(col)
            need_dict["A"] = 1

        elif col == "job_stats":
            col = "B.*"
            need_dict["B"] = 1

        elif col in job_helper.job_stats_props:
            col = "B.[{}]".format(col)
            need_dict["B"] = 1

        elif col == "hparams":
            col = "H.*"
            need_dict["H"] = 1

        elif col.startswith("hparams."):
            raw_col = col[8:]   # strip off the "hparams."
            col = "H.[{}]".format(raw_col)
            if not raw_col in hparams:
                new_hparams[raw_col] = VARCHAR
            need_dict["H"] = 1

        elif col == "tags":
            col = "T.*"
            need_dict["T"] = 1

        elif col.startswith("tags."):
            raw_col = col[5:]   # strip off the "tags."
            col = "T.[{}]".format(raw_col)
            if not raw_col in tags:
                new_tags[raw_col] = VARCHAR
            need_dict["T"] = 1

        elif col == "$or":
            # value is a list of dict
            # recusively call on each col/value of element dict
            for elem_dict in value:
                ed = dict(elem_dict)    # make a copy to iterate with as orig is changed
                for key, value in ed.items():
                    qcol = self._qualify_job_info_col(key, value, need_dict, hparams, tags, new_hparams, new_tags)
                    utils.rename_dict_key(elem_dict, key, qcol)

        elif col == "$and":
            # value is a list of dict
            # recusively call on each col/value of element dict
            for elem_dict in value:
                ed = dict(elem_dict)    # make a copy to iterate with as orig is changed
                for key, value in ed.items():
                    qcol = self._qualify_job_info_col(key, value, need_dict, hparams, tags, new_hparams, new_tags)
                    utils.rename_dict_key(elem_dict, key, qcol)

        else:
            errors.internal_error("unrecognized job_info (or related table) col: {}".format(col))
        
        return col

    def _add_job_info_col_aliases(self, fd, need_dict, hparams, tags, new_hparams, new_tags):
        '''
        "fd" can be either a fields dict or a filter dict.  Find each 
        col name and replace it with the qualified alias name.
        '''

        if fd:
            keys = list(fd)   # capture full list before modifying dict
            for key in keys:
                value = fd[key]
                qkey = self._qualify_job_info_col(key, value, need_dict, hparams, tags, new_hparams, new_tags)
                utils.rename_dict_key(fd, key, qkey)

    def _join_log_records(self, records, log_recs):
        # build a dict to quickly find records
        rd = {r["_id"]: r for r in records}

        # create a list property on each record
        for record in records:
            record["log_records"] = []

        # add each log_rec to associated record
        for log in log_recs:
            id = log["key"]
            if id in rd:
                record = rd[id]

                # fixup log record
                del log["_id"] 
                del log["key"]

                if "data" in log:
                    data = log["data"]
                    if "_id" in data:
                        del data["_id"]

                # add to record
                record["log_records"].append(log)

    def _build_where_from_run_list(self, run_list):
        filter = ""

        for obj_name in run_list:
            if filter:
                filter += " or " 
            else:
                filter += " where "

            if run_helper.is_run_name(obj_name):
                filter += "[run_info].[run_name] = '{}'".format(obj_name)

            elif node_helper.is_node_name(obj_name):
                filter += "[run_info].[node_id] = '{}'".format(obj_name)

            elif job_helper.is_job_id(obj_name):
                filter += "[run_info].[job_id] = '{}'".format(obj_name)

            else:
                errors.user_error("name must be a job, node, or run name: {}".format(obj_name))
            
        return filter

    # API call
    def get_group_query_run_names(self, ws_id, run_list, group_by, agg_name, sort_col, first, last):
        '''
        Used to quickly fetch a set of run_names corresponding to a limited number of aggregation results (e.g., grouping runs by hp_set, averaging one of their metrics, 
        limiting aggregated scores to first/last 10, and then returning all of the run_names that comprised those 10 results.  This is super quick for SQL to do and 
        gives our plot or list runs report a jumpstart.
        '''
        dbx = self._get_db(ws_id)
        sql_cmd = "select"
        
        if first:
            sql_cmd += " top {}".format(first)
        elif last:
            sql_cmd += " top {}".format(last)

        sql_cmd += " count(*) as count, {}(metrics.[{}]) as avg_score, STRING_AGG (run_info.run_name, ',') AS run_names".format(agg_name, sort_col)
        sql_cmd += " from run_info"
        # get group_by from correct table
        if group_by.startswith("hparams."):
            group_by = group_by.split(".")[1]
            #sql_cmd += " hparams.{} from hparams".format(group_by)
            sql_cmd += " inner join metrics on run_info._id = metrics._id"
            sql_cmd += " inner join hparams on run_info._id = hparams._id"
            sql_cmd += self._build_where_from_run_list(run_list)
            sql_cmd += " group by hparams.{} order by avg_score".format(group_by)
        else:
            #sql_cmd += " run_info.{} from run_info".format(group_by)
            sql_cmd += " inner join metrics on run_info._id = metrics._id"
            sql_cmd += self._build_where_from_run_list(run_list)
            sql_cmd += " group by run_info.{} order by avg_score".format(group_by)

        if last:
            sql_cmd += " desc"

        records = self._execute_with_retry("get_group_query_run_names", cmd=sql_cmd, dbx=dbx, fetch_type="fetchall")

        # run_names are in tuple[2]
        run_names = [record[2] for record in records]

        # flatten into a single list of run_names
        flat_run_names = ",".join(run_names)

        # make a true list
        run_names_list = flat_run_names.split(",")

        return run_names_list 

    # API call
    def job_run_start(self, ws_name, job_id):
        '''
        A job's run has started running.  We need to:
            - increment the job's "running_runs" property 
        '''
        if self.update_job_stats_enabled:
            dbx = self._get_db(ws_name)
            _id = self._make_id(ws_name, job_id)

            cmd = "UPDATE [job_stats] SET"
            cmd += " [running_runs] = [running_runs] + 1" 
            cmd += " WHERE [_id] = '{}' ".format(_id)

            self._execute_with_retry("job_run_start", cmd=cmd, dbx=dbx)

    # API call
    def job_run_exit(self, ws_name, job_id, exit_code, run_was_started=True):
        '''
        A job's run has finished running.  We need to:
            - decrement the job's "running_runs" property 
            - increment the job's "completed_runs" property
            - if exit_code != 0, increment the job's "error_runs" property
        '''
        if self.update_job_stats_enabled:
            dbx = self._get_db(ws_name)
            _id = self._make_id(ws_name, job_id)

            if run_was_started:
                cmd = "UPDATE [job_stats] SET"
                cmd += " [running_runs] = iif([running_runs] - 1 < 0, 0, [running_runs] - 1)" 
                cmd += ", [completed_runs] = [completed_runs] + 1"

                if exit_code:
                    cmd += ", [error_runs] = [error_runs] + 1"
                    
                cmd += " WHERE [_id] = '{}' ".format(_id)

                self._execute_with_retry("job_run_exit", cmd=cmd, dbx=dbx)

    # API call
    def update_job_stats(self, ws_name, job_id, data_dict):
        dbx = self._get_db(ws_name)
        id = self._make_id(ws_name, job_id)

        self._update_record(dbx, "job_stats", ws_name, id, data_dict)

    # API call
    def update_node_stats(self, ws_name, job_id, node_index, data_dict):
        dbx = self._get_db(ws_name)
        id = self._make_node_id(ws_name, job_id, node_index)

        self._update_record(dbx, "node_stats", ws_name, id, data_dict)

    # API call
    def node_run_start(self, ws_name, job_id, node_index):
        '''
        A node's run has started running.  We need to:
            - increment the node's "running_runs" property 
        '''
        if self.update_node_stats_enabled:
            dbx = self._get_db(ws_name)
            _id = self._make_node_id(ws_name, job_id, node_index)

            cmd = "UPDATE [node_stats] SET"
            cmd += " [running_runs] = [running_runs] + 1" 
            cmd += " WHERE [_id] = '{}' ".format(_id)

            self._execute_with_retry("node_run_start", cmd=cmd, dbx=dbx)

    # API call
    def node_run_end(self, ws_name, job_id, node_index, exit_code, run_was_started=True):
        '''
        A node's run has finished running.  We need to:
            - decrement the node's "running_runs" property 
            - increment the node's "completed_runs" property
            - if exit_code != 0, increment the node's "error_runs" property
        '''
        if self.update_node_stats_enabled:
            dbx = self._get_db(ws_name)
            _id = self._make_node_id(ws_name, job_id, node_index)

            if run_was_started:
                cmd = "UPDATE [node_stats] SET"
                cmd += " [running_runs] = iif([running_runs] - 1 < 0, 0, [running_runs] - 1)" 
                cmd += ", [completed_runs] = [completed_runs] + 1"

                if exit_code:
                    cmd += ", [error_runs] = [error_runs] + 1"
                    
                cmd += " WHERE [_id] = '{}' ".format(_id)

                self._execute_with_retry("node_run_end", cmd=cmd, dbx=dbx)

    # API call
    def job_node_start(self, ws_name, job_id, node_index, is_restart):
        '''
        A job's node has started running. 

        Processing:
            if is_restart:
                - increment job's RESTART count
            else:
                - increment the job's "running_nodes" property
           set the "job_status" property to "running"
        '''
        dbx = self._get_db(ws_name)

        if self.update_job_stats_enabled:
            _id = self._make_id(ws_name, job_id)

            if is_restart:
                cmd = "UPDATE [job_stats] SET"
                cmd += " [restarts] = [restarts] + 1"
            else:
                cmd = "UPDATE [job_stats] SET"
                cmd += " [running_nodes] = [running_nodes] + 1"

            cmd += ", [job_status] = 'running'"
            cmd += " OUTPUT DELETED.[job_status]"
            cmd += " WHERE [_id] = '{}' ".format(_id)

            output_record = self._execute_with_retry("job_node_start", cmd=cmd, dbx=dbx, fetch_type="fetchone")
            
            console.print("job_node_start: output_record={}".format(output_record))
            old_status = output_record[0]
            console.print("job_node_start: old_status={}".format(old_status))

            # was this the first node to start on this job?
            if old_status == "submitted":
                self.mark_job_started_running(ws_name, job_id)

    def execute_sql_command(self, workspace, cmd, called_from_name, fetch_type=None):
        dbx = self._get_db(workspace)

        output_record = self._execute_with_retry(called_from_name, cmd=cmd, dbx=dbx, fetch_type=fetch_type)
        return output_record

    # API call
    def mark_job_started_running(self, ws_name, job_id):
        dbx = self._get_db(ws_name)
        _id = self._make_id(ws_name, job_id)

        console.print("job_node_start: first node to start job: {}".format(job_id))

        rd = {}
        run_start_time = time_utils.get_arrow_now_str()
        rd["run_started"] = run_start_time

        # compute run_duration (need to fetch started from job_info)
        records = self._query(dbx, "job_info", {"_id": _id}, {"started": 1})
        doc = records[0] if records else None
        if doc and "started" in doc:
            started_time = doc["started"]
            queue_duration = time_utils.get_time_from_arrow_str(run_start_time) - time_utils.get_time_from_arrow_str(started_time)
            rd["queue_duration"] = queue_duration
                                                                            
        self._update_record(dbx, "job_stats", ws_name, _id, rd)

    # API call
    def job_node_exit(self, ws_name, job_id):
        '''
        A job's node has finished running.  We need to:
            - decrement the job's "running_nodes" property 
            - if running_nodes==0, set the "job_status" property to "completed"
        '''
        dbx = self._get_db(ws_name)
        job_completed = False
        result2 = None

        if self.update_job_stats_enabled:
            _id = self._make_id(ws_name, job_id)

            cmd = "UPDATE [job_stats] SET"
            cmd += " [running_nodes] = iif([running_nodes] - 1 < 0, 0, [running_nodes] - 1)"
            cmd += " OUTPUT INSERTED.[running_nodes]"
            cmd += " WHERE [_id] = '{}' ".format(_id)

            record = self._execute_with_retry("job_node_exit__a", cmd=cmd, dbx=dbx, fetch_type="fetchone")
            running_nodes = record[0]
    
            job_completed = (running_nodes == 0)
            if job_completed:
                self.mark_job_completed(ws_name, job_id, "completed", run_started=None, end_time=None, zero_counts=True)

            console.diag("job_node_exit: job_completed={}".format(job_completed))

        return job_completed
    
    # API call
    def mark_node_cancelled(self, ws_name, job_id, node_index):
        '''
        A NODE has been cancelled:
            - set status to "cancelled"
            - set running_runs to 0
        '''
        dbx = self._get_db(ws_name)

        if self.update_job_stats_enabled:
            _id = self._make_node_id(ws_name, job_id, node_index)
            now = arrow.now()
            now_str = str(now)

            cmd = "UPDATE [node_stats] SET"
            cmd += " [running_runs] = 0, "
            cmd += " [node_status] = 'cancelled'"
            #cmd += " [end_time] = '{}'".format(now_str)               # end_time not defined for node_stats
            cmd += " WHERE [_id] = '{}' ".format(_id)

            record = self._execute_with_retry("mark_node_cancelled", cmd=cmd, dbx=dbx)

            console.diag("mark_node_cancelled")

    # API call
    def mark_job_completed(self, ws_name, job_id, status, run_started, end_time, zero_counts):
        '''
        A job has completed.  We need to:
            - set the "job_status" property to one of: "completed", "cancelled", "error"
            - set the "end_time" property to the current time
            - set the "run_duration" property to the difference between the run_started and end_time
            - zero the "running_nodes" property
            - zero the "running_runs" property
        '''
        if self.update_job_stats_enabled:
            dbx = self._get_db(ws_name)
            _id = self._make_id(ws_name, job_id)

            if not end_time:
                end_time = time_utils.get_arrow_now_str()

            jd = {}
            jd["job_status"] = status
            jd["end_time"] = end_time

            # compute run_duration 
            if not run_started:
                records = self._query(dbx, "job_stats", {"_id": _id}, {"run_started": 1})
                doc = records[0] if records else None
                if doc and "run_started" in doc:
                    run_started = doc["run_started"]

            if run_started:
                start_time_secs = time_utils.get_time_from_arrow_str(run_started)
                end_time_secs = time_utils.get_time_from_arrow_str(end_time) if end_time else time.time()
                run_duration = end_time_secs - start_time_secs
                jd["run_duration"] = run_duration

            if zero_counts:
                jd["running_nodes"] = 0
                jd["running_runs"] = 0

            self._update_record(dbx, "job_stats", ws_name, _id, jd, ensure_record_found=False)
        
    # API call
    def mark_job_ended_in_past(self, ws_name, job_id, status, job_info, end_time_secs, new_completed_runs, new_error_runs):
        '''
        A JOB has been cancelled or terminated in error in the past:
            - set status
            - set running_runs, etc. to 0
        '''
        if self.update_job_stats_enabled:
            dbx = self._get_db(ws_name)
            _id = self._make_id(ws_name, job_id)

            rd = {"job_status": status, "running_runs": 0, "running_nodes": 0}

            if new_completed_runs is not None and new_completed_runs > 0:
                rd["completed_runs"] = job_info["completed_runs"] + new_completed_runs

            if new_error_runs is not None and new_error_runs> 0:
                rd["error_runs"] = job_info["error_runs"] + new_error_runs

            started = job_info["started"]
            run_started = job_info["run_started"]

            if end_time_secs:

                if run_started:
                    # compute run_duration 
                    start_time_secs = time_utils.get_time_from_arrow_str(run_started)
                    run_duration = end_time_secs - start_time_secs
                    rd["run_duration"] = run_duration

                    # set end_time
                    end_time = time_utils.get_arrow_str_from_time(end_time_secs)
                    rd["end_time"] = end_time

                else:
                    # compute queue_duration
                    create_time_secs = time_utils.get_time_from_arrow_str(started)

                    # ensure we don't have a negative queue_duration (since end_time is estimated here)
                    if end_time_secs < create_time_secs:
                        end_time_secs = create_time_secs + 60

                    queue_duration = end_time_secs - create_time_secs
                    rd["queue_duration"] = queue_duration

            self._update_record(dbx, "job_stats", ws_name, _id, rd, ensure_record_found=False)
    

    # API call
    def create_db_run(self, rd):
        ws_name = rd["ws_name"]
        run_name = rd["run_name"]

        self.update_run_info(ws_name, run_name, rd, update_primary=True, new_run=True)
        
    # API call
    def update_run_info(self, ws_name, run_name, orig_dd, hparams=None, metrics=None, 
        update_primary=False, new_run=False, update_last_time=True):
        '''
        Args:
            - ws_name: name of the associated workspace
            - run_name: name of the run being updated
            - orig_dd: a dictionary of name/value pairs.  Can include nested: hparams, metrics, tags, log_records
            - hparams dict (optional, usually passed in orig_dd)
            - metrics dict (optional, usually passed in orig_dd)
            - update_primary: specifies if the run_info collection be updated

        Processing:
            This is the CORE function for updating run related information.  The following 
            collections may be updated: run_info, run_stats, metrics, hparams, tags

            In order for the run_info collection to be updated, update_primary must = True.
        '''
        dbx = self._get_db(ws_name)
        dd = dict(orig_dd)      # make copy so we can modify

        # we use upsert to add info, but we can skip the insert step when it is new_run=False
        skip_insert = not new_run

        # normalize nested info, if present
        if not hparams:
            hparams = {}
            utils.safe_move(hparams, dd, "hparams", flatten=True)

        if not metrics:
            metrics = {}
            utils.safe_move(metrics, dd, "metrics", flatten=True)

        tags = {"run_name": run_name}
        utils.safe_move(tags, dd, "tags", flatten=True)

        log_records = {}
        utils.safe_move(log_records, dd, "log_records", flatten=False)

        run_stats = run_helper.remove_run_stats(dd)

        _id = self._make_id(ws_name, run_name)

        # update RUN_INFO
        if update_primary:
            # this MAY be new run, so use UPSERT
            self._upsert_record(dbx, "run_info", ws_name, _id, dd, skip_insert=skip_insert)

        # update RUN_STATS
        if self.update_run_stats_enabled and run_stats:
            if update_last_time:
                run_stats["last_time"] = time_utils.get_arrow_now_str()
            self._flatten_prop(run_stats, "metric_names")

            self._upsert_record(dbx, "run_stats", ws_name, _id, run_stats, skip_insert=skip_insert)

        # update HPARAMS
        if hparams:
            self._upsert_record(dbx, "hparams", ws_name, _id, hparams, skip_insert=skip_insert)

        # update METRICS
        if metrics:
            self._upsert_record(dbx, "metrics", ws_name, _id, metrics, skip_insert=skip_insert)

        # update TAGS
        if tags or new_run:
            self._upsert_record(dbx, "run_tags", ws_name, _id, tags, skip_insert=skip_insert)

    # API call
    def on_run_close(self, ws_name, run_name):
        if self.metrics and self.metrics_dirty:
            # at end of run, write out the buffered metrics record
            console.print("writing buffered METRICS at end of run: {}".format(self.metrics))

            # we use upsert since we are not sure if this record has been written yet
            dbx = self._get_db(ws_name)
            _id = self._make_id(ws_name, run_name)

            self._upsert_record(dbx, "metrics", ws_name, _id, self.metrics)
            self.metrics_dirty = False

    # API call
    def update_run_at_end(self, ws_name, run_name, status, exit_code, end_time, log_records, hparams, metrics):
        # what should be updated?
        dbx = self._get_db(ws_name)

        # if self.update_run_stats:
        #     # update properties
        #     updates = {}
        #     updates["status"] = status
        #     updates["exit_code"] = exit_code
        #     updates["end_time"] = end_time

        #     # add the unique end_id (relative to ws_name)
        #     updates["end_id"] = self.get_next_id_from_workspace(ws_name, "next_end_id")

        #     # don't update hparams (it should be up-to-date from run events)
        #     #self.update_run_info(ws_name, run_name, updates, hparams, metrics)
        #     self.update_run_info(ws_name, run_name, updates, None, metrics)

    # API call
    def run_exit(self, ws_name, run_name, status, exit_code, db_retries=None, storage_retries=None, start_time=None, 
        error_msg=None):
        '''
        Processing:
            Update the "run_stats" record for this run:
                - set the run "run_duration" property to NOW - start_time
                - write "db_errors" and "storge_errors" also to record
        '''

        if self.update_run_stats_enabled:
            now = arrow.now()
            now_str = str(now)
            dbx = self._get_db(ws_name)

            print("run_exit: error_msg: {}".format(error_msg))

            # fetch start_time of run
            _id = self._make_id(ws_name, run_name)

            if not start_time:
                records = self._query(dbx, "run_stats", {"_id": _id}, {"start_time": 1})

                doc = records[0] if records else None
                if doc and "start_time" in doc:
                    start_time_str = doc["start_time"]
                    start_time = time_utils.get_time_from_arrow_str(start_time_str)

            # compute run_duration 
            run_duration = time.time() - start_time if start_time else None

            # add the unique end_id (relative to ws_name)
            end_id = self.get_next_id_from_workspace(ws_name, "next_end_id")

            rd = {"run_duration": run_duration, "db_retries": db_retries, 
                "storage_retries": storage_retries, "status": status, 
                "exit_code": exit_code, "error_msg": error_msg, "end_time": now_str, "end_id": end_id}

            self._update_record(dbx, "run_stats", ws_name, _id, rd, ensure_record_found=False)

    # API call
    def mark_run_ended_in_past(self, ws_name, run_name, status, create_time, start_time, end_time, exit_code, error_msg):
        '''
        Processing:
            Update the "run_stats" record for this run that occured in the past (called from update workspace cmd):
                - set the run "run_duration" property to exit_time - start_time
        '''
        if self.update_run_stats_enabled:
            dbx = self._get_db(ws_name)

           #print("mark_run_ended_in_past: error_msg: {}".format(error_msg))

            # fetch start_time of run
            _id = self._make_id(ws_name, run_name)

            rd = {"status": status}

            if exit_code is not None:
                rd["exit_code"] = exit_code

            if error_msg is not None:
                rd["error_msg"] = error_msg

            # add the unique end_id (relative to ws_name)
            end_id = self.get_next_id_from_workspace(ws_name, "next_end_id")
            rd["end_id"] = end_id

            if end_time:
                end_time_secs = time_utils.get_time_from_arrow_str(end_time) if end_time else time.time()

                if start_time:
                    # compute run_duration 
                    start_time_secs = time_utils.get_time_from_arrow_str(start_time)
                    run_duration = end_time_secs - start_time_secs
                    rd["run_duration"] = run_duration

                    # set end_time
                    end_time = time_utils.get_arrow_str_from_time(end_time_secs)
                    rd["end_time"] = end_time

                else:
                    # compute queue_duration
                    create_time_secs = time_utils.get_time_from_arrow_str(create_time)
                    queue_duration = end_time_secs - create_time_secs
                    rd["queue_duration"] = queue_duration

            self._update_record(dbx, "run_stats", ws_name, _id, rd, ensure_record_found=False)

    # API call
    def print_call_stats(self):
        total_count = 0
        total_elapsed = 0
        total_actual = 0
        total_calls = 0
        total_retries = 0

        # build a list of records that we can generate a report from
        records = []

        for name, entries in self.call_stats.items():
            elapsed_list = [entry["elapsed"] for entry in entries]
            actual_call_list = [entry["actual_call_time"] for entry in entries]
            retry_count_list = [entry["retry_count"] for entry in entries]

            mean_elapsed = np.mean(elapsed_list)
            mean_actual_call = np.mean(actual_call_list)
            mean_retry = np.mean(retry_count_list)

            record = {}
            record["calls"] = len(elapsed_list)
            record["name"] = name
            record["mean_elapsed"] = mean_elapsed
            record["mean_actual"] = mean_actual_call
            record["mean_retry"] = mean_retry

            records.append(record)

            # name = (name + ":").ljust(45)
            # print("  {}x {}\t AVERAGE elapsed={:.2f},\t actual={:.2f},\t retries={:.1f}".format(len(elapsed_list), name,
            #     mean_elapsed, mean_actual_call, mean_retry))

            total_calls += len(elapsed_list)
            total_elapsed += np.sum(elapsed_list)
            total_actual += np.sum(actual_call_list)
            total_retries += np.sum(retry_count_list)
            total_count += 1

        builder = report_builder.ReportBuilder()

        text, row_count = builder.build_formatted_table(records)

        # print report
        print(text)

        print("  {}x {}: TOTAL elapsed={:.2f} secs, actual={:.2f} secs, retries={:,}". \
            format(total_calls, "CALLS", total_elapsed, total_actual, total_retries))
        print()

    # API call
    def create_child_name(self, ws_name, job_id, node_index, entry, parent_run_name, rename_restarts: bool):
        # create a name for this child run.  Use run_index as the child part of the name.  It
        # may also contain a restart number if this is a restart of a run.
        run_index = entry["run_index"]
        parent_num = run_helper.get_parent_run_number(parent_run_name)

        child_name = "run{}.{}".format(parent_num, run_index)
        status = entry["status"]
        prev_name = None

        if status == "restart" and rename_restarts:
            # don't overwrite info from last instance of this run; give new instance a unique name
            prev_name = self.get_latest_run_name(ws_name, job_id, node_index, run_index)
            child_name = run_helper.increment_restart_number(prev_name)

        return child_name, prev_name

    # API call
    def get_all_runs(self, aggregator_dest, ws_name, job_or_exper_name, filter_dict=None, fields_dict=None, use_cache=True, 
        fn_cache=None, batch_size=None):
        '''
        Args:
            aggregator_dest: "job" or "experiment"
            ws_name: name of workspace containing the job or experiment
            job_or_exper_name: name of the aggregating job or experiment
            filter_dict: dict of fields to filter with
            fields_dict: dict of fields to return
            use_cache: (currently not used)
            fn_cache: (currently not used)
            batch_size: used to limit the number of records returned on each round trip to the server
        '''
        if not filter_dict:
            if aggregator_dest == "job":
                filter_dict = {"job_id": job_or_exper_name}
            elif aggregator_dest == "experiment":
                filter_dict = {"exper_name": job_or_exper_name}

        runs = self.get_filtered_sorted_run_info(ws_name, filter_dict, fields_dict, buffer_size=batch_size)

        # diagnostic: check for duplicates
        before_count = len(runs)
        # make a dict of records, using run_name as keys
        kd = {rd["_id"]:rd for rd in runs}
        runs = list(kd.values())
        after_count = len(runs)

        if before_count != after_count:
            print("FYI: get_all_runs: {:,} duplicate records found and removed".format(before_count-after_count))
      
        return runs

    # API call
    def does_run_exist(self, ws_name, run_name):
        dbx = self._get_db(ws_name)
        _id = self._make_id(ws_name, run_name)
        fd = {"_id": _id}

        records = self._query(dbx, "run_info", fd)
        return bool(records)

    # API call
    def get_latest_run_name(self, ws_name, job_id, node_index, run_index):
        '''
        finds the latest instance of a run (the most recent restart of a run)
        '''
        dbx = self._get_db(ws_name)
        cmd = "select run_name from [run_info] where ws_name = '{}' and job_id = '{}' and run_index = {}".format(ws_name, job_id, run_index)
        records = self._execute_with_retry("get_run_count", cmd=cmd, dbx=dbx, fetch_type="fetchall")

        # find the latest run_name (one with largest restart_num)
        run_names = [record[0] for record in records]
        lastest_num = -1
        latest_name = None

        for run_name in run_names:
            restart_num = run_helper.get_restart_number(run_name)
            if restart_num > lastest_num:
                lastest_num = restart_num
                latest_name = run_name

        return latest_name

    # API call
    def update_node_info_with_service_info(self, ws_name, job_id, node_index, node_info):
        dbx = self._get_db(ws_name)
        _id = self._make_node_id(ws_name, job_id, node_index)

        # update the "service_info" field
        json_text = json.dumps(node_info)
        vd = {"service_info": json_text} 
        self._update_record(dbx, "node_info", ws_name, _id, vd)

    # API call
    def node_start(self, ws_name, job_id, node_index, node_restart, prep_start_str):

        if self.update_node_stats_enabled:
            _id = self._make_node_id(ws_name, job_id, node_index)
            dbx = self._get_db(ws_name)

            # read record for this node
            filter = {"_id": _id}
            fields = {"create_time": 1, "prep_start_time": 1, "restarts": 1}
            records = self._query(dbx, "node_stats", filter, fields)
            
            doc = records[0] if records else None
            create_time_str = utils.safe_value(doc, "create_time")
            create_time = arrow.get(create_time_str)

            restarts = utils.safe_value(doc, "restarts")

            # if prep_start_time has been written, our node has been RESTARTED
            prev_prep_start_time = utils.safe_value(doc, "prep_start_time")
            if not node_restart and prev_prep_start_time is not None:
                node_restart = True

            if node_restart:
                # increment the "restarts" field of node_stats
                restarts = restarts + 1
                console.print("===> NODE restart #{} detected: {} <======".format(restarts, _id))

            now = arrow.now()
            now_str = str(now)

            # compute time in "queue" 
            prep_start_time = arrow.get(prep_start_str)
            queue_duration = time_utils.time_diff(prep_start_time, create_time)

            # compute time in PREP setup script (aka wrapper)
            prep_duration = time_utils.time_diff(now, prep_start_time)

            # update: times, durations, restarts, and status
            vd = {"prep_start_time": prep_start_str, "app_start_time": now_str, 
                "queue_duration": queue_duration, "prep_duration": prep_duration, 
                "restarts": restarts, "node_status": "running"} 

            self._update_record(dbx, "node_stats", ws_name, _id, vd)

        return node_restart

    # API call
    def mark_run_completed(self, ws_name, job_id, node_id, run_name, status, exit_code, db_retries, storage_retries, 
        start_time, error_msg, is_parent):

        self.run_exit(ws_name, run_name, status, exit_code, db_retries, storage_retries, start_time, error_msg)

        if not is_parent:
            # tell database this job has a completed run
            node_index = utils.node_index(node_id)
            run_was_started = (start_time is not None)

            utils.log_info("calling DATABASE job_run_exit", run_name)
            self.job_run_exit(ws_name, job_id, exit_code, run_was_started)

            utils.log_info("calling DATABASE node_run_end", run_name)
            self.node_run_end(ws_name, job_id, node_index, exit_code, run_was_started)

    # API call
    def node_end(self, ws_name, job_id, node_index, db_retries, storage_retries, app_start_str):
        '''
        Processing:
            called at the end of XT controller to compute/write to node_stats:
                - post_start_time
                - app_duration
                - node_status
                - db_retries
                - storage_retries
        '''

        dbx = self._get_db(ws_name)

        if self.update_node_stats_enabled:
            node_id = self._make_node_id(ws_name, job_id, node_index)

            now = arrow.now()
            now_str = str(now)

            # compute time in controller + apps 
            app_start_time = arrow.get(app_start_str)
            app_duration = time_utils.time_diff(now, app_start_time)

            # update: node_status, run_duration, end_time
            vd = {"post_start_time": now_str, "app_duration": app_duration, "node_status": "completed", 
                "db_retries": db_retries, "storage_retries": storage_retries} 

            self._update_record(dbx, "node_stats", ws_name, node_id, vd)

        if self.update_job_stats_enabled:
            # add our RETRY ERRORS to our job entry
            js_id = self._make_id(ws_name, job_id)
            cmd = "UPDATE [job_stats] SET [db_retries] = [db_retries] + {}, " \
                "[storage_retries] = [storage_retries] + {} WHERE [_id] = '{}'".\
                    format(db_retries, storage_retries, js_id)

            #console.print("node_end: updating JOB STATS with cmd:\n  {}".format(cmd))

            self._execute_with_retry("node_end", cmd=cmd, dbx=dbx)

    # API call
    def mark_node_ended_in_past(self, ws_name, job_id, node_info, status, end_time, ended_count, error_count):
        '''
        Processing:
            called from "update workspace" cmd to mark false ALIVE nodes as terminated; update:
                - post_start_time
                - app_duration
                - node_status
        '''
        if self.update_node_stats_enabled:
            dbx = self._get_db(ws_name)

            node_id = node_info["node_id"]
            node_index = utils.node_index(node_id)
            _id = self._make_node_id(ws_name, job_id, node_index)

            nd = {"node_status": status}

            if ended_count > 0:
                nd["completed_runs"] = node_info["completed_runs"] + ended_count

            if error_count > 0:
                nd["error_runs"] = node_info["error_runs"] + error_count

            if end_time:
                end_time_secs = time_utils.get_time_from_arrow_str(end_time) 

                # compute duration for the phase of processing active when node was terminated
                post_end_time = node_info["post_end_time"]

                if post_end_time:
                    # all durations have already been updated
                    pass

                else:
                    post_start_time = node_info["post_start_time"]
                    if post_start_time:
                        post_start_time_secs = time_utils.get_time_from_arrow_str(post_start_time)
                        post_duration = end_time_secs - post_start_time_secs
                        nd["post_duration"] = post_duration
                        nd["post_end_time"] = end_time

                    else:
                        app_start_time = node_info["app_start_time"]
                        if app_start_time:
                            app_start_time_secs = time_utils.get_time_from_arrow_str(app_start_time)
                            app_duration = end_time_secs - app_start_time_secs
                            nd["app_duration"] = app_duration

                        else:
                            prep_start_time = node_info["prep_start_time"]
                            if prep_start_time:
                                prep_start_time_secs = time_utils.get_time_from_arrow_str(prep_start_time)
                                prep_duration = end_time_secs - prep_start_time_secs
                                nd["prep_duration"] = prep_duration
                            
                            else:
                                create_time = node_info["create_time"]
                                if create_time:
                                    create_time_secs = time_utils.get_time_from_arrow_str(create_time)
                                    queue_duration = end_time_secs - create_time_secs
                                    nd["queue_duration"] = queue_duration

            self._update_record(dbx, "node_stats", ws_name, _id, nd)

    # API call
    def node_post_end(self, ws_name, job_id, node_index, post_start_str):
        '''
        Processing:
            called at the end of XT setup script (aka wrapper) to compute/write to node_stats:
                - post_end_time
                - post_duration
        '''

        dbx = self._get_db(ws_name)

        if self.update_node_stats_enabled:
            id = self._make_node_id(ws_name, job_id, node_index)

            now = arrow.now()
            now_str = str(now)

            # compute time in POST part of setup script (aka wrapper)
            post_start_time = arrow.get(post_start_str)
            post_duration = time_utils.time_diff(now, post_start_time)

            # update: node_status, run_duration, end_time
            vd = {"post_end_time": now_str, "post_duration": post_duration} 
            console.print("node_post_end: id={}, vd={}".format(id, vd))

            self._update_record(dbx, "node_stats", ws_name, id, vd)

    # API call
    def get_run_count(self, ws_name):
        dbx = self._get_db(ws_name)

        cmd = "select count(*) from [run_info] where ws_name = '{}'".format(ws_name)
        record = self._execute_with_retry("get_run_count", cmd=cmd, dbx=dbx, fetch_type="fetchone")

        count = record[0]
        return count

    # API call
    def get_collection(self, ws_name, collection_name, filter, fields=None, sort_col=None, 
        sort_dir=1, skip=None, first=None, count_runs=False, buffer_size=None):
        '''
        Query on flat table for specified filter and fields.
        '''

        dbx = self._get_db(ws_name)

        if not "ws_name" in filter:
            filter["ws_name"] = ws_name

        docs = self._query(dbx, collection_name, filter, fields, sort_col, sort_dir, skip, first)
        return docs

    # API call
    def set_job_tags(self, ws_name, filter_dict, tag_dict, clear_tags):
        return self._set_tags("job_tags", ws_name, filter_dict, tag_dict, clear_tags)

    # API call
    def set_run_tags(self, ws_name, filter_dict, tag_dict, clear_tags):
        return self._set_tags("run_tags", ws_name, filter_dict, tag_dict, clear_tags)

    # API call
    def set_node_tags(self, ws_name, filter_dict, tag_dict, clear_tags):
        return self._set_tags("node_tags", ws_name, filter_dict, tag_dict, clear_tags)

    def _set_tags(self, table_name, ws_name, filter_dict, tag_dict, clear_tags):
        dbx = self._get_db(ws_name)

        def fixup_key(key):
            if key.startswith("tags."):
                key = key[5:]
            return key

        def fixup_value(value):
            if clear_tags:
                value = None
            elif value is None:
                value = ""
            return value

        # remove "tags." prefix from names in tag_dict & fixup values
        tag_dict = {fixup_key(key): fixup_value(value) for key, value in tag_dict.items()}

        if not ws_name in filter_dict:
            filter_dict["ws_name"] = ws_name

        col_dict = self._get_table_columns(dbx, table_name)
        values, actual_cols = self._expand_doc_as_tuple(dbx, table_name, tag_dict, col_dict, force_vchar=True)

        # build cmd
        where_str = self._build_where_from_filter(filter_dict)
        set_str = self._build_set_from_cols(actual_cols)
        cmd = "update [{}] {} {}".format(table_name, set_str, where_str)

        rows_updated = self._execute_with_retry("_set_tags", cmd=cmd, dbx=dbx, values=values)
        return rows_updated

    # API call
    def set_workspace_counters(self, ws_name, next_job_number, next_end_id, next_request_number=1):

        dbx = self._get_db(ws_name=None)

        dd = {"next_job_number": next_job_number, "next_end_id": next_end_id, "next_request_number": next_request_number}
        self._update_record(dbx, WORKSPACES, ws_name, id=ws_name, values=dd)

    # API call
    def get_all_experiments_in_ws(self, ws_name):
        dbx = self._get_db(ws_name)

        cmd = "SELECT DISTINCT [exper_name] FROM [job_info] WHERE [ws_name] = '{}'".format(ws_name)
        records = self._execute_with_retry("get_all_experiments_in_ws", cmd=cmd, dbx=dbx, fetch_type="fetchall")
        exper_names = [record[0] for record in records]

        console.diag("after get_all_experiments()")        
        return exper_names        

    # API call
    def update_job_run_stats(self, ws_name, job_id, sd):
        '''
        Processing:
            update records in the RUN_STATS collection, using the specified name/values
            in "sd" for all runs in the specified "job_id".
        '''
        dbx = self._get_db(ws_name)

        set_str = self._build_set_from_cols(sd)
        cmd = "UPDATE [run_stats] {} WHERE [job_id] = '{}'".format(set_str, job_id)
        values = list(sd.values())

        self._execute_with_retry("update_job_run_stats", cmd=cmd, dbx=dbx, values=values)

    # API call
    def update_connect_info_by_node(self, ws_name, job_id, node_id, connect_info):
        dbx = self._get_db(ws_name)

        node_index = utils.node_index(node_id)
        id = self._make_node_id(ws_name, job_id, node_index)

        # console.print("update_connect_info_by_node: id={}, connect_info={}".format( \
        #     id, connect_info))

        self._update_record(dbx, "node_info", ws_name, id, connect_info)

    # API call
    def update_requests_record(self, ws_name, request_id, rr):
        dbx = self._get_db(ws_name)
        id = self._make_id(ws_name, request_id)

        self._update_record(dbx, "requests", ws_name, id, rr)

def test_new_metrics():
    from xtlib.helpers import xt_config
    from xtlib.storage.store import Store

    class Bag(): pass

    config = xt_config.get_merged_config()
    store = Store(config=config)  
    db = store.database

    ws_name = "ws4"
    run_name = "run1160.2"
    dd = {"step": 42, "new_metric": .34}

    dbx = db._get_db(ws_name)
    _id = db._make_id(ws_name, run_name)
    db._upsert_record(dbx, "metrics", ws_name, _id, dd)

if __name__ == "__main__":
    test_new_metrics()