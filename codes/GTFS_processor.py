#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 14:58:34 2020

@author: danielgui
"""

import gtfs_kit as gk
import pandas as pd
import os
import numpy as np
import sys
import traci

class GTFS_processor:
    def __init__(self, data_path ,date):
        path = data_path + self.get_path(date) + '/'
        stop_times = pd.read_csv(path + "stop_times.txt", sep=',', index_col = "trip_id")
        trips = pd.read_csv(path + 'trips.txt', sep=',', index_col = 'trip_id')
        test = stop_times.join(trips, how='left')
        test['tripid'] = test.index
        test.set_index('stop_id', inplace=True)
        self.stops = pd.read_csv(path + "stops.txt", sep=',')
        self.gtfs_data = test
        #self.parse()
        self.assignment = None
        #self.schedule_def = pd.read_csv(path + "calendar.txt", sep=',', index_col = "trip_id")
    
    def parse(self):
        self.gtfs_data['arrival_time'] = self.gtfs_data['arrival_time'].astype(str)
        self.gtfs_data['departure_time'] = self.gtfs_data['departure_time'].astype(str)
        def convert(data):
            return data['arrival_time'][:2]+ data['arrival_time'][3:5] + data['arrival_time'][6:]
        self.gtfs_data['arrival_time'] = self.gtfs_data.apply(lambda x: convert(self.gtfs_data), axis=1)
        self.gtfs_data['arrival_time'] = self.gtfs_data['arrival_time'].astype(int)
        def convert(data):
            return data['departure_time'][:2]+ data['departure_time'][3:5] + data['departure_time'][6:]
        self.gtfs_data['departure_time'] = self.gtfs_data.apply(lambda x: convert(self.gtfs_data), axis=1)
        self.gtfs_data['departure_time'] = self.gtfs_data['departure_time'].astype(int)
        
    
    def get_path(self, date):
        if date == 'latest':
            return '20200816' #FIXME
        else:
            return date
    
    def assign_vehicle(self, tripid, blockid):
        self.assignment = [tripid, blockid]
    
    def parse_schedule(self, schedule): #FIXME
        if schedule == 'weekday':
            return [2]
        else:
            return [1, 5]
    
    # generate intermediate dataframe for busstop information
    def convert_bus_stop(self, network):
        LAT = self.stops['stop_lat']
        LON = self.stops['stop_lon']
        
        if 'SUMO_HOME' in os.environ:
            tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
            sys.path.append(tools)
        else:   
            sys.exit("please declare environment variable 'SUMO_HOME'")
            raise ValueError('Environment Variable "SUMO HOME" not declared!')
        # Connect to SUMO  
        traci.start(["sumo", "-n", network])
        def get_edge(lon, lat):
            edgeID, lanePosition, laneIndex = traci.simulation.convertRoad(lon,lat, True)
            return edgeID, lanePosition, laneIndex
        edgeinf =[]
        for i in range(len(LAT)):
            edgeinf.append(get_edge(LON[i],LAT[i]))
        # Write to     
        df = pd.DataFrame(edgeinf, columns=['edgeID', 'lanepos', 'laneind'])
        return df
        
    
    def export_route_file(self,time_start, time_end, schedule, export_path):
        time_start = time_start * 100
        time_end = time_end * 100
        data = self.gtfs_data
        #trips = data[data['arrival_time'] >= time_start & data['departure_time']<= time_end]
        trips = data
        schedule = self.parse_schedule(schedule)
        trips = trips[trips['service_id'].isin(schedule)]
        # testing
        busline_trips = export_path
        if os.path.exists(busline_trips):
            os.remove(busline_trips)
        
        # read from stopsinf
        data = pd.read_excel("../data/busstops.xlsx",index_col = 'ID')
        data.index.names = ['stop_id']
        # read from Comprehensive_GTFS.xlsx
        
        
        trips=trips[trips['departure_time'].map(lambda x: x[0:2]!=24)]
        
        trips['depart'] = pd.to_timedelta(trips.departure_time).dt.total_seconds()
        trips['depart'] = trips['depart'].apply(lambda x: round(x, 1))
        trips['arrival'] = trips['depart']-3
        trips['bus_type'] = np.random.randint(101,105, trips.shape[0]) # FIXME
        trips['start_time'] = trips.groupby(['tripid'])['depart'].transform('min')
        trips['trip_headsign'] = trips.trip_headsign.str.replace(' ', '_')
        trips=trips.sort_values(['start_time', 'tripid'])
        trip = dict(tuple(trips.groupby([trips['start_time'],trips['tripid'],trips['route_id'],trips['trip_headsign']])))
        
        # join each of those dataframe with stopsinf
        for tripid, df in trip.items():
            trip[tripid] = df.join(data, how='inner')
        
        #Create BusLines.xml file to write in
        f = open(busline_trips, "x")
        
        # write first line
        f.write("<routes>\n")
        for tripid, df in trip.items():
            
            df['stop_id'] = df.index
            #depart = df['depart'].iloc[0]
            BUS=df['bus_type'].iloc[0]
            block=df['block_name'].iloc[0]
            if self.assignment:
                if int(block) in self.assignment[1]:
                    f.write('\t<trip id="Route'+str(tripid[2])+ "_"+tripid[3]+"_block"+str(block)+"_trip" +str(tripid[1])+'" line="Route'+str(tripid[2])+"_trip" +str(tripid[1])+'" type="'+ self.assignment[1][block] +'" depart="' + str(tripid[0]) + '" color="1,1,0" departPos="stop">\n')
                elif int(tripid[1]) in self.assignment[0]:
                    f.write('\t<trip id="Route'+str(tripid[2])+ "_"+tripid[3]+"_block"+str(block)+"_trip" +str(tripid[1])+'" line="Route'+str(tripid[2])+"_trip" +str(tripid[1])+'" type="'+ self.assignment[0][tripid[1]] +'" depart="' + str(tripid[0]) + '" color="1,1,0" departPos="stop">\n')
                else:
                    f.write('\t<trip id="Route'+str(tripid[2])+ "_"+tripid[3]+"_block"+str(block)+"_trip" +str(tripid[1])+'" line="Route'+str(tripid[2])+"_trip" +str(tripid[1])+'" type="Gillig_'+str(BUS)+'" depart="' + str(tripid[0]) + '" color="1,1,0" departPos="stop">\n')
                if (int(block) in self.assignment[1]) and (int(tripid[1]) in self.assignment[0]):
                    if self.assignment[1][block] != self.assignment[0][int(tripid[1])]:
                        print('Same trip with multiple assignment, used assignment for block: tripid: ',int(tripid[1]),', blockid: ', int(block))
            else:
                f.write('\t<trip id="Route'+str(tripid[2])+ "_"+tripid[3]+"_block"+str(block)+"_trip" +str(tripid[1])+'" line="Route'+str(tripid[2])+"_trip" +str(tripid[1])+'" type="Gillig_'+str(BUS)+'" depart="' + str(tripid[0]) + '" color="1,1,0" departPos="stop">\n')
            # helper function to parse data to html
            def parser(r):
                return '\t\t<stop busStop="busStop_' + r['edgeID']+ "_"\
                    + r['laneind'] + "_" + r['stop_id']\
                    + '" duration="3" until="'+ r['depart'] + '" arrival="'+ r['arrival']+ '"/>\n'
            #Write all the bus stop defination under the "<additional>" 
            df["export"] = df.apply(lambda x: parser(x.astype(str)), axis=1)
            for index, row in df.iterrows():
                f.write(row['export'])
            f.write("\t</trip>\n")
        
        f.write("</routes>")
        f.close()
    
    def export_busstop_file(self, export_path, network):
        # for testing
        busstop = export_path
        if os.path.exists(busstop):
            os.remove(busstop)
        
        #Read xlsx file from folder named "data"
        data = pd.read_excel("../data/busstops.xlsx")
        
        #Create new columns 'startpos' and 'endpos' in data based on the "lanepos" in "stopsinf_CARTA.xlsx"
        data['startPos'] = round(data["lanepos"] - 5, 2)
        data['endPos'] = round(data['startPos'] + 10, 2)
        data['startPos'][data['startPos']<0] = 0
        #Create busStopsCARTA.txt file to write in
        f = open(busstop, "x")
        #Write the fist line in the .txt file
        f.write("<additional>\n")
        
        # helper function to parse data to html
        def parser(r):
            return '\t<busStop id="busStop_' + r['edgeID']+ "_"\
                + r['laneind'] + "_" + r['ID']\
                + '" lane="' + r['edgeID'] + '_'\
                + r['laneind'] + '" startPos="'\
                + r['startPos'] + '" endpos="'\
                + r['endPos'] + '" friendlyPos="1"/>\n'
        #Write all the bus stop defination under the "<additional>" 
        data["export"] = data.apply(lambda x: parser(x.astype(str)), axis=1)
        for index, row in data.iterrows():
            f.write(row['export'])
        
        #Write the last line in the .txt file
        f.write("</additional>")
        f.close()
    
    def get_trip_id_by_block(self,blockid):
        return list(self.gtfs[self.gtfs['blockid']==blockid].index)
    
    def get_trip_id(self, blockid, tripid):
        return 0
    
    
    
        
        
        
        