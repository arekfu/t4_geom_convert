'''Integration tests for MCNP conversion.'''
# pylint: disable=no-value-for-parameter

import shlex
import pytest
from t4_geom_convert.main import conversion, parse_args
from ..conftest import foreach_data


def cli_options(mcnp_path, n_lines=3):
    '''Detect custom CLI options in the first few lines of an MCNP file.

    ;param mcnp_path: the path to the MCNP file
    :type mcnp_path: :class:`py.path.LocalPath`
    :returns: the parsed options, as a list.
    '''
    with mcnp_path.open() as mcnp_file:
        lines = [mcnp_file.readline() for _ in range(n_lines)]
    cli_str = 'cli:'
    for line in lines:
        pos = line.find(cli_str)
        if pos == -1:
            continue
        return shlex.split(line[pos + len(cli_str):])
    return []


def do_conversion(mcnp_i, output_dir):
    '''Perform the actual conversion from MCNP to T4.'''
    cli_opts = cli_options(mcnp_i)
    output = output_dir / (mcnp_i.name + '.t4')
    args = parse_args(['-o', str(output), str(mcnp_i)] + cli_opts)
    conversion(args)
    return output


@foreach_data(mcnp_i=lambda path: str(path).endswith('.imcnp'))
def test_convert(mcnp_i, tmp_path):
    '''Test conversion for all data files in the ``data`` subfolder.'''
    do_conversion(mcnp_i, tmp_path)


def do_test_oracle(mcnp_i, tmp_path, mcnp, oracle):
    '''Actually perform a conversion test, followed by an oracle test.'''
    t4_o = do_conversion(mcnp_i, tmp_path)
    mcnp_ptrac = mcnp.run(mcnp_i)
    n_failed_points = oracle.run(t4_o, mcnp_i, mcnp_ptrac)
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
    --extra-mcnp-input CLI option.'''
    do_test_oracle(extra_input, tmp_path, mcnp, oracle)
