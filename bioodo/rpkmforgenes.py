# Copyright (C) 2015 by Per Unneberg
from blaze import resource
import pandas as pd
from .pandas import annotate_by_uri
import bioodo

config = bioodo.__RESOURCE_CONFIG__['rpkmforgenes']


@resource.register(config['rpkmforgenes']['pattern'],
                   priority=config['rpkmforgenes']['priority'])
@annotate_by_uri
def resource_rpkmforgenes(uri, **kwargs):
    with open(uri):
        data = pd.read_csv(uri, sep="\t", header=None, comment="#",
                           names=["gene_id", "transcript_id", "FPKM", "TPM"],
                           index_col=["gene_id"])
    return data
