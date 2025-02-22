# plot_helper.py: common code used by plots in XT
import os
import sys
import pickle
import subprocess
import tempfile

def show_plot(show_detached=False, hide_toolbar=False):

    import matplotlib.pyplot as plt

    if show_detached:
        fig = plt.gcf()

        # Save the figure object to a temp file
        wrapper = tempfile.NamedTemporaryFile(delete=False, suffix='.pickle')
        fn_plot = wrapper.name
        #print("fn_plot=", fn_plot)deee

        with open(fn_plot, 'wb') as tmpfile:
            pickle.dump(fig, tmpfile)

        plt.close(fig)  # Close the plot window

        # Launch a detached process to show the plot
        fn_show_plot = os.path.dirname(__file__) + "/show_plot.py"
        command = [sys.executable, fn_show_plot, fn_plot, str(hide_toolbar)]

        p = subprocess.Popen(command, #stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)

        # while p:
        #     output = p.stdout.readline()
        #     print(output)

        #print("opened plot in detached window")

    else:
        plt.show()

