# Copyright (C) 2015 by Per Unneberg
import pandas as pd
from blaze import append, DataFrame


@append.register(DataFrame, DataFrame)
def append_dataframe_to_dataframe(tgt, src, **kw):
    tgt = pd.concat([tgt, src])
    return tgt


def annotate_by_uri(func):
    """Decorator function annotate_by_uri.

    Wrap function with wrapper that will optionally add an annotation
    to the data frame based on the uri. This can be particularly
    useful when merging several files and the data provenance needs to
    be tracked.

    Params:
      annotate (bool): whether or not to annotate data frame
      annotation_fn (function): use custom function to annotate data frame

    """
    def wrap(uri, **kwargs):
        df = func(uri, **kwargs)
        if not kwargs.get('annotate', False):
            return df
        annotation_fn = kwargs.get('annotation_fn', None)
        if annotation_fn is not None:
            df = annotation_fn(df, uri, **kwargs)
        else:
            df['uri'] = uri
        return df
    return wrap
