import os
import yaml
from bioodo import settings

__import__('pkg_resources').declare_namespace(__name__)

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

ROOT = os.path.dirname(os.path.realpath(__file__))

# Make odo visible via bioodo
from odo import odo

# Module imports for all submodules
from blaze import resource, DataFrame
from .pandas import annotate_by_uri, pivot
import numpy as np
import re
import logging
from . import config

logger = logging.getLogger(__name__)


# Set global configuration varibable to hold resource configuration
global __RESOURCE_CONFIG__
with open(os.path.join(ROOT, "data", "config.yaml")) as fh:
    __RESOURCE_CONFIG__ = yaml.load(fh)

def load_config():
    for f in settings.CONFIGFILES:
        logger.info("Looking for configuration file {}".format(f))
        logger.debug("Looking for configuration file {}".format(f))
        if os.path.exists(f):
            logger.debug("Reading local config {}".format(f))
            with open(f) as fh:
                _localconfig = yaml.load(fh)
            config.update_config(__RESOURCE_CONFIG__, _localconfig)

load_config()
