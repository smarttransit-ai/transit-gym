
import pandas as pd
import os
import datetime

# testing
if os.path.exists('../data/BusLines.xml'):
    os.remove("../data/BusLines.xml")

# read from stopsinf
data = pd.read_excel("../data/stopsinf_CARTA.xlsx",index_col = 'ID')
data.index.names = ['stop_id']
# read from Comprehensive_GTFS.xlsx
trips = pd.read_excel("../data/Comprehensive_GTFS.xlsx",index_col = 'stop_id')

#Function to convert 24:xx:xx to 00:xx:xx
def convert_time(date_str):
    if date_str[0:2] != '24':
        return date_str
    date_str = '00' + date_str[2:8]
    return date_str

trips['departure_time'] = trips.departure_time.apply(convert_time)
trips['depart'] = pd.to_timedelta(trips.departure_time).dt.total_seconds()
trip = dict(tuple(trips.groupby(trips['tripid'])))

# join each of those dataframe with stopsinf
for tripid, df in trip.items():
    trip[tripid] = df.join(data, how='inner')

#Create BusLines.xml file to write in
f = open("../data/BusLines.xml", "x")

# write first line
f.write("<routes>\n")

for tripid, df in trip.items():
    # FIXME: depart: the first value of 'depart' column in dict 'trip' for each 'tripid'
    df['stop_id'] = df.index
    #FIX here:
    f.write('\t<trip id="'+str(tripid)+'" type="BUS" depart=" " color="1,1,0" departPos="stop">\n')
    # helper function to parse data to html
    def parser(r):
        return '\t\t<stop busStop="busStop_' + r['edgeID']+ "_"\
            + r['laneind'] + "_" + r['stop_id']\
            + '" duration="2"/>\n'
    #Write all the bus stop defination under the "<additional>" 
    df["export"] = df.apply(lambda x: parser(x.astype(str)), axis=1)
    for index, row in df.iterrows():
        f.write(row['export'])
    f.write("\t</trip>\n")

f.write("</routes>")
f.close
