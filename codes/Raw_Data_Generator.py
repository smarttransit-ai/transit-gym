#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 03:13:35 2020

@author: danielgui
"""
import pandas as pd
import numpy as np
import os

class Raw_Data_Generator:
    def __init__(self):
        return 
    
    def generate_trip_file_from_GTFS(self, export_path):
        self.generate_busline_trips(export_path)
        self.generate_busstop_file(export_path)
        
    def generate_busline_trips(self, export_path):
        # testing
        busline_trips = export_path + 'BusLines.trips.xml'
        if os.path.exists(busline_trips):
            os.remove(busline_trips)
        
        # read from stopsinf
        data = pd.read_excel("../data/stopsinf_CARTA.xlsx",index_col = 'ID')
        data.index.names = ['stop_id']
        # read from Comprehensive_GTFS.xlsx
        trips = pd.read_excel("../data/Comprehensive_GTFS.xlsx",index_col = 'stop_id')
        
        
        trips=trips[trips['departure_time'].map(lambda x: x[0:2]!=24)]
        trips['depart'] = pd.to_timedelta(trips.departure_time).dt.total_seconds()
        trips['depart'] = trips['depart'].apply(lambda x: round(x, 1))
        trips['arrival'] = trips['depart']-3
        trips['bus_type'] = np.random.randint(101,105, trips.shape[0])
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
    
    def generate_busstop_file(self, export_path):
        # for testing
        busstop = export_path + "busStopsCARTA.xml"
        if os.path.exists(busstop):
            os.remove(busstop)
        
        #Read xlsx file from folder named "data"
        data = pd.read_excel("../data/stopsinf_CARTA.xlsx")
        
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
        
        
        