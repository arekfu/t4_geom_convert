# Copyright 2019-2021 Davide Mancusi, Martin Maurey, Jonathan Faustin
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
import subprocess as sub
import re

import pytest

# pylint: disable=redefined-outer-name

##############
#  fixtures  #
##############


@pytest.fixture
def datadir(tmp_path, request):
    '''Fixture responsible for searching a folder called 'data' in the same
    directory as the test module and, if available, moving all contents to a
    temporary directory so tests can use them freely.
    '''
    import py
    filename = request.fspath
    test_dir = filename.dirpath('data')

    if test_dir.check():
        test_dir.copy(py.path.local(tmp_path))  # pylint: disable=no-member

    return tmp_path


@pytest.fixture
def mcnp_path(request):
    '''Fixture yielding the path to the MCNP executable specified on the
    command line.'''
    path = request.config.getoption('--mcnp-path')
    if path is not None:
        path = path.expanduser()
    return path


@pytest.fixture
def oracle_path(request):
    '''Fixture yielding the path to the oracle executable specified on the
    command line.'''
    path = request.config.getoption('--oracle-path')
    if path is not None:
        path = path.expanduser()
    return path


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
    :class:`pathlib.Path` object.  In this example, `pytest` will parametrize
    :func:`!test_something` only over files whose name ends in ``'.txt'``.
    '''

    if args:
        if len(args) != 1:
            raise ValueError('Only one positional argument allowed to '
                             '@foreach_data')
        if kwargs:
            raise ValueError('No kwargs allowed with a positional '
                             'argument to @foreach_data')
        fix_name = args[0]

        def fil(_):
            return True
    else:
        if len(kwargs) != 1:
            raise ValueError('Only one kwarg allowed in @foreach_data')
        fix_name, fil = next(iter(kwargs.items()))

    def _decorator(wrapped, fil=fil):
        from inspect import getfile
        module_dir = pathlib.Path(getfile(wrapped))  # pylint: disable=E1101
        test_dir = module_dir.parent / 'data'
        datafiles = [path for path in test_dir.iterdir()
                     if path.is_file() and fil(path)]
        ids = [str(path.name) for path in datafiles]
        return pytest.mark.parametrize(fix_name, datafiles, ids=ids)(wrapped)
    return _decorator


class MCNPRunner:  # pylint: disable=too-few-public-methods
    '''A helper class to run MCNP on a given input file.'''

    def __init__(self, path, work_path):
        '''Create an instance of :class:`MCNPRunner`.

        :param path: path to the MCNP executable
        :type path: pathlib.Path
        :param work_path: path to the working directory
        :type work_path: pathlib.Path
        '''
        self.path = path
        self.work_path = work_path

    def run(self, input_file):
        '''Run MCNP on the given input file.

        :param str input_file: absolute path to the input file
        :returns: the paths to the generated output and PTRAC files
        :rtype: (pathlib.Path, pathlib.Path)
        '''
        run_name = 'run_' + input_file.name
        cli = [str(self.path),
               'inp={}'.format(input_file),
               'name={}'.format(run_name)]
        output = self.work_path / (run_name + 'o')
        ptrac = self.work_path / (run_name + 'p')
        try:
            sub.check_call(cli, cwd=str(self.work_path))
        except sub.CalledProcessError:
            msg = 'MCNP run failed. The output is here: {}'.format(str(output))
            raise ValueError(msg)
        return output, ptrac


@pytest.fixture
def mcnp(mcnp_path, tmp_path):
    '''Return an instance of the :class:`MCNPRunner` class.'''
    return MCNPRunner(mcnp_path, tmp_path)


def check_failed_points(failed_path):
    '''Read the `failed_path` file and return the number of failed points
    and the maximum distance for them.'''
    n_points, dist = 0, 0
    with failed_path.open() as failed_path_file:
        for line in failed_path_file:
            n_points += 1
            fields = line.strip().split()
            assert len(fields) == 8
            dist = max(dist, float(fields[6]))
    return n_points, dist


def parse_outside_points(stdout_path):
    '''Parse the file at `stdout_path` and return the number of points that
    fall outside the geometry.'''
    outside_re = re.compile(r'Number of OUTSIDE {8}: (\d+)')
    with stdout_path.open() as stdout:
        for line in stdout:
            match = outside_re.match(line)
            if match:
                return int(match.group(1))
    return None


class OracleRunner:  # pylint: disable=too-few-public-methods
    '''A helper class to run the test oracle.'''

    def __init__(self, path, work_path):
        '''Create an instance of :class:`OracleRunner`.

        :param path: path to the MCNP executable
        :type path: str or path-like object
        :param work_path: path to the working directory
        :type work_path: str or path-like object
        '''
        self.path = path
        self.work_path = work_path

    def run(self, t4_o, mcnp_i, mcnp_ptrac, oracle_opts=None):
        '''Run the test oracle on the given files.

        :param str t4_o: absolute path to the TRIPOLI-4 file to test
        :param str mcnp_i: absolute path to the MCNP input file
        :param str mcnp_ptrac: absolute path to the MCNP PTRAC file
        :returns: the number of failed points in the comparison
        '''
        cli = [str(self.path), str(t4_o), str(mcnp_i), str(mcnp_ptrac)]
        if oracle_opts is not None:
            cli += oracle_opts
        stdout_fname = self.work_path / 'stdout'
        print('Running oracle...\n' + '---8<---' * 9)
        try:
            with stdout_fname.open('w') as stdout:
                sub.check_call(cli, cwd=str(self.work_path), stdout=stdout,
                               stderr=sub.STDOUT)
        except sub.CalledProcessError:
            msg = ('Oracle run failed. The output is:\n'
                   + stdout_fname.read_text())
            raise ValueError(msg)
        print(stdout_fname.read_text() + '---8<---' * 9)
        failed_path = self.work_path / (t4_o.stem + '.failedpoints.dat')
        n_points, dist = check_failed_points(failed_path)
        n_outside = parse_outside_points(stdout_fname)
        return n_points, n_outside, dist, stdout_fname


@pytest.fixture
def oracle(oracle_path, tmp_path):
    '''Return an instance of the :class:`OracleRunner` class.'''
    return OracleRunner(oracle_path, tmp_path)
