# -*- coding: utf-8 -*-
'''
:author: Sogeti
:data : 06 February 2019
'''

from collections import OrderedDict

from .CDictCompositionT4 import CDictCompositionT4
from .CDictCompositionMCNP import CDictCompositionMCNP
from .CIsotopeConversion import CIsotopeConversion
from .EIsotopeNameElementT4 import EIsotopeNameElement


def compositionConversionMCNPToT4(mcnpParser):
    '''
    :brief: method recuperate the dictionary of the composition from MCNP
    and return a dictionary of the composition for T4
    '''
    d_CompositionT4 = OrderedDict()
    obj_T4 = CDictCompositionT4(d_CompositionT4)
    l_compositionT4 = []
    for key, val in CDictCompositionMCNP(mcnpParser).d_compositionMCNP.items():
        l_compositionT4 = []
        listMaterialsSurface = val.ordDict()
        for element in listMaterialsSurface:
            isotopeId, fraction = element
            atomicNumber, massNumber = CIsotopeConversion(isotopeId).conversionIsotope()
            atomicNumberT4 = EIsotopeNameElement(atomicNumber.value)
            if massNumber == '0':
                massNumberT4 = '-NAT'
            else:
                massNumberT4 = massNumber
            isotopeT4 = atomicNumberT4, massNumberT4
            l_compositionT4.append((isotopeT4, str_fabs(fraction)))
        valueT4 = l_compositionT4
        obj_T4[key] = valueT4
    return d_CompositionT4

def str_fabs(number_str):
    '''Remove the leading minus sign (if any) from a string representing a
    number. It behaves in a very similar way to `str(fabs(float(number_str)))`,
    except that it preserves the representation of `number_str` (precision,
    scientific notation, etc.). The input parameter must represent a valid
    float.

    :param str number_str: a number, as a string
    :returns: the absolute value of the number represented by `number_str`

    Examples:

    >>> str_fabs('-1.5')
    '1.5'
    >>> str_fabs('-1e-30')
    '1e-30'
    >>> str_fabs('-1.0e24')
    '1.0e24'
    >>> str_fabs('56.5')
    '56.5'
    >>> str_fabs('   -44  ')  # spaces are tolerated
    '44'
    '''
    number_str = number_str.strip()
    if number_str[0] == '-':
        return number_str[1:]
    return number_str
