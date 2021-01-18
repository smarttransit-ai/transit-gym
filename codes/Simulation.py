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
    def __init__(self, metamodel_file="TransitSimulatorDSL.tx", data_path="../data/", export_path = "../SUMO_simulation/"):
        self.interpreter = Interpreter(metamodel_file,data_path,export_path)
    
    def run(self, file_name):
        #result = self.interpreter.interpret(file_name)
        result = ['../SUMO_Simulation/Simulation_3/']
        env = os.environ
        env['SUMO_HOME'] = '/usr/local/opt/sumo/share/sumo'
        env['PATH'] += ':/usr/local/bin' #FIXME
        # for res in result:
        #     subprocess.call('sumo ' + res + 'config.sumocfg', shell=True)
        processor = Output_Processor()
        for res in result:
            processor.generate(res)
        print("All Done")
        
        