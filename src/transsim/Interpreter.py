#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: danielgui
"""

import os
import io
import shutil
from textx import metamodel_from_str
#from Matching_Func import Matcher
from transsim.Veh_Type_Container import Veh_Types_Container
from transsim.GTFS_processor import GTFS_processor
from transsim.Transportation_Demand_Processor import TDProcessor

import pkgutil


class Interpreter(object):
    def __init__(self, metamodel_file, data_path, export_path):
        if not metamodel_file:
            metamodel_str = pkgutil.get_data(__name__, "templates/TransitSimulatorDSL.tx").decode('ascii')
            self.metamodel = metamodel_from_str(metamodel_str)
        else:
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
        network_path = None
        vehicle_path = None
        gtfs_path = None
        taz_path = None
        td_path = None
        gui_path = None
        busstop_path = None
        routes = []

        # parse imports
        for imp in imports:
            imp = imp.importName
            if imp.startswith('gtfs.'):
                imp = imp[5:]
                gtfs_path = self.data_path + '/gtfs/' + imp + '/'
                #GTFS = GTFS_processor(self.data_path, imp) FIXME
            elif imp.startswith('vehicle.'):
                imp = imp[8:]
                vehicle_path = self.data_path + '/vehicle/' + imp
                #vehicles = Veh_Types_Container(self.data_path, imp)
            elif imp.startswith('network.'):
                imp = imp[8:]
                if not imp.endswith('.net.xml'):
                    raise ValueError('Network file format incorrect')
                network_path = self.data_path + '/network/' + imp
                # checker
        
            elif imp.startswith("travel-demand."):
                imp = imp[14:]
                if not imp.endswith('.od'):
                    raise ValueError('Transportation demand file format incorrect')
                td_path = self.data_path + '/travel-demand/' + imp
                #td = TDProcessor(imp, self.data_path)
            elif imp.startswith('routes.'):
                imp = imp[6:]
                if not imp.endswith('.xml'):
                    raise ValueError('Route file format incorrect', imp)
                routes.append(self.data_path + '/routes/' + imp)
            elif imp.startswith('taz.'):
                imp = imp[4:]
                if not imp.endswith('.xml'):
                    raise ValueError('taz file incorrect')
                taz_path = self.data_path + '/taz/' + imp
            elif imp.startswith('gui.'):
                imp = imp[4:]
                if not imp.endswith('.xml'):
                    raise ValueError('gui file incorrect')
                gui_path = self.data_path + '/gui/' + imp
            elif imp.startswith('bus-stop.'):
                imp = imp[9:]
                busstop_path = self.data_path + '/bus-stop/' + imp
            else:
                raise ValueError("Invalid import:", imp)

        # input checking
        for route in routes:
            if not os.path.exists(route):
                raise ValueError("Imported route file does not exist: ", route)
        data = [gtfs_path, network_path, vehicle_path, taz_path,td_path,gui_path,busstop_path]

        for dat in data:
            if not os.path.exists(dat):
                raise ValueError("Imported file does not exist: ", dat)

        data.append(routes)

        return data
    
    def analyze_simulation(self, data, simulation):
        gtfs_path, network_path, vehicle_path, taz_path, td_path, gui_path, busstop_path, routes = data
        vehicles = Veh_Types_Container(vehicle_path)
        gtfs = GTFS_processor(gtfs_path)
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

        gtfs.assign_vehicle(tripid, blockid)
        #FIXME shutil.rmtree(self.export_path + 'Simulation_' + str(confignum), ignore_errors=True) #FIXME
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
        person_trips = self.export_path + 'Simulation_' + str(confignum) + '/Person_trips.xml'
        routefileFull = self.export_path + 'Simulation_' + str(confignum) + '/' + routefile
        busStopfileFull = self.export_path + 'Simulation_' + str(confignum) + '/' + busStopfile
        vehiclefileFull = self.export_path + 'Simulation_' + str(confignum) + '/' + vehiclefile
        configfileFull = self.export_path + 'Simulation_' + str(confignum) + '/' + 'config' + '.sumocfg'
        
        final_route_file_full = self.export_path + 'Simulation_' + str(confignum) + '/' + final_route_file
        gtfs.export_route_file(busstop_path, time_start, time_end, schedule, routefileFull)
        gtfs.export_busstop_file(busstop_path, busStopfileFull, network_path)
        vehicles.export(vehiclefileFull)

        #code_path = os.path.abspath(__file__)
        td = TDProcessor()

        td.merge_route_file(person_trips, td_path, taz_path, routefileFull, vehiclefileFull, busStopfileFull, network_path, final_route_file_full, time_end)
        
        
        # generate config file
        if os.path.exists(configfileFull):
            os.remove(configfileFull)
        
        f = open(configfileFull, "x")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<configuration xmlns:xsi="http://www.w3.org' +
                '/2001/XMLSchema-instance" xsi:noNamespaceSchema'+ 
                'Location="http://sumo.dlr.de/xsd/sumoConfiguration.xsd">\n')
        f.write('\t<input>\n\t\t<net-file value="' + network_path + '"/>\n')
        f.write('\t\t<route-files value="')
        f.write(final_route_file)
        for route in routes:
            f.write(', ' + route) #FIXME
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
        f.write('\t</output>\n\t<gui_only>\n\t\t<gui-settings-file value="' + gui_path + '"/>\n')
        f.write('\t<report>\n\t\t<no-warnings value="true"/>\n\t\t<error-log value="error_warning_log.xml"/>\n\t</report>\n')
        f.write('\t</gui_only>\n</configuration>')
        f.close()
        print('\nConfig File Saved. Please find configured simulation file at: ' + self.export_path + 'Simulation_' + str(confignum) + '\n')
        return self.export_path + 'Simulation_' + str(confignum) + '/'
        
        
        
        
        
        
        
        
            
        
        
    
    

    
                
        
        
