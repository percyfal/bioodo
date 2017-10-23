# Copyright (C) 2016 by Per Unneberg
import logging
import pandas as pd
import re
import bioodo
from bioodo import resource, annotate_by_uri, pivot, DataFrame, utils

logger = logging.getLogger(__name__)
config = bioodo.__RESOURCE_CONFIG__['bamtools']


@resource.register(config['stats']['pattern'],
                   priority=config['stats']['priority'])
@pivot
@annotate_by_uri
def resource_bamtools_stats(uri, **kwargs):
    """Parse bamtools stats text output file.

    Args:
      uri (str): filename

    Returns:
      DataFrame: DataFrame for requested section
    """
    def _parse():
        data = []
        with open(uri) as fh:
            for x in fh.readlines()[5:]:
                if x.startswith("\n"):
                    continue
                x = re.sub("Read (\d+)", "Read_\\1", x)
                x = re.sub("(^\t|:|'|\s+$)", "", x)
                x = re.sub("\s+(\d+)", "\t\\1", x).split("\t")
                data.append(x)
        return data

    data = _parse()
    df = DataFrame.from_records(data)
    df.columns = ["statistic", "value", "percent"]
    df['percent'].replace("[\(\)%]", "", inplace=True, regex=True)
    df["percent"] = pd.to_numeric(df['percent'], errors="ignore")
    df["value"] = pd.to_numeric(df['value'], errors="ignore")
    df.set_index("statistic", inplace=True, drop=False)
    return df


aggregate = utils.aggregate_factory("bamtools")
