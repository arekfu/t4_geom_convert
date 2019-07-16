# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CConfigParameters..py
'''
import os
from .. import Configuration
import configparser
from .CMessages import INPUT_FILE_MCNP, FILE, INPUT_FILE_T4, LATTICE

class CConfigParameters(object):
    '''
    :brief: Class fixing the constant value of the converter as the name of the
    file MCNP and the file T4
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.confPath = os.path.join(os.path.dirname(Configuration.__file__),
                                     'config_parameters.ini')


    def setMCNPInputFile(self, p_nameInuptFileMCNP):
        '''
        :brief: method writing the name of the input file MCNP in the
        config_parameters.ini
        '''
        config = configparser.ConfigParser()
        config.read(self.confPath)
        config.add_section(FILE)
        config[FILE][INPUT_FILE_MCNP] = p_nameInuptFileMCNP
        with open(self.confPath, 'w') as configfile:
            config.write(configfile)

    def setT4InputFile(self, p_nameInuptFileT4):
        '''
        :brief: method writing the name of the input file T4 in the
        config_parameters.ini
        '''
        config = configparser.ConfigParser()
        config.read(self.confPath)
        config.add_section(FILE)
        config[FILE][INPUT_FILE_T4] = p_nameInuptFileT4
        with open(self.confPath, 'w') as configfile:
            config.write(configfile)

    def readNameMCNPInputFile(self):
        '''
        :brief: method reading the name of the input file MCNP
        '''
        config = configparser.ConfigParser()
        config.read(self.confPath)
        p_nameInuptFileMCNP = config[FILE][INPUT_FILE_MCNP]
        return p_nameInuptFileMCNP

    def readNameT4InputFile(self):
        '''
        :brief: method reading the name of the input file T4
        '''
        config = configparser.ConfigParser()
        config.read(self.confPath)
        p_nameInuptFileT4 = config[FILE][INPUT_FILE_T4]
        return p_nameInuptFileT4

    def readDomainForLattice(self, key):
        listeDomaine = []
        config = configparser.ConfigParser()
        config.read(self.confPath)
        p_range = config[LATTICE]['cell' + str(key)]
        list1 = p_range.split(',')
        for element in list1:
            partial_list = element.split(':')
            if len(partial_list) != 2:
                raise ValueError('Problem with lattice domain of cell %s' %key)
            else:
                listeDomaine.append((int(partial_list[0]),int(partial_list[1])))
        return listeDomaine
