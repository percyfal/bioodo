#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from bioodo import picard
from pytest_ngsfixtures import factories
import pytest


FILES = ["applications/picard/2.9.0/pe/medium.align_metrics"]
data = factories.fileset(src=FILES, dst=["medium.align_metrics.foo"],
                         fdir="data")


def test_parse_uri_failure(data):
    infiles = [str(x) for x in data.listdir()]
    with pytest.raises(NotImplementedError):
        picard.aggregate(infiles)


def test_parse_uri_with_parser(data):
    infiles = [str(x) for x in data.listdir()]
    picard.aggregate(infiles, parser=picard.resource_align_metrics)
