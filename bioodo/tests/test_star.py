# Copyright (C) 2015 by Per Unneberg
from bioodo import star, odo, DataFrame
from pytest_ngsfixtures.config import application_fixtures
import utils


fixtures = application_fixtures(application="star")
data = utils.fixture_factory(fixtures)
aggregate_data = utils.aggregation_fixture_factory(
    [tuple([x[0], x[1], x[2], x[3], {'final': x[4]['final']}])
     for x in fixtures], 2)


def test_star_final_log(data):
    module, command, version, end, pdir = data
    fn = pdir.join("medium.Log.final.out")
    df = odo(str(fn), DataFrame)
    assert df.loc["Number of input reads", "value"] == 30483


def test_star_aggregate(aggregate_data):
    module, command, version, end, pdir = aggregate_data
    df = star.aggregate([str(x.listdir()[0]) for x in pdir.listdir()
                         if x.isdir()],
                        regex=".*/(?P<repeat>[0-9]+)/medium.Log.final.out")
    assert sorted(list(df["repeat"].unique())) == ['0', '1']
