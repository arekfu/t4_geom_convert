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


@pytest.mark.oracle
@foreach_data(mcnp_i=lambda path: str(path).endswith('.imcnp'))
def test_oracle(mcnp_i, tmp_path, mcnp, oracle):
    '''Run the conversion and check the oracle for all data files in the
    ``data`` subfolder.'''
    t4_o = do_conversion(mcnp_i, tmp_path)
    mcnp_ptrac = mcnp.run(mcnp_i)
    oracle_response = oracle.run(t4_o, mcnp_i, mcnp_ptrac)
    assert oracle_response
