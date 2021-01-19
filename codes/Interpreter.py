#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: danielgui
"""

import os
import shutil
from textx import metamodel_from_file
#from Matching_Func import Matcher
from Veh_Type_Container import Veh_Types_Container
from GTFS_processor import GTFS_processor
from Transportation_Demand_Processor import TDProcessor

class Interpreter(object):
    def __init__(self, metamodel_file="TransitSimulatorDSL.tx", data_path="../data/", export_path = "../SUMO_simulation/"):
        self.metamodel = metamodel_from_file(metamodel_file)
        self.data_path = data_path
        self.export_path = export_path
    
    def interpret(self, file_name):
        model_c = self.metamodel.model_from_file(file_name)
        imports = model_c.imports
        data = self.analyze_import(imports)
        simulations = model_c.simulations
        export_directory = []
        for simulation in simulations:
            export_directory.append(self.analyze_simulation(data, simulation))
        return export_directory
        
    
    def analyze_import(self, imports):
        network = None
        vehicles = None
        GTFS = None
        for imp in imports:
            imp = imp.importName
            if imp[0:5] == 'gtfs.':
                imp = imp[5:]
                GTFS = GTFS_processor(self.data_path, imp)
            elif imp[0:8] == 'vehicle.':
                imp = imp[8:]
                vehicles = Veh_Types_Container(self.data_path, imp)
            elif imp[0:8] == 'network.':
                imp = imp[8:]
                network = self.data_path + imp + '_SUMO_Network.net.xml'
                # checker
                if not os.path.exists(network):
                    raise ValueError("Imported Network file does not exist: ", network)
            elif imp[0:3] == "td.":
                imp = imp[3:]
                td = TDProcessor(imp, self.data_path)
            else:
                raise ValueError("Invalid import:", imp)
                
        return [GTFS, vehicles, network, td]
    
    def analyze_simulation(self, data, simulation):
        GTFS, vehicles, network, td = data
        confignum = simulation.configNum
        time_start = 0
        time_end = int(simulation.timeEnd / 100 * 3600 + simulation.timeEnd % 100 * 60)
        
        schedule = simulation.schedule 
        assignments = simulation.assignments
        blockid = {}
        tripid = {}
        for assignment in assignments:
            if not vehicles.isin(assignment.vehicleid):
                raise ValueError('Not a valid vehicle id')
            else:
                if assignment.blockid:
                    blockid[assignment.blockid] = assignment.vehicleid
                if assignment.tripid:
                    tripid[assignment.tripid] = assignment.vehicleid
                    
        GTFS.assign_vehicle(tripid, blockid)
        shutil.rmtree(self.export_path + 'Simulation_' + str(confignum), ignore_errors=True) #FIXME
        os.makedirs(self.export_path + 'Simulation_' + str(confignum) + '/')
        # if configured frequency
        edge_dump_file = None
        if simulation.frequency:
            frequency = simulation.frequency
            edge_dump_file = 'edge.dump.add' + '.xml'
            edge_dump_file_full = self.export_path + 'Simulation_' + str(confignum) + '/' + edge_dump_file
            f = open(edge_dump_file_full, "x")
            f.write("<additional>")
            f.write('\n\t<edgeData id="msmid" freq="'+ str(frequency) + '" file="EdgeMean.xml" />')
            f.write('\n</additional>')
            f.close()
            
        routefile = 'raw_routefile.xml'
        final_route_file = 'final_routefile.xml'
        busStopfile = 'stopfile.add.xml'
        vehiclefile = 'vehicle.add.xml'
        dumpfile = 'trajectories_output.xml'
        busstopdump = 'busstop_output.xml'
        routefileFull = self.export_path + 'Simulation_' + str(confignum) + '/' + routefile
        busStopfileFull = self.export_path + 'Simulation_' + str(confignum) + '/' + busStopfile
        vehiclefileFull = self.export_path + 'Simulation_' + str(confignum) + '/' + vehiclefile
        configfileFull = self.export_path + 'Simulation_' + str(confignum) + '/' + 'config' + '.sumocfg'
        
        final_route_file_full = self.export_path + 'Simulation_' + str(confignum) + '/' + final_route_file
        GTFS.export_route_file(time_start, time_end, schedule, routefileFull)
        GTFS.export_busstop_file(busStopfileFull, network)
        vehicles.export(vehiclefileFull)
        td.merge_route_file(routefileFull, vehiclefileFull, busStopfileFull, network, final_route_file_full, time_end)
        
        
        # generate config file
        if os.path.exists(configfileFull):
            os.remove(configfileFull)
        
        f = open(configfileFull, "x")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<configuration xmlns:xsi="http://www.w3.org' +
                '/2001/XMLSchema-instance" xsi:noNamespaceSchema'+ 
                'Location="http://sumo.dlr.de/xsd/sumoConfiguration.xsd">\n')
        f.write('\t<input>\n\t\t<net-file value="'+ '../' + network + '"/>\n')
        f.write('\t\t<route-files value="')
        f.write(final_route_file)
        f.write(', ../../data/Chattanooga_Daily_Trips.rou.xml')
        f.write('"/>\n')
        if edge_dump_file:
            f.write('\t\t<additional-files value="'+ busStopfile + ',' + edge_dump_file + '"/>\n')
        else:
            f.write('\t\t<additional-files value="'+ busStopfile + '"/>\n')
        f.write('\t</input>\n')
        f.write('\t<time>\n\t\t<begin value="' + str(time_start) + '"/>\n')
        f.write('\t\t<end value="'+ str(time_end) + '"/>\n')
        f.write('\t</time>\n')
        f.write('\t<processing>\n\t\t<ignore-route-errors value="true"/>\n'+
                '\t</processing>\n')
        f.write('\t<output>\n\t\t<stop-output value="'+ busstopdump + '"/>\n') #FIXME
        f.write('\t\t<amitran-output value="' + dumpfile + '"/>\n')
        f.write('\t</output>\n\t<gui_only>\n\t\t<gui-settings-file value="../' + self.data_path + 'gui.view.xml"/>\n')
        f.write('\t<report>\n\t\t<no-warnings value="true"/>\n\t\t<error-log value="error_warning_log.xml"/>\n\t</report>\n')
        f.write('\t</gui_only>\n</configuration>')
        f.close()
        print('\nConfig File Saved. Please find configured simulation file at: ' + self.export_path + 'Simulation_' + str(confignum) + '\n')
        return self.export_path + 'Simulation_' + str(confignum) + '/'
        
        
        
        
        
        
        
        
            
        
        
    
    

    
                
        
        