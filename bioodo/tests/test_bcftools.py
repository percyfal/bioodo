# Copyright (C) 2015 by Per Unneberg
from bioodo import bcftools, odo, DataFrame
from pytest_ngsfixtures.config import application_fixtures
import utils

fixtures = application_fixtures(application="bcftools")

stat_fixtures = [x for x in fixtures if x[1] == "bcftools_stats"]
bcftools_stats = utils.fixture_factory(stat_fixtures)
bcftools_aggregate_QUAL_data = utils.aggregation_fixture_factory(
    [x for x in stat_fixtures], 2)


def test_basic_statistics(bcftools_stats):
    module, command, version, end, pdir = bcftools_stats
    fn = str(pdir.join("medium.call.stats"))
    df = odo(fn, DataFrame)
    assert (list(df.index)[0] == 'number of samples')
    n = 10667 if end == "pe" else 7400
    assert(df.loc["number of records", "value"] == n)


def test_TSTV(bcftools_stats):
    module, command, version, end, pdir = bcftools_stats
    fn = str(pdir.join("medium.call.stats"))
    df = odo(fn, DataFrame, key="TSTV")
    tstv = 2.12 if end == "pe" else 2.19
    assert (df.loc[0]["ts/tv"] == tstv)


def test_IDD(bcftools_stats):
    module, command, version, end, pdir = bcftools_stats
    fn = str(pdir.join("medium.call.stats"))
    df = odo(fn, DataFrame, key="IDD")
    count = 123 if end == "pe" else 95
    assert (df.loc[-1]["count"] == count)


def test_QUAL(bcftools_stats):
    module, command, version, end, pdir = bcftools_stats
    fn = str(pdir.join("medium.call.stats"))
    df = odo(fn, DataFrame, key="QUAL")
    assert "number_of_transitions_(1st_ALT)" in list(df.columns)
    nsnps = 83 if end == "pe" else 90
    assert (df.loc[3]["number_of_SNPs"] == nsnps)


def test_bcftools_aggregate_QUAL(bcftools_aggregate_QUAL_data):
    module, command, version, end, pdir = bcftools_aggregate_QUAL_data
    df = bcftools.aggregate(
        [str(x.listdir()[0]) for x in pdir.listdir() if x.isdir()],
        regex=".*/(?P<repeat>[0-9]+)/medium.call.stats",
        key="QUAL")
    assert df.index.name == "Quality"
    assert sorted(list(df["repeat"].unique())) == ['0', '1']
