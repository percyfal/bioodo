# Copyright (C) 2015 by Per Unneberg
from bioodo import qualimap, odo, DataFrame
from pytest_ngsfixtures.config import application_fixtures
import utils


fixtures = application_fixtures(application="qualimap")

# Separate pe and se cases
outputs = {'pe': {}, 'se': {}}
newfixtures = []
for x in fixtures:
    for k, v in x[4].items():
        y = tuple([x[0], x[1], x[2], x[3], {k: v}])
        newfixtures.append(y)

data = utils.fixture_factory(newfixtures, scope="function", unique=True)
qualimap_aggregate_data = utils.aggregation_fixture_factory(
    [x for x in newfixtures if "homopolymer_indels" in x[4].keys()], 2)


def test_qualimap(data):
    module, command, version, end, pdir = data
    if command.startswith("qualimap_bamqc_genome_results"):
        fn = pdir.listdir()[0]
        df = odo(str(fn), DataFrame, key='Coverage_per_contig')
        assert list(df.columns) == ['chrlen', 'mapped_bases',
                                    'mean_coverage', 'sd']
        assert list(df.index)[0] == 'scaffold1'
    else:
        fn = pdir.listdir()[0]
        df = odo(str(fn), DataFrame)
        assert "#" not in df.columns[0]


def test_qualimap_aggregate(qualimap_aggregate_data):
    module, command, version, end, pdir = qualimap_aggregate_data
    df = qualimap.aggregate(
        [str(x.listdir()[0]) for x in pdir.listdir()
         if x.isdir()],
        regex=".*/(?P<repeat>[0-9]+)/homopolymer_indels.txt")
    assert sorted(list(df["repeat"].unique())) == ['0', '1']


def test_qualimap_aggregate_compress(qualimap_aggregate_data):
    module, command, version, end, pdir = qualimap_aggregate_data
    qualimap.aggregate(
        [str(x.listdir()[0]) for x in pdir.listdir()
         if x.isdir()],
        regex=".*/(?P<repeat>[0-9]+)/homopolymer_indels.txt",
        outfile=str(pdir.join("test.csv.gz")))
    assert pdir.join("test.csv.gz").exists()
