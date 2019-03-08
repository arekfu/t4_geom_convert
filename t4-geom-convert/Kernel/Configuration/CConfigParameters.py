# -*- coding: utf-8 -*-
'''
Created on 6 févr. 2019

:author: Sogeti
:data : 06 february 2019
:file : CConfigParameters..py
'''
import os
import Kernel.Configuration
import configparser

class CConfigParameters(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.confPath = os.path.join(os.path.dirname(Kernel.Configuration.__file__),'config_parameters.ini')
        

    def m_setMCNPInputFile(self, p_nameInuptFileMCNP):
        '''
        :brief: method writing the name of the input file MCNP in th config_parameters.ini
        '''
        config = configparser.ConfigParser()
        config.read(self.confPath)
        config['FILE']['inputFileMCNP'] = p_nameInuptFileMCNP
        with open(self.confPath,'w') as configfile:
            config.write(configfile)
            
    def m_setT4InputFile(self, p_nameInuptFileT4):
        '''
        :brief: method writing the name of the input file T4 in th config_parameters.ini
        '''
        config = configparser.ConfigParser()
        config.read(self.confPath)
        config['FILE']['inputFileT4'] = p_nameInuptFileT4
        with open(self.confPath,'w') as configfile:
            config.write(configfile)
    
    def m_readNameMCNPInputFile(self):
        
        config = configparser.ConfigParser()
        config.read(self.confPath)
        p_nameInuptFileMCNP = config['FILE']['inputFileMCNP']
        return p_nameInuptFileMCNP
    
    def m_readNameT4InputFile(self):
        
        config = configparser.ConfigParser()
        config.read(self.confPath)
        p_nameInuptFileT4 = config['FILE']['inputFileT4']
        return p_nameInuptFileT4
    
    
    
    