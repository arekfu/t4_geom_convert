'''Integration tests for MCNP conversion.'''
# pylint: disable=no-value-for-parameter

import shlex
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


@foreach_data(mcnp_i=lambda path: str(path).endswith('.i'))
def test_convert_mcnp_input(mcnp_i, workdir):
    '''Test conversion for all data files in the ``data`` subfolder.'''
    cli_opts = cli_options(mcnp_i)
    output = workdir / (mcnp_i.purebasename + '.t4')
    args = parse_args(['-o', str(output), str(mcnp_i)] + cli_opts)
    conversion(args)
