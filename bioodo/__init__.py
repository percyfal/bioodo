import os

__import__('pkg_resources').declare_namespace(__name__)

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

# Make odo visible via bioodo
from odo import odo

# Module imports for all submodules
from blaze import resource, DataFrame
from .pandas import annotate_by_uri
import numpy as np
import re
import logging
