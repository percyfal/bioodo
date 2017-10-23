# Copyright (C) 2016 by Per Unneberg
import re
import logging
import bioodo
from bioodo import resource, annotate_by_uri, pivot, DataFrame, utils
import pandas as pd

logger = logging.getLogger(__name__)
config = bioodo.__RESOURCE_CONFIG__['sga']


@resource.register(config['preprocess']['pattern'],
                   priority=config['preprocess']['priority'])
@pivot
@annotate_by_uri
def resource_sga_preprocess(uri, **kwargs):
    """Parse sga preprocess log output file.

    Args:
      uri (str): filename

    Returns:
      DataFrame: DataFrame for requested section
    """
    logger.debug("Parsing {} in resource_sga_preprocess".format(uri))
    with open(uri) as fh:
        data = "".join(fh)
    sections = re.split("Preprocess stats:\n", data)
    parameters = [["parameter"] +
                  [x.strip() for x in y.strip().split(":")]
                  for y in re.sub("Parameters:\n", "", sections[0]).split("\n")
                  if ":" in y]
    preprocess = [["preprocess stats"] +
                  [x.strip() for x in y.strip().split(":")]
                  for y in re.sub("\([0-9\.]+\)", "", sections[1]).split("\n")
                  if y and "wall" not in y]
    df = DataFrame.from_records(parameters + preprocess,
                                columns=["type", "statistic", "value"])
    df = df.set_index('statistic')
    df["value"] = df["value"].apply(pd.to_numeric, errors="ignore")
    return df


@resource.register(config['filter']['pattern'],
                   priority=config['filter']['priority'])
@pivot
@annotate_by_uri
def resource_sga_filter(uri, **kwargs):
    """Parse sga filter log output file.

    Args:
      uri (str): filename

    Returns:
      DataFrame: DataFrame for requested section
    """
    logger.debug("Parsing {} in resource_sga_filter".format(uri))
    with open(uri) as fh:
        data = [[y for y in x.strip().split(":")]
                for x in fh.readlines() if x.startswith("Reads")]
    df = DataFrame.from_records(data, columns=["statistic", "value"])
    df = df.set_index('statistic')
    df["value"] = df["value"].apply(pd.to_numeric, errors="ignore")
    return df


aggregate = utils.aggregate_factory("sga")
