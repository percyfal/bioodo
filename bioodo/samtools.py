# Copyright (C) 2016 by Per Unneberg
logger = logging.getLogger(__name__)

# Headers: 
# Summary Numbers. Use `grep ^SN | cut -f 2-` to extract this part.
# First Fragment Qualitites. Use `grep ^FFQ | cut -f 2-` to extract this part.
# Last Fragment Qualitites. Use `grep ^LFQ | cut -f 2-` to extract this part.
# GC Content of first fragments. Use `grep ^GCF | cut -f 2-` to extract this part.
# GC Content of last fragments. Use `grep ^GCL | cut -f 2-` to extract this part.
# ACGT content per cycle. Use `grep ^GCC | cut -f 2-` to extract this part. The columns are: cycle, and A,C,G,T counts [%]
# Insert sizes. Use `grep ^IS | cut -f 2-` to extract this part. The columns are: pairs total, inward oriented pairs, outward oriented pairs, other pairs
# Read lengths. Use `grep ^RL | cut -f 2-` to extract this part. The columns are: read length, count
# Indel distribution. Use `grep ^ID | cut -f 2-` to extract this part. The columns are: length, number of insertions, number of deletions
# Indels per cycle. Use `grep ^IC | cut -f 2-` to extract this part. The columns are: cycle, number of insertions (fwd), .. (rev) , number of deletions (fwd), .. (rev)
# Coverage distribution. Use `grep ^COV | cut -f 2-` to extract this part.
# GC-depth. Use `grep ^GCD | cut -f 2-` to extract this part. The columns are: GC%, unique sequence percentiles, 10th, 25th, 50th, 75th and 90th depth percentile

SECTION_NAMES = ['SN', 'FFQ', 'LFQ', 'GCF', 'GCL', 'GCC', 'IS', 'RL', 'ID', 'IC', 'COV', 'GCD']
COLUMNS = {
    'SN' : ['statistic', 'value'],
    'FFQ' : None,
    'LFQ' : None,
    'GCF' : ['percent', 'count'],
    'GCL' : ['percent', 'count'],
    'GCC' : ['cycle', 'A', 'C', 'G', 'T'],
    'RL' : ['length', 'count'],
    'ID' : ['length', 'insertions', 'deletions'],
    'IC' : ['cycle', 'insertions_fwd', 'insertions_rev', 'deletions_fwd', 'deletions_rev'],
    'COV' : ['bin', 'coverage', 'count'],
    'GCD' : ['percent', 'unique', 'p10', 'p25', 'p50', 'p75', 'p90'],
}


@resource.register('.*samtools_stats.txt', priority=30)
@annotate_by_uri
def resource_samtools_stats(uri, key="SN", **kwargs):
    """Parse fastqc text output file.

    Args:
      uri (str): filename
      key (str): result section to return
      
    Returns:
      DataFrame: DataFrame for requested section
    """
    if key not in SECTION_NAMES:
        raise KeyError("Not in allowed section names; allowed values are {}".format(", ".join(SECTION_NAMES + ["Summary"])))
    with open(uri) as fh:
        data = [x[1:] for x in fh.readlines() if x.startswith(key)]
    df = DataFrame.from_records(data)
    if key in ['FFQ', 'LFQ']:
        df.columns = [''] + [str(x) for x in range(cols)]
    return df
