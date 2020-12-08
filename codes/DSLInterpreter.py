#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: danielgui
"""
import os
from textx import metamodel_from_file
from bs4 import BeautifulSoup
#from Matching_Func import Matcher
from Veh_Type_Container import Veh_Types_Container
from Raw_Data_Generator import Raw_Data_Generator

# initialize model

class Simulation(object):
    def __init__(self, metamodel_file="TransitSimulatorDSL.tx", data_path="../SUMO_simulation/"):
        self.routeSet = {}
        self.carSet = {}
        self.metamodel = metamodel_from_file(metamodel_file)
        self.data_path = data_path
        self.veh_type_container = Veh_Types_Container()
        
    
    # interpret model
    def interpret(self, file_name):
        model_c = self.metamodel.model_from_file(file_name)
        raw_generator = Raw_Data_Generator()
        raw_generator.generate_trip_file_from_GTFS(export_path=self.data_path)
        
        for model in model_c.files:
            self.file_name = model.configName
            self.start_time = model.timeStart
            self.end_time = model.timeEnd
            self.network = model.networkFile
            self.additional = model.additionalFile
            self.dump = model.dumpFile
        
            for route in model.routeSet:
                vehicles = []
                cars = {}
                # build a list of vehicle for each file
                if route.how == "INCLUDE":
                    vehicles = ['INCLUDE']
                    for vehicle in route.vehicleSet:
                        vehicles.append(vehicle.vehicleid)
                        if vehicle.vehicleType:
                            cars[vehicle.vehicleid] = vehicle.vehicleType
                            #FIXME
                        if vehicle.vehicleNewType:
                            cars[vehicle.vehicleid] = vehicle.vehicleNewType
                            v = {}
                            v['id'] = vehicle.vehicleNewType
                            if vehicle.accel:
                                v['accel'] = vehicle.accel
                            if vehicle.decel:
                                v['decel'] = vehicle.decel
                            if vehicle.length:
                                v['length'] = vehicle.length
                            if vehicle.maxSpeed:
                                v['maxSpeed'] = vehicle.maxSpeed
                            if vehicle.capacity:
                                v['capacity'] = vehicle.capacity
                            self.veh_type_container.add(v) 
                
                elif route.how == 'EXCLUDE':
                    vehicles = ['EXCLUDE']
                    for vehicle in route.vehicleSet:
                        
                        vehicles.append(vehicle.vehicleid)
                        
                else:
                    vehicles = ['ALL']
                self.routeSet[route.routeFileName] = vehicles
                self.carSet[route.routeFileName] = cars
            self.generateConfig()
            
    # generate route files
    def generateRouteFiles(self):
        count = 0
        for file in self.routeSet:
            infile = open(self.data_path + file, 'r')
            contents = infile.read()
            route = BeautifulSoup(contents, 'xml')
            vehlist = self.routeSet[file]
            cardict = self.carSet[file]
            # include those vehicle if use INCLUDE option
            if vehlist[0] == 'INCLUDE':
                for vehicle in route.find_all('vehicle'):
                    matched_id = vehicle['id']
                    if not matched_id in vehlist:
                        vehicle.decompose()
                    else:
                        if matched_id in cardict:
                            vehicle['type'] = cardict[matched_id]
            # exclude those vehicle if use EXCLUDE option
            elif vehlist[0] == 'EXCLUDE':
                for vehicle in route.find_all('vehicle'):
                    if self.vehicle['id'] in vehlist:
                        vehicle.decompose()
            # do nothing if include ALL option
            xml = route.prettify('utf-8')
            with open(self.data_path + self.file_name + '_data_' + str(count) + '.xml', 'wb') as file:
                file.write(xml)
                file.close()
            count += 1
        
        
    
    def generateConfig(self):
        self.generateRouteFiles()
        vehDef = self.data_path + "vehtype.add.xml"
        self.veh_type_container.export(vehDef)
        self.additional = self.additional + "," + "vehtype.add.xml"
        if os.path.exists(self.data_path + self.file_name + '.sumocfg'):
            os.remove(self.data_path + self.file_name + '.sumocfg')
        
        # write SUMOCFG file to initialize simulation
        f = open(self.data_path+self.file_name + '.sumocfg', "x")
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<configuration xmlns:xsi="http://www.w3.org' +
                '/2001/XMLSchema-instance" xsi:noNamespaceSchema'+ 
                'Location="http://sumo.dlr.de/xsd/sumoConfiguration.xsd">\n')
        f.write('\t<input>\n\t\t<net-file value="'+ self.network + '"/>\n')
        f.write('\t\t<route-files value="')
        count = 0
        files_to_write = ''
        for key in self.routeSet:
            files_to_write = files_to_write + self.file_name + '_data_' + str(count) + '.xml' + ','
            count = count + 1
        if len(files_to_write) > 0:
            files_to_write = files_to_write[:-1]
            
        f.write(files_to_write)
        f.write('"/>\n')
        f.write('\t\t<additional-files value="'+ self.additional +'"/>\n')
        f.write('\t</input>\n')
        f.write('\t<time>\n\t\t<begin value="' + str(self.start_time) + '"/>\n')
        f.write('\t\t<end value="'+  str(self.end_time) + '"/>\n')
        f.write('\t\t<time-to-teleport value="150" />\n\t</time>\n')
        f.write('\t<processing>\n\t\t<ignore-route-errors value="true"/>\n'+
                '\t</processing>\n')
        f.write('\t<output>\n\t\t<netstate-dump value="' + self.dump + '"/>\n')
        f.write('\t</output>\n\t<gui_only>\n\t\t<gui-settings-file value="gui.view.xml"/>\n')
        f.write('\t</gui_only>\n</configuration>')
        f.close()
    
    def generate_Raw_from_GTFS(self):
        rgt = Raw_Data_Generator()
        rgt.generate_trip_file_from_GTFS(self.data_path)
        rgt.generate_busline_trips(self.data_path)
        
        


                    
            
            
        