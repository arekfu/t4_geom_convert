# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
'''

from ...Composition.ConstructCompositionT4 import constructCompositionT4
from ...Composition.CompositionConversionMCNPToT4 import str_fabs


def writeT4Composition(mcnp_parser, mcnp_new_dict, ofile):
    '''
    :brief: method writing composition of the T4 input file
    '''
    ofile.write("\nCOMPOSITION\n")
    temperature = 300
    dic_composition = constructCompositionT4(mcnp_parser, mcnp_new_dict)
    n_compos = 0
    for mats in dic_composition.values():
        n_compos += len(mats)
    ofile.write(str(n_compos + 1) + "\n")  # +1 from the m0 (void) composition

    if dic_composition:
        n_compos = len(dic_composition)
        fmt_string = ('\rconverting composition {{:{0}d}} ({{:{1}d}}/'
                      '{{:{1}d}}, {{:3d}}%)'
                      .format(len(str(max(dic_composition))),
                              len(str(n_compos))))
        for j, (key, mats) in enumerate(dic_composition.items()):
            percent = int(100.0*j/(n_compos-1)) if n_compos > 1 else 100
            print(fmt_string.format(key, j+1, n_compos, percent),
                  end='', flush=True)
            for mat in mats:
                typ = mat.typeDensity
                density = mat.valueOfDensity
                list_isotope = mat.listMaterialComposition
                p_number_of_isotope = len(list_isotope)
                isotopes_str = '\n  '.join(name + ' ' + abundance
                                           for name, abundance in list_isotope)
                p_material_name = mat.material + '_' + density
                if typ == 'POINT_WISE':
                    ofile.write("{} {:d} {} {:d}\n  {}\n"
                                .format(typ, temperature, p_material_name,
                                        p_number_of_isotope, isotopes_str))
                else:
                    ofile.write("{} {:d} {} {} {} {:d}\n  {}\n"
                                .format(typ, temperature,
                                        p_material_name, str_fabs(density),
                                        'NB_ATOM' if mat.nb_atom else '',
                                        p_number_of_isotope, isotopes_str))
    ofile.write("POINT_WISE 300 m0 1\n  HE4 1E-30\n\nEND_COMPOSITION\n")
    print('... done', flush=True)
