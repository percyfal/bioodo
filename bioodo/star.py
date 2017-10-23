# Copyright (C) 2015 by Per Unneberg
import pandas as pd
import bioodo
from bioodo import resource, annotate_by_uri, pivot, utils
import logging


logger = logging.getLogger(__name__)
config = bioodo.__RESOURCE_CONFIG__['star']


@resource.register(config['log_final']['pattern'],
                   priority=config['log_final']['priority'])
@pivot
@annotate_by_uri
def resource_star_log(uri, **kwargs):
    """Parse Star Log.final.out log file"""
    df = pd.read_table(uri, sep="|", names=["name", "value"])
    df["name"] = [x.strip() for x in df["name"]]
    df["value"] = [utils.recast(x) for x in df["value"]]
    df = df.set_index("name")
    return df


aggregate = utils.aggregate_factory("star")
