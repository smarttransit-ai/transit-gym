
import numpy as np
import pandas as pd
import os
import datetime
import random

# testing
if os.path.exists('BusLines.trips.xml'):
    os.remove("BusLines.trips.xml")

# read from stopsinf
data = pd.read_excel("../data/stopsinf_CARTA.xlsx",index_col = 'ID')
data.index.names = ['stop_id']
# read from Comprehensive_GTFS.xlsx
trips = pd.read_excel("../data/Comprehensive_GTFS.xlsx",index_col = 'stop_id')


trips=trips[trips['departure_time'].map(lambda x: x[0:2]!=24)]
trips['depart'] = pd.to_timedelta(trips.departure_time).dt.total_seconds()
trips['depart'] = trips['depart'].apply(lambda x: round(x, 1))
trips['arrival'] = trips['depart']-30
trips['start_time'] = trips.groupby(['tripid'])['depart'].transform('min')
trips['start_rtime']= pd.to_datetime(trips['start_time'], unit='s').dt.strftime("%H:%M:%S")
trips['trip_headsign'] = trips.trip_headsign.str.replace(' ', '_')
trips=trips.sort_values(['start_time', 'tripid'])
trip = dict(tuple(trips.groupby([trips['start_time'],trips['tripid'],trips['route_id'],trips['trip_headsign'],trips['start_rtime'],trips['block_name']])))

# join each of those dataframe with stopsinf
for tripid, df in trip.items():
    trip[tripid] = df.join(data, how='inner')

#Create BusLines.xml file to write in
f = open("BusLines.trips.xml", "x")

# write first line
f.write("<routes>\n")

for tripid, df in trip.items():
    df['stop_id'] = df.index
    # add one element as bus type           
    tripid=tripid+(random.randint(101,105),) 
    f.write('\t<trip id="Route'+str(tripid[2])+"_trip"+str(tripid[1])+
            "_"+str(tripid[4])+'" line="Route'+str(tripid[2])+
            "_"+tripid[3]+"_block"+str(tripid[5])+"_trip"+str(tripid[1])+'" type="Gillig_'
            +str(tripid[6])+'" depart="' + str(tripid[0]) + 
            '" color="1,1,0" departPos="stop">\n')
    # helper function to parse data to html
    def parser(r):
        return '\t\t<stop busStop="busStop_' + r['edgeID']+ "_"\
            + r['laneind'] + "_" + r['stop_id']\
            + '" duration="30" until="'+ r['depart'] + '" arrival="'+ r['arrival']+ '"/>\n'
    #Write all the bus stop defination under the "<additional>" 
    df['export'] = df.apply(lambda x: parser(x.astype(str)), axis=1)
    for index, row in df.iterrows():
        f.write(row['export'])
    f.write("\t</trip>\n")

f.write("</routes>")
f.close()
