.. _usage:

=====
Usage
=====

To use biodo, import a parsing module for the bioinformatics
application of interest and apply the odo function on a given output
file. The following example uses the star module to parse a star
output log file:

.. code-block:: python

    from bioodo import star, odo, DataFrame
    df = odo("/path/to/Log.final.out", DataFrame)

odo parses the output file by seamlessly invoking the star resource
function :meth:`bioodo.star.resource_star_log` and returns a pandas
DataFrame object.

Output files can also be aggregated with function
:func:`bioodo.utils.aggregate`:

.. code-block:: python

   from bioodo import star, odo, DataFrame
   df = star.aggregate(['/path/to/sample1/Log.final.out',
		        '/path/to/sample2/Log.final.out'],
			annotate=True)

Here, two output files will be aggregated. Data provenance is tracked
through the `annotate` option, which will cause the aggregation
function to add an additional column named `uri` in which the uris
themselves will be stored (`/path/to/sample1/Log.final.out` and
`/path/to/sample2/Log.final.out` in this case).

Alternatively, data provenance can be tracked via a custom parsing of
the uri by passing a regex to the `regex` option:

.. code-block:: python

   from bioodo import star, odo, DataFrame
   df = star.aggregate(['/path/to/sample1/Log.final.out',
		        '/path/to/sample2/Log.final.out'],
			regex=".*/(?P<sample>sample[0-9]+/Log.final.out)")

Here, an additional column `sample` will be added, in which matches to
the regular expression pattern will be stored (`sample1` and `sample2`
in this case).

Finally, data can be pivoted on the fly to convert between wide and
long format. For instance, the following code block will pivot the
data frame to contain observations (sample) in rows and variables
(statistic) in columns.

.. code-block:: python

   from bioodo import star, odo, DataFrame
   df = odo("/path/to/sample1/Log.final.out", DataFrame,
            regex=".*/(?P<sample>sample[0-9]+)/.*",
	    index="sample", columns="stastic", value="value")

See the docstrings for further examples.



Resource configuration
-----------------------

New backends are added to odo by applying a decorator
:py:func:`resource.register` to a function that parses output. The decorator
takes as a mandatory argument a regular expression pattern, and
optionally a priority number that is used to resolve ambiguous
matches:

.. code-block:: python

   @resource.register('.*.txt', priority=10)
   def resource_application_command(uri, **kwargs):
       """Parse application_command output file"""
       # parsing code follows here


In bioodo, the regular expression patterns are actually loaded from
the resource configuration file `bioodo/data/config.yaml` and accessed
via a global config variable
:any:`bioodo.__init__.__RESOURCE_CONFIG__`. The configuration consists
of application sections and resource subsections under which pattern
and priority are defined:

.. code-block:: yaml

   application:
     resource:
       pattern: '.*foo|.*bar'
       priority: 10

See `bioodo/data/config.yaml` for default settings.
       
The default configuration can be modified through a user-defined
configuration file named `.bioodo.yaml`, located either in the user
home directory or in the working directory. Consequently, the patterns
and priorities can be configured to suit whatever file naming
convention the user has in mind.

.. _resource.register: http://odo.pydata.org/en/latest/add-new-backend.html#resource
