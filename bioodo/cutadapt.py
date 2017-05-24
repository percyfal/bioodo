# Copyright (C) 2015 by Per Unneberg
import re
import pandas as pd
import logging
import bioodo
from bioodo import resource, annotate_by_uri, DataFrame, utils

logger = logging.getLogger(__name__)
config = bioodo.__RESOURCE_CONFIG__['cutadapt']


# Potentially add regexp for adapter sections as these are repetitive
adapter_re = re.compile(r'''
===\s*(?P<Read>(First read|Second read)?):?\s+Adapter\s+'(?P<Adapter>[^\s]+)'\s+===
''')

re_trim = re.compile(r'(\([0-9.]+%\)|,| |bp)')


def _split_x(x, delim=":"):
    y = x.strip().split(delim)
    return [y[0], re_trim.sub("", y[1])]


# For now only return the summary section
@resource.register(config['metrics']['pattern'],
                   priority=config['metrics']['priority'])
@annotate_by_uri
def resource_cutadapt_metrics(uri, **kwargs):
    with open(uri) as fh:
        data = "".join(fh)
    sections = re.split("\n===.*===\n", data)
    df = DataFrame.from_records([_split_x(x) for x in sections[1].split("\n") if x],
                                index=["statistic"], columns=["statistic", "value"])
    df["value"] = pd.to_numeric(df["value"])
    return df


# Aggregation function
def aggregate(infiles, outfile=None, regex=None, **kwargs):
    """Aggregate individual cutadapt reports to one output file

    Args:
      infiles (list): list of input files
      outfile (str): csv output file name
      regex (str): regular expression pattern to parse input file names
      kwargs (dict): keyword arguments

    """
    logger.debug("Aggregating cutadapt infiles {} in cutadapt aggregate".format(",".join(infiles)))
    df = utils.aggregate_files(infiles, regex=regex, **kwargs)
    if outfile:
        df.to_csv(outfile)
    else:
        return df
