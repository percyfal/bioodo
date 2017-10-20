#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bioodo import bamtools, odo, DataFrame
from pytest_ngsfixtures.config import application_fixtures
import utils

fixtures = application_fixtures(application="bamtools")
bamtools_data = utils.fixture_factory([x for x in fixtures])
bamtools_aggregate_data = utils.aggregation_fixture_factory(
    [x for x in fixtures], 2)


def test_bamtools(bamtools_data):
    module, command, version, end, pdir = bamtools_data
    df = odo(str(pdir.listdir()[0]), DataFrame)
    n = 59499 if end == "se" else 119413
    assert df.loc["Mapped reads", "value"] == n


def test_bamtools_aggregate(bamtools_aggregate_data):
    module, command, version, end, pdir = bamtools_aggregate_data
    df = bamtools.aggregate(
        [str(x.listdir()[0]) for x in pdir.listdir() if x.isdir()],
        regex=".*/(?P<repeat>[0-9]+)/medium.stats")
    assert sorted(list(df["repeat"].unique())) == ['0', '1']


def test_bamtools_pivot(bamtools_data):
    module, command, version, end, pdir = bamtools_data
    df = odo(
        str(pdir.listdir()[0]), DataFrame,
        values=["value", "percent"], columns="statistic",
        index="sample",
        regex=".*/(?P<sample>medium.*)"
    )
    n = 59499 if end == "se" else 119413
    assert df["value", "Mapped reads"].loc["medium.stats"] == n


def test_bamtools_aggregate_pivot(bamtools_aggregate_data):
    module, command, version, end, pdir = bamtools_aggregate_data
    df = bamtools.aggregate(
        [str(x.listdir()[0]) for x in pdir.listdir() if x.isdir()],
        values=["value", "percent"], columns="statistic",
        index="repeat",
        regex=".*/(?P<repeat>[0-9]+)/medium.stats"
    )
    n = 59499 if end == "se" else 119413
    assert df["value", "Mapped reads"].loc["0"] == n
