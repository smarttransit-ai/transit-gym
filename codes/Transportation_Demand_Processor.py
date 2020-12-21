#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: danielgui
"""
import subprocess
import os
import sys
class TDProcessor:
    def __init__(self, td_path, data_path):
        self.td_path = data_path + td_path
        self.data_path = data_path
    
    def merge_route_file(self, routefileFull, vehiclefileFull, busStopfileFull, network, final_route_file_full):
        # errorcode = subprocess.call('od2trips -d '+ self.td_path +
        #           ' --taz-files "'+ self.data_path + 'taz.xml" --prefix person --persontrips --persontrips.modes public -o "' + 
        #           'Person_trips.xml"', shell=True)
        env = os.environ
        env['PATH'] += ':/usr/local/bin' #FIXME
        env['SUMO_HOME'] = '/usr/local/opt/sumo/share/sumo' #FIXME
        errorcode = subprocess.call('od2trips -d '+ self.td_path +
                  ' --taz-files "'+ self.data_path + 'taz.xml" --prefix person --persontrips --persontrips.modes public -o "' + 
                  'Person_trips.xml"', shell=True)
        if errorcode:
            raise RuntimeError("generation of Person_trips command failed with exit code:", errorcode)
        
        command = 'duarouter --route-files "'+ routefileFull + ', ' + \
            'Person_trips.xml" --net-file "' + network + '" --unsorted-input --additional-files "'+ \
                busStopfileFull + ', ' + vehiclefileFull + '" --ptline-routing --output-file "' + \
                    final_route_file_full + '" --ignore-errors'
        print(command)
        errorcode = subprocess.call(command, shell=True)
        
        
        if errorcode:
            raise RuntimeError("generation of final route file failed with exit code:", errorcode)
        
        
        