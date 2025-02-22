.. _hp_set_column:

=====================================================
The hp_set Column for Runs
=====================================================

This page introduces the hp_set column created for each run, and how it can be used in the ``list runs`` and plotting commands.

The hp_set column is part of the run_info table record created for each run.  hp_set is a string     
version of a dictionary containing the hyperparameters (and their associated values) for the run.  If this run
was produced by the XT hyperparameter search process, the hyperparameters are those returned by the 
search process.  Otherwise, the full set of logged hyperparameters for the run are used, if they exist.

The value of the --hp-set-display option of the ``list runs`` command controls how the hp_set is used and formatted in the report:

    - **changed**                 (hp_set is filtered to only include hyperparameters that change in 1 or more runs within the report)
    - **full**                    (hp_set is unchanged)
    - **simple**                  (hp_set is changed to a simple name corresponding the unique set of values, e.g., hp_set_3)
    - **columns**                 (adds a new column to the report for each changed hyperparameter)
    - **user-columns**            (adds a new column for changed hyperparameter if column has been specified by user, e.g., run-reports, named-columns, etc.)
    - **simple_plus_columns**     (adds a column for each changed hyperparameter, and a column for the hp_set value)
    - **hidden**                  (the hp_set column is not shown in the columns of the report)

-------------------------------------------
Grouping Run and Plot records by hp_set
-------------------------------------------

When your job includes multiple runs of the same hyperparameter set of values, you can use ``--group=hp_set`` to group and average 
metrics of interest, so you can see your different hyperparameter values impact your runs' metrics.

.. seealso:: 

    - :ref:`XT list runs command <list_runs>`
    - :ref:`XT plot command <plot>`
    - :ref:`XT seaborn command <seaborn>`
    - :ref:`Plotting with XT <plotting>`
