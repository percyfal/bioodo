#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pytest_ngsfixtures.config import application_fixtures
import utils


fixtures = application_fixtures(application="bwa")
bwa_data = utils.fixture_factory([x for x in fixtures])
bwa_aggregate_data = utils.aggregation_fixture_factory(
    [x for x in fixtures], 2)


def test_bwa(bwa_data):
    pass
