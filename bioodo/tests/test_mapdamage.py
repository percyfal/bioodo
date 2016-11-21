# Copyright (C) 2015 by Per Unneberg
import os
import pytest
from bioodo import mapdamage, odo, DataFrame


results = ['3pGtoA_freq.txt', '5pCtoT_freq.txt', 'Runtime_log.txt',
           'Stats_out_MCMC_correct_prob.csv', 'Stats_out_MCMC_iter.csv',
           'Stats_out_MCMC_iter_summ_stat.csv', 'dnacomp.txt', 'dnacomp_genome.csv',
           'lgdistribution.txt', 'misincorporation.txt']


@pytest.fixture(scope="module")
def mapdamage_results(tmpdir_factory):
    """Setup mapdamage results"""
    p = tmpdir_factory.mktemp('mapdamage')
    for f in results:
        tmp = p.join(f)
        tmp.mksymlinkto(os.path.join(pytest.datadir, "s2_mapdamage2", f))
    return p


def test_mapdamage_runtime(mapdamage_results):
    fn = mapdamage_results.join("Runtime_log.txt")
    df = odo(str(fn), DataFrame)


def test_mapdamage_3pGtoA(mapdamage_results):
    fn = mapdamage_results.join("3pGtoA_freq.txt")
    df = odo(str(fn), DataFrame)
    assert(df.index.name == "pos")


def test_mapdamage_5pCtoT(mapdamage_results):
    fn = mapdamage_results.join("5pCtoT_freq.txt")
    df = odo(str(fn), DataFrame)
    assert(df.index.name == "pos")
    

def test_mapdamage_mcmc_correct_prob(mapdamage_results):
    fn = mapdamage_results.join("Stats_out_MCMC_correct_prob.csv")
    df = odo(str(fn), DataFrame)
    assert(df.index.name == "Position")
    assert(df.shape[1] == 2)


def test_mapdamage_mcmc_iter(mapdamage_results):
    fn = mapdamage_results.join("Stats_out_MCMC_iter.csv")
    df = odo(str(fn), DataFrame)
    assert(df.shape[1] == 6)


def test_mapdamage_mcmc_iter_summ(mapdamage_results):
    fn = mapdamage_results.join("Stats_out_MCMC_iter_summ_stat.csv")
    df = odo(str(fn), DataFrame)
    assert(df.shape[1] == 6)


def test_mapdamage_dnacomp(mapdamage_results):
    fn = mapdamage_results.join("dnacomp.txt")
    df = odo(str(fn), DataFrame)
    assert (df["Chr"][0] == "chr11")
    

def test_mapdamage_dnacomp_genome(mapdamage_results):
    fn = mapdamage_results.join("dnacomp_genome.csv")
    df = odo(str(fn), DataFrame)
    assert (list(df["A"])[0] - 0.224099 < 0.0001)


def test_mapdamage_lgdistribution(mapdamage_results):
    fn = mapdamage_results.join("lgdistribution.txt")
    df = odo(str(fn), DataFrame)
    assert (list(df.columns) == ['Std', 'Length', 'Occurences'])


def test_mapdamage_misincorporation(mapdamage_results):
    fn = mapdamage_results.join("misincorporation.txt")
    df = odo(str(fn), DataFrame)
    assert (df.shape[1] == 30)
    
