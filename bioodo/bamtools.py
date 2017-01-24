# Copyright (C) 2016 by Per Unneberg
import logging
import pandas as pd
import re
from bioodo import resource, annotate_by_uri, DataFrame
from .utils import recast

logger = logging.getLogger(__name__)

@resource.register('.*.bamtools.stats.txt')
@annotate_by_uri
def resource_bamtools_stats(uri, **kwargs):
    """Parse bamtools stats text output file.

    Args:
      uri (str): filename
      
    Returns:
      DataFrame: DataFrame for requested section
    """
    with open(uri) as fh:
        data = [[y for y in re.sub("\s+(\d+)", "\t\\1", re.sub("(^\t|:|'|\s+$)", "", x)).split("\t")] for x in fh.readlines()[5:] if not x.startswith("\n")]
    df = DataFrame.from_records(data)
    df.columns = ["statistic", "value", "percent"]
    df = df.set_index('statistic')
    return df



def aggregate(infiles, outfile, regex=None,  **kwargs):
    import odo
    dflist = []
    for f in infiles:
        logger.info("loading {}".format(f))
        df = odo.odo(f, DataFrame)
        if regex:
            m = re.search(regex, f)
            if m:
                logger.info("adding columns {}".format(",".join(["{}={}".format(k, v) for k,v in m.groupdict().items()])))
                for k, v in m.groupdict().items():
                    df[k] = v
        dflist.append(df)
    df = pd.concat(dflist)
    df.to_csv(outfile)

    
