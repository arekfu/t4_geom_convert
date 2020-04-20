# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
'''
import sys
import argparse
from datetime import datetime

from MIP import mip

from . import __version__
from .Kernel.FileHandlers.Writer.WriteT4Geometry import writeT4Geometry
from .Kernel.FileHandlers.Writer.WriteT4Composition import writeT4Composition
from .Kernel.FileHandlers.Writer.WriteT4GeomComp import writeT4GeomComp
from .Kernel.FileHandlers.Writer.WriteT4BoundCond import writeT4BoundCond
from .Kernel.Volume.Lattice import parse_ranges


def parse_lattice(lattice_list):
    '''Check the arguments to the --lattice option and parse them into a usable
    form.

    The arguments to --lattice (the option may be given multiple times) have
    the form :samp:`{cell},{i_min}:{i_max}[,{j_min}:{j_max}[,{k_min}:{k_max}]]`

    >>> opt_lattice = ['200,2:5,0:4', '5902,0:5,0:5,0:5', '10,-4:4']

    This function parses the `opt_lattice` list into a dictionary associating
    cell numbers to a list of ranges, as tuples:

    >>> dic = parse_lattice(opt_lattice)
    >>> dic == {200: [(2, 5), (0, 4)],
    ...         5902: [(0, 5), (0, 5), (0, 5)],
    ...         10: [(-4, 4)]}
    True

    The function does some error checking, too:

    >>> parse_lattice(['malformed'])
    Traceback (most recent call last):
        ...
    ValueError: no ranges specified in option 'malformed'
    >>> parse_lattice(['three,-1:5'])
    Traceback (most recent call last):
        ...
    ValueError: cell number 'three' is not an integer in option 'three,-1:5'
    >>> parse_lattice(['100,'])
    Traceback (most recent call last):
        ...
    ValueError: needs exactly 2 colon-separated range bounds in argument '' \
in option '100,'
    >>> parse_lattice(['100,0:4,0:4,0:4,0:4'])
    Traceback (most recent call last):
        ...
    ValueError: too many ranges specified in option '100,0:4,0:4,0:4,0:4'
    >>> parse_lattice(['100,0:6.022e23'])
    Traceback (most recent call last):
        ...
    ValueError: range bound '6.022e23' is not an integer in option \
'100,0:6.022e23'
    >>> parse_lattice(['100,-6.022e23:0'])
    Traceback (most recent call last):
        ...
    ValueError: range bound '-6.022e23' is not an integer in option \
'100,-6.022e23:0'
    '''

    lattice_params = {}

    for option in lattice_list:
        head, *rest = option.split(',')
        if not rest:
            raise ValueError('no ranges specified in option {!r}'
                             .format(option))
        if len(rest) > 3:
            raise ValueError('too many ranges specified in option {!r}'
                             .format(option))
        try:
            cell = int(head)
        except ValueError:
            raise ValueError('cell number {!r} is not an integer in option '
                             '{!r}'.format(head, option)) from None

        try:
            lattice_params[cell] = parse_ranges(rest)
        except ValueError as err:
            # add information about the failing option
            raise ValueError('{} in option {!r}'.format(err, option)) from None

    return lattice_params


def conversion(args):
    '''Orchestrate the conversion.'''

    start = datetime.now()
    print('started at: {}\n'.format(start.isoformat()))

    from pathlib import Path
    if args.output is not None:
        t4_output_filename = Path(args.output)
    else:
        t4_output_filename = Path(args.input).with_suffix('.t4')

    try:
        mcnp_parser = mip.MIP(args.input, encoding=args.encoding)
    except UnicodeError as err:
        msg = ("Could not decode input file using encoding {!r}. Probably you "
               "need to specify the encoding with the `-e' option."
               .format(args.encoding))
        raise UnicodeError(msg)

    lattice_params = parse_lattice(args.lattice)
    with t4_output_filename.open('w') as ofile:
        geom_conv = writeT4Geometry(mcnp_parser, lattice_params, args, ofile)
        dic_surf_mcnp, dic_vol, mcnp_new_dict, skipped_cells = geom_conv
        if not args.skip_compositions:
            writeT4Composition(mcnp_parser, mcnp_new_dict, ofile)
        if not args.skip_geomcomp:
            writeT4GeomComp(dic_vol, mcnp_new_dict, ofile)
        if not args.skip_boundary_conditions:
            writeT4BoundCond(dic_surf_mcnp, ofile)

    if skipped_cells:
        print('\nNOTE: the following cells have been omitted from the '
              'conversion\n      because their importance is equal to zero:'
              '\n      {}'.format(skipped_cells))

    end = datetime.now()
    elapsed = end - start
    print('\nfinished at: {}'.format(end.isoformat()))
    print('elapsed time: {} s'.format(elapsed.total_seconds()))


def parse_args(argv):
    '''Parse the command-line arguments.

    :returns: a namespace containing the parsed arguments.
    '''
    parser = argparse.ArgumentParser(
        description='Convert source code for a Geant4 detector construction '
                    'into a geometry that can be read by TRIPOLI-4®.',
        allow_abbrev=False)

    # general arguments
    g_general = parser.add_argument_group('general arguments')
    g_general.add_argument('input', metavar='MCNP_INPUT_FILE',
                           help='MCNP input file to convert')
    g_general.add_argument('-v', '--verbose', help='increase verbosity',
                           action='count', default=0)
    g_general.add_argument('-V', '--version',
                           action='version', version=__version__)
    g_general.add_argument('-o', '--output', metavar='T4_OUTPUT_FILE',
                           help='name of the TRIPOLI-4® file to generate',
                           default=None)
    g_general.add_argument('-e', '--encoding',
                           help='encoding of the input file', default='utf-8')
    g_general.add_argument('--skip-deduplication', action='store_true',
                           help='skip deduplication of surfaces')
    g_general.add_argument('--skip-compositions', action='store_true',
                           help='skip conversion of the compositions')
    g_general.add_argument('--skip-geomcomp', action='store_true',
                           help='skip conversion of the volume-composition '
                           'association')
    g_general.add_argument('--skip-boundary-conditions', action='store_true',
                           help='skip conversion of the boundary conditions')
    g_general.add_argument('--cache', action='store_true',
                           help='read/write surfaces, cells etc. from a disk '
                           'cache (avoids parsing, mostly for debug)',
                           default=False)

    # lattice args
    g_lattice = parser.add_argument_group('arguments for the conversion of '
                                          'lattices')
    g_lattice.add_argument('--lattice', metavar='LATTICE_SPEC',
                           help='bounds for converting a given lattice',
                           action='append', default=[])

    return parser.parse_args(argv)


def main():
    '''Main entry point for the CLI tool.'''
    args = parse_args(sys.argv[1:])
    conversion(args)


if __name__ == '__main__':
    main()
