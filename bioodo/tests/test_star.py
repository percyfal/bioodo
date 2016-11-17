# Copyright (C) 2015 by Per Unneberg
import os
import pytest
from bioodo import star, DataFrame, odo


@pytest.fixture(scope="module")
def star_data(tmpdir_factory):
    fn = tmpdir_factory.mktemp('data').join('star.Log.final.out')
    fn.mksymlinkto(os.path.join(pytest.datadir, "star", "star.Log.final.out"))    
    return fn


def test_star_log(star_data):
    df = odo(str(star_data), DataFrame)
    assert df.loc["% of reads unmapped: too short","value"] == 8.73
    assert df.loc["Uniquely mapped reads number","value"] == 4011114

