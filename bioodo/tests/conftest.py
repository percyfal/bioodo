# Copyright (C) 2016 by Per Unneberg
import os
from os.path import abspath, dirname, join, isdir
import re
import logging
import pytest
import shutil
import subprocess as sp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TESTDIR = abspath(dirname(__file__))
DATADIR = join(TESTDIR, "data")
BIOODO = join(TESTDIR, os.pardir, os.pardir, "bioodo")

blacklist = ['__pycache__', '__init__.py', 'tests', '_version.py', 'pandas.py', 'utils.py']
applications = [x.strip('.py') for x in os.listdir(BIOODO) if x not in blacklist]
    
# Add namespace with test files and director
def pytest_namespace():
    return {
        'testdir': TESTDIR,
        'datadir': DATADIR,
        'applications' : applications,
    }

##################################################
# Setup test fixtures
##################################################
# Input files
sample1_1 = abspath(join(dirname(__file__), "data", "s1_1.fastq.gz"))
sample1_2 = abspath(join(dirname(__file__), "data", "s1_2.fastq.gz"))
sam = abspath(join(dirname(__file__), "data", "s1.sam"))
bam = abspath(join(dirname(__file__), "data", "s1.bam"))

##############################
# sample
##############################
@pytest.fixture(scope="function", autouse=False)
def data(tmpdir_factory):
    """
    Setup input data
    """
    p = tmpdir_factory.mktemp('data')
    p.join("s1_1.fastq.gz").mksymlinkto(sample1_1)
    p.join("s1_2.fastq.gz").mksymlinkto(sample1_2)
    p.join("s1.sam").mksymlinkto(sam)
    p.join("s1.bam").mksymlinkto(bam)
    return p
