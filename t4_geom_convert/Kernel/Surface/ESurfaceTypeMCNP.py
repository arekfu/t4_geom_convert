'''
Created on 19 févr. 2019

:author: Sogeti
:file: ESurfaceTypeMCNP.py
'''
from enum import Enum

ESurfaceTypeMCNP = Enum('ESurfaceTypeMCNP', 'PX PY PZ P SO S SX SY SZ C_X '
                        'C_Y C_Z CX CY CZ K_X K_Y K_Z KX KY KZ GQ TX TY TZ')

# yo = ESurfaceTypeMCNP
# print(yo.PX.name == 'PX')
