# log_helper.py: used by the Controller to log into to the console
import os
import time

from xtlib import utils
from xtlib import pc_utils
from xtlib import console

class LogHelper():
    def __init__(self, context):
        self.xt_started = int(os.getenv("XT_STARTED", "0"))
        self.context = context
        self.logging_enabled = True

    def log_title(self, title, double=False, force_log=False):
        if self.logging_enabled or force_log:
            elapsed = time.time() - self.xt_started
            elapsed_str = utils.friendly_duration_format(elapsed, True)

            # make title stand out a bit
            title = title.upper()

            if double:
                line = "=========================================="
            else:
                line = "------------------------------------------"

            console.print(line)
            console.print("{} [{}, {}]".format(title, self.context, elapsed_str))
            console.print(line)

    def log_info(self, title, value=None, force_log=False):
        if self.logging_enabled or force_log:
            title = (title + ":").ljust(25)
            console.print("{} \t{}".format(title, value))

    def log_info_to_text(self, title, value):
        title = (title + ":").ljust(25)
        text = "{} \t{}".format(title, value)
        return text    