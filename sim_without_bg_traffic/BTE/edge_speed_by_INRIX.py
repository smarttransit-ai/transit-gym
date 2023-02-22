import pandas as pd
import geopandas as gpd
import random
import numpy as np
import pickle
import traci
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--date", type=str, default="20210820", help="date")
parser.add_argument("--sim", type=str, default="transit-sim-date", help="simulation folder")
parser.add_argument("--INRIX_data", type=str, default="INRIX-data/part-00054-49075979-b38a-4685-b377-f8d38d569b56.c000.snappy.parquet", help="INRIX data")
parser.add_argument("--INRIX_geo", type=str, default="INRIX-data/USA_Tennessee.geojson", help="INRIX geojson")
args = parser.parse_args()

SUMO_CMD = ["/usr/bin/sumo"]
SUMO_CONFIG_FILE = ["-c", "{}/SUMO_configuration.sumocfg".format(args.sim), 
                    "-r", "{}/routes-{}.rou.xml,{}/passenger-{}.rou.xml".format(args.sim, args.date, args.sim, args.date),
                    "-a", "{}/busStop-{}.add.xml".format(args.sim, args.date)]
traci.start(SUMO_CMD, label=str(random.randint(10000, 50000)))

df = pd.read_parquet(args.INRIX_data, engine='pyarrow')
geo_df = gpd.read_file(args.INRIX_geo)

HAMILTON = geo_df[geo_df.County=='HAMILTON'].copy()
HAMILTON['lat'] = HAMILTON.geometry.centroid.y
HAMILTON['lon'] = HAMILTON.geometry.centroid.x

def get_edge_id(row):
    edge, _, _ = traci.simulation.convertRoad(row['lon'], row['lat'], isGeo=True)
    return edge

date_str = '{}-{}-{}'.format(args.date[:4], args.date[4:6], args.date[6:])

HAMILTON['edge_id'] = HAMILTON.apply(lambda row: get_edge_id(row), axis=1)
one_day_df = df[(df['measurement_tstamp'] >= np.datetime64(date_str)) & (df['measurement_tstamp'] < np.datetime64(date_str))]
speed_log = {}
date = np.datetime64(date_str)
for xd_id in one_day_df['xd_id'].unique():
    print(xd_id)
    edge_df = one_day_df[one_day_df['xd_id'] == xd_id].sort_values(by=['measurement_tstamp'])
    geo_edge_df = HAMILTON[HAMILTON['XDSegID'] == xd_id]
    if len(geo_edge_df) <= 0:
        continue
    edge_id = geo_edge_df[['edge_id']].values[0][0]
    cur_ts = -5*60
    last_speed = -1
    while cur_ts < 3600*24:
        cur_ts += 5*60
        edge_df = edge_df[(edge_df['measurement_tstamp'] >= date + np.timedelta64(cur_ts, 's'))]
        if cur_ts not in speed_log:
            speed_log[cur_ts] = []
        tmp_df = edge_df[(edge_df['measurement_tstamp'] < date + np.timedelta64(cur_ts + 5*60, 's'))]
        if len(tmp_df) <= 0:
            continue
        speed = tmp_df[['average_speed']].values[0][0]
        if last_speed != speed:
            speed_log[cur_ts].append([edge_id, speed])
            last_speed = speed
            
pickle.dump(speed_log, open('edge_speed_by_INRIX.pkl', 'wb'))
