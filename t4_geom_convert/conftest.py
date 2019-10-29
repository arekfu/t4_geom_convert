'''.. _pytest: https://docs.pytest.org/en/latest

`pytest`_ configuration file.
'''
import pathlib
import pytest
import py


def pytest_addoption(parser):
    '''Add the ``--run-slow`` and ``--mcnp-path`` options to `pytest`.'''
    parser.addoption('--run-slow', action='store_true',
                     default=False, help='run slow tests')
    parser.addoption('--mcnp-path', action='store',
                     help='path to the MCNP executable', default=None,
                     type=pathlib.Path)
    parser.addoption('--oracle-path', action='store',
                     help='path to the oracle executable', default=None,
                     type=pathlib.Path)


def pytest_collection_modifyitems(config, items):
    '''Handle CLI options to pytest.'''
    a_mcnp_path = config.getoption('--mcnp-path')
    a_or_path = config.getoption('--oracle-path')
    if not (a_mcnp_path and a_mcnp_path.exists()
            and a_or_path and a_or_path.exists()):
        skip_or = pytest.mark.skip(reason='needs --mcnp-path and '
                                   '--oracle-path options to run')
        for item in items:
            if 'oracle' in item.keywords:
                item.add_marker(skip_or)

    if not config.getoption("--run-slow"):
        skip_slow = pytest.mark.skip(reason="needs --run-slow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)


##############
#  fixtures  #
##############


@pytest.fixture
def datadir(tmpdir, request):
    '''Fixture responsible for searching a folder called 'data' in the same
    directory as the test module and, if available, moving all contents to a
    temporary directory so tests can use them freely.
    '''
    filename = request.fspath
    test_dir = filename.dirpath('data')

    if test_dir.check():
        test_dir.copy(tmpdir)

    return tmpdir


@pytest.fixture
def workdir(tmpdir):
    '''Fixture that cd's to a temporary working directory.'''
    with tmpdir.as_cwd():
        yield tmpdir


@pytest.fixture
def mcnp_path(request):
    '''Fixture yielding the path to the MCNP executable specified on the
    command line.'''
    return request.config.getoption('--mcnp-path')


@pytest.fixture
def oracle_path(request):
    '''Fixture yielding the path to the oracle executable specified on the
    command line.'''
    return request.config.getoption('--oracle-path')


def foreach_data(*args, **kwargs):
    '''Decorator that parametrizes a test function over files in the data
    directory for the current tests.

    Assume that the following snippet resides in
    :file:`tests/submod/test_submod.py`::

        @foreach_data('datafile')
        def test_something(datafile):
            pass

    When `pytest` imports :file:`test_submod.py`, it will parametrize
    the `datafile` argument to :func:`!test_something` over all the files
    present in :file:`tests/submod/data/`.

    If you wish to filter away some of the files, you can use the alternative
    syntax::

        @foreach_data(datafile=lambda path: str(path).endswith('.txt'))
        def test_something(datafile):
            pass

    Here the argument to the `datafile` keyword argument is a predicate that
    must return `True` if `path` is to be parametrized over, and `False`
    otherwise. Note that the `path` argument to the lambda is a
    :class:`py._path.local.LocalPath` object.  In this example, `pytest` will
    parametrize :func:`!test_something` only over files whose name ends in
    ``'.txt'``.
    '''

    if args:
        if len(args) != 1:
            raise ValueError('Only one positional argument allowed to '
                             '@foreach_data')
        if kwargs:
            raise ValueError('No kwargs allowed with a positional '
                             'argument to @foreach_data')
        fix_name = args[0]
        fil = None
    else:
        if len(kwargs) != 1:
            raise ValueError('Only one kwarg allowed in @foreach_data')
        fix_name, fil = next(iter(kwargs.items()))

    def _decorator(wrapped):
        from inspect import getfile
        module_dir = py.path.local(getfile(wrapped))  # pylint: disable=E1101
        test_dir = module_dir.dirpath('data')
        datafiles = [path for path in test_dir.listdir(fil=fil)
                     if path.isfile()]
        ids = [str(path.basename) for path in datafiles]
        return pytest.mark.parametrize(fix_name, datafiles, ids=ids)(wrapped)
    return _decorator
