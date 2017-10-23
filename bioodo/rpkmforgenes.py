# Copyright (C) 2015 by Per Unneberg
import pandas as pd
import bioodo
from bioodo import resource, annotate_by_uri, pivot, utils

config = bioodo.__RESOURCE_CONFIG__['rpkmforgenes']


@resource.register(config['rpkmforgenes']['pattern'],
                   priority=config['rpkmforgenes']['priority'])
@pivot
@annotate_by_uri
def resource_rpkmforgenes(uri, **kwargs):
    with open(uri):
        data = pd.read_csv(uri, sep="\t", header=None, comment="#",
                           names=["gene_id", "transcript_id", "FPKM", "TPM"],
                           index_col=["gene_id"])
    return data


aggregate = utils.aggregate_factory("rpkmforgenes")
