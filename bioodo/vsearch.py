# Copyright (C) 2016 by Per Unneberg
import re
import logging
import pandas as pd
from bioodo import resource, annotate_by_uri, DataFrame, utils
import bioodo

config = bioodo.__RESOURCE_CONFIG__['vsearch']
logger = logging.getLogger(__name__)

SECTION_NAMES = ["Read length distribution", "Q score distribution",
                 "Truncate at first Q"]


@resource.register(config['stats']['pattern'],
                   priority=config['stats']['priority'])
@annotate_by_uri
def resource_vsearch_fastqc_stats(uri, key="Read length distribution", **kwargs):
    """Parse vsearch fastqc_stats text output file.

    Args:
      uri (str): filename
      key (str): result section to return

    Returns:
      DataFrame: DataFrame for requested section
    """
    if key not in SECTION_NAMES:
        raise KeyError("Not in allowed section names; allowed values are {}".format(", ".join(SECTION_NAMES)))
    with open(uri) as fh:
        data = "".join(fh.readlines())
    if key == "Read length distribution":
        m = re.search("Read length distribution\n(?P<header>[a-zA-Z\s]+)\n[\s\-]+\n(?P<data>.*)Q score", data, re.DOTALL)
        indexcol = "L"
    elif key == "Q score distribution":
        m = re.search("Q score distribution\s*\n(?P<header>[a-zA-Z\s]+)\n[\s\-]+\n(?P<data>.*)\n\s+L\s+PctRecs", data, re.DOTALL)
        indexcol = "Q"
    elif key == "Truncate at first Q":
        m = re.search("Truncate at first Q\s*\n(?P<header>[0-9=a-zA-Z\s]+)\n[\s\-]+\n(?P<data>.*)\n\n\s+\d+\s+Recs", data, re.DOTALL)
        indexcol = "Len"
    else:
        logger.warn("No such key '{}'".format(key))
    try:
        header = re.split("\s+", m.group("header").strip())
        if key == "Read length distribution":
            d = [re.split("\s+", re.sub("[><=]+", "", x).strip()) for x in re.split("\n", m.group("data").strip())]
        else:
            d = [re.split("\s+", x.strip()) for x in re.split("\n", m.group("data").strip())]
        df = DataFrame.from_records(d, columns=header)
        df = df.apply(pd.to_numeric, errors='ignore')
        df = df.set_index(indexcol)
    except:
        raise
    return df


# Aggregation function
def aggregate(infiles, outfile=None, regex=None, **kwargs):
    """Aggregate individual vsearch reports to one output file

    Args:
      infiles (list): list of input files
      outfile (str): csv output file name
      regex (str): regular expression pattern to parse input file names
      kwargs (dict): keyword arguments

    """
    logger.debug("Aggregating vsearch infiles {} in vsearch aggregate".format(",".join(infiles)))
    df = utils.aggregate_files(infiles, regex=regex, **kwargs)
    if outfile:
        df.to_csv(outfile)
    else:
        return df
