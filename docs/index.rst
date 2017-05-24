.. bioodo documentation master file, created by
   sphinx-quickstart on Thu Oct 13 16:04:58 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

bioodo - odo parser library for bioinformatics
===============================================

bioodo is a parsing library for bioinformatics applications based on
`odo`_. It consists of custom defined `odo backends`_ where odo
resources match URIs to parsing functions based on regular
expressions. A backend parses URIs and transforms them to `pandas
DataFrames`_.

Contents:

.. toctree::
   :maxdepth: 2

   usage
   authors
   history
   modules
	      

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _odo: http://odo.pydata.org/en/latest
.. _odo backends: http://odo.pydata.org/en/latest/add-new-backend.html
.. _pandas DataFrames: https://pandas.pydata.org/pandas-docs/stable/dsintro.html
