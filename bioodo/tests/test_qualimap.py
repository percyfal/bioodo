# Copyright (C) 2015 by Per Unneberg
import os
import pytest
from bioodo import qualimap, DataFrame, odo


@pytest.fixture(scope="module")
def qualimap_data(tmpdir_factory):
    fn = tmpdir_factory.mktemp('test.bam.qualimap').join('genome_results.txt')
    fn.mksymlinkto(os.path.join(pytest.datadir, "qualimap", "genome_results.txt"))
    return fn


def test_qualimap(qualimap_data):
    df = odo(str(qualimap_data), DataFrame, key='Coverage_per_contig')
    assert list(df.columns) == ['chrlen', 'mapped_bases', 'mean_coverage', 'sd']
    assert list(df.index) == ['chr11']
