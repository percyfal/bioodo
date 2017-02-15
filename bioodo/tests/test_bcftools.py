# Copyright (C) 2015 by Per Unneberg
import os
import pytest
from bioodo import bcftools, odo, DataFrame


@pytest.fixture(scope="module")
def bcftools_stats(tmpdir_factory):
    """Setup bcftools stats"""
    fn = tmpdir_factory.mktemp('bcftools').join("s1.bcftools_stats.txt")
    fn.mksymlinkto(os.path.join(pytest.datadir, "bcftools", "s1.bcftools_stats.txt"))
    return fn


def test_basic_statistics(bcftools_stats):
    df = odo(str(bcftools_stats), DataFrame)
    assert (list(df.index)[0] == 'raw total sequences')
    assert(df.loc["sequences", "value"] == 50)


def test_GCC(bcftools_stats):
    df = odo(str(bcftools_stats), DataFrame, key="GCC")
    assert (df.loc[1]["A"] == 36.0)


def test_FFQ(bcftools_stats):
    df = odo(str(bcftools_stats), DataFrame, key="FFQ")
    assert (df.loc[1][32] == 17)
