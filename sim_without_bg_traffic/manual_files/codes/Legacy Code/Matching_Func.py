#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 02:09:08 2020

@author: danielgui
"""

import pandas as pd

# implementation of the mapping table
class Matcher:
    def __init__(self):
        self.gtfs = pd.read_excel("../data/GTFS_Data.xlsx").applymap(str)
        # Mapping criteria: tripid -> trip_headsign + " " + block_id 
        self.gtfs = self.gtfs[['tripid', 'trip_headsign', 'block_id']]
        self.gtfs['name'] = self.gtfs.apply(lambda x: x['trip_headsign'] + ' ' + str(x['block_id']), axis =1)
        self.gtfs = self.gtfs[['tripid', 'name']]
        self.forward = dict(zip(self.gtfs.tripid, self.gtfs.name))
        self.backward = dict(zip(self.gtfs.name, self.gtfs.tripid))

    def match_gtfs(self,vehid):
        return self.forward[vehid]
    def match_back(self, vehname):
        return self.backward[vehname]
