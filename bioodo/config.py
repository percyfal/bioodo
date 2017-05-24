#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import Mapping


def update_config(config, overwrite_config):
    """Recursively update dictionary config with overwrite_config.

    See
    http://stackoverflow.com/questions/3232943/update-value-of-a-nested-dictionary-of-varying-depth
    for details.

    Args:
      config (dict): dictionary to update
      overwrite_config (dict): dictionary whose items will overwrite
                               those in config

    """

    def _update(d, u):
        for (key, value) in u.items():
            if (isinstance(value, Mapping)):
                d[key] = _update(d.get(key, {}), value)
            else:
                d[key] = value
        return d

    _update(config, overwrite_config)
