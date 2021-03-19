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
'''Integration tests for MCNP conversion.'''
# pylint: disable=no-value-for-parameter

import shlex
import pytest
from t4_geom_convert.main import conversion, parse_args
from ..conftest import foreach_data, parse_outside_points


def get_options(mcnp_path, n_lines=50):
    '''Detect custom CLI options in the first few lines of an MCNP file.

    ;param mcnp_path: the path to the MCNP file
    :type mcnp_path: py.path.LocalPath
    :returns: the parsed options, as a list.
    '''
    if 'latin1' in str(mcnp_path):
        encoding = 'latin1'
    else:
        encoding = None
    with mcnp_path.open(encoding=encoding) as mcnp_file:
        lines = [mcnp_file.readline() for _ in range(n_lines)]
    conv_str = 'converter-flags:'
    oracle_str = 'oracle-flags:'
    tol_str = 'oracle-tolerance:'
    fail_str = 'fail-if-outside:'
    conv_opts, oracle_opts = [], []
    tol = 0
    fail_if_outside = True
    for line in lines:
        pos = line.find(conv_str)
        if pos != -1:
            conv_opts = shlex.split(line[pos + len(conv_str):])
        pos = line.find(oracle_str)
        if pos != -1:
            oracle_opts = shlex.split(line[pos + len(oracle_str):])
        pos = line.find(tol_str)
        if pos != -1:
            tol = int(line[pos + len(tol_str):])
        pos = line.find(fail_str)
        if pos != -1:
            fail_if_outside = bool(line[pos + len(fail_str):])
    return conv_opts, oracle_opts, tol, fail_if_outside


def do_conversion(mcnp_i, output_dir, conv_opts):
    '''Perform the actual conversion from MCNP to T4.'''
    output = output_dir / (mcnp_i.name + '.t4')
    args = parse_args(['-o', str(output), str(mcnp_i)] + conv_opts)
    conversion(args)
    return output


@foreach_data(mcnp_i=lambda path: str(path).endswith('.imcnp'))
def test_convert(mcnp_i, tmp_path):
    '''Test conversion for all data files in the ``data`` subfolder.'''
    conv_opts, _, _, _ = get_options(mcnp_i)
    do_conversion(mcnp_i, tmp_path, conv_opts)


def do_test_oracle(mcnp_i, tmp_path, mcnp, oracle):
    '''Actually perform a conversion test, followed by an oracle test.'''
    mcnp_output, mcnp_ptrac = mcnp.run(mcnp_i)
    mcnp_output_txt = mcnp_output.read_text()
    assert 'trouble' not in mcnp_output_txt
    assert 'fatal error' not in mcnp_output_txt
    conv_opts, oracle_opts, tolerance, fail_if_outside = get_options(mcnp_i)
    t4_o = do_conversion(mcnp_i, tmp_path, conv_opts)
    (n_failed, n_outside, distance,
     output) = oracle.run(t4_o, mcnp_i, mcnp_ptrac, oracle_opts)
    assert 'ERROR' not in output.read_text()
    msg = '{} failed points, max distance = {}'.format(n_failed, distance)
    assert n_failed <= tolerance, msg
    if fail_if_outside:
        msg = '{} outside points'.format(n_outside)
        assert n_outside == 0


@pytest.mark.oracle
@foreach_data(mcnp_i=lambda path: str(path).endswith('.imcnp'))
def test_oracle(mcnp_i, tmp_path, mcnp, oracle):
    '''Run the conversion and check the oracle for all data files in the
    ``data`` subfolder.'''
    do_test_oracle(mcnp_i, tmp_path, mcnp, oracle)


@pytest.mark.oracle
def test_extra_mcnp(extra_input, tmp_path, mcnp, oracle):
    '''Test conversion + oracle for any MCNP input files provided via the
    --extra-mcnp-inputs CLI option.'''
    do_test_oracle(extra_input, tmp_path, mcnp, oracle)


def test_density_zeros(datadir, tmp_path):
    '''Test that the the conversion of :file:`density_zeros.imcnp` produces
    only one material.

    This input file contains two material cards, but the materials appear
    multiple times, with densities that differ only in the number of trailing
    zeros.
    '''
    mcnp_i = datadir / 'density_zeros.imcnp'
    conv_opts, _, _, _ = get_options(mcnp_i)
    t4_o = do_conversion(mcnp_i, tmp_path, conv_opts)
    t4_text = t4_o.read_text()
    assert 'COMPOSITION\n3' in t4_text, t4_text
    assert 'm1_-2.7 ' in t4_text, t4_text
    assert 'm2_-1.0 ' in t4_text, t4_text


def test_parse_outside_points(datadir):
    '''Test that :func:`~.parse_outside_points` correctly returns the number of
    points outside the geometry.'''
    oracle_stdout = datadir / 'oracle_stdout'
    n_outside = parse_outside_points(oracle_stdout)
    assert n_outside == 9619
