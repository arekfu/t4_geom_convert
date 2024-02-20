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

from ...Progress import Progress
from ...Composition.ConstructCompositionT4 import constructCompositionT4
from ...Composition.CompositionConversionMCNPToT4 import str_fabs


def writeT4Composition(mcnp_parser, mcnp_new_dict, ofile):
    '''Function writing composition of the T4 input file.'''
    ofile.write("\nCOMPOSITION\n")
    temperature = 300
    dic_composition = constructCompositionT4(mcnp_parser, mcnp_new_dict)
    n_compos = 0
    for mats in dic_composition.values():
        n_compos += len(mats)
    ofile.write(str(n_compos + 1) + "\n")  # +1 from the m0 (void) composition

    if dic_composition:
        n_compos = len(dic_composition)
        with Progress('converting composition',
                      n_compos, max(dic_composition)) as progress:
            for j, (key, mats) in enumerate(dic_composition.items()):
                progress.update(j, key)
                for mat in mats:
                    typ = mat.typeDensity
                    density = mat.valueOfDensity
                    list_isotope = mat.listMaterialComposition
                    p_number_of_isotope = len(list_isotope)
                    isotopes_str = '\n  '.join(name + ' ' + abd
                                               for name, abd in list_isotope)
                    p_material_name = mat.material + '_' + density
                    if typ == 'POINT_WISE':
                        ofile.write(f'{typ} {temperature:d} {p_material_name} '
                                    f'{p_number_of_isotope:d}\n  '
                                    f'{isotopes_str}\n')
                    else:
                        s_density = str_fabs(density)
                        nb_atom = 'NB_ATOM' if mat.nb_atom else ''
                        ofile.write(f'{typ} {temperature:d} {p_material_name} '
                                    f'{s_density} {nb_atom} '
                                    f'{p_number_of_isotope:d}\n  '
                                    f'{isotopes_str}\n')
    ofile.write("POINT_WISE 300 m0 1\n  HE4 1E-30\n\nEND_COMPOSITION\n")
