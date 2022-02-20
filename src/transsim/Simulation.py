#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 18:18:22 2021

@author: danielgui, abhishek dubey
"""
from transsim.Interpreter import Interpreter
import subprocess
from transsim.Output_Processor import Output_Processor
import os,time

class Simulation:
    def __init__(self, data_path, export_path = "./", metamodel_file=None, sumo_home=None, add_path=None):
        #FIXME
        env = os.environ
        if sumo_home:
            env['SUMO_HOME'] = sumo_home
        if add_path:
            env['PATH'] += add_path
        self.interpreter = Interpreter(metamodel_file,data_path,export_path)
        
        # env['SUMO_HOME'] = '/usr/local/opt/sumo/share/sumo'
        # env['PATH'] += ':/usr/local/bin' #FIXME
    
    def run(self, file_name):
        if not file_name.endswith('.transsim'):
            raise ValueError('Wrong extension of program')
        print(time.ctime(),":",'Generating Configuration files for Simulation from ',file_name)
        result = self.interpreter.interpret(file_name)
        print(time.ctime(),":",'Done.')
        #result = ['../SUMO_Simulation/Simulation_3/']        
        for res in result:
            print(time.ctime(),":",'Starting Simulation. Calling Sumo: ','sumo ' + res + 'config.sumocfg')
            print(subprocess.run('sumo ' + res + 'config.sumocfg', shell=True,check=True,capture_output=True).stdout)
        print(time.ctime(),":",'Simulation Complete - Proceeding to output processing')
        processor = Output_Processor()
        for res in result:
            processor.generate(res)
        print(time.ctime(),":","All Done")
        
        