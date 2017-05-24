.. _usage:

=====
Usage
=====

To use biodo, import a parsing module for the bioinformatics
application of interest and apply the odo function on a given output
file:

.. code-block:: python

    from bioodo import star, odo, DataFrame
    df = odo(str("/path/to/Log.final.out"), DataFrame)

Output files can also me aggregated with function
`:py:func:bioodo.utils.aggregate_files`.



Resource configuration
-----------------------
