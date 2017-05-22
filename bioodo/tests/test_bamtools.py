#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import bioodo
from bioodo import bamtools, odo, DataFrame
import logging
from pytest_ngsfixtures.config import application_fixtures
import utils

fixtures = application_fixtures(application="bamtools")
bamtools_data = utils.fixture_factory([x for x in fixtures])
bamtools_aggregate_data = utils.aggregation_fixture_factory(
    [x for x in fixtures], 2)


def test_bamtools(bamtools_data, caplog):
    caplog.setLevel(logging.DEBUG)
    module, command, version, end, pdir = bamtools_data
    df = odo(str(pdir.listdir()[0]), DataFrame)
    n = 59499 if end == "se" else 119413
    assert df.loc["Mapped reads", "value"] == n


def test_bamtools_aggregate(bamtools_aggregate_data, caplog):
    caplog.setLevel(logging.DEBUG)
    module, command, version, end, pdir = bamtools_aggregate_data
    df = bamtools.aggregate([str(x.listdir()[0]) for x in pdir.listdir() if x.isdir()],
                            regex=".*/(?P<repeat>[0-9]+)/medium.stats")
    assert sorted(list(df["repeat"].unique())) == ['0', '1']



