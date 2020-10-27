#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 04:28:36 2020

@author: danielgui
"""
import pandas as pd

trips = pd.read_csv('trips.txt', sep=',', index_col = 'trip_id')
stop_times = pd.read_csv('stop_times.txt', sep=',', index_col = 'trip_id')

test = stop_times.join(trips, how='left')
test['tripid'] = test.index
test.to_excel('Comprehensive_GTFS.xlsx', index=False)
test = test[['tripid','arrival_time', 'departure_time', 'stop_id', 'trip_headsign', 'block_id']]
test.to_excel('GTFS_Data.xlsx', index=False)
