import traci
import pandas as pd
import random
import time
import pickle
import xmltodict
import json
from collections import OrderedDict
import datetime

BUS_ROUTE_FILE = './transit_run/bus_routes_only.rou.xml'
ROUTE_ASM_FILE = 'trips_vid_n_timebyGTFS_20220111.csv'
SUMO_CMD = ["/usr/bin/sumo"]
SUMO_CONFIG_FILE = ["-c", "./transit_run/Chattanooga_SUMO_mehdi_final.sumocfg"]
EDGE_DATA_FILE = './filtered_edge_data.pkl'

USING_BACKGROUND_ELIMINATION = True

# preprocess route assignment file ----------------------------
## get all route ids --------------------
with open(BUS_ROUTE_FILE) as fd:
    doc = xmltodict.parse(fd.read())
route_ids = {}
for route in doc['routes']['route']:
    route_ids[route['@id']] = True
## --------------------------------------

## process route_id to match with bus_with_person.rou.xml -------
route_asm_df = pd.read_csv(ROUTE_ASM_FILE)
route_asm_df['route_id'] = route_asm_df.apply(lambda row: str(row['trip_id']) + '020' + '_' + row['gtfs_time_start'], axis=1)
route_asm_df['valid'] = route_asm_df['route_id'].apply(lambda x: x in route_ids)
print('WARNING: There are {} invalid trips'.format(len(route_asm_df[route_asm_df['valid'] == False])))
route_asm_df = route_asm_df[route_asm_df['valid']] # get only valid trips (found in .rou.xml)

def to_second(time_str):
    h, m, s = time_str.split(':')
    return int(h)*3600 + int(m)*60 + int(s)

route_asm_df['depart'] = route_asm_df['gtfs_time_start'].apply(to_second)
del route_ids
## --------------------------------------------------------------
# -------------------------------------------------------------------

# start SUMO ---------------------------------------------------
SUMO_CMD.extend(SUMO_CONFIG_FILE)

if USING_BACKGROUND_ELIMINATION:
    print("START LOADING EDGE DATA ==================================  ")
    edge_data_by_step = pickle.load(open(EDGE_DATA_FILE, 'rb'))
INTERVAL = 60
print("START LOADING .NET.XML ==================================  ")
traci.start(SUMO_CMD, label=str(random.randint(10000, 50000)))
# --------------------------------------------------------------

# Create a dict to monitor vehicles -------------------------------
veh_obj = {}
for veh_id in route_asm_df['vid'].unique():
    veh_obj[veh_id] = {}
    veh_obj[veh_id]['routes'] = []
    veh_obj[veh_id]['counter'] = 0
    df_veh = route_asm_df[route_asm_df['vid'] == veh_id]
    for idx, row in df_veh.iterrows():
        veh_obj[veh_id]['routes'].append({'route_id': row['route_id'], 'depart': row['depart']})
# -----------------------------------------------------------------

# Add first trips of vehicles -------------------------------------
for veh_id in veh_obj:
    veh_routes, veh_counter = veh_obj[veh_id]['routes'], veh_obj[veh_id]['counter']
    traci.vehicle.add('{}-{}'.format(veh_id, veh_counter), veh_routes[veh_counter]['route_id'],
                                depart=veh_routes[veh_counter]['depart'], typeID='Gillig_105', departPos='stop')
    veh_obj[veh_id]['counter'] += 1
# -----------------------------------------------------------------

# SIMULATING :::::::::::::::::::::::::::::::::::::::::::::::::::
while traci.simulation.getTime() < 3600*24:
    step = int(traci.simulation.getTime())
    
    # if any trip is finished, add the next trip -----------------------------
    for veh_id_sim in traci.simulation.getArrivedIDList():
        veh_id = int(veh_id_sim.split('-')[0])
        veh_routes, veh_counter = veh_obj[veh_id]['routes'], veh_obj[veh_id]['counter']
        if veh_counter < len(veh_routes):
            new_veh_id = '{}-{}'.format(veh_id, veh_counter)
            traci.vehicle.add(new_veh_id, veh_routes[veh_counter]['route_id'],
                                        depart=veh_routes[veh_counter]['depart'],  typeID='Gillig_105', departPos='stop')
            if step > veh_routes[veh_counter]['depart']:
                delta = step - veh_routes[veh_counter]['depart']
                for stop in traci.vehicle.getStops(new_veh_id):
                    stop_dict = stop.__dict__
                    new_until = stop_dict['until'] - delta
                    new_arrival = stop_dict['intendedArrival'] - delta
                    traci.vehicle.setBusStop(new_veh_id, stop_dict['stoppingPlaceID'], duration=1, until=new_until, flags=8)
            veh_obj[veh_id]['counter'] += 1
    # -------------------------------------------------------------------------
    
    # mimic background traffic ------------------------------------------------                
    if (USING_BACKGROUND_ELIMINATION & (step % INTERVAL == 0)):
        if step in edge_data_by_step:
            for item in edge_data_by_step[step]:
                traci.edge.setMaxSpeed(item['edge_id'], item['edge_speed'])    
    traci.simulationStep()
    # -------------------------------------------------------------------------
    if step % 200 == 0:
        print(step)

traci.close()
print("FINISH !!!!!")
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::