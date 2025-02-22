# node_usage_logger.py: runs on a bg thread to sample machine usage and log it to TPX storage
import json
import time
import threading
from xtlib import time_utils

import torch

class NodeUsageLogger():

    def __init__(self, storage, ws_id, job_id, node_id, sample_freq_secs, storage_freq_secs):
        self.storage = storage
        self.ws_id = ws_id
        self.job_id = job_id
        self.node_id = node_id
        self.sample_freq_secs = sample_freq_secs
        self.storage_freq_secs = storage_freq_secs
        self.closing = False

        self.sample_start_time = time.time()
        self.last_storage_time = time.time()

        # create a lock to protect the samples list
        self.samples_lock = threading.Lock()

        self.samples = []

    def start(self):
        gpu_thread = threading.Thread(target=self.sample_gpu_utilization, daemon=True)
        gpu_thread.start()        

    def take_samples(self):

        # report time is the middle of the sample duration
        sample_duration = time.time() - self.sample_start_time
        report_time = self.sample_start_time + sample_duration / 2

        sd = {"time": time_utils.get_arrow_str_from_time(report_time)}

        # GPU utilization
        value = torch.cuda.utilization()
        sd["gpu_utilization"] = value/100     # normalize int percentage

        free, total = torch.cuda.mem_get_info(0)
        percent_in_use = 1 - (free / total)
        sd["gpu_memory_in_use"] = percent_in_use

        with self.samples_lock:
            self.samples.append(sd)
            self.sample_start_time = time.time()

        #print("$", end="", flush=True)

    def write_samples_to_storage(self):

        with self.samples_lock:
            if self.samples:
                self.storage.log_node_usage(self.ws_id, self.job_id, self.node_id, self.samples)
                self.samples = []

            self.last_storage_time = time.time()

    def sample_gpu_utilization(self):
        
        if torch.cuda.is_available():

            while not self.closing:
                self.take_samples()

                if time.time() - self.last_storage_time > self.storage_freq_secs:
                    self.write_samples_to_storage()

                time.sleep(self.sample_freq_secs)

    def flush_samples(self):
        self.write_samples_to_storage()
        #print("flushed samples")

    def close(self):
        self.closing = True
        self.write_samples_to_storage()

