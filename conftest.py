# Copyright 2019-2024 French Alternative Energies and Atomic Energy Commission
#
# This file is part of t4_geom_convert.
#
# t4_geom_convert is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# t4_geom_convert is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along with
# t4_geom_convert.  If not, see <https://www.gnu.org/licenses/>.
#
# vim: set fileencoding=utf-8 :
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
    parser.addoption('--oracle-zero-tolerance', action='store_true',
                     help='Do not tolerate any failed point in the oracle '
                     'test, regardless of what the ``oracle-tolerance`` magic '
                     'comment says')


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


@pytest.fixture
def oracle_zero_tolerance(request):
    '''Returns the value of the ``--oracle-zero-tolerance`` CLI option.'''
    return request.config.getoption('--oracle-zero-tolerance')


def pytest_generate_tests(metafunc):
    '''Generate tests for the --extra-mcnp-inputs option'''
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    if 'extra_input' in metafunc.fixturenames:
        extra_inputs_file = metafunc.config.option.extra_mcnp_inputs
        if extra_inputs_file is None:
            paths = []
        else:
            extra_inputs_file = extra_inputs_file.expanduser()
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
