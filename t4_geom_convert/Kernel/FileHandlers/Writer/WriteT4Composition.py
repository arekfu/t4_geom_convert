# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
'''

from ...Composition.ConstructCompositionT4 import constructCompositionT4
from ...Composition.CompositionConversionMCNPToT4 import str_fabs


def writeT4Composition(mcnpParser, mcnp_new_dict, ofile):
    '''
    :brief: method writing composition of the T4 input file
    '''
    ofile.write("\nCOMPOSITION\n")
    temperature = 300
    dic_composition = constructCompositionT4(mcnpParser, mcnp_new_dict)
    n_compos = 0
    for mat in dic_composition.values():
        n_compos += len(mat.valueOfDensity)
    ofile.write(str(n_compos + 1) + "\n")  # +1 from the m0 (void) composition

    n_mcnp_compos = len(dic_composition)
    fmt_string = ('\rconverting composition {{:{}d}}/{}'
                  .format(len(str(n_mcnp_compos)), n_mcnp_compos))
    for j, mat in enumerate(dic_composition.values()):
        print(fmt_string.format(j+1), end='', flush=True)
        l_typeDensity = mat.typeDensity
        l_densityValue = mat.valueOfDensity
        list_isotope = mat.listMaterialComposition
        p_numberOfIsotope = len(list_isotope)
        isotopes_str = '\n  '.join(name + ' ' + abundance
                                   for name, abundance in list_isotope)
        for typ, density in zip(l_typeDensity, l_densityValue):
            p_materialName = mat.material + '_' + density
            if typ == 'POINT_WISE':
                ofile.write("{} {:d} {} {:d} {}\n"
                            .format(typ, temperature, p_materialName,
                                    p_numberOfIsotope, isotopes_str))
            else:
                ofile.write("{} {:d} {} {} {:d} {}\n"
                            .format(typ, temperature,
                                    p_materialName, str_fabs(density),
                                    p_numberOfIsotope, isotopes_str))
    ofile.write("POINT_WISE 300 m0 1 HE4 1E-30\n")
    print('... done', flush=True)

    ofile.write("\n")
    ofile.write("END_COMPOSITION")
    ofile.write("\n")
