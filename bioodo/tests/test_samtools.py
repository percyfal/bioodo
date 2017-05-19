# Copyright (C) 2015 by Per Unneberg
import os
import pytest
from bioodo import samtools, odo, DataFrame
from pytest_ngsfixtures.config import application_fixtures
import utils

fixtures = application_fixtures(application="samtools")

stat_fixtures = [x for x in fixtures if x[1] == "samtools_stats"]
samtools_stats = utils.fixture_factory(stat_fixtures)


def test_basic_statistics(samtools_stats):
    module, command, version, end, pdir = samtools_stats
    fn = str(pdir.join("medium.stats.txt"))
    df = odo(samtools.resource_samtools_stats(fn), DataFrame)
    assert (list(df.index)[0] == 'raw total sequences')
    n = 60000 if end == "se" else 120000
    assert(df.loc["sequences", "value"] == n)


_gcc_stats = {'1.2': {'se': 30.12, 'pe': 30.21}, '1.3.1': {'se': 30.19, 'pe': 30.27}}
def test_GCC(samtools_stats):
    module, command, version, end, pdir = samtools_stats
    fn = str(pdir.join("medium.stats.txt"))
    df = odo(samtools.resource_samtools_stats(fn, key="GCC"), DataFrame)
    assert (df.loc[1]["A"] == _gcc_stats[version][end])


_ffq_stats = {'1.2': {'se': 27624, 'pe': 27630}, '1.3.1': {'se': 27598, 'pe': 27598}}    
def test_FFQ(samtools_stats):
    module, command, version, end, pdir = samtools_stats
    fn = str(pdir.join("medium.stats.txt"))
    df = odo(samtools.resource_samtools_stats(fn, key="FFQ"), DataFrame)
    assert (df.loc[1][33] == _ffq_stats[version][end])
