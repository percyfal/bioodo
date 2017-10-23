# Copyright (C) 2015 by Per Unneberg
import logging
import re
import pandas as pd
from functools import wraps
from blaze import append, DataFrame

logger = logging.getLogger(__name__)


@append.register(DataFrame, DataFrame)
def append_dataframe_to_dataframe(tgt, src, **kw):
    tgt = pd.concat([tgt, src])
    return tgt


def annotate_by_uri(func):
    """Decorator function annotate_by_uri.

    Wrap function with wrapper that will optionally add an annotation
    to the data frame based on the uri. This can be particularly
    useful when merging several files and the data provenance needs to
    be tracked.

    Example:

      The following example parses a qualimap output file and
      annotates the resulting data frame with the uri:

      .. code-block:: python

         from bioodo import qualimap, odo
         df = odo("Sample1/genome_results.txt", annotate=True)

      The data frame will contain an extra column named "uri" with the
      value "Sample1/genome_results.txt".

      Alternatively, we can use a regular expression to parse the uri:

      .. code-block:: python

         from bioodo import qualimap, odo
         df = odo("Sample1/genome_results.txt",
                  regex="(?P<sample>Sample[0-9]+)/(?P<file>.*)")

      Here, the data frame will contain two extra columns, "sample"
      with value "Sample1", and "file" with value "genome_results.txt".


    Args:
      annotate (bool): whether or not to annotate data frame
      annotation_fn (function): use custom function to annotate data frame
      regex (str): use regular expression to annotate data frame

    """
    def default_annotation_fn(df, uri, **kwargs):
        logger.debug("Annotating dataframe with uri {}".format(uri))
        df['uri'] = uri

    def regex_annotation_fn(df, uri, regex, **kwargs):
        logger.debug("Searching uri {} with regex {}".format(uri, regex))
        m = re.search(regex, uri)
        if m:
            logger.debug("adding columns {}".format(
                ",".join(["{}={}".format(k, v)
                          for k, v in m.groupdict().items()])))
            for k, v in m.groupdict().items():
                df[k] = v

    @wraps(func)
    def wrap(uri, **kwargs):
        df = func(uri, **kwargs)
        regex = kwargs.get('regex', None)
        annotation_fn = kwargs.get('annotation_fn', None)
        annotate_default = regex is not None or annotation_fn is not None
        annotate = kwargs.get('annotate', annotate_default)
        if not annotate:
            return df
        if regex is not None:
            annotation_fn = regex_annotation_fn
        else:
            annotation_fn = kwargs.get('annotation_fn', default_annotation_fn)
        annotation_fn(df, uri, **kwargs)
        return df
    return wrap


def pivot(func):
    """Decorator function pivot.

    Wrap function with wrapper that will pivot a data frame to wide
    format.

    Example:

      The following example parses a qualimap output file and
      annotates the resulting data frame with a regex, at the same
      time pivoting the data frame so that the sample column is used
      to construct the new index.

      .. code-block:: python

         from bioodo import qualimap, odo
         df = odo("Sample1/genome_results.txt",
                  regex=="(?P<sample>Sample[0-9]+)/(?P<file>.*)",
                  index="sample",
                  columns="statistic",
                  values=["value"])


    The arguments are identical to those in
    :meth:`pandas.DataFrame.pivot`.

    Args:
      index (str): Column name to use to make new frame’s index. If
                   None, uses existing index.
      columns (str): Column name to use to make new frame’s columns
      values (str, list): string or list. Column name to use for
                          populating new frame’s values. If not
                          specified, all remaining columns will be
                          used and the result will have hierarchically
                          indexed columns

    """
    @wraps(func)
    def wrap(uri, **kwargs):
        df = func(uri, **kwargs)
        columns = kwargs.get('columns', None)
        index = kwargs.get('index', None)
        values = kwargs.get('values', None)
        if columns is None and index is None and values is None:
            return df
        if isinstance(values, list):
            dfdict = {k: df.pivot(index=index, columns=columns, values=k)
                      for k in values}
            return pd.concat(dfdict.values(), axis=1, keys=dfdict.keys())
        else:
            return df.pivot(index=index, columns=columns, values=values)
    return wrap
