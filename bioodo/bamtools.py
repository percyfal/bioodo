# Copyright (C) 2016 by Per Unneberg
import logging
import pandas as pd
import re
import bioodo
from bioodo import resource, annotate_by_uri, DataFrame, utils

logger = logging.getLogger(__name__)
config = bioodo.__RESOURCE_CONFIG__['bamtools']


@resource.register(config['stats']['pattern'],
                   priority=config['stats']['priority'])
@annotate_by_uri
def resource_bamtools_stats(uri, **kwargs):
    """Parse bamtools stats text output file.

    Args:
      uri (str): filename

    Returns:
      DataFrame: DataFrame for requested section
    """
    with open(uri) as fh:
        data = [
            [y for y in re.sub("\s+(\d+)", "\t\\1",
                               re.sub("(^\t|:|'|\s+$)", "",
                                      re.sub("Read (\d+)", "Read_\\1", x))).split("\t")]
            for x in fh.readlines()[5:] if not x.startswith("\n")]
    df = DataFrame.from_records(data)
    df.columns = ["statistic", "value", "percent"]
    df['percent'].replace("[\(\)%]", "", inplace=True, regex=True)
    df["percent"] = pd.to_numeric(df['percent'], errors="ignore")
    df["value"] = pd.to_numeric(df['value'], errors="ignore")
    df = df.set_index('statistic')
    return df


aggregate = utils.aggregate_factory("bamtools")
