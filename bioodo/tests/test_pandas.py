# Copyright (C) 2015 by Per Unneberg
import os
from blaze import DataFrame, odo, resource
import pandas as pd
from bioodo.pandas import annotate_by_uri, pivot
import pytest


@resource.register('.+\.csv', priority=20)
@pivot
@annotate_by_uri
def resource_csv_to_df(uri, **kwargs):
    df = pd.read_csv(uri)
    return df


@pytest.fixture(scope="module")
def dataframe1(tmpdir_factory):
    fn = tmpdir_factory.mktemp('data').join('sample1.dataframe1.csv')
    fn.write("""foo,bar\n1,2\n3,4""")
    return fn


@pytest.fixture(scope="module")
def dataframe2(tmpdir_factory):
    fn = tmpdir_factory.mktemp('data').join('sample2.dataframe2.csv')
    fn.write("""foo,bar\n5,6\n7,8""")
    return fn


def test_annotate_df(dataframe1, dataframe2):
    df1 = odo(str(dataframe1), DataFrame, annotate=True)
    df2 = df1.append(odo(str(dataframe2), DataFrame, annotate=True))
    assert set([os.path.basename(x) for x in df2['uri']]) == \
        {'sample1.dataframe1.csv', 'sample2.dataframe2.csv'}


def test_custom_annotate_df(dataframe1, dataframe2):
    def _annotate_fn(df, uri, **kwargs):
        uristr = os.path.basename(uri)
        df['sample'] = uristr.split(".")[0]
        return df

    df1 = odo(str(dataframe1), DataFrame, annotate=True,
              annotation_fn=_annotate_fn)
    df2 = df1.append(odo(str(dataframe2), DataFrame, annotate=True,
                         annotation_fn=_annotate_fn))
    assert set(df2['sample']) == {'sample1', 'sample2'}


def test_annotate_df_regex(dataframe1, dataframe2):
    df1 = odo(str(dataframe1), DataFrame, annotate=True,
              regex=".*(?P<sample>sample\d+)\.(?P<df>[a-z]+\d+)\.csv")
    df2 = df1.append(
        odo(str(dataframe2), DataFrame,
            annotate=True,
            regex=".*(?P<sample>sample\d+)\.(?P<df>[a-z]+\d+)\.csv"))
    assert set(df2['sample'] == {'sample1', 'sample2'})
    assert set(df2['df'] == {'dataframe1', 'dataframe2'})


def test_pivot_uri(dataframe1):
    df = odo(str(dataframe1), DataFrame, columns="foo", values="bar",
             index="uri", annotate=True)
    assert df.shape == (1, 2)
    assert list(df.columns) == [1, 3]
    assert df.index.name == "uri"


def test_pivot_regex(dataframe1):
    df = odo(str(dataframe1), DataFrame, columns="foo", values="bar",
             index="sample",
             regex=".*(?P<sample>sample\d+)\.(?P<df>[a-z]+\d+)\.csv")
    assert list(df.index) == ["sample1"]


def test_pivot_no_index(dataframe1):
    with pytest.raises(ValueError):
        odo(str(dataframe1), DataFrame, values="bar",
            annotate=True)


def test_pivot_no_column(dataframe1):
    with pytest.raises(ValueError):
        odo(str(dataframe1), DataFrame, values="bar",
            annotate=True, index="uri")


def test_pivot_no_value(dataframe1):
    df = odo(str(dataframe1), DataFrame, columns="bar",
             annotate=True, index="uri")
    assert df.index.name == "uri"
