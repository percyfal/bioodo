# Copyright (C) 2016 by Per Unneberg
import re
from os.path import abspath, dirname, join, basename
import logging
import shutil
import subprocess as sp
import pytest

logger = logging.getLogger(__name__)

applications = [pytest.config.getoption("--application")] if pytest.config.getoption("--application") else pytest.applications

THREADS = pytest.config.getoption("--threads")

if not set(applications).issubset(pytest.applications):
    raise Exception("No such application '{}'".format(applications[0]))


