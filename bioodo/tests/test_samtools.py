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
    print(df)
    # assert(list(df.index) == ['Filename', 'File type', 'Encoding', 'Total Sequences', 'Sequences flagged as poor quality', 'Sequence length', '%GC'])
    # assert(df.loc["Filename", "Value"] == "s1_1.fastq.gz")

