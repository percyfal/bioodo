# Copyright (C) 2015 by Per Unneberg
import os
from bioodo import rseqc, odo, DataFrame
from pytest_ngsfixtures.config import application_fixtures
import utils

blacklist = ["rseqc_junction_annotation", "rseqc_read_duplication"]
fixtures = application_fixtures(application="rseqc")
fixture_list = [f for f in fixtures if f[1] not in blacklist]
data = utils.fixture_factory(fixture_list, scope="function")
rseqc_aggregate_data = utils.aggregation_fixture_factory(
    [x for x in fixture_list], 2)


def test_rseqc_parse(data):
    module, command, version, end, pdir = data
    fn = pdir.listdir()[0]
    if command == "rseqc_read_duplication":
        odo(str(fn), DataFrame)
        fn = pdir.listdir()[1]
        odo(str(fn), DataFrame)
    else:
        odo(str(fn), DataFrame)


def test_rseqc_aggregate(rseqc_aggregate_data):
    module, command, version, end, pdir = rseqc_aggregate_data
    infiles = [str(x.listdir()[0]) for x in pdir.listdir() if x.isdir()]
    df = rseqc.aggregate(
        infiles,
        regex=".*/(?P<repeat>[0-9]+)/" + os.path.basename(infiles[0]))
    assert sorted(list(df["repeat"].unique())) == ['0', '1']
