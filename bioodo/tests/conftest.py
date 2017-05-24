# Copyright (C) 2016 by Per Unneberg
import os
import logging
import bioodo
from bioodo import settings

settings.CONFIGFILES = [os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                     ".bioodo.yaml"))]
bioodo.load_config()

pytest_plugins = 'pytester'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


blacklist = ['__pycache__', '__init__.py', 'tests', '_version.py',
             'pandas.py', 'utils.py']


def pytest_addoption(parser):
    group = parser.getgroup("bioodo", "bioodo test options")
    group.addoption("-M", "--bioodo-module", action="store",
                    default=False,
                    help="module to test",
                    dest="module")
