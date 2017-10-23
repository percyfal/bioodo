# Copyright (C) 2015 by Per Unneberg
from bioodo import sga, odo, DataFrame
from pytest_ngsfixtures.config import application_fixtures
import utils

fixtures = application_fixtures(application="sga")

sga_preprocess_data = utils.fixture_factory([x for x in fixtures if
                                             "preprocess" in x[1]])
sga_filter_data = utils.fixture_factory([x for x in fixtures if
                                         "filter" in x[1]])
sga_aggregate_filter_data = utils.aggregation_fixture_factory(
    [x for x in fixtures if "filter" in x[1]], 2)


def test_sga_preprocess(sga_preprocess_data):
    module, command, version, end, pdir = sga_preprocess_data
    df = odo(str(pdir.listdir()[0]), DataFrame)
    n = 10000 if end == "se" else 20000
    assert df.loc["Reads parsed", "value"] == n


def test_sga_filter(sga_filter_data):
    _filter_stats = {'0.10.13': {'se': 9400, 'pe': 16670}}
    module, command, version, end, pdir = sga_filter_data
    df = odo(str(pdir.listdir()[0]), DataFrame)
    assert (df.loc["Reads failed kmer check", "value"] ==
            _filter_stats[version][end])


def test_sga_aggregate_filter(sga_aggregate_filter_data):
    module, command, version, end, pdir = sga_aggregate_filter_data
    df = sga.aggregate(
        [str(x.listdir()[0]) for x in pdir.listdir() if x.isdir()],
        regex=".*/(?P<repeat>[0-9]+)/sga.filter.log",
        parser=sga.resource_sga_filter)
    assert sorted(list(df["repeat"].unique())) == ['0', '1']
