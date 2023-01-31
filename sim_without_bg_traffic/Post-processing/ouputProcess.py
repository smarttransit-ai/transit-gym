import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--date", type=str, default="2021-08-s20", help="date")
# parser.add_argument("--sim", type=str, default="transit-sim-date", help="simulation folder")
# parser.add_argument("--BTE_data", type=str, default="BTE/edge_speed_by_sim.pkl", help="BTE data")
args = parser.parse_args()

## bus stop output containing delay and person load information
stopO = pd.read_csv("../transit-sim-date/busstop_output.csv",sep=';')
stopO=stopO[["stopinfo_id","stopinfo_busStop","stopinfo_started","stopinfo_arrivalDelay",
             "stopinfo_ended","stopinfo_delay","stopinfo_initialPersons",
             "stopinfo_loadedPersons","stopinfo_unloadedPersons",
             "stopinfo_lane","stopinfo_pos","stopinfo_parking"]]
stopO=stopO.sort_values(["stopinfo_id","stopinfo_started"])

## trajectory for all vehicles during the simulation time interval
motion = pd.read_csv("../transit-sim-date/trajectory_output.csvmotionState.csv",sep=';',low_memory=False)
vehtype = pd.read_csv("../transit-sim-date/trajectory_output.csvactorConfig.csv",sep=';')
vehref = pd.read_csv("../transit-sim-date/trajectory_output.csvvehicle.csv",sep=';')

# extract the output values for buses
vehref['vehicle_ref'] = vehref['vehicle_ref'].astype('str')
bus = vehref
# bus=vehref[vehref['vehicle_ref'].apply(lambda x: len(x)>20)]
busref=bus[['vehicle_ref','vehicle_id','vehicle_actorConfig']]
busref.rename(columns={'vehicle_actorConfig' : 'actorConfig_id'},inplace = True)
# join busref and vehtype by the same column 'actorConfig_id'
businfo=pd.merge(busref, vehtype, on='actorConfig_id')

traj=motion.loc[motion.motionState_vehicle.isin(businfo.vehicle_id), ]
traj=traj[['motionState_vehicle','motionState_time','motionState_speed','motionState_acceleration']]
traj=traj.sort_values(['motionState_vehicle','motionState_time'])
traj.rename(columns={'motionState_vehicle' : 'vehicle_id','motionState_time':'time','motionState_speed':'speed',
                     'motionState_acceleration':'acceleration'},inplace = True)
# UNIT: time:milliseconds, speed:0.01m/s, acceleration:0.0001m/s^2
trajectory=pd.merge(traj, businfo, on='vehicle_id')
trajectory=trajectory.drop(['vehicle_id'],axis=1)
#group dataframe into multiple dataframe as a dict by bus name
trajectory=dict(tuple(trajectory.groupby('vehicle_ref')))

# date = '2021-08-20'
trip_asm = pd.read_csv('../Pre-processing/trip-assignments/trip-asm-{}.csv'.format(args.date))

def time_conv(x):
    h, m, s = x.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

stopO['gtfs_time'] = stopO['stopinfo_started'] - stopO['stopinfo_arrivalDelay'].apply(float)

final_stopO = pd.DataFrame()
for veh_id in stopO['stopinfo_id'].unique():
    df_stop_veh = stopO[stopO['stopinfo_id'] == veh_id]
    trip_asm_veh = trip_asm[trip_asm['vid'] == int(veh_id)]
    traj_veh = trajectory[str(veh_id)]
    for idx, row in trip_asm_veh.iterrows():
        df_stop_trip = df_stop_veh[(df_stop_veh['gtfs_time'] >= time_conv(row['gtfs_time_start'])) & 
                         (df_stop_veh['gtfs_time'] < time_conv(row['gtfs_time_end']))]
        df_stop_trip['trip_id'] = int(row['trip_id'])
        final_stopO = pd.concat([final_stopO, df_stop_trip], ignore_index=True)
        
        actual_start_time, actual_end_time = df_stop_trip['stopinfo_started'].min(), df_stop_trip['stopinfo_started'].max()
        traj_trip = traj_veh[(traj_veh['time'] >= actual_start_time*1000) & (traj_veh['time'] <= actual_end_time*1000)]
        if len(traj_trip) > 0:
            traj_trip.to_csv('./trip-level-output/trajectory_{}.csv'.format(row['trip_id']), index=None)
        
final_stopO.to_csv("./trip-level-output/busstop_info.csv",index=False)
# write final stop output 