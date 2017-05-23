# Copyright (C) 2015 by Per Unneberg
import re
import pandas as pd
import bioodo
from bioodo import resource, annotate_by_uri, DataFrame, utils
import logging


logger = logging.getLogger(__name__)
config = bioodo.__RESOURCE_CONFIG__['star']


@resource.register(config['log_final']['pattern'],
                   priority=config['log_final']['priority'])
@annotate_by_uri
def resource_star_log(uri, **kwargs):
    df = pd.read_table(uri, sep="|", names=["name", "value"])
    df["name"] = [x.strip() for x in df["name"]]
    df["value"] = [utils.recast(x) for x in df["value"]]
    df = df.set_index("name")
    return df


# Aggregation function
def aggregate(infiles, outfile=None, regex=None, **kwargs):
    """Aggregate individual star reports to one output file

    Params:
      infiles (list): list of input files
      outfile (str): csv output file name
      regex (str): regular expression pattern to parse input file names
      kwargs (dict): keyword arguments

    """
    logger.debug("Aggregating star infiles {} in star aggregate".format(",".join(infiles)))
    df = utils.aggregate_files(infiles, regex=regex, **kwargs)
    if outfile:
        df.to_csv(outfile)
    else:
        return df
