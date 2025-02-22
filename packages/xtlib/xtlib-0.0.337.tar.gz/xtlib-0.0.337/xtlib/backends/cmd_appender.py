# cmd_appender.py: shared code for appending commands

from xtlib import constants
from xtlib import pc_utils

class CmdAppender():
    def __init__(self, capture_setup_cmds, add_timestamps, snapshot_dirs) -> None:
        self.capture_setup_cmds = capture_setup_cmds
        self.add_timestamps = add_timestamps
        self.snapshot_dirs = snapshot_dirs
        self.echo_override = None
        self.tracing = False
        self.context = "normal"

    def init_cmds(self):
        cmds = []

        # hide these commands from log (for now)
        cmds.append("# set up tools for script")
        cmds.append("set +x")
        cmds.append("shopt -s expand_aliases")
        cmds.append("alias trace_on='set -x'")
        cmds.append("alias trace_off='{ set +x; } 2>/dev/null'")

        cmds.append("# define the duration function (for a running log timer)")
        cmds.append('duration() {')
        cmds.append(' diff=$(perl -e "print $(date +%s) - $XT_STARTED") ')
        cmds.append(''' if [ $diff -gt 72000 ]; then echo $(perl -e "printf '%.2f %s', $diff/72000, 'days'") ; ''')
        cmds.append(''' elif [ $diff -gt 3600 ]; then echo $(perl -e "printf '%.2f %s',$diff/3600, 'hrs'") ; ''')
        cmds.append(''' elif [ $diff -gt 60 ]; then echo $(perl -e "printf '%.2f %s', $diff/60, 'mins'") ; ''')
        cmds.append(' else echo $diff secs ; fi } ')
        cmds.append(' ')
        cmds.append(' ')
        return cmds

    def set_context(self, value):
        self.context = value

    def sync_trace(self, cmds, value):
        # only change self.tracing and emit trace_on/trace_off HERE to keep them in sync
        if value:
            cmds.append("trace_on")
            self.tracing = True
        else:
            cmds.append("trace_off")
            self.tracing = False

    def append(self, cmds:list, cmd, expand=False, log=None, echo=None, add_time=None):

        if cmd.startswith("timeout"):
            bp = 9

        if add_time is None:
            add_time = self.add_timestamps

        if expand:
            cmd = self.expand_system_names(cmd)

        if log and self.capture_setup_cmds:
            assert isinstance(log, str)

            cmd = "{} > {}/__{}__.log".format(cmd, constants.LINUX_AFTER_LOGS, log)

        if self.echo_override is not None:
            echo = self.echo_override
        elif echo is None:
            echo = True

        truncated_cmd_to_echo = None

        if echo:
            if echo == "old_style":
                use_old_style_echo = True
            else:
                use_old_style_echo = cmd and (cmd.startswith("export") or cmd.startswith("test") or \
                    cmd.startswith("timeout") or (" >" in cmd) or (" |" in cmd))

            if use_old_style_echo:
                # the only problem with this approach is that it makes the script harder to read
                # ensure tracing is off
                echo = False

                # manually echo the command before it is run
                truncated_cmd_to_echo = self.limit_cmd_len_for_echo(cmd)

        # set self.tracing to match echo
        if echo and (not self.tracing):
            cmds.append("")
            self.sync_trace(cmds, True)

        elif (not echo) and self.tracing:
            self.sync_trace(cmds, False)
            cmds.append("")

        if truncated_cmd_to_echo:
            # use singe quotes to AVOID expanding variables
            cmds.append("echo + '{}'".format(truncated_cmd_to_echo))

        # finally, add the cmd to be run
        cmds.append(cmd)

    def limit_cmd_len_for_echo(self, cmd):
        # avoid echo of super long (multiple line) commands
        max_echo_len = 400        
        cmd_text = cmd
        if len(cmd_text) > max_echo_len:
            cmd_text = cmd_text[0:max_echo_len-3] + "..."

        return cmd_text

    def append_echo(self, cmds, cmd, add_time=None):
        cmd_text = self.limit_cmd_len_for_echo(cmd)

        # ECHO the command before it is run 
        cmd_text = "'{}'".format(cmd_text)

        if add_time:
            cmds.append('''echo @$(date +%b-%d-%Y"  "%T)"     "+ {}'''.format(cmd_text))
        else:
            cmds.append('''echo + {}'''.format(cmd_text))

    def append_export(self, cmds, name, value, value_is_windows=False, fix_value=True, echo=None):
        '''
        args:
            - cmds: the set of commands to append the export cmd to
            - name: the name of the environment var to set/export
            - value: the string value (could have $xx or %xx% variables in a list)
            - value_is_windows: if value is windows style (vs. linux style)
        '''
        # ensure value is a str
        value = str(value)

        if fix_value and value_is_windows:
            # need to split value into parts to remove surrounding %
            parts = value.split(";")
            for i, part in enumerate(parts):
                if part.startswith("%") and part.endswith("%"):
                    parts[i] = "$" + part[1:-1] 
            value = ":".join(parts)

        # export causes a double-echo, so we now run with echo=False
        # add quotes around value to handle special chars that shell would otherwise interpret
        cmd = 'export {}="{}"'.format(name, value)

        self.append(cmds, cmd, echo=echo)

    def append_title(self, cmds:list, title, echo=None, double=False, zero_duration=False):
        # skip a line to improve grouping/readability
        #cmds.append("")

        # make it stand out a bit
        title = title.upper()

        if double:
            line = "echo ==============================================================="
        else:
            line = "echo ---------------------------------------------------------------"

        duration_str = "+$(duration)"
        if zero_duration:
            duration_str = "+0 secs"
        
        if self.context:
            extra = '[{}, "{}"]'.format(self.context, duration_str)
        else:
            extra = '["{}"]'.format(duration_str)

        # always hide echo of title 
        self.echo_override = False

        # NOTE: tracing must be off when we evaluate the "duration" function for our elapsed time
        if self.tracing:
            self.sync_trace(cmds, False)

        self.append(cmds, line, echo=False)

        if extra:
            self.append(cmds, 'echo "{} {}"'.format(title, extra), echo=False)
        else:
            self.append(cmds, 'echo "{}"'.format(title), echo=False)
        
        self.append(cmds, line, echo=False)

        # let this title control the echo of its commands (if not None)
        self.echo_override = echo

    def append_dir(self, cmds, path=".", recursive=False, include_hidden=False):
        # limit to 30 lines

        if self.snapshot_dirs:
            display_path = path
            if path == ".":
                display_path += " ($PWD)"

            self.append_title(cmds, "DIR: " + display_path)

            # grep is used to supress the distracting "total" line
            # head is used to limit to 30 lines
            opts = "-R " if recursive else ""
            opts += "-a " if include_hidden else ""
            #cmd = "ls -lt {}{} | grep -vh '^total' | head -n 30".format(opts, path)
            cmd = "ls -l {}{} | grep -vh '^total'".format(opts, path)

            self.append(cmds, cmd, echo=True)

    def expand_system_names(self, cmd:str):
        cmd = cmd.replace("$call ", "")
        cmd = cmd.replace("$export", "export")

        if "$current_conda_env" in cmd:
            conda = pc_utils.get_conda_env() 
            if conda:
                cmd = cmd.replace("$current_conda_env", conda)
        
        return cmd

    def append_unzip(self, cmds, fn_zip, dest_dir, echo=None):
        self.append(cmds, "mkdir -p {}".format(dest_dir))

        # use double quotes around files (vs. single) to improve readability of cmd in log
        self.append(cmds, 'python -c \'import zipfile, os; zipfile.ZipFile(os.path.expandvars("{}")).extractall(os.path.expandvars("{}"))\''. \
            format(fn_zip, dest_dir), echo=echo)

    def append_dir_clean(self, cmds, cwd):
        # remove all files and dirs in the current dir
        self.append(cmds, "rm -rf {}".format(cwd))
