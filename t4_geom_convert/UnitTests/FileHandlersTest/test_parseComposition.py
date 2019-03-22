'''
Created on 18 mars 2019

@author: mmaurey
'''
import pytest

from t4_geom_convert.Kernel.FileHanlders.Parser.CParseMCNPComposition import CParseMCNPComposition

def test_composition():
    pass

@pytest.mark.parametrize("p_fname",[1,2,3])
def test_lambda(p_fname):
    assert p_fname < 2 
