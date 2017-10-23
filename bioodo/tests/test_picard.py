# Copyright (C) 2015 by Per Unneberg
from bioodo import picard, odo, DataFrame
from pytest_ngsfixtures.config import application_fixtures
import utils

fixtures = application_fixtures(application="picard")
insert_metrics = utils.fixture_factory(
    [x for x in fixtures if "CollectInsertSizeMetrics" in x[1]])
align_metrics = utils.fixture_factory(
    [x for x in fixtures if "CollectAlignmentSummaryMetrics" in x[1]])
aggregate_data_insert = utils.aggregation_fixture_factory(
    [x for x in fixtures if "CollectInsertSizeMetrics" in x[1]], 2)


def test_hist_metrics(insert_metrics):
    module, command, version, end, pdir = insert_metrics
    fn = pdir.join("medium.insert_size_metrics")
    metrics = odo(str(fn), DataFrame)
    hist = odo(str(fn), DataFrame, key="hist")
    assert all(metrics["MEDIAN_INSERT_SIZE"] == [367])
    assert all(hist["insert_size"][0:3] == [19, 22, 23])


def test_metrics(align_metrics):
    module, command, version, end, pdir = align_metrics
    fn = pdir.join("medium.align_metrics")
    metrics = odo(str(fn), DataFrame)
    if end == "pe":
        assert metrics.loc["FIRST_OF_PAIR"]["MEAN_READ_LENGTH"] - 92.29 < 0.01
    else:
        assert metrics.loc["UNPAIRED"]["MEAN_READ_LENGTH"] - 92.29975 < 0.001


def test_aggregate_insert_data(aggregate_data_insert):
    module, command, version, end, pdir = aggregate_data_insert
    df = picard.aggregate(
        [str(x.listdir()[0]) for x in pdir.listdir() if x.isdir()],
        regex=".*/(?P<repeat>[0-9]+)/medium.insert_size_metrics")
    assert sorted(list(df["repeat"].unique())) == ['0', '1']
