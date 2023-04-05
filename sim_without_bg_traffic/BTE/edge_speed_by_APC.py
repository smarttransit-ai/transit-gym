import traci
import time
import pickle
import random
import numpy as np
import pandas as pd
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--date", type=str, default="20210820", help="date")
parser.add_argument("--sim", type=str, default="transit-sim-date", help="simulation folder")
parser.add_argument("--trips_from_blocks", type=str, default="../Post-processing/trips_from_blocks.csv", help="trip from blocks files")
parser.add_argument("APC", type=str, default="../APC/202108.parquet", help="APC data")
args = parser.parse_args()


SUMO_CMD = ["/usr/bin/sumo"]
SUMO_CONFIG_FILE = ["-c", "../transit-sim-v1/SUMO_configuration.sumocfg"]

SUMO_CONFIG_FILE = ["-c", "../{}/SUMO_configuration.sumocfg".format(args.sim), 
                    "-r", "../{}/routes-{}.rou.xml,{}/passenger-{}.rou.xml".format(args.sim, args.date, args.sim, args.date),
                    "-a", "../{}/busStop-{}.add.xml".format(args.sim, args.date)]


SUMO_CMD.extend(SUMO_CONFIG_FILE)
print("LOADING .NET.XML ==================================  ")
traci.start(SUMO_CMD, label=str(random.randint(10000, 50000)))
# --------------------------------------------------------------

traj_list = []
while traci.simulation.getTime() < 3600*24:
    step = int(traci.simulation.getTime())
    traci.simulationStep()
    for veh_id in traci.vehicle.getIDList():
        traj_list.append({'veh': veh_id, 'step': step, 'lane': traci.vehicle.getLaneID(veh_id), 
                          'distance': traci.vehicle.getDistance(veh_id)})
    # -------------------------------------------------------------------------
    if step % 1000 == 0:
        print(step)

traj_df = pd.DataFrame(traj_list)
stop_df = pd.read_csv(args.trips_from_blocks)
APC_df = pd.read_parquet(args.APC, engine='pyarrow')
date_str = '{}-{}-{}'.format(args.date[:4], args.date[4:6], args.date[6:])
APC_df = APC_df[(APC_df['transit_date'] == date_str) & (APC_df['time_actual_arrive'].notnull())]
APC_df['timestamp'] = APC_df['time_actual_arrive'].apply(lambda x: (x - np.datetime64(f'{date_str}T00:00:00'))/np.timedelta64(1, 's'))

speed_dict = []
for veh_id in traj_df['veh'].unique():
    veh_stop = stop_df[stop_df['id'] == int(veh_id)].sort_values(by=['started'])
    veh_traj = traj_df[traj_df['veh'] == veh_id].sort_values(by=['step'])
    veh_apc = APC_df[APC_df['vehicle_id'] == int(veh_id)].sort_values(by=['timestamp'])
    for trip_id in veh_apc['gtfs_trip_id'].unique():
        trip_stop = veh_stop[veh_stop['trip_id'] == int(trip_id)]
        trip_apc = veh_apc[veh_apc['gtfs_trip_id'] == trip_id]
        trip_stop = trip_stop[trip_stop['busStop'].isin(trip_apc['stop_id'].unique())]
        trip_stop = trip_stop.drop_duplicates(subset=['busStop']).reset_index()
        trip_apc = trip_apc[trip_apc['stop_id'].isin(trip_stop['busStop'].unique())].reset_index()
        num_stops = len(trip_apc)
        for i, j in zip(range(0, num_stops-1), range(1, num_stops)):
            from_stop, to_stop = trip_apc.iloc[i]['stop_id'], trip_apc.iloc[j]['stop_id']
            apc_depart_time, apc_arrival_time = trip_apc.iloc[i]['timestamp'], trip_apc.iloc[j]['timestamp']
            sim_depart_time, sim_arrival_time = trip_stop.iloc[i]['started'], trip_stop.iloc[j]['started']
            start_pos, end_pos = trip_stop.iloc[i]['pos'], trip_stop.iloc[j]['pos']
            window_traj = veh_traj[(veh_traj['step'] >= sim_depart_time) & (veh_traj['step'] <= sim_arrival_time)]
            lanes = window_traj.lane.unique()
            edges = [lane[:-2] for lane in lanes if ':' not in lane]
            edges = [*set(edges)]
            travel_distance = window_traj.distance.max() - window_traj.distance.min()
            avg_speed = (travel_distance)/(sim_arrival_time - sim_depart_time)
            if avg_speed <= 0:
                continue
            for edge in edges:
                speed_dict.append({'edge': edge, 'speed': avg_speed, 'start': apc_depart_time, 'end': apc_arrival_time})
                
speed_df = pd.DataFrame(speed_dict)
last_edge_speed = {}
edge_speed = {}
for t in range(0, 288):
    start_time, end_time = t*300, (t+1)*300
    edge_speed_within_5_min = speed_df[(speed_df['start'] >= start_time) & (speed_df['start'] <= end_time)]
    if len(edge_speed_within_5_min) == 0:
        continue
    edge_speed[start_time] = []
    edge_speed_within_5_min = edge_speed_within_5_min.groupby('edge')['speed'].mean()
    for edge in edge_speed_within_5_min.index:
        set_new_speed = False
        if (edge not in last_edge_speed) or (last_edge_speed[edge] != edge_speed_within_5_min[edge]):
            set_new_speed = True
        if set_new_speed:
            edge_speed[start_time].append((edge, edge_speed_within_5_min[edge]))
            last_edge_speed[edge] = edge_speed_within_5_min[edge]
            
pickle.dump(edge_speed, open('edge_speed_by_APC.pkl', 'wb'))
