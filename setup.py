from __future__ import print_function

# stdlib
import os
from setuptools import setup
from os.path import realpath, dirname, relpath, join

# Extensions
import versioneer

# --------------------------------------------------
# globals and constants
# --------------------------------------------------

ROOT = dirname(realpath(__file__))

# --------------------------------------------------
# classes and functions
# --------------------------------------------------

package_data = []

def package_path(path, filters=()):
    if not os.path.exists(path):
        raise RuntimeError("packaging non-existent path: %s" % path)
    elif os.path.isfile(path):
        package_data.append(relpath(path, 'bioodo'))
    else:
        for path, dirs, files in os.walk(path):
            path = relpath(path, 'bioodo')
            for f in files:
                if not filters or f.endswith(filters):
                    package_data.append(join(path, f))

scripts = []                    

REQUIRES = [
    'pandas',
    'odo',
]
                    
# Integrating pytest with setuptools: see
# http://pytest.org/latest/goodpractices.html#integrating-with-setuptools-python-setup-py-test-pytest-runner

_version = versioneer.get_version()
_cmdclass = versioneer.get_cmdclass()
_cmdclass.update({'test': PyTest})
setup(
    name="bioodo",
    version=_version,
    cmdclass=_cmdclass,
    author="Per Unneberg",
    author_email="per.unneberg@scilifelab.se",
    description="odo extensions for use with bioinformatics",
    license="MIT",
    url="http://github.com/percyfal/bioodo",
    scripts=scripts,
    packages=[
        'bioodo',
        'bioodo.tests',
    ],
    package_data={'bioodo': package_data},
    install_requires=REQUIRES,
    tests_requires=["pytest"],
)
