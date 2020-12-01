
import numpy as np
import pandas as pd
import os
import datetime

# testing
if os.path.exists('E:/SUMO/RUIXIAO/newChattanooganet/Data/BusLines.trips.xml'):
    os.remove("E:/SUMO/RUIXIAO/newChattanooganet/Data/BusLines.trips.xml")

# read from stopsinf
data = pd.read_excel("E:/SUMO/RUIXIAO/newChattanooganet/Data/stopsinf_CARTA.xlsx",index_col = 'ID')
data.index.names = ['stop_id']
# read from Comprehensive_GTFS.xlsx
trips = pd.read_excel("E:/SUMO/RUIXIAO/newChattanooganet/Data/Comprehensive_GTFS.xlsx",index_col = 'stop_id')


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
f = open("E:/SUMO/RUIXIAO/newChattanooganet/Data/BusLines.trips.xml", "x")

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
