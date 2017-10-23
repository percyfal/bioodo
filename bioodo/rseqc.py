# Copyright (C) 2015 by Per Unneberg
import re
import pandas as pd
import bioodo
from bioodo import resource, annotate_by_uri, pivot, DataFrame, utils
import logging


logger = logging.getLogger(__name__)
config = bioodo.__RESOURCE_CONFIG__['rseqc']


@resource.register(config['read_distribution']['pattern'],
                   priority=config['read_distribution']['priority'])
@pivot
@annotate_by_uri
def resource_read_distribution(uri, **kwargs):
    df = pd.read_table(uri, skiprows=list(range(0, 4)) + [15],
                       sep="[ ]+", engine="python")
    df = df.set_index("Group")
    return df


@resource.register(config['data_frame']['pattern'],
                   priority=config['data_frame']['priority'])
@pivot
@annotate_by_uri
def resource_data_frame(uri, **kwargs):
    df = pd.read_table(uri, header=0)
    return df


@resource.register(config['clipping_profile']['pattern'],
                   priority=config['clipping_profile']['priority'])
@pivot
@annotate_by_uri
def resource_clipping_profile(uri, **kwargs):
    pe = False
    with open(uri) as fh:
        data = "".join(fh)
    header, read = [x.strip() for x in data.split("\n")[0:2]]
    if read == "Read-1:":
        pe = True
    if pe:
        sections = re.split("\nRead-2:\n", data)
        df1 = DataFrame.from_records(
            [x.split("\t") for x in sections[0].split("\n")[2:]])
        df1.columns = header.split("\t")
        df1["Read"] = 1
        df2 = DataFrame.from_records(
            [x.split("\t") for x in sections[1].split("\n")])
        df2.columns = header.split("\t")
        df2["Read"] = 2
        df = pd.concat([df1, df2])
    else:
        df = pd.read_table(uri)
    df.set_index("Position")
    return df


@resource.register(config['xls']['pattern'],
                   priority=config['xls']['priority'])
@pivot
@annotate_by_uri
def resource_xls(uri, **kwargs):
    df = pd.read_table(uri, header=0)
    return df


aggregate = utils.aggregate_factory("rseqc")
