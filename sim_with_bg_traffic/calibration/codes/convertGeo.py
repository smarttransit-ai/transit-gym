#Check the environment variable SUMO_HOME is set before running the script
#The <SUMO_HOME>/tools directory must be on the python load path
import os, sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:   
    sys.exit("please declare environment variable 'SUMO_HOME'")
# Connect to SUMO  
import traci
traci.start(["sumo", "-n", "Chattanooga_SUMO_Network.net.xml"])

#Get geographic coordinates of bus stops
import pandas as pd
detectors = pd.read_excel('GeoCoordinate.xlsx',sheet_name = "GeoCoordinate").copy()
LAT = detectors['Latitude']
LON = detectors['Longitude']

#Convert geographic coordinates to position info (edge ID, lane position and lane index)
def get_edge(lon, lat):
    edgeID, lanePosition, laneIndex = traci.simulation.convertRoad(lon,lat, True)
    return edgeID, lanePosition, laneIndex

edgeinf =[]
for i in range(len(LAT)):
    edgeinf.append(get_edge(LON[i],LAT[i]))
# Write to     
df = pd.DataFrame(edgeinf, columns=['edgeID', 'lanepos', 'laneind'])
df.to_excel(r'sumoCoordinate.xlsx', index = False)
