'''
Created on 19 févr. 2019

:author: Sogeti
:file: ESurfaceTypeMCNP.py
'''
from enum import Enum

ESurfaceTypeMCNP = Enum('ESurfaceTypeMCNP', 'PX PY PZ P SO S SX SY SZ C/X \
C/Y C/Z CX CY CZ K/X K/Y K/Z KX KY KZ GQ TX TY TZ')

# yo = ESurfaceTypeMCNP
# print(yo.PX.name == 'PX')
