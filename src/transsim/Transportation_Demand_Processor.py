#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: danielgui
"""
import subprocess
import os

class TDProcessor:
    def __init__(self, td_path, data_path):
        self.td_path = data_path + 'models/travel-demand/' + td_path
        self.data_path = data_path
    
    def merge_route_file(self, routefileFull, vehiclefileFull, busStopfileFull, network, final_route_file_full, time_end):
        if not os.path.exists(self.td_path):
            raise ValueError("Missing transportation demand file", self.td_path)
        if not os.path.exists(self.data_path + "model/travel-demand/taz.xml"):
            raise ValueError("Missing transportation demand file: ", self.data_path + "taz.xml")
        errorcode = subprocess.call('od2trips -d '+ self.td_path +
                  ' --taz-files "'+ self.data_path + 'taz.xml" --prefix person --persontrips --persontrips.modes public -o "' + 
                  'Person_trips.xml"', shell=True)
        
        
        command = 'duarouter --route-files "'+ routefileFull + ', ' + \
            'Person_trips.xml" --net-file "' + network + '" --unsorted-input --additional-files "'+ \
                busStopfileFull + ', ' + vehiclefileFull + '" --ptline-routing --output-file "' + \
                    final_route_file_full + '" --ignore-errors --no-warnings -b 0 -e ' + str(time_end)
        errorcode = subprocess.call(command, shell=True)
        
        
        # if errorcode:
        #     raise RuntimeError("generation of final route file failed with exit code:", errorcode)
        
        
        