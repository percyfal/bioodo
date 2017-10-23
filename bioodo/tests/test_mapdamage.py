# Copyright (C) 2015 by Per Unneberg
from bioodo import mapdamage, odo, DataFrame
from pytest_ngsfixtures.config import application_fixtures
import utils

fixtures = application_fixtures(application="mapdamage2")
mapdamage_data = utils.fixture_factory(fixtures)
mapdamage_agg_data_misincorp = utils.aggregation_fixture_factory(
    [x for x in fixtures], 2, keys=["misincorp"])


def test_mapdamage_runtime(mapdamage_data):
    module, command, version, end, pdir = mapdamage_data
    fn = pdir.join("Runtime_log.txt")
    odo(str(fn), DataFrame)


def test_mapdamage_3pGtoA(mapdamage_data):
    module, command, version, end, pdir = mapdamage_data
    fn = pdir.join("3pGtoA_freq.txt")
    df = odo(str(fn), DataFrame)
    assert(df.index.name == "pos")


def test_mapdamage_5pCtoT(mapdamage_data):
    module, command, version, end, pdir = mapdamage_data
    fn = pdir.join("5pCtoT_freq.txt")
    df = odo(str(fn), DataFrame)
    assert(df.index.name == "pos")


def test_mapdamage_mcmc_correct_prob(mapdamage_data):
    module, command, version, end, pdir = mapdamage_data
    fn = pdir.join("Stats_out_MCMC_correct_prob.csv")
    df = odo(str(fn), DataFrame)
    assert(df.index.name == "Position")
    assert(df.shape[1] == 2)


def test_mapdamage_mcmc_iter(mapdamage_data):
    module, command, version, end, pdir = mapdamage_data
    fn = pdir.join("Stats_out_MCMC_iter.csv")
    df = odo(str(fn), DataFrame)
    assert(df.shape[1] == 6)


def test_mapdamage_mcmc_iter_summ(mapdamage_data):
    module, command, version, end, pdir = mapdamage_data
    fn = pdir.join("Stats_out_MCMC_iter_summ_stat.csv")
    df = odo(str(fn), DataFrame)
    assert(df.shape[1] == 6)


def test_mapdamage_dnacomp(mapdamage_data):
    module, command, version, end, pdir = mapdamage_data
    fn = pdir.join("dnacomp.txt")
    df = odo(str(fn), DataFrame)
    assert (df["Chr"][0] == "scaffold1")


def test_mapdamage_dnacomp_genome(mapdamage_data):
    module, command, version, end, pdir = mapdamage_data
    fn = pdir.join("dnacomp_genome.csv")
    df = odo(str(fn), DataFrame)
    assert (list(df["A"])[0] - 0.265786 < 0.0001)


def test_mapdamage_lgdistribution(mapdamage_data):
    module, command, version, end, pdir = mapdamage_data
    fn = pdir.join("lgdistribution.txt")
    df = odo(str(fn), DataFrame)
    assert (list(df.columns) == ['Std', 'Length', 'Occurences'])


def test_mapdamage_misincorporation(mapdamage_data):
    module, command, version, end, pdir = mapdamage_data
    fn = pdir.join("misincorporation.txt")
    df = odo(str(fn), DataFrame)
    assert (df.shape[1] == 30)


def test_mapdamage_aggregate_misincorporation(mapdamage_agg_data_misincorp):
    module, command, version, end, pdir = mapdamage_agg_data_misincorp
    df = mapdamage.aggregate(
        [str(x.listdir()[0]) for x in pdir.listdir() if x.isdir()],
        regex=".*/(?P<repeat>[0-9]+)/misincorporation.txt")
    assert sorted(list(df["repeat"].unique())) == ['0', '1']
