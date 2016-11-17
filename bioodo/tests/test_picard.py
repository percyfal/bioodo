# Copyright (C) 2015 by Per Unneberg
import os
import pytest
from bioodo import picard, odo, DataFrame


@pytest.fixture(scope="module")
def insert_metrics(tmpdir_factory):
    fn = tmpdir_factory.mktemp('picard').join('test.insert_metrics')
    fn.mksymlinkto(os.path.join(pytest.datadir, "picard", "s1.sort.insert_metrics"))
    return fn


@pytest.fixture(scope="module")
def align_metrics(tmpdir_factory):
    fn = tmpdir_factory.mktemp('picard').join('test.align_metrics')
    fn.mksymlinkto(os.path.join(pytest.datadir, "picard", "s1.sort.align_metrics"))
    return fn


def test_hist_metrics(insert_metrics):
    metrics = odo(str(insert_metrics), DataFrame)
    hist = odo(str(insert_metrics), DataFrame, key="hist")
    assert all(metrics["MEDIAN_INSERT_SIZE"] == [155])
    assert all(hist["insert_size"][0:3] == [91,99,107])
    

def test_metrics(align_metrics):
    metrics = odo(str(align_metrics), DataFrame)
    assert metrics.loc["FIRST_OF_PAIR"]["MEAN_READ_LENGTH"] == 76


