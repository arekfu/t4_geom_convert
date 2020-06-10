'''.. _pytest: https://docs.pytest.org/en/latest

`pytest`_ configuration file.
'''
import pathlib

import pytest


def pytest_addoption(parser):
    '''Add the ``--oracle-path`` and ``--mcnp-path`` options to `pytest`.'''
    parser.addoption('--oracle-path', action='store',
                     help='path to the oracle executable', default=None,
                     type=pathlib.Path)
    parser.addoption('--mcnp-path', action='store',
                     help='path to the MCNP executable', default=None,
                     type=pathlib.Path)
    parser.addoption('--extra-mcnp-inputs', action='store',
                     help='Path to a file containing a list of additional '
                     'MCNP input files to test conversion',
                     default=None, type=pathlib.Path)


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


def pytest_generate_tests(metafunc):
    '''Generate tests for the --extra-mcnp-inputs option'''
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    if 'extra_input' in metafunc.fixturenames:
        extra_inputs_file = metafunc.config.option.extra_mcnp_inputs
        if extra_inputs_file is None:
            paths = []
        else:
            with extra_inputs_file.open() as extra_file:
                extra_inputs = extra_file.readlines()
            extra_inputs_path = extra_inputs_file.parent.resolve()
            paths = []
            for name in extra_inputs:
                path = pathlib.Path(name.strip())
                if path.is_absolute():
                    paths.append(path)
                else:
                    paths.append(extra_inputs_path / path)
        ids = [path.name for path in paths]
        metafunc.parametrize('extra_input', paths, ids=ids)
