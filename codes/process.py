import dask.dataframe as dd
import pandas as pd
## trajectory for all vehicles during the simulation time interval
motion = dd.read_csv("trajectories_outputmotionState.csv",sep=';',low_memory=False)
print("motion file imported. length",motion.shape[0])
vehtype = pd.read_csv("trajectories_outputactorConfig.csv",sep=';')
print('actor config imported. lenthi', vehtype.shape[0])
vehref = pd.read_csv("trajectories_outputvehicle.csv",sep=';')
print('vehref imported. length', vehref.shape[0])
# extract the output values for buses
vehref['vehicle_ref'] = vehref['vehicle_ref'].astype('str')
bus=vehref[vehref['vehicle_ref'].apply(lambda x: len(x)>20)]
busref=bus[['vehicle_ref','vehicle_id','vehicle_actorConfig']]
busref= busref.rename(columns={'vehicle_actorConfig' : 'actorConfig_id'})
print('busref',busref.shape[0])
# join busref and vehtype by the same column 'actorConfig_id'
businfo=pd.merge(busref, vehtype, on='actorConfig_id')
traj=motion.loc[motion.motionState_vehicle.isin(businfo.vehicle_id) ]
traj=traj[['motionState_vehicle','motionState_time','motionState_speed','motionState_acceleration']]
# traj=traj.sort_values(['motionState_vehicle','motionState_time'])
traj=traj.rename(columns={'motionState_vehicle' : 'vehicle_id','motionState_time':'time','motionState_speed':'speed',
                     'motionState_acceleration':'acceleration'})
print('traj',traj.shape[0])
# UNIT: time:milliseconds, speed:0.01m/s, acceleration:0.0001m/s^2
trajectory=dd.merge(traj, businfo, on='vehicle_id')
trajectory=trajectory.drop(['vehicle_id'],axis=1)
print(trajectory.columns)
def write_file(grp):
    pc = grp["vehicle_ref"].unique()[0]
    pc = pc.replace(':','')
    grp.to_csv(f"./outtest/"+ 'Trajectory_' + pc + ".csv",
                    header=False,
                    index=False)
    return None


trajectory.groupby('vehicle_ref').apply(write_file, meta=('x', 'f8')).compute()
#group dataframe into multiple dataframe as a dict by bus name
#trajectory=dict(tuple(trajectory.groupby('vehicle_ref')))
#write in csv files, bus trip name as the file name
#for key, df in trajectory.items():
#    bus=key.replace(':','')
#    with open('./outtest/' + 'Trajectory_' + bus + '.csv', 'w', newline='') as oFile:
#        df.to_csv(oFile, index = False)
#    print("Finished writing: " + 'Trajectory_' + bus)

