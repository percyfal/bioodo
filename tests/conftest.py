# Copyright (C) 2016 by Per Unneberg
import pytest

# Custom options
def pytest_addoption(parser):
    parser.addoption("-A", "--application", action="store",
                     help="application to test",
                     dest="application")
    parser.addoption("-T", "--threads", action="store",
                     default="1",
                     help="number of threads to use",
                     dest="threads")


