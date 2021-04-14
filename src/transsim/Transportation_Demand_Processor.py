#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


@author: danielgui
"""
import subprocess
import os

class TDProcessor:
    def __init__(self):
        #self.code_path = code_path
        pass
        
    def merge_route_file(self, person_trips, td_path, taz_path, routefileFull, vehiclefileFull, busStopfileFull, network, final_route_file_full, time_end):

        if not os.path.exists(td_path):
            raise ValueError("Missing transportation demand file", td_path)
        if not os.path.exists(taz_path):
            raise ValueError("Missing transportation demand file: ", taz_path)
        errorcode = subprocess.call('od2trips -d "'+ td_path +
                  '" --taz-files "'+ taz_path + '" --prefix person --persontrips --persontrips.modes public -o "' + person_trips + '"', shell=True)
        
        
        command = 'duarouter --route-files "'+ routefileFull + ', ' + \
            person_trips + '" --net-file "' + network + '" --unsorted-input --additional-files "'+ \
                busStopfileFull + ', ' + vehiclefileFull + '" --ptline-routing --output-file "' + \
                    final_route_file_full + '" --ignore-errors --no-warnings' + str(time_end)
        errorcode = subprocess.call(command, shell=True)
        
        
        # if errorcode:
        #     raise RuntimeError("generation of final route file failed with exit code:", errorcode)
        
        
        