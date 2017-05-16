# Copyright (C) 2015 by Per Unneberg
from bioodo import cutadapt, odo, DataFrame

from pytest_ngsfixtures.config import application_fixtures
import utils

fixtures = application_fixtures(application="cutadapt")
cutadapt_metrics = utils.fixture_factory(fixtures)


def test_cutadapt(cutadapt_metrics):
    module, command, version, end, pdir = cutadapt_metrics
    fn = str(pdir.join("cutadapt_metrics.txt"))
    df = odo(cutadapt.resource_cutadapt_metrics(fn), DataFrame, foo="bar")
    if end == "se":
        assert df.loc["Reads with adapters"]["value"] == 792
    elif end == "pe":
        assert df.loc["Read 1 with adapter"]["value"] == 792
