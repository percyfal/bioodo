# Copyright (C) 2015 by Per Unneberg
from bioodo import cutadapt, odo, DataFrame
from pytest_ngsfixtures.config import application_fixtures
import utils

fixtures = application_fixtures(application="cutadapt")
cutadapt_metrics = utils.fixture_factory(fixtures)
cutadapt_aggregate_data = utils.aggregation_fixture_factory(
    [x for x in fixtures], 2)


def test_cutadapt(cutadapt_metrics):
    module, command, version, end, pdir = cutadapt_metrics
    fn = str(pdir.join("cutadapt_metrics.txt"))
    df = odo(fn, DataFrame)
    if end == "se":
        assert df.loc["Reads with adapters"]["value"] == 792
    elif end == "pe":
        assert df.loc["Read 1 with adapter"]["value"] == 792


def test_cutadapt_aggregate(cutadapt_aggregate_data):
    module, command, version, end, pdir = cutadapt_aggregate_data
    df = cutadapt.aggregate(
        [str(x.listdir()[0]) for x in pdir.listdir() if x.isdir()],
        regex=".*/(?P<repeat>[0-9]+)/cutadapt_metrics.txt")
    assert sorted(list(df["repeat"].unique())) == ['0', '1']
