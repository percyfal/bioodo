import os
import pytest
from pytest_ngsfixtures import factories
import logging


logger = logging.getLogger(__name__)


def fixture_factory(fixture_list, unique=False, **kwargs):
    """Fixture factory to generate fixtures from
    a list of pytest-ngsfixtures fixtures

    Params:
      fixture_list(list): list of tuples, where each tuple consists of
                          module, command, version, end and file name format
      unique(boolean): make unique fixture directories; useful if one
                       wants to separate multiple outputs into
                       separate directories
      kwargs(dict): keyword arguments
    """
    if unique:
        for i in range(len(fixture_list)):
            y = list(fixture_list[i])
            y[1] = "{}_{}".format(y[1], i)
            fixture_list[i] = tuple(y)

    @pytest.fixture(scope="session", autouse=False, params=fixture_list,
                    ids=["{} {}:{}/{}".format(x[0], x[1], x[2], x[3])
                         for x in fixture_list])
    def bioodo_fixture(request, tmpdir_factory):
        # NB: fmtdict is a dictionary, potentially pointing to
        # multiple output files
        module, command, version, end, fmtdict = request.param
        params = {'version': version, 'end': end}
        # Generate pytest_ngsfixtures application output names relative to
        # applications/module directory
        outputs = [fmt.format(**params) for fmt in fmtdict.values()]
        # Add applications/module prefix
        sources = [os.path.join("applications", module, output)
                   for output in outputs]
        # Extract source basenames
        dests = [os.path.basename(src) for src in sources]
        # Generate a unique test output directory name
        fdir = os.path.join(module, str(version), command, end)
        # Make a temporary directory using unique test directory name
        pdir = factories.safe_mktemp(tmpdir_factory, fdir)
        # Symlink pytest_ngsfixtures files to temporary directory; the
        # safe_symlink function automagically uses pytest_ngsfixtures
        # installation directory to infer location of src
        for src, dst in zip(sources, dests):
            factories.safe_symlink(pdir, src, dst)
        return module, command, version, end, pdir
    return bioodo_fixture


def aggregation_fixture_factory(fixture_list, repeat, **kwargs):
    """Fixture factory for aggregation data.

    Aggregation data requires multiple inputs. This can be
    accomplished by using the same output multiple times, generating
    unique fixture names on the fly.

    Params:
      fixture_list (list): an application fixture
      repeat (int): number of times to repeat input file
      kwargs (dict): keyword arguments

    Returns:
       a fixture, corresponding to a directory where input files reside
       in subdirectories named after version and end

    """
    @pytest.fixture(scope=kwargs.get("scope", "session"),
                    autouse=kwargs.get("autouse", False),
                    params=fixture_list,
                    ids=["{} {}:{}/{}".format(x[0], x[1], x[2], x[3])
                         for x in fixture_list])
    def bioodo_aggregation_fixture(request, tmpdir_factory):
        # NB: fmtdict is a dictionary, potentially pointing to
        # multiple output files; if so the multiple files must be put
        # in the same directory
        module, command, version, end, fmtdict = request.param
        params = {'version': version, 'end': end}
        keys = kwargs.get("keys", fmtdict.keys())
        outputs = [fmtdict[k].format(**params)
                   for k in keys] * len(range(repeat))
        # Add applications/module prefix
        sources = [os.path.join("applications", module, output)
                   for output in outputs]
        # Extract source basenames
        dests = [os.path.basename(src) for src in outputs]
        # Generate a unique test output directory
        fdir = os.path.join(module, str(version), command, end)
        # Make a temporary directory using unique test directory name
        pdir = factories.safe_mktemp(tmpdir_factory, fdir)
        # Symlink pytest_ngsfixtures files to temporary directory; the
        # safe_symlink function automagically uses pytest_ngsfixtures
        # installation directory to infer location of src
        count = 0
        for src, dst in zip(sources, dests):
            rdir = pdir.mkdir(str(count))
            factories.safe_symlink(rdir, src, dst)
            count += 1
        return module, command, version, end, pdir
    return bioodo_aggregation_fixture
