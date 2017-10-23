# Copyright (C) 2015 by Per Unneberg
import pandas as pd
import bioodo
from bioodo import resource, annotate_by_uri, pivot, utils

config = bioodo.__RESOURCE_CONFIG__['rsem']


@resource.register(config['genes']['pattern'],
                   priority=config['genes']['priority'])
@pivot
@annotate_by_uri
def resource_genes_results(uri, **kwargs):
    with open(uri):
        data = pd.read_csv(uri, sep="\t", header=0, comment="#",
                           index_col=["gene_id"])
    return data


@resource.register(config['isoforms']['pattern'],
                   priority=config['isoforms']['priority'])
@pivot
@annotate_by_uri
def resource_isoforms_results(uri, **kwargs):
    with open(uri):
        data = pd.read_csv(uri, sep="\t", header=0, comment="#",
                           index_col=["transcript_id"])
    return data


aggregate = utils.aggregate_factory("rsem")
