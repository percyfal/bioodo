# Copyright (C) 2016 by Per Unneberg
import logging
import pandas as pd
from bioodo import resource, annotate_by_uri, DataFrame

logger = logging.getLogger(__name__)

SECTION_NAMES = ['ID', 'SN', 'TSTV', 'SiS', 'AF', 'QUAL', 'IDD', 'ST', 'DP']
COLUMNS = {
    'ID' : ['id', 'filename'],
    'SN' : ['id', 'key', 'value'],
    'TSTV' : ['id', 'ts', 'tv', 'ts/tv', 'ts_(1st_ALT)', 'tv_(1st_ALT)', 'ts/tv_(1st_ALT)'],
    'SiS' : ['id', 'allele_count', 'number_of_SNPs', 'number_of_transitions', 'number_of_transversions', 'number_of_indels', 'repeat_consistent', 'repeat_inconsistent', 'NA'],
    'AF' : ['id', 'allele_frequency', 'number_of_SNPs', 'number_of_transitions', 'number_of_transversions', 'number_of_indels', 'repeat_consistent', 'repeat_inconsistent', 'NA'],
    'QUAL' : ['id', 'Quality', 'number_of_SNPs', 'number_of_transitions_(1st_ALT)', 'number_of_transversions_(1st_ALT)', 'number_of_indels'],
    'IDD' : ['id', 'length_(deletions_negative)', 'count'],
    'ST' : ['id', 'type', 'count'],
    'DP' : ['id', 'bin', 'number_of_genotypes', 'fraction_of_genotypes', 'number_of_sites', 'fraction_of_sites'],
}


@resource.register('.*vcf.gz.stats', priority=30)
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
        raise KeyError("Not in allowed section names; allowed values are {}".format(", ".join(SECTION_NAMES + ["Summary"])))
    with open(uri) as fh:
        data = [[y for y in x.replace(":", "").strip().split("\t")[1:] if not y.startswith("#")] for x in fh.readlines() if x.startswith(key)]
    df = DataFrame.from_records(data, columns = COLUMNS[key])
    df = df.apply(pd.to_numeric, errors='ignore')
    df = df.set_index(df[COLUMNS[key][0]])
    del df[COLUMNS[key][0]]
    return df