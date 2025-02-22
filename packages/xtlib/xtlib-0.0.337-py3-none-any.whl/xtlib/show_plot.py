# show_plot.py: this runs as a detached process to show a plot from its pickled form
import os
import sys
import matplotlib.pyplot as plt
import pickle

from xtlib import plot_helper

def show_plot_from_file(fn_plot, hide_toolbar):

    if hide_toolbar:
        # hide the toolbar
        plt.rcParams['toolbar'] = 'None'

    with open(fn_plot, 'rb') as file:
        fig = pickle.load(file)

    # Ensure the loaded figure is the current figure
    plt.figure(fig.number)

    # Display the plot
    print("showing plot from show_plot_from_file ")
    plt.show()

    # remove the file
    os.remove(fn_plot)

if __name__ == "__main__":
    #print("hi from show_plot.py")

    if len(sys.argv) < 2:
        print("usage: show_plot <chart .pkl file>")
        exit(1)
        
    # Load the figure from a file
    fn_plot = sys.argv[1]

    if len(sys.argv) > 2:
        hide_toolbar = (sys.argv[2] == "True")
    else:
        hide_toolbar = False

    show_plot_from_file(fn_plot, hide_toolbar)

