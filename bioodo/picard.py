# Copyright (C) 2015 by Per Unneberg
from blaze import resource, DataFrame
import pandas as pd
from .pandas import annotate_by_uri, pivot
import logging
import bioodo
from bioodo import utils


config = bioodo.__RESOURCE_CONFIG__['picard']
logger = logging.getLogger(__name__)


def _hist_reader(uri):
    with open(uri) as fh:
        data = [x.strip("\n").split("\t") for x in fh
                if not x.strip() == ""]
        indices = list((i for i, val in enumerate(data)
                        if val[0].startswith("## METRICS CLASS") or
                        val[0].startswith("## HISTOGRAM")))
        if len(indices) == 1:
            indices.append(len(data))
        metrics = DataFrame.from_records(data[(indices[0] + 2):(indices[1])],
                                         columns=data[(indices[0] + 1)])
        # We could be missing the histogram
        try:
            hist = DataFrame.from_records(data[(indices[1] + 2):],
                                          columns=data[(indices[1] + 1)])
        except:
            logger.warn("No histogram data for {}".format(uri))
            hist = None
    return (metrics, hist)


def _reader(uri):
    with open(uri) as fh:
        data = [x.strip("\n").split("\t") for x in fh
                if not x.strip() == ""]
        indices = list((i for i, val in enumerate(data)
                        if val[0].startswith("## METRICS CLASS")))
        metrics = DataFrame.from_records(data[(indices[0] + 2):],
                                         columns=data[(indices[0] + 1)],
                                         index="CATEGORY")
    return (metrics, None)


@resource.register(config['align_metrics']['pattern'],
                   priority=config['align_metrics']['priority'])
@pivot
@annotate_by_uri
def resource_align_metrics(uri, **kwargs):
    """Parse picard AlignmentSummaryMetrics text output file.

    Args:
      uri (str): filename

    Returns:
      DataFrame
    """
    metrics, _ = _reader(uri)
    metrics = metrics.apply(pd.to_numeric, axis=1)
    return metrics


@resource.register(config['insert_metrics']['pattern'],
                   priority=config['insert_metrics']['priority'])
@pivot
@annotate_by_uri
def resource_insert_metrics(uri, key="metrics", **kwargs):
    """Parse picard InsertSummaryMetrics text output file.

    Args:
      uri (str): filename
      key (str): result section to return (hist or metrics)

    Returns:
      DataFrame for requested section
    """
    logger.debug("Reading {}".format(uri))
    (_metrics, hist) = _hist_reader(uri)
    metrics = _metrics[_metrics.columns.difference(
        ["PAIR_ORIENTATION"])].apply(pd.to_numeric, axis=0)
    metrics["PAIR_ORIENTATION"] = _metrics["PAIR_ORIENTATION"]
    hist = hist.apply(pd.to_numeric, axis=0)
    if key == "metrics":
        return metrics
    elif key == "hist":
        return hist


@resource.register(config['hs_metrics']['pattern'],
                   priority=config['hs_metrics']['priority'])
@pivot
@annotate_by_uri
def resource_hs_metrics(uri, **kwargs):
    """Parse picard HybridSelectionMetrics text output file.

    Args:
      uri (str): filename

    Returns:
      DataFrame
    """
    return _hist_reader(uri)


@resource.register(config['dup_metrics']['pattern'],
                   priority=config['dup_metrics']['priority'])
@pivot
@annotate_by_uri
def resource_dup_metrics(uri, key="metrics", **kwargs):
    """Parse picard DuplicationMetrics text output file.

    Args:
      uri (str): filename
      key (str): result section to return (hist or metrics)

    Returns:
      DataFrame for requested section
    """
    (_metrics, hist) = _hist_reader(uri)
    metrics = _metrics[
        _metrics.columns.difference(["LIBRARY"])].apply(pd.to_numeric, axis=0)
    if hist is not None:
        hist = hist.apply(pd.to_numeric, axis=0)
    if key == "metrics":
        return metrics
    elif key == "hist":
        return hist


aggregate = utils.aggregate_factory("picard")
