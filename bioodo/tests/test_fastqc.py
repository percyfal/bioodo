# Copyright (C) 2015 by Per Unneberg
import os
import pytest
from bioodo import fastqc, odo, DataFrame

@pytest.fixture(scope="module")
def fastqc_data(tmpdir_factory):
    """Setup fastqc data"""
    fn = tmpdir_factory.mktemp('fastqc').join("fastqc_data.txt")
    fn.mksymlinkto(os.path.join(pytest.datadir, "fastqc", "fastqc_data.txt"))
    return fn


def test_basic_statistics(fastqc_data):
    df = odo(str(fastqc_data), DataFrame)
    assert(list(df.index) == ['Filename', 'File type', 'Encoding', 'Total Sequences', 'Sequences flagged as poor quality', 'Sequence length', '%GC'])
    assert(df.loc["Filename", "Value"] == "s1_1.fastq.gz")


def test_summary(fastqc_data):
    df = odo(str(fastqc_data), DataFrame, key="Summary")
    assert(df.loc['Basic_Statistics', 'Value'] == "pass")


def test_wrong_key(fastqc_data):
    with pytest.raises(KeyError):
        df = odo(str(fastqc_data), DataFrame, key="foo")


def test_per_base_sequence_quality(fastqc_data):
    df = odo(str(fastqc_data),  DataFrame, key="Per_base_sequence_quality")
    assert df.shape[0] == 43
    assert df.shape[1] == 6

