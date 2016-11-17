# Copyright (C) 2015 by Per Unneberg
import os
import pytest
from bioodo import cutadapt, odo, DataFrame


@pytest.fixture(scope="module")
def cutadapt_se_data(tmpdir_factory):
    fn = tmpdir_factory.mktemp('cutadapt').join('single_end.cutadapt_metrics')
    fn.mksymlinkto(os.path.join(pytest.datadir, "cutadapt", "s1_1.trimmed.fastq.gz.cutadapt_metrics"))
    return fn

@pytest.fixture(scope="module")
def cutadapt_pe_data(tmpdir_factory):
    fn = tmpdir_factory.mktemp('cutadapt').join('paired_end.cutadapt_metrics')
    fn.mksymlinkto(os.path.join(pytest.datadir, "cutadapt", "s1.fastq.gz.cutadapt_metrics"))
    return fn

             
def test_cutadapt_se(cutadapt_se_data):
    df = odo(str(cutadapt_se_data), DataFrame)
    assert df.loc["Reads with adapters"]["value"] == 3

def test_cutadapt_pe(cutadapt_pe_data):
    df = odo(str(cutadapt_pe_data), DataFrame)
    assert df.loc["Read 1 with adapter"]["value"] == 3
    assert list(df.loc["Read 1"]["value"]) == [1900, 1868]

