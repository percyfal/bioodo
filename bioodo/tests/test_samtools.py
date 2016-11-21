# Copyright (C) 2015 by Per Unneberg
import os
import pytest
from bioodo import samtools, odo, DataFrame


@pytest.fixture(scope="module")
def samtools_stats(tmpdir_factory):
    """Setup samtools stats"""
    fn = tmpdir_factory.mktemp('samtools').join("s1.samtools_stats.txt")
    fn.mksymlinkto(os.path.join(pytest.datadir, "samtools", "s1.samtools_stats.txt"))
    return fn


def test_basic_statistics(samtools_stats):
    df = odo(str(samtools_stats), DataFrame)
    assert (list(df.index)[0] == 'raw total sequences')
    assert(df.loc["sequences", "value"] == 50)


def test_GCC(samtools_stats):
    df = odo(str(samtools_stats), DataFrame, key="GCC")
    assert (df.loc[1]["A"] == 36.0)


def test_FFQ(samtools_stats):
    df = odo(str(samtools_stats), DataFrame, key="FFQ")
    assert (df.loc[1][32] == 17)
