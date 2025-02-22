# plot_restarts.py: code to support the "xt plot restarts" command
import math
import time
import arrow
import json
import numpy as np
from collections import defaultdict

from xtlib import time_utils, utils, xt_cmds
from xtlib import job_helper, run_helper, node_helper
from xtlib import plot_helper

CATCH_UP = 2
RUNNING = 1
QUEUED = 0

class TimeEvents:

    def __init__(self):
        self.events = []
        self.dt_first_time = None
        self.secs_first_time = None

    def set_first_time(self, at):
        self.dt_first_time = at
        self.secs_first_time = at.datetime.timestamp() 

    def add(self, at, state_or_name):
        secs = at.datetime.timestamp()

        rel_secs = secs - self.secs_first_time
        rel_hours = rel_secs / 3600

        if self.events:
            assert rel_hours >= self.events[-1][0] 

        # also add at, for debugging
        self.events.append( (rel_hours, state_or_name, at) )

        # if state_or_name == "restart_caught_up":
        #     print("catch_up at: ", at)

    def sort(self):
        self.events.sort(key=lambda x: x[0])

class PlotRestarts:
    def __init__(self, store, node_list, workspace, plot_end_runs, plot_checkpoints, plot_catchup, gpu, show_toolbar):
        self.store = store
        self.ws_name = workspace
        self.plot_end_runs = plot_end_runs
        self.plot_checkpoints = plot_checkpoints
        self.plot_catchup = plot_catchup
        self.plot_gpu = gpu
        self.show_toolbar = show_toolbar

        # for now, just support a single job or node name
        job_id = node_list[0]

        if not job_helper.is_job_id(job_id):
            node_index = node_helper.get_node_index(job_id)
            job_id = node_helper.get_job_id(job_id)
        else:
            node_index = -1

        self.job_id = job_id
        self.node_index = node_index

    def get_node_queued_running_data(self, last_times_dict, node_index, catch_up = False):
        times = []
        states = []

        # 1. read CREATE_TIME from NODE_STATS
        fields_dict = {"create_time": 1, "post_end_time": 1}
        filter_dict = {"ws_name": self.ws_name, "job_id": self.job_id, "node_index": node_index}
        node_records = self.store.database.get_info_for_nodes(self.ws_name, filter_dict, fields_dict)
        text_create_time = node_records[0]["create_time"]
        at_created = time_utils.get_arrow_from_arrow_str(text_create_time)

        # completed_time = node_records[0]["post_end_time"]
        #dt_completed = time_utils.get_time_from_arrow_str(completed_time) if completed_time else None

        # read NODE.LOG for exact start and restart times
        fn = "nodes/node{}/node.log".format(node_index)

        if not self.store.does_job_file_exist(self.ws_name, self.job_id, fn):
            return None, None, None

        text = self.store.read_job_file(self.ws_name, self.job_id, fn)
        node_log_records = utils.load_json_records(text)
        restart_count = 0
        current_run_name = None
        active_programs = {}    # key=run_name, value=last step number logged

        # build time_states list
        time_states = TimeEvents()
        event_list = TimeEvents()
        end_run_count = 0
        catch_up_count = 0     # relative to current node session

        # add first queued record
        time_states.set_first_time(at_created)
        event_list.set_first_time(at_created)

        time_states.add(at_created, QUEUED)

        def is_program_active(name):
            base_name = name.split(".r")[0]
            return base_name in active_programs
        
        def add_to_active(name):
            base_name = name.split(".r")[0]
            active_programs[base_name] = 0

        def remove_from_active(name):
            base_name = name.split(".r")[0]
            del active_programs[base_name]

        at_last_activity = None
        found_node_end = False

        for r, record in enumerate(node_log_records):
            event = record["event"]
            data = record["data"]
            at = time_utils.get_arrow_from_arrow_str(record["time"])

            # # debug
            # if r == 0:
            #     print("------------------------------------------------")
            # print("event: ", event, "  data: ", data, "  time: ", record["time"])

            if event == "started" or event == "restarted":
                # these are dup events for node_start/node_restart
                pass
                
            elif event == "node_start":
                time_states.add(at, RUNNING)
                at_last_activity = at
                catch_up_count = 0
                
            elif event == "node_restart":
                queued_time = None
                catch_up_count = 0

                # do this so we can match the end run
                # node_run_name = data["run"]
                # add_to_active(node_run_name)

                if current_run_name and current_run_name in last_times_dict:

                    # limit last_time, in case it was updated after run ended (how??)
                    last_time = last_times_dict[current_run_name]

                    if last_time < at:
                        # its a valid last_time
                        queued_time = last_time

                if not queued_time:
                    # preemption happened somewhere between last activity and the restart; use their average
                    queued_time = self.avg_arrow_times(at_last_activity, at)

                time_states.add(queued_time, QUEUED)

                if catch_up:
                    time_states.add(at, CATCH_UP)
                else:
                    time_states.add(at, RUNNING)

                current_run_name = None
                restart_count += 1
                
            elif event == "start_run":
                current_run_name = data["run"]
                at_last_activity = at

                # if catch_up and is_program_active(current_run_name):
                #     time_states.add(at, CATCH_UP)
                # else:
                #     # new program being run
                #     add_to_active(current_run_name)
                #     #time_states.add(at, RUNNING)
                add_to_active(current_run_name)
                
            elif event == "end_run"and not data["is_parent"]:
                # program completed
                if not current_run_name:
                    print("warning: end_run without start_run: ", data["run"])

                elif data["run"] != current_run_name:
                    print("WARNING: plot nodes command doesn't currently support simultaneous runs on same node (end_run doesn't match most recent start_run): {}, {}".format(data["run"], current_run_name))
                    #raise Exception("plot nodes command doesn't currently support simultaneous runs on same node: {}, {}".format(data["run"], current_run_name))
                
                if current_run_name:
                    remove_from_active(current_run_name)
                    current_run_name = None

                at_last_activity = at

                if self.plot_end_runs:
                    event_list.add(at, "end_run")
                end_run_count += 1

            elif event == "checkpoint_upload":
                if self.plot_checkpoints:
                    event_list.add(at, "checkpoint")

                if not at_last_activity or at > at_last_activity:
                    at_last_activity = at

               # adjust last_times, if needed
                if current_run_name and current_run_name in last_times_dict:
                    last_time = last_times_dict[current_run_name]
                    if at > last_time:
                        last_times_dict[current_run_name] = at                    


            elif event == "restart_caught_up":
                assert catch_up_count == 0

                # this is a restart that caught up to the last activity
                time_states.add(at, RUNNING)
                event_list.add(at, "restart_caught_up")
                catch_up_count += 1

                if not at_last_activity or at > at_last_activity:
                    at_last_activity = at

                # adjust last_times, if needed
                if current_run_name and current_run_name in last_times_dict:
                    last_time = last_times_dict[current_run_name]
                    if at > last_time:
                        last_times_dict[current_run_name] = at

            elif event == "get_index":
                at_last_activity = at
                
            elif event == "node_end":
                # the node has completed
                current_run_name = None   # data["run"]
                time_states.add(at, QUEUED)
                found_node_end = True
                break

        if not found_node_end:
            # add an ending transition based on last time logged (not "now")
            last_pair = time_states.events[-1]
            last_state = last_pair[1]

            if last_state == RUNNING:
                # extend RUNNING state to last known activity
                if current_run_name and current_run_name in last_times_dict:
                    last_time = last_times_dict[current_run_name]
                else:
                    last_time = arrow.now()
                time_states.add(last_time, QUEUED)
            else:
                # extend QUEUED state to NOW
                time_states.add(arrow.now(), RUNNING)

        # time_states.sort()
        # event_list.sort()

        # convert time_states to times and states
        times = [pair[0] for pair in time_states.events]
        states = [pair[1] for pair in time_states.events]
        events = [ev for ev in event_list.events]

        return times, states, events, restart_count, end_run_count, at_created

    def avg_arrow_times(self, at1, at2):
        secs1 = at1.datetime.timestamp()
        secs2 = at2.datetime.timestamp()
        avg_secs = (secs1 + secs2) / 2
        return arrow.get(avg_secs)

    def build_last_times(self):
        '''
        gets the latest activity time for each run in the job (using run_name, not base_run_name).  Returns a dict of dicts.
        Outer dict key=node_index.  Inner dict key/value is run_name/last_time (as arrow object).
        '''

        # using run_stats is faster, but the LAST_TIME field is sometimes updated after the run ends
        method = "run_steps"      # run_steps, run_stats, or log_records

        if method == "run_steps":
            last_times_by_node = self.store.database.get_latest_activity_by_node(self.ws_name, self.job_id)

            if not last_times_by_node:
                # legacy runs: some were not yet using run_steps
                method = "run_stats"

        if method == "run_stats":
            '''
            read LAST_TIME from all run records for this job or node.
            group the results by node_index
            '''
            fields_dict = {"run_name": 1, "node_index": 1, "last_time": 1}
            filter_dict = {"ws_name": self.ws_name, "job_id": self.job_id}

            if self.node_index > -1:
                filter_dict["node_index"] = self.node_index

            run_records = self.store.database.get_info_for_runs(self.ws_name, filter_dict, fields_dict)

            last_times_by_node = defaultdict(dict)

            for rr in run_records:
                last_time = rr["last_time"]
                node_index = rr["node_index"]
                run_name = rr["run_name"]

                ltd = last_times_by_node[node_index]    # create dict on demand, when needed
                ltd[run_name] = time_utils.get_arrow_from_arrow_str(last_time)

            # sort last_times_by_node by node_index (ascending)
            last_times_by_node = dict(sorted(last_times_by_node.items(), key=lambda item: item[0]))

        elif method == "log_records":
            '''
            read all logged records for this job or node to determine the time of last activity.
            group the results by node_index
            '''
            started = time.time()
            fields_dict = {"run_name":1, "node_index": 1}
            filter_dict = {"ws_name": self.ws_name, "job_id": self.job_id}

            if self.node_index > -1:
                filter_dict["node_index"] = self.node_index
            
            run_records = run_helper.get_run_records(job_id=self.job_id, workspace_name=self.ws_name, fields_dict=fields_dict, 
                filter_dict=filter_dict, include_log_records=True)

            last_times_by_node = defaultdict(dict)

            for rr in run_records:
                run_name = rr["run_name"]
                node_index = rr["node_index"]

                log_records = rr["log_records"]
                last_time = log_records[-1]["time"]

                ltd = last_times_by_node[node_index]    # create dict on demand, when needed
                ltd[run_name] = time_utils.get_arrow_from_arrow_str(last_time)


            # sort last_times_by_node by node_index (ascending)
            last_times_by_node = dict(sorted(last_times_by_node.items(), key=lambda item: item[0]))

        return last_times_by_node

    def convert_stats_to_tuples(self, stats, key, at_created):
        '''
        input: 
            stats: a list of dict, each with a "time" field and various usage key/value pairs
            key: the usage stat to extract from each dict
            at_created: the time the node was created (as arrow object)

        output: 
            a list of tuples of the form: (time_rel_hours, value)
        '''
        tuple_list = []
        secs_created = at_created.datetime.timestamp() 

        for sd in stats:
            time_str = sd["time"]
            time_secs = time_utils.get_time_from_arrow_str(time_str)
            time_rel_hours = (time_secs - secs_created) / 3600

            value = sd[key]
            tuple_list.append( (time_rel_hours, value) )

        return tuple_list

    def get_node_stats(self, node_index, at_created):

        stats_by_key = {}

        # read the node_usage.log for this node
        fn = "nodes/node{}/node_usage.log".format(node_index)
        if self.store.does_job_file_exist(self.ws_name, self.job_id, fn):
            text = self.store.read_job_file(self.ws_name, self.job_id, fn)
            nested_records = utils.load_json_records(text)

            # convert the lists of lists to a single list
            records = [item for sublist in nested_records for item in sublist]

            for key in ["gpu_utilization", "gpu_memory_in_use"]:
                hours_tuple = self.convert_stats_to_tuples(records, key, at_created)
                stats_by_key[key] = hours_tuple

        elif self.plot_gpu:
            print("Note: no node_usage.log file found for job: {}, node: {}".format(self.job_id, node_index))


        return stats_by_key

    def plot_core(self):
        # restart_report.py: sketch out code needed to show queued/running states of a run over time
        import matplotlib.pyplot as plt

        # build last_times of runs, grouped node_index        
        last_times = self.build_last_times()

        node_data = {}
        max_time = None
        created_times = {}

        for node_index, ltd in last_times.items():
            times, states, events, restart_count, end_run_count, at_created = self.get_node_queued_running_data(ltd, node_index, catch_up=self.plot_catchup)
            if times is not None:

                mt = times[-1]
                if max_time is None or mt > max_time:
                    max_time = mt    

                node_data[node_index] = (times, states, events, restart_count, end_run_count)

                created_times[node_index] = at_created

        plt_count = len(node_data)
        if plt_count == 0:
            print("no nodes found to plot: {}".format(self.job_id))
            return      

        fig_height = 1.5*plt_count
        figsize = (20, min(10, fig_height))
        fig, axes = plt.subplots(plt_count, 1, squeeze=False, figsize=figsize)  # plt_count rows, 1 column

        queue_percents = []
        avg_gpu_util = 0
        avg_gpu_mem = 0

        catch_up_percents = []
        for node_index, (times, states, events, restart_count, end_run_count) in node_data.items():
            # set axis_index to the key index of node_index in last_times
            axis_index = list(node_data.keys()).index(node_index)
            axis = axes[axis_index][0]
            at_created = created_times[node_index]

            stats_by_key = self.get_node_stats(node_index, at_created)
            if stats_by_key:

                gpu_util_tuples = stats_by_key["gpu_utilization"]
                node_avg_gpu_util = sum([xy[1] for xy in gpu_util_tuples]) / len(gpu_util_tuples)
                avg_gpu_util += node_avg_gpu_util

                gpu_mem_tuples = stats_by_key["gpu_memory_in_use"]
                node_avg_gpu_mem = sum([xy[1] for xy in gpu_mem_tuples]) / len(gpu_mem_tuples)
                avg_gpu_mem += node_avg_gpu_mem

            queue_percent, catch_up_percent = self.create_node_subplot(axis, times, states, events, restart_count, node_index, plt_count, 
                end_run_count, max_time, stats_by_key, avg_gpu_util, avg_gpu_mem)

            queue_percents.append(queue_percent)
            catch_up_percents.append(catch_up_percent)

        # Show the plot
        total_restarts = sum([data[3] for data in node_data.values()])
        total_end_runs = sum([data[4] for data in node_data.values()])
        avg_queue_percent = sum(queue_percents) / len(queue_percents)
        avg_catch_up_percent = sum(catch_up_percents) / len(catch_up_percents)
        progress_percent = 1 - (avg_queue_percent + avg_catch_up_percent)

        title = "Restart Report: {} (restarts: {:}, queue: {:.0f}%, catch_up: {:.0f}%, progress: {:.0f}%".format(self.job_id, total_restarts, 
                100*avg_queue_percent, 100*avg_catch_up_percent, 100*progress_percent)

        if self.plot_end_runs:
            title += ", ends={}".format(total_end_runs)

        if self.plot_gpu:
            title += ", GPU util: {:.0f}%, GPU mem: {:.0f}%".format(100*avg_gpu_util, 100*avg_gpu_mem)

        title += ")"
            
        fig.suptitle(title)

        our_cmd = "xt " + xt_cmds.orig_xt_cmd
        fig.canvas.manager.set_window_title(our_cmd)
        plt.tight_layout()

        plot_helper.show_plot(True, not self.show_toolbar)

    def extract_node_stat(self, node_stats, key, rel_start, rel_end):
        tuple_list = node_stats[key]
        x = [xy[0] for xy in tuple_list if xy[0] >= rel_start and xy[0] <= rel_end]
        y = [xy[1] for xy in tuple_list if xy[0] >= rel_start and xy[0] <= rel_end]
        return x, y
    
    def create_node_subplot(self, axis, times, states, events, restart_count, node_index, plt_count, end_run_count, max_time, 
        node_stats, avg_gpu_util, avg_gpu_memory):

        import matplotlib
        import matplotlib.markers as mmarkers

        linewidth = 1.25
        plot_alpha = .4
        gpu_alpha = .4
        colors = ["r-", "g-", "r-"]    # QUEUED, RUNNING, CATCH_UP
        plot_verticals = True

        def y_val(state):
            return 0 if state == 0 else 1
        
        # Draw each segment separately
        for i in range(1, len(times)):
            # Horizontal line from the previous time to the current time
            last_state = states[i-1]
            curr_state = states[i]

            color = colors[last_state]
            axis.plot([times[i-1], times[i]], [y_val(last_state), y_val(last_state)], color, linewidth=linewidth, alpha=plot_alpha)  # Default blue

            if self.plot_gpu and y_val(last_state) == 1 and node_stats:
                # plot GPU USAGE
                x, y = self.extract_node_stat(node_stats, "gpu_utilization", times[i-1], times[i])

                # adjust y values so that we see y=0 plotted just above queued line (map from [0, 1] to [.05, .95])
                y = .9*np.array(y) + .05
                axis.fill_between(x, y, linewidth=0, alpha=gpu_alpha, color="gray")

                # # plot GPU MEMORY
                # x, y = self.extract_node_stat(node_stats, "gpu_memory_in_use", times[i-1], times[i])
                # axis.plot(x, y, linewidth=.7, alpha=.7, color="gray")

            if plot_verticals:
                # Vertical line with opacity=.2
                if i < len(times)-1:    
                    if y_val(curr_state) != y_val(last_state):
                        axis.plot([times[i], times[i]], [y_val(last_state), y_val(curr_state)], 'r-', linewidth=linewidth, alpha=plot_alpha)

        # plot markers for events 
        marker_size = 20
        endrun_marker = mmarkers.MarkerStyle('$e$')
        checkpoint_marker = mmarkers.MarkerStyle('$\u2713$')
        catchup_marker = mmarkers.MarkerStyle('$u$')
        marker_y = .75
        marker_opacity = .7
        linewidth = .8

        for rel_hours, name, _ in events:
            if name == "end_run" and self.plot_end_runs:
                axis.scatter(rel_hours, 1.0, marker="+", color="green", s=20, alpha=.7, linestyle='None', linewidths=.5)
                #axis.scatter(rel_hours, marker_y, marker=endrun_marker, color="blue", s=marker_size, alpha=marker_opacity, linewidths=linewidth)

            if name == "checkpoint" and self.plot_checkpoints:
                axis.scatter(rel_hours, 1.0, marker=checkpoint_marker, color="red", s=20, alpha=.7, linestyle='None', linewidths=.5)
                #axis.scatter(rel_hours, marker_y, marker=checkpoint_marker, color="red", s=marker_size, alpha=marker_opacity, linewidth=linewidth)

            if name == "restart_caught_up" and self.plot_catchup:
                axis.scatter(rel_hours, 1.0, marker='$\$$', color="green", s=26, alpha=.7, linestyle='None', linewidths=.5)
                #axis.scatter(rel_hours, marker_y, marker=catchup_marker, color="green", s=15, alpha=marker_opacity, linewidth=linewidth)

        self.adjust_axes(axis, max_time, node_index)

        queue_percent, catch_up_percent = self.write_text(axis, times, max_time, states, plt_count, restart_count, end_run_count, 
            node_index, avg_gpu_util, avg_gpu_memory)

        return queue_percent, catch_up_percent 

    def adjust_axes(self, axis, max_time, node_index):
        import matplotlib.ticker as ticker
        alpha = .4

        # this doesn't work
        #axis.margins(x=.15, y=.2)   # adds 5% padding to the x-axis and 5% padding to the y-axis
        #self.add_fixed_space_x_margins(axis, 5, 10)

        axis.set_yticks([0, 1], ['Queued', 'Running'], alpha=alpha, fontsize=8)

        xlabel = "Hours [node{}]".format(node_index)
        axis.set_xlabel(xlabel, alpha=alpha, fontsize=8)

        x_margin = .01*max_time
        axis.set_xlim(0-x_margin, max_time+x_margin)
        axis.set_ylim(-.1, 1.1)

        # set major, minor ticks
        hour_range = math.ceil(max_time)
        if hour_range > 3 and hour_range <= 24:
            axis.xaxis.set_major_locator(ticker.MaxNLocator(nbins=hour_range))
        #axis.xaxis.set_minor_locator(ticker.AutoMinorLocator(4))

        # Set fontsize and alpha for x-axis tick labels
        for label in axis.get_xticklabels():
            label.set_fontsize(8)        # set font size
            label.set_alpha(alpha)       # set transparency

        # Make spines less prominent
        for position in ["left", "right", "top", "bottom"]:
            # axis.spines[position].set_visible(False)
            axis.spines[position].set_color('lightgray')
            axis.spines[position].set_linewidth(0.5)        

    def write_text(self, axis, times, max_time, states, plt_count, restart_count, end_run_count, node_index, avg_gpu_util, avg_gpu_memory):
        # calculate the run_percentages (time in run state / total time)
        queue_times = []
        catch_up_times = []
        time_duration = times[-1] - times[0]

        for i in range(0, len(times)-1):
            if states[i] == QUEUED:
                queue_times.append(times[i+1] - times[i])
            elif states[i] == CATCH_UP:
                catch_up_times.append(times[i+1] - times[i])

        total_queue_times = sum(queue_times)
        queue_percent = total_queue_times / time_duration
 
        total_catch_up_times = sum(catch_up_times)
        catch_up_percent = total_catch_up_times / time_duration

        # # debug
        # rt_text = ["{:.1f}".format(rt) for rt in run_times]
        # print("\nrun_times: {}".format(", ".join(rt_text)))
        # print("node: {}, elapsed: {}, total_run_time: {}, run_percent: {:.0f}%".format(node_index, times[-1] - times[0], total_run_time, run_percent*100))

        # text lines to the right of the 
        if plt_count == 1:
            y_spacing = .35
        elif plt_count == 2:
            y_spacing = .3
        elif plt_count > 10:
            y_spacing = .5
        else:
            y_spacing = .25

        text_x = 1.02*max_time

        #axis.text(text_x, 1, "node {}".format(node_index), fontsize=8)
        axis.text(text_x, 1-0*y_spacing, "restarts: {}".format(restart_count), fontsize=8)
        axis.text(text_x, 1-1*y_spacing, "queue: {:.0f}%".format(queue_percent*100), fontsize=8)
        axis.text(text_x, 1-2*y_spacing, "catch_up: {:.0f}%".format(catch_up_percent*100), fontsize=8)
        axis.text(text_x, 1-3*y_spacing, "GPU util: {:.0f}%".format(avg_gpu_util*100), fontsize=8)

        # ss.text(text_x, 1-4*y_spacing, "ends: {}".format(end_run_count), fontsize=8)

        return queue_percent, catch_up_percent
