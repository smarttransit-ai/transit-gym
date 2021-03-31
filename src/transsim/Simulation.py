#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 18:18:22 2021

@author: danielgui
"""
from Interpreter import Interpreter
import subprocess
from Output_Processor import Output_Processor
import os

class Simulation:
    def __init__(self, data_path, export_path = "./", metamodel_file="TransitSimulatorDSL.tx", sumo_home=None, add_path=None):
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
            print('Wrong extension of program')
        print('Starting Interpretion...\n')
        result = self.interpreter.interpret(file_name)
        #result = ['../SUMO_Simulation/Simulation_3/']
        print('Starting Simulation\n')
        for res in result:
            subprocess.call('sumo ' + res + 'config.sumocfg', shell=True)
        print('\nSimulation Complete - Proceed to output processing\n')
        processor = Output_Processor()
        for res in result:
            processor.generate(res)
        print("\nAll Done")
        
        