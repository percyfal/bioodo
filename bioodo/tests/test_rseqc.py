# Copyright (C) 2015 by Per Unneberg
from bioodo import rseqc, odo, DataFrame
from pytest_ngsfixtures.config import application_fixtures
import utils

blacklist = ["rseqc_junction_annotation"]
fixtures = application_fixtures(application="rseqc")
fixture_list = [f for f in fixtures if f[1] not in blacklist]
data = utils.fixture_factory(fixture_list, scope="function")


def test_rseqc_parse(data):
    module, command, version, end, pdir = data
    fn = pdir.listdir()[0]
    if command == "rseqc_read_duplication":
        df = odo(str(fn), DataFrame)
        fn = pdir.listdir()[1]
        df = odo(str(fn), DataFrame)
    else:
        df = odo(str(fn), DataFrame)
