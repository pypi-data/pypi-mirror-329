.. _seaborn_plotting:

======================================
Seaborn Plotting with XT
======================================

This page gives an overview of using the Seaborn plotting library with the XT.

.. image:: ../images/barplot.png
  :width: 600
  :alt: a bar plot with 10 vertical bars, whose height reflects the test accuracy for each run

======================================
The XT Approach to Seaborn Plotting
======================================

Our goal is to enable users to take cool seaborn visualizations that they find on the web and to be able to reproduce them with 
the XT seaborn command, based on run data from their jobs.  This can usually be acoomplished by plotting a one or more layers (see
the **Multiple Layers** section below), but some plots may require custom python code (see the **Custom Code** section at the bottom of this page).

The options for the seaborn command include the arguments passed to the seaborn plotting functions, along with some extra
options to shape the dataframe, and control other aspects of the overall plot (legend, title, theme, style, etc.)

======================================
Data Sources
======================================

The XT seaborn command helps the user create ad-hoc plots of logged metrics across 1 or more runs.  The general syntax is:   
    - xt seaborn <data name> <options>

The <data name> is typically the name of a job or run (e.g., job441 or run441.3), but it can also be:

    - sample_run
    - sample_job
    - name/path of a .csv file
    - the name of one of the seaborn built in datasets:
        - anagrams      
        - anscombe      
        - attention     
        - brain_networks
        - car_crashes   
        - diamonds      
        - dots
        - dowjones      
        - exercise      
        - flights       
        - fmri
        - geyser        
        - glue
        - healthexp     
        - iris
        - mpg
        - penguins      
        - planets       
        - seaice        
        - taxis
        - tips
        - titanic

    The "sample_run" is data from a simulated run, created to help you try out seaborn plots without having to rely on using 
    actual run data.

    The "sample_job" is a data from a simulated job, created for the same purpose.  It contains the simulated results of a grid search 
    across 2 hyperparameters, using 5 seeds each:

        - hparam1 (3 values)
        - hparam2 (2 values)

    So, for each of the 6 combination of hyperparameter values, we create 5 runs (with different random seeds), for a total of 30 runs.  We 
    will use sample_run and sample_job for our below plots, so you can get the same results as our examples.


--------------------------
Plotting Summary Data
--------------------------

When you specify a job or run name for the <data name>, by default you get a summary record for each run (or the single run).  For plotting with 
the step-by-step metric detail, see the below section on **Plotting Detail Data**.

The summary record will include:
    - general run information (columns like job_id, run_name, creation time, etc.)
    - logged hyperparameters (each hyperparameter as a column)
    - the final set of logged metrics for the run (each metric as a column)

In general, you can pass any column name as one of the following seaborn command options:
    - x 
    - y 
    - hue 
    - groupby


-----------------------------------------------------------------------------------------------
Bar Plot  (`Seaborn barplot <https://seaborn.pydata.org/generated/seaborn.barplot.html>`_)
-----------------------------------------------------------------------------------------------

