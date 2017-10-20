# Copyright (C) 2015 by Per Unneberg
from bioodo import vsearch, odo, DataFrame
from pytest_ngsfixtures.config import application_fixtures
import utils

blacklist = ['vsearch_fastqc_filter']
fixtures = [x for x in application_fixtures(application="vsearch")
            if x[1] not in blacklist]
data = utils.fixture_factory(fixtures)
aggregate_data = utils.aggregation_fixture_factory(
    fixtures, 2)


def test_vsearch_fastq_stats(data):
    module, command, version, end, pdir = data
    fn = pdir.join("medium.fastq_stats.txt")
    df = odo(str(fn), DataFrame)
    assert list(df.columns) == ["N", "Pct", "AccPct"]
    assert df.index.name == "L"
    df = odo(str(fn), DataFrame, key="Truncate at first Q")
    assert list(df.columns) == ["Q=5", "Q=10", "Q=15", "Q=20"]
    assert df.index.name == "Len"


def test_vsearch_aggregate(aggregate_data):
    module, command, version, end, pdir = aggregate_data
    df = vsearch.aggregate(
        [str(x.listdir()[0]) for x in pdir.listdir()
         if x.isdir()],
        regex=".*/(?P<repeat>[0-9]+)/medium.fastq_stats.txt")
    assert sorted(list(df["repeat"].unique())) == ['0', '1']
