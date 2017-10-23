# Copyright (C) 2016 by Per Unneberg
import logging
import pandas as pd
from bioodo import resource, annotate_by_uri, pivot, DataFrame, utils
import bioodo

logger = logging.getLogger(__name__)
config = bioodo.__RESOURCE_CONFIG__['samtools']


SECTION_NAMES = ['SN', 'FFQ', 'LFQ', 'GCF', 'GCL', 'GCC',
                 'IS', 'RL', 'ID', 'IC', 'COV', 'GCD']
COLUMNS = {
    'SN': ['statistic', 'value'],
    'FFQ': None,
    'LFQ': None,
    'GCF': ['percent', 'count'],
    'GCL': ['percent', 'count'],
    'GCC': ['cycle', 'A', 'C', 'G', 'T', 'ACGT_PCT', 'NO_PCT'],
    'IS': ['insert_size', 'pairs_total', 'inward_oriented_pairs',
           'outward_oriented_pairs', 'other_pairs'],
    'RL': ['length', 'count'],
    'ID': ['length', 'insertions', 'deletions'],
    'IC': ['cycle', 'insertions_fwd', 'insertions_rev',
           'deletions_fwd', 'deletions_rev'],
    'COV': ['bin', 'coverage', 'count'],
    'GCD': ['percent', 'unique', 'p10', 'p25', 'p50', 'p75', 'p90'],
}

IDXSTATS_COLUMNS = ["name", "length", "mapped", "unmapped"]


@resource.register(config['stats']['pattern'],
                   priority=config['stats']['priority'])
@pivot
@annotate_by_uri
def resource_samtools_stats(uri, key="SN", **kwargs):
    """Parse samtools stats text output file.

    Args:
      uri (str): filename
      key (str): result section to return

    Returns:
      DataFrame: DataFrame for requested section
    """
    def _parse():
        data = []
        with open(uri) as fh:
            for x in fh.readlines():
                if not x.startswith(key):
                    continue
                y = []
                for z in x.replace(":", "").strip().split("\t")[1:]:
                    if not z.startswith("#"):
                        y.append(z)
                data.append(y)
        return data

    if key not in SECTION_NAMES:
        raise KeyError("Not in allowed section names; " +
                       "allowed values are {}".format(
                           ", ".join(SECTION_NAMES + ["Summary"])))
    data = _parse()
    if key in ['FFQ', 'LFQ']:
        df = DataFrame.from_records(data)
        df = df.apply(pd.to_numeric, errors='ignore')
        df.columns = ['cycle'] + [str(x) for x in range(len(df.columns) - 1)]
        df = df.set_index('cycle')
    else:
        n = len(data[0])
        df = DataFrame.from_records(data, columns=COLUMNS[key][0:n])
        df = df.apply(pd.to_numeric, errors='ignore')
        df = df.set_index(df[COLUMNS[key][0]])
        del df[COLUMNS[key][0]]
    return df


@resource.register(config['idxstats']['pattern'],
                   priority=config['idxstats']['priority'])
@annotate_by_uri
def resource_samtools_idxstats(uri, **kwargs):
    """Parse samtools idxstats output file.

    From the documentation:

        The output is TAB-delimited with each line consisting of
        reference sequence name, sequence length, # mapped reads and #
        unmapped reads.

    Args:
      uri (str): filename

    Returns:
      DataFrame:

    """
    df = pd.read_table(uri, names=IDXSTATS_COLUMNS)
    return df


aggregate = utils.aggregate_factory("samtools")
