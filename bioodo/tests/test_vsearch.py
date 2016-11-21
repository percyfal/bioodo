# Copyright (C) 2015 by Per Unneberg
import os
import pytest
from bioodo import vsearch, odo, DataFrame


@pytest.fixture(scope="module")
def vsearch_fastq_stats(tmpdir_factory):
    """Setup vsearch fastq stats"""
    fn = tmpdir_factory.mktemp('vsearch').join("s1_1.fastq_stats.txt")
    fn.mksymlinkto(os.path.join(pytest.datadir, "vsearch", "s1_1.fastq_stats.txt"))
    return fn


def test_vsearch_fastq_stats(vsearch_fastq_stats):
    df = odo(str(vsearch_fastq_stats), DataFrame)
    assert (list(df.columns) == ["N", "Pct", "AccPct"])
    df = odo(str(vsearch_fastq_stats), DataFrame, key="Q score distribution")
    assert (list(df.index)[0:3] == [44, 43, 42])
    assert (df.index.name == "Q")
    df = odo(str(vsearch_fastq_stats), DataFrame, key="Truncate at first Q")
    assert (df.index.name == "Len")
    assert (list(df.index)[0:3] == [76, 75, 74])
    assert (df.loc[76]["Q=5"] == "68.0%")
