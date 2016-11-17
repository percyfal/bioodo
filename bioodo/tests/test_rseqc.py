# Copyright (C) 2015 by Per Unneberg
import os
from blaze import DataFrame, odo
from bioodo import rseqc
import pytest


@pytest.fixture(scope="module")
def rseqc_read_distribution(tmpdir_factory):
    fn = tmpdir_factory.mktemp('rseqc').join('read_distribution.txt')
    fn.mksymlinkto(os.path.join(pytest.datadir, "rseqc", "read_distribution.txt"))
    return fn

@pytest.fixture(scope="module")
def rseqc_read_distribution2(tmpdir_factory):
    fn = tmpdir_factory.mktemp('rseqc_2').join('read_distribution.txt')
    fn.mksymlinkto(os.path.join(pytest.datadir, "rseqc", "read_distribution.txt"))
    return fn


def test_rseqc_read_distribution(rseqc_read_distribution):
    df = odo(str(rseqc_read_distribution), DataFrame)
    assert "TES_down_10kb" in df.index
    assert df.loc["Introns", "Tag_count"] == 2022848
    

# Proof of principle of globbing functionality
def test_rseqc_glob(rseqc_read_distribution, rseqc_read_distribution2):
    df = odo(os.path.join(os.path.dirname(os.path.dirname(str(rseqc_read_distribution))), "*/*distribution.txt"), DataFrame)
    assert df.shape == (20,3)
