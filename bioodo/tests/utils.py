import os
import pytest
from pytest_ngsfixtures import factories


def fixture_factory(fixture_list):
    @pytest.fixture(scope="session", autouse=False, params=fixture_list,
                    ids=["{} {}:{}/{}".format(x[0], x[1], x[2], x[3]) for x in fixture_list])
    def bioodo_fixture(request, tmpdir_factory):
        # This assumes only one file is used for test
        module, command, version, end, fmtdict = request.param
        params = {'version': version, 'end': end}
        # Generate pytest_ngsfixtures application output names relative to
        # applications/module directory
        outputs = [fmt.format(**params) for fmt in fmtdict.values()]
        # Add applications/module prefix
        sources = [os.path.join("applications", module, output) for output in outputs]
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
            p = factories.safe_symlink(pdir, src, dst)
        return module, command, version, end, pdir
    return bioodo_fixture
