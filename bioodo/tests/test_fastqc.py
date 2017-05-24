# Copyright (C) 2015 by Per Unneberg
import pytest
from bioodo import fastqc, odo, DataFrame

from pytest_ngsfixtures.config import application_fixtures
import utils

fixtures = application_fixtures(application="fastqc")
fastqc_data = utils.fixture_factory(fixtures)
fastqc_aggregate_data = utils.aggregation_fixture_factory(
    [x for x in fixtures], 2)


def test_basic_statistics(fastqc_data):
    module, command, version, end, pdir = fastqc_data
    fn = str(pdir.join("medium_fastqc.zip"))
    df = odo(fn, DataFrame)
    major, minor, patch = version.split(".")
    if int(minor) >= 11:
        assert(list(df.index) == ['Filename', 'File type', 'Encoding',
                                  'Total Sequences',
                                  'Sequences flagged as poor quality',
                                  'Sequence length', '%GC'])
    else:
        assert(list(df.index) == ['Filename', 'File type', 'Encoding',
                                  'Total Sequences', 'Filtered Sequences',
                                  'Sequence length', '%GC'])
    assert(df.loc["Filename", "Value"] == "medium.bam")


def test_summary(fastqc_data):
    module, command, version, end, pdir = fastqc_data
    fn = str(pdir.join("medium_fastqc.zip"))
    df = odo(fn, DataFrame, key="Summary")
    assert(df.loc['Basic_Statistics', 'Value'] == "pass")


def test_wrong_key(fastqc_data):
    module, command, version, end, pdir = fastqc_data
    fn = str(pdir.join("medium_fastqc.zip"))
    with pytest.raises(KeyError):
        odo(fn, DataFrame, key="foo")


def test_per_base_sequence_quality(fastqc_data):
    module, command, version, end, pdir = fastqc_data
    fn = str(pdir.join("medium_fastqc.zip"))
    df = odo(fn, DataFrame, key="Per_base_sequence_quality")
    major, minor, patch = version.split(".")
    if int(minor) <= 10:
        assert df.shape[0] == 28
    else:
        assert df.shape[0] == 55
    assert df.shape[1] == 6


def test_fastqc_aggregate(fastqc_aggregate_data):
    module, command, version, end, pdir = fastqc_aggregate_data
    df = fastqc.aggregate([str(x.listdir()[0]) for x in pdir.listdir()
                           if x.isdir()],
                          regex=".*/(?P<repeat>[0-9]+)/medium_fastqc.zip")
    assert sorted(list(df["repeat"].unique())) == ['0', '1']
