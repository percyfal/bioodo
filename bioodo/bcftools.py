# Copyright (C) 2016 by Per Unneberg
import logging
import pandas as pd
import bioodo
from bioodo import resource, annotate_by_uri, pivot, DataFrame, utils

logger = logging.getLogger(__name__)
config = bioodo.__RESOURCE_CONFIG__['bcftools']


SECTION_NAMES = ['ID', 'SN', 'TSTV', 'SiS', 'AF', 'QUAL', 'IDD', 'ST', 'DP']
COLUMNS = {
    'ID': ['id', 'filename'],
    'SN': ['id', 'key', 'value'],
    'TSTV': ['id', 'ts', 'tv', 'ts/tv', 'ts_(1st_ALT)',
             'tv_(1st_ALT)', 'ts/tv_(1st_ALT)'],
    'SiS': ['id', 'allele_count', 'number_of_SNPs', 'number_of_transitions',
            'number_of_transversions', 'number_of_indels', 'repeat_consistent',
            'repeat_inconsistent', 'NA'],
    'AF': ['id', 'allele_frequency', 'number_of_SNPs', 'number_of_transitions',
           'number_of_transversions', 'number_of_indels', 'repeat_consistent',
           'repeat_inconsistent', 'NA'],
    'QUAL': ['id', 'Quality', 'number_of_SNPs',
             'number_of_transitions_(1st_ALT)',
             'number_of_transversions_(1st_ALT)', 'number_of_indels'],
    'IDD': ['id', 'length_(deletions_negative)', 'count'],
    'ST': ['id', 'type', 'count'],
    'DP': ['id', 'bin', 'number_of_genotypes', 'fraction_of_genotypes',
           'number_of_sites', 'fraction_of_sites'],
}
INDEX_COLUMN = {
    'ID': None,
    'SN': 1,
    'TSTV': None,
    'SiS': None,
    'AF': None,
    'QUAL': 1,
    'IDD': 1,
    'ST': 1,
    'DP': 1,
}


@resource.register(config['stats']['pattern'],
                   priority=config['stats']['priority'])
@pivot
@annotate_by_uri
def resource_bcftools_stats(uri, key="SN", **kwargs):
    """Parse bcftools stats text output file.

    Args:
      uri (str): filename
      key (str): result section to return

    Returns:
      DataFrame: DataFrame for requested section
    """
    if key not in SECTION_NAMES:
        raise KeyError("Not in allowed section names; " +
                       "allowed values are {}".format(
                           ", ".join(SECTION_NAMES + ["Summary"])))
    with open(uri) as fh:
        data = [[y for y in x.replace(":", "").strip().split("\t")[1:]
                 if not y.startswith("#")]
                for x in fh.readlines() if x.startswith(key)]
    df = DataFrame.from_records(data, columns=COLUMNS[key])
    df = df.apply(pd.to_numeric, errors='ignore')
    i = INDEX_COLUMN[key]
    if i is not None:
        df = df.set_index(df[COLUMNS[key][i]])
        del df[COLUMNS[key][i]]
    return df


aggregate = utils.aggregate_factory("bcftools")
