'''
Created on 19 févr. 2019

:author: Sogeti
:file: ESurfaceTypeT4.py
'''
from enum import Enum

ESurfaceTypeT4Eng = Enum('ESurfaceTypeT4Eng', 'PLANEX PLANEY PLANEZ PLANE '
                         'SPHERE CYLX CYLY CYLZ CYL CONEX CONEY CONEZ CONE QUAD TORUSX '
                         'TORUSY TORUSZ')

# ESurfaceTypeT4Fr = Enum('ESurfaceTypeMCNPFr','PLANX PLANY PLANZ PLAN \
# SPHERE CYLX CYLY CYLZ CONEX CONEY CONEZ \
# QUAD TOREX TOREY TOREZ')

# yo = ESurfaceTypeT4Eng
# print(str(yo.PLANEX.name))
