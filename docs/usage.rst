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
function :func:`bioodo.star.resource_star_log` and returns a pandas
DataFrame object.

Output files can also be aggregated with function
:func:`bioodo.utils.aggregate`. See the docstring for examples.



Resource configuration
-----------------------

New backends are added to odo by applying a decorator
`resource.register` to a function that parses output. The decorator
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
via a global config variable :any:`bioodo.__RESOURCE_CONFIG__`. The
configuration consists of application sections and resource
subsections under which pattern and priority are defined:

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
