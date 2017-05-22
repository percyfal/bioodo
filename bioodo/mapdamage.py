# Copyright (C) 2016 by Per Unneberg
import logging
import pandas as pd
from bioodo import resource, annotate_by_uri, DataFrame, utils

logger = logging.getLogger(__name__)


@resource.register('.*Runtime_log.txt', priority=30)
@annotate_by_uri
def resource_mapdamage_runtime(uri, **kwargs):
    """Parse mapdamage runtime log.

    Args:
      uri (str): filename
      
    Returns:
      DataFrame: DataFrame representation of runtime log
    """
    df = pd.read_table(uri, sep="\t", header=None)
    return df


@resource.register('.*3pGtoA_freq.txt', priority=30)
@annotate_by_uri
def resource_mapdamage_3pGtoA_freq(uri, **kwargs):
    """Parse mapdamage 3pGtoA_freq.txt

    Args:
      uri (str): filename
      
    Returns:
      DataFrame: DataFrame representation of 3pGtoA
    """
    df = pd.read_table(uri, index_col=0)
    return df


@resource.register('.*5pCtoT_freq.txt', priority=30)
@annotate_by_uri
def resource_mapdamage_5pCtoT_freq(uri, **kwargs):
    """Parse mapdamage 5pCtoT_freq.txt

    Args:
      uri (str): filename
      
    Returns:
      DataFrame: DataFrame representation of 5pCtoT
    """
    df = pd.read_table(uri, index_col=0)
    return df

@resource.register('.*Stats_out_MCMC_correct_prob.csv', priority=30)
@annotate_by_uri
def resource_mapdamage_mcmc_correct_prob_freq(uri, **kwargs):
    """Parse mapdamage Stats_out_MCMC_correct_prob.csv

    Args:
      uri (str): filename
      
    Returns:
      DataFrame: DataFrame representation of mcmc correct prob.
    """
    df = pd.read_csv(uri, index_col="Position")
    del df["Unnamed: 0"]
    return df


@resource.register('.*Stats_out_MCMC_iter.csv', priority=30)
@annotate_by_uri
def resource_mapdamage_mcmc_iter(uri, **kwargs):
    """Parse mapdamage Stats_out_MCMC_iter.csv

    Args:
      uri (str): filename
      
    Returns:
      DataFrame: DataFrame representation of mcmc iter.
    """
    df = pd.read_csv(uri, index_col=0)
    return df


@resource.register('.*Stats_out_MCMC_iter_summ_stat.csv', priority=30)
@annotate_by_uri
def resource_mapdamage_mcmc_iter_summ_stat(uri, **kwargs):
    """Parse mapdamage Stats_out_MCMC_iter_summ_stat.csv

    Args:
      uri (str): filename
      
    Returns:
      DataFrame: DataFrame representation of mcmc iter summ stat.
    """
    df = pd.read_csv(uri, index_col=0)
    return df


@resource.register('.*dnacomp.txt', priority=30)
@annotate_by_uri
def resource_mapdamage_dnacomp(uri, **kwargs):
    """Parse mapdamage dnacomp.txt

    Args:
      uri (str): filename
      
    Returns:
      DataFrame: DataFrame representation of dnacomp
    """
    df = pd.read_table(uri, comment="#")
    return df


@resource.register('.*dnacomp_genome.csv', priority=30)
@annotate_by_uri
def resource_mapdamage_dnacomp_genome(uri, **kwargs):
    """Parse mapdamage dnacomp_genome.csv

    Args:
      uri (str): filename
      
    Returns:
      DataFrame: DataFrame representation of dnacomp_genome
    """
    df = pd.read_csv(uri)
    return df


@resource.register('.*lgdistribution.txt', priority=30)
@annotate_by_uri
def resource_mapdamage_lgdistribution(uri, **kwargs):
    """Parse mapdamage lgdistribution.txt

    Args:
      uri (str): filename
      
    Returns:
      DataFrame: DataFrame representation of lgdistribution
    """
    df = pd.read_table(uri, sep="\s+", comment="#")
    return df


@resource.register('.*misincorporation.txt', priority=30)
@annotate_by_uri
def resource_mapdamage_misincorporation(uri, **kwargs):
    """Parse mapdamage misincorporation.txt

    Args:
      uri (str): filename
      
    Returns:
      DataFrame: DataFrame representation of misincorporation
    """
    df = pd.read_table(uri, sep="\t", comment="#")
    return df



# Aggregation function
def aggregate(infiles, outfile=None, regex=None, **kwargs):
    """Aggregate individual mapdamage reports to one output file

    Params:
      infiles (list): list of input files
      outfile (str): csv output file name
      regex (str): regular expression pattern to parse input file names
      kwargs (dict): keyword arguments

    """
    logger.debug("Aggregating mapdamage infiles {} in mapdamage aggregate".format(",".join(infiles)))
    df = utils.aggregate_files(infiles, regex=regex, **kwargs)
    if outfile:
        df.to_csv(outfile)
    else:
        return df

