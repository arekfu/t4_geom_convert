'''
Created on 19 févr. 2019

:author: Sogeti
:file: ESurfaceTypeMCNP.py
'''
from enum import Enum

ESurfaceTypeMCNP = Enum('ESurfaceTypeMCNP', 'PX PY PZ P SO S SX SY SZ C_X '
                        'C_Y C_Z CX CY CZ C K_X K_Y K_Z KX KY KZ K GQ '
                        'T TX TY TZ X Y Z')

def mcnp_to_mip(en):
    if isinstance(en, str):
        s = en
    else:
        s = en.name
    return s.lower().replace('_', '/')

def string_to_enum(p_typeSurface):
    typeSurf = p_typeSurface.upper().replace('/','_')
    try:
        enumSurface = getattr(ESurfaceTypeMCNP, typeSurf)
    except AttributeError:
        raise ValueError('{}: The type of this surface does not exist'
                         .format(p_typeSurface.upper()))
    return enumSurface
