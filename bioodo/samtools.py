# Copyright (C) 2016 by Per Unneberg
import logging
import pandas as pd
from bioodo import resource, annotate_by_uri, DataFrame

logger = logging.getLogger(__name__)

SECTION_NAMES = ['SN', 'FFQ', 'LFQ', 'GCF', 'GCL', 'GCC', 'IS', 'RL', 'ID', 'IC', 'COV', 'GCD']
COLUMNS = {
    'SN' : ['statistic', 'value'],
    'FFQ' : None,
    'LFQ' : None,
    'GCF' : ['percent', 'count'],
    'GCL' : ['percent', 'count'],
    'GCC' : ['cycle', 'A', 'C', 'G', 'T'],
    'IS' : ['insert_size', 'pairs_total', 'inward_oriented_pairs', 'outward_oriented_pairs', 'other_pairs'],
    'RL' : ['length', 'count'],
    'ID' : ['length', 'insertions', 'deletions'],
    'IC' : ['cycle', 'insertions_fwd', 'insertions_rev', 'deletions_fwd', 'deletions_rev'],
    'COV' : ['bin', 'coverage', 'count'],
    'GCD' : ['percent', 'unique', 'p10', 'p25', 'p50', 'p75', 'p90'],
}


@resource.register('.*samtools_stats.txt', priority=30)
@annotate_by_uri
def resource_samtools_stats(uri, key="SN", **kwargs):
    """Parse samtools stats text output file.

    Args:
      uri (str): filename
      key (str): result section to return
      
    Returns:
      DataFrame: DataFrame for requested section
    """
    if key not in SECTION_NAMES:
        raise KeyError("Not in allowed section names; allowed values are {}".format(", ".join(SECTION_NAMES + ["Summary"])))
    with open(uri) as fh:
        data = [[y for y in x.replace(":", "").strip().split("\t")[1:] if not y.startswith("#")] for x in fh.readlines() if x.startswith(key)]
    if key in ['FFQ', 'LFQ']:
        df = DataFrame.from_records(data)
        df = df.apply(pd.to_numeric, errors='ignore')
        df.columns = ['cycle'] + [str(x) for x in range(len(df.columns) - 1)]
        df = df.set_index('cycle')
    else:
        df = DataFrame.from_records(data, columns = COLUMNS[key])
        df = df.apply(pd.to_numeric, errors='ignore')
        df = df.set_index(df[COLUMNS[key][0]])
        del df[COLUMNS[key][0]]
    return df



def aggregate(infiles, outfile, key="SN", regex=None, **kwargs):
    import odo
    dflist = []
    for f in infiles:
        logger.info("loading {}".format(f))
        df = odo.odo(f, DataFrame, key=key)
        if regex:
            m = re.search(regex, f)
            if m:
                logger.info("adding columns {}".format(",".join(["{}={}".format(k, v) for k,v in m.groupdict().items()])))
                for k, v in m.groupdict().items():
                    df[k] = v
        dflist.append(df)
    df = pd.concat(dflist)
    df.to_csv(outfile)
