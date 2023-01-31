# -*- coding: utf-8 -*-
"""
Created on Mon Oct 25 21:38:37 2021

@author: 15304
"""

import pandas as pd
import os

# helper class for converting buses input
class Veh_Types_Container:
    def __init__(self, vehicle_path):
        self.data = pd.read_excel(vehicle_path)
        self.data = self.data.applymap(str).set_index("BusID")
        self.data['guiShape'] = 'bus'
        self.data['minGap'] = '3.00'
        self.data['sigma'] = '0.5'
        self.data = self.data.to_dict("index")
        self.default_value = {"id": 'BUS', 'accel':'1.2', 'decel':'bus', 'guiShape': 'bus',
                              "length":'8.00', "maxSpeed":"65.00", "minGap":"3.00",
                              "personCapacity":"32", "sigma": "0.5", "vClass": "bus", 
                              "emissionClass": "HBEFA3/Bus"}
    
    # check if vehicle is in
    def isin(self, vehicle_id):
        return True if vehicle_id in self.data else False
    
    # add a new vehicle
    def add(self, vehicle):
        newVeh = {}
        data_list = ['accel', 'decel', 'guiShape', 'length', 'maxSpeed', 'minGap', 'personCapacity', 'sigma', 
                     'vClass', 'emissionClass']
        for item in data_list:
            if item in vehicle:
                newVeh[item] = vehicle[item]
            else:
                newVeh[item] = self.default_value[item]
        self.data[vehicle['id']] = newVeh
    
    # export to additional file
    def export(self, export_loc):
        if os.path.exists(export_loc):
            os.remove(export_loc)
        f = open(export_loc, "x")
        f.write("<additional>\n")
        for key, r in self.data.items():
            f.write('\t<vType id="' + key+ '" accel="'\
                + r['accel'] + '" decel="'+ r['decel'] + '" sigma="' + r['sigma'] + '" length="'\
                + r['length']+'" minGap="' + r['minGap'] + '" maxSpeed="'+ r['maxSpeed']+'" personCapacity="'\
                + r['personCapacity']+'" guiShape="' + r['guiShape'] + '" vClass="bus" emissionClass="' + r['emissionClass'] + '"/>\n')
        
        #Write the last line in the .txt file
        f.write("</additional>")
        f.close()