Let's try one of the simplest plots, a barplot.  We'll start with this example from the web (https://seaborn.pydata.org/generated/seaborn.barplot.html).  
Since this is our first plot, let's try to reproduce the web sample exactly, using the "penguins" dataset:

    > ``xt seaborn penguins --type=barplot --x=island --y=body_mass_g``

.. image:: ../images/penguins1.png
  :width: 600
  :alt: a bar plot 3 bars whose height represent the average body mass of penguins on the associated 3 island

Now, let's use run data from sample_job:

    > ``xt seaborn sample_job --type=barplot --y=valid_acc``

.. image:: ../images/fat_barplot.png
  :width: 600
  :alt: a bar plot with a single fat bar

What happened in the above plot?  By default, seaborn averages all of the y data into a single bar.  Let's try 
averaging the valid_acc of the runs by the value of hparam1:

    > ``xt seaborn sample_job --type=barplot --y=valid_acc --x=hparam1``

.. image:: ../images/barplot3.png
  :width: 600
  :alt: a bar plot with 3 bars

If you want to check on the columns and typical values in your data, you can use the --head and/or --tail 
options to show the first and last 5 records of your dataframe on the console, before displaying your plot:

    > ``xt seaborn sample_job --type=barplot --y=valid_acc --x=hparam1 --head``

.. image:: ../images/head.png
  :width: 600
  :alt: the first 5 records displayed as text


For bar plots, we can also group by a second column, using the --hue option:

    > ``xt seaborn sample_job --type=barplot --y=valid_acc --x=hparam1 --hue=hparam2``

.. image:: ../images/barplot_hue.png
  :width: 600
  :alt: a bar plot with 3 groups of 2 bars

Sometimes you will need a horizontal bars (e.g., when you are having trouble fitting all your x labels without overlap).  You are use 
the --orient option for this, but you have to swap the x and y columns:

    > ``xt seaborn sample_job --type=barplot --x=valid_acc --y=hparam1 --orient=h``

.. image:: ../images/barplot_h.png
  :width: 600
  :alt: a horizontal bar plot


--------------------------
More Plot Types
--------------------------

**Scatter Plot** (`Seaborn scatterplot <https://seaborn.pydata.org/generated/seaborn.scatterplot.html>`_)

    > ``xt sea sample_job --type=scatterplot --x=train_acc --y=valid_acc --hue=hparam2 --loc="upper left" --anchor=1,1 --tight``

.. note::
  In some commands, the legend is automatically placed on the outside right of the plot.  In scatterplot it isn't, so 
  we have chosen to specify it thru the XT direct options ``--loc`` and ``--anchor``.  Also, the ``--tight`` layout is needed
  to make everything work together correctly.

.. image:: ../images/scatter.png
  :width: 600
  :alt: a scatterplot of train_acc vs. valid_acc for the sample runs in sample_job

**Category Plot** (`Seaborn catplot <https://seaborn.pydata.org/generated/seaborn.catplot.html>`_)

    > ``xt sea sample_job --type=catplot --y=hparam1 --x=valid_acc --hue=hparam2 --kind=boxen``

.. note:: 
  The catplot uses the ``--kind`` value to determine the base plot type that is repeated as appropriate for this plot.
  
.. image:: ../images/catplot.png
  :width: 600
  :alt: a scatterplot of train_acc vs. valid_acc for the sample runs in sample_job

**Relational Plot** (`Seaborn relplot <https://seaborn.pydata.org/generated/seaborn.relplot.html>`_)

    > ``xt sea sample_job --type=relplot --x=train_acc --y=valid_acc --hue=hparam2 --col=hparam1``

.. note:: 
  The relplot uses the optional ``--col`` to create a facet graph, a separate plot for each value of the specified column, 
  in a grid layout. 
  
.. image:: ../images/relplot.png
  :width: 900
  :alt: a scatterplot of train_acc vs. valid_acc for the sample runs in sample_job

**Histogram** (`Seaborn histplot <https://seaborn.pydata.org/generated/seaborn.histplot.html>`_)

    > ``xt sea sample_job --type=histplot --x=valid_acc``

.. image:: ../images/histplot.png
  :width: 600
  :alt: a histogram plot of valid_acc

**Strip Plot** (`Seaborn stripplot <https://seaborn.pydata.org/generated/seaborn.stripplot.html>`_)

    > ``xt sea sample_job --type=stripplot --x=valid_acc --hue=hparam1``

.. image:: ../images/stripplot.png
  :width: 600
  :alt: a strip plot plot of valid_acc


**Swarm Plot** (`Seaborn swarmplot <https://seaborn.pydata.org/generated/seaborn.swarmplot.html>`_)

    > ``xt sea sample_job --type=swarmplot --x=valid_acc --hue=hparam1``

.. image:: ../images/swarmplot.png
  :width: 600
  :alt: a swarm plot plot of valid_acc

**Box Plot** (`Seaborn boxplot <https://seaborn.pydata.org/generated/seaborn.boxplot.html>`_)

    > ``xt sea sample_job --type=boxplot --x=valid_acc --y=hparam1``

.. image:: ../images/boxplot.png
  :width: 600
  :alt: a box plot plot of valid_acc

**Violin Plot** (`Seaborn violin <https://seaborn.pydata.org/generated/seaborn.violinplot.html>`_)

    > ``xt sea sample_job --type=violinplot --x=valid_acc --y=hparam1``

.. image:: ../images/violinplot.png
  :width: 600
  :alt: a violin plot plot of valid_acc

**Boxen Plot** (`Seaborn boxenplot <https://seaborn.pydata.org/generated/seaborn.boxenplot.html>`_)

    > ``xt sea sample_job --type=boxenplot --x=valid_acc --y=hparam1 --detail``

.. image:: ../images/boxenplot.png
  :width: 600
  :alt: a boxen plot plot of valid_acc detail for all runs in the job

**Point Plot** (`Seaborn pointplot <https://seaborn.pydata.org/generated/seaborn.pointplot.html>`_)

    > ``xt sea sample_job --type=pointplot --x=valid_acc --y=hparam1``

.. image:: ../images/pointplot.png
  :width: 600
  :alt: a point plot plot of valid_acc detail for all runs in the job

**Heat Map** (`Seaborn heatmap <https://seaborn.pydata.org/generated/seaborn.heatmap.html>`_)

    > ``xt sea sample_job --type=heatmap --pivottable=hparam1, hparam2, valid_acc --annot=1``

.. note::
  The heatmap plot requires that the data be pre-aggregated and in pivot table format.  If ``--pivottable`` is 
  specified without specifying ``--aggfunc`` (the type of aggregation to be done), ``--aggfunc`` defaults to 
  "mean".  With ``--pivottable``, here we specify the 3 columns that we want to 
  preserve for plotting, with the last column being the numeric value used to color (and optionally 
  annotate) each cell in the heatmap.

.. image:: ../images/heatmap.png
  :width: 600
  :alt: a heatmap of valid_acc values in a table of hparam1, hparam2 values

**Pair Plot** (`Seaborn pairplot <https://seaborn.pydata.org/generated/seaborn.pairplot.html>`_)

    > ``xt sea sample_job --type=pairplot --drop=step --hue=hparam1``

.. note::
  Here we use the ``--drop`` option to remove the step column, so that the pair columns don't use it
  (since they use all numeric columns in the dataframe).

.. image:: ../images/pairplot.png
  :width: 600
  :alt: a pairplot of metrics, colored by the values of hparam1

--------------------------
Plotting Lines
--------------------------

There are times when we want to track what happens in the course of training.  We can specify the --detail option to create a DataFrame of the run with multiple 
records (vs. a single summary record).  A detail record will be created for each unique step value in the logged metrics for the run, for the metric columns 
being plotted.  Here is a simple example of a line plot (`Seaborn lineplot <https://seaborn.pydata.org/generated/seaborn.lineplot.html>`_) 
by specifying a single metric column for a single run:

    > ``xt sea sample_run --type=lineplot --x=step --y=valid_acc --detail``

.. image:: ../images/lineplot.png
  :width: 600
  :alt: a line plot of valid_acc

If we want to look at the detail across steps for "valid_acc" in all runs of our job, grouped and averaged
by the values of hparam1, we can use the following command:

    > ``xt sea sample_job --type=lineplot --x="step" --y=valid_acc --select step, hparam1, valid_acc --x=step --y=valid_acc  --hue=hparam1 --detail --head  --dropna=1``

.. note::
  Here, we have selected (extracted) the 3 colums step, hparam1, and valid_acc. We also specify ``--head`` so we can preview the data at various stages
  and ``--dropna`` to drop rows with NAN values.  We have NAN values because we form our initial dataframe from metrics with varying step values: the train
  metrics are logged by our job at every step, but the valid metrics are only logged every 5 steps.  Sometimes the seaborn plotting functions 
  get tripped up on columns with NAN values, as is the case here, so we explictly remove them.

.. image:: ../images/lineplot_runs.png
  :width: 600
  :alt: a line plot of train_acc for 3 hparam1 values, with stderr bands around each line

Let's say we want to plot train_loss, valid_loss, train_acc, valid_acc each in their own plot, averaging metrics over runs by their hparam1 value.  
That can be done with the relplot function:

  > ``xt sea sample_job --detail --select step, hparam1, train_loss, train_acc, valid_loss, valid_acc --melt=step, hparam1 --type=relplot 
  --x=step --y=value --col=variable --dropna --kind=line --hue=hparam1 --col_wrap=2 --facet_kws={--sharex=1 --sharey=0 } --head``

.. note::
  Here, we have request the sample_job detail, select the columns step (for x), hparam1 (for coloring), and the 4 metrics.  We melt the result, 
  and plot using the variable and value names that represent the long-format metrics.  Specifying ``--col=variable`` produces our 4 plots and we 
  specify ``--kind=line`` to plot lines.  We use ``--hue=hparam1`` to create separate lines for each hparam1 value.  We set ``--col_wrap=2`` to 
  form a 2x2 grid from our 4 plots.  We pass ``--sharex=1`` and ``--sharey=0`` to the underlying FacetGrid plot in order to let loss and accuracy 
  plots to have their own y scales.  With long commands like this one, we suggest you make use of the XT command templates to make the command
  easier to remember and invoke (using only the parameters you need to change).

.. image:: ../images/relplot_x4.png
  :width: 900
  :alt: a 2x2 plot grid for train_loss, valid_loss, train_acc, valid_acc as average lines with error shadows

--------------------------
Multiple Layers
--------------------------

The seaborn command has the ability to draw multiple layers on a plot, where each layer is a different plot type.  To 
plot multiple layers, you should separate the options for each layer by the --layer option.
Also, each layer should explictly include its plot type using the --type option.  Finally, add any non-plot function options.

Here is an example of a barplot on the first layer, and a striplot on the 2nd layer:

    > ``xt seaborn sample_job --ci=0 --type=barplot --y=valid_acc --x=hparam1 --layer --type=stripplot --x=hparam1 --y=valid_acc --linewidth=1.5 --ymin=0``

.. image:: ../images/layers.png
  :width: 600
  :alt: a barplot with the individual data points overlaid on the top of each bar

.. note::
  Notice in the above that the only direct XT option for the command, ``--ymin``, appears after the last option for the last layer.  This ordering 
  is required when using multiple layers.  ``--ymin`` is needed here to ensure that both layers were aligned at y==0.  Also, ``--ci=0`` (confidence interval
  is specified to remove the error bars on the bar plot.  

--------------------------
Data Shaping Options
--------------------------

The XT seaborn command offers several options for shaping your data before it is plotted:

  --detail    include the detail logged metric records in each run
  --melt      convert the dataframe from wide to long format.  more info here: `Pandas melt docs <https://pandas.pydata.org/docs/reference/api/pandas.melt.html>`_
  --select    extract only the specified columns to form the new dataframe
  --drop      delete the specified columns to form the new dataframe
  --dropna    delete rows containing NAN values
  --groupby   group the dataframe rows by the specified columns
  --aggfunc       apply the specified aggregation function to a grouped dataframe, one of: min, max, sum, mean, median, mode
  --ungroup   convert a grouped dataframe back to its flat form
  --pivot     convert the dataframe to a pivot form (without aggregation).  more info here: `Pandas pivot docs <https://pandas.pydata.org/docs/reference/api/pandas.pivot.html>`_
  --pivottable  create a pivot dataframe using the specified columns, aggregating the dataframe using the --aggfunc operation
  --head      print out first few records of the dataframe to the console
  --tail      print out last few records of the dataframe to the console

--------------------------
Styles and Sizes
--------------------------

The XT seaborn command offers a few options for controlling the look and size of your visualization:

  --context   sets the seaborn context, to control the scaling of the plot. must be 1 of: paper, notebook, talk, and poster
  --style     sets the seaborn style, to control the look of the plot.  must be 1 of: darkgrid, whitegrid, dark, white, and ticks
  --theme     this is a bool flag to turn the all of the seaborn styling on/off (default is True)

--------------------------
Frame Level Options
--------------------------

The XT seaborn command offers several options for controlling the frame-level items of your visualization:

  --anchor        sets the legend starting point, which is normally 0,0.  To place the legend to the right of the plot, use --anchor=1,1
  --loc           sets the legend position (relative to its starting point).  See the 'loc' arg in the `matplotlib docs for legend <https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.legend.html#matplotlib.axes.Axes.legend>`_
  --legendcolor   sets the background color of the legend
  --gridcolor     sets the plot's background color
  --title         sets the title of the overall plot
  --tight         when set, the matplotlilb tight layout will be used.  more info here: `matplotlib tight layout <https://matplotlib.org/stable/tutorials/intermediate/tight_layout_guide.html>`_
  --xmin          sets the minimum value shown on the x axis
  --xmax          sets the maximum value shown on the x axis
  --ymin          sets the minimum value shown on the y axis
  --ymax          sets the maximum value shown on the y axis
  --layer         this marks the start of a new layer in the list of specified seaborn command options (see the Multiple Plot Layers section above)
  --type          this specifies the name of the seaborn plot to be used.  it must be specified for each layer defined.
  
--------------------------
Pass-Thru Options
--------------------------
   
The above 3 sections comprise the directly supported options for the seaborn command.  Any other options that you specify are passed thru to 
the associated seaborn plot function (determined by the ``--type`` option).  In a similiar fashion, the seaborn plot function processes a subset of the arguments 
passed to it, and passes the remaining arguments to the underlying matplotlib plot function.

Some of the seaborn plotting function accept a named argument ending in "_kws", like ``facet_kws``, that can be used to pass a set of options to a specific downstream 
function.  You can specify a set of embedded options for these types of arguments, by surrounding the options with curly braces, and using backquotes for
string values with spaces or special characters, as in the following example:

  > ``xt seaborn sample_job --type=catplot --facet_kws={--margin_titles=1 --legend_out=0 --palette=red, green, `light blue`}``

Note that nested embedded options are not currently supported by XT.  

So, to gain more control over your plotting, you should refer to the Seaborn docs for the plot type you are using, as well as the MatPlotLib docs for 
controlling alpha blending, marker types, edges, etc.  Here are some of the docs to get you started:

`MatPlotLib Markers' <https://matplotlib.org/stable/api/markers_api.html>`_

`MatPlotLib Colors <https://matplotlib.org/stable/gallery/color/named_colors.html>`_ 

`MatPlotLib Line Styles <https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html>`_ 

`MatPlotLIb Alpha Blending <https://matplotlib.org/stable/gallery/images_contours_and_fields/image_transparency_blend.html>`_ 

--------------------------
Custom Code
--------------------------

Finally, when the seaborn command cannot meet your plotting needs, you can use the XT API to create a Pandas Dataframe for your job or run.  Here is 
an example of a complete python program that creates a custom Seaborn plot, based on their kdeplot (`Seaborn kdeplot <https://seaborn.pydata.org/generated/seaborn.kdeplot.html>`_) 

.. code-block:: python

    # custom_plot.py: shows how to create a seaborn plot using the XT API 
    import seaborn as sns
    import matplotlib.pyplot as plt
    from xtlib import run_helper

    job_id = "job895"
    metric_names = ["train-acc", "test-acc"]

    # call XT to create a Pandas dataframe from the job data
    df = run_helper.get_run_records_as_dataframe(job_id=job_id, include_hparams=True, metric_names=metric_names, detail=False, melt=False)

    sns.set_theme()

    for col in metric_names:
        sns.kdeplot(df[col], shade=True)

    plt.legend(labels=["train-acc", "test-acc"], bbox_to_anchor=(1, 1), loc="upper left")
    plt.tight_layout()
    plt.show()

Here is the plot resulting from running the above code:

.. image:: ../images/custom_plot.png
  :width: 600
  :alt: a bimodal density chart with a legend outside the plot

.. seealso:: 

    - :ref:`XT seaborn command <seaborn>`
    - `Seaborn data visualization library <https://seaborn.pydata.org/index.html>`_
    - :ref:`XT plot command <plot>`
    - :ref:`Plotting with XT <plotting>`
    - `MatPlotLib plot command <https://seaborn.pydata.org/index.html>`_
