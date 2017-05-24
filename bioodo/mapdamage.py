# Copyright (C) 2016 by Per Unneberg
import logging
import pandas as pd
import bioodo
from bioodo import resource, annotate_by_uri, utils

logger = logging.getLogger(__name__)
config = bioodo.__RESOURCE_CONFIG__['mapdamage']


@resource.register(config['runtime']['pattern'],
                   priority=config['runtime']['priority'])
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


@resource.register(config['3pGtoA_freq']['pattern'],
                   priority=config['3pGtoA_freq']['priority'])
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


@resource.register(config['5pCtoT_freq']['pattern'],
                   priority=config['5pCtoT_freq']['priority'])
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


@resource.register(config['mcmc_correct_prob_freq']['pattern'],
                   priority=config['mcmc_correct_prob_freq']['priority'])
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


@resource.register(config['mcmc_iter']['pattern'],
                   priority=config['mcmc_iter']['priority'])
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


@resource.register(config['mcmc_iter_summ']['pattern'],
                   priority=config['mcmc_iter_summ']['priority'])
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


@resource.register(config['dnacomp']['pattern'],
                   priority=config['dnacomp']['priority'])
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


@resource.register(config['dnacomp_genome']['pattern'],
                   priority=config['dnacomp_genome']['priority'])
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


@resource.register(config['lgdistribution']['pattern'],
                   priority=config['lgdistribution']['priority'])
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


@resource.register(config['misincorporation']['pattern'],
                   priority=config['misincorporation']['priority'])
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

    Args:
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
