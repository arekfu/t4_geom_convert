'''Integration tests for MCNP conversion.'''
# pylint: disable=no-value-for-parameter

import shlex
import pytest
from t4_geom_convert.main import conversion, parse_args
from ..conftest import foreach_data


def get_options(mcnp_path, n_lines=50):
    '''Detect custom CLI options in the first few lines of an MCNP file.

    ;param mcnp_path: the path to the MCNP file
    :type mcnp_path: :class:`py.path.LocalPath`
    :returns: the parsed options, as a list.
    '''
    with mcnp_path.open() as mcnp_file:
        lines = [mcnp_file.readline() for _ in range(n_lines)]
    conv_str, oracle_str = 'converter-flags:', 'oracle-flags:'
    conv_opts, oracle_opts = [], []
    for line in lines:
        pos = line.find(conv_str)
        if pos != -1:
            conv_opts = shlex.split(line[pos + len(conv_str):])
        pos = line.find(oracle_str)
        if pos != -1:
            oracle_opts = shlex.split(line[pos + len(oracle_str):])
    return conv_opts, oracle_opts


def do_conversion(mcnp_i, output_dir, conv_opts):
    '''Perform the actual conversion from MCNP to T4.'''
    output = output_dir / (mcnp_i.name + '.t4')
    args = parse_args(['-o', str(output), str(mcnp_i)] + conv_opts)
    conversion(args)
    return output


@foreach_data(mcnp_i=lambda path: str(path).endswith('.imcnp'))
def test_convert(mcnp_i, tmp_path):
    '''Test conversion for all data files in the ``data`` subfolder.'''
    conv_opts, _ = get_options(mcnp_i)
    do_conversion(mcnp_i, tmp_path, conv_opts)


def do_test_oracle(mcnp_i, tmp_path, mcnp, oracle):
    '''Actually perform a conversion test, followed by an oracle test.'''
    conv_opts, oracle_opts = get_options(mcnp_i)
    t4_o = do_conversion(mcnp_i, tmp_path, conv_opts)
    mcnp_ptrac = mcnp.run(mcnp_i)
    n_failed_points = oracle.run(t4_o, mcnp_i, mcnp_ptrac, oracle_opts)
    assert n_failed_points == 0


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
