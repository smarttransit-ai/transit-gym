#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 18:29:04 2021

@author: danielgui
"""
import pandas as pd
import numpy as np
import xml2csv
class Output_Processor:
    def __init__(self):
        pass
    
    def generate(self, result_path):
        

        ## convert xml to csv
        xml2csv.main(result_path + 'EdgeData.xml')
        xml2csv.main(result_path + 'busstop_output.xml')
        xml2csv.main(result_path + 'trajectories_output.xml -p')
        # -p is used to split the output files based on the first level
        
        ## bus stop output containing delay and person load information
        stopO = pd.read_csv(result_path + "busstop_output.csv",sep=';')
        stopO=stopO[["stopinfo_id","stopinfo_busStop","stopinfo_started","stopinfo_arrivalDelay",
                     "stopinfo_ended","stopinfo_delay","stopinfo_initialPersons",
                     "stopinfo_loadedPersons","stopinfo_unloadedPersons",
                     "stopinfo_lane","stopinfo_pos","stopinfo_parking"]]
        stopO=stopO.sort_values(["stopinfo_id","stopinfo_started"])
        # write final stop output 
        stopO.to_csv(result_path + "output/busstop_info.csv",index=False)
        
        
        ## edge based output with mean speed for each hour(3600s)
        edgeO = pd.read_csv(result_path + "EdgeData.csv",sep=';')
        edgeO=edgeO[["interval_begin","interval_end","edge_id","edge_speed",
                     "edge_density","edge_laneDensity","edge_left",
                     "edge_occupancy","edge_traveltime",
                     "edge_waitingTime","edge_entered"]]
        # UNIT: "edge_speed":m/s, "edge_density":#veh/km, "edge_occupancy":%
        edgeO.to_csv(result_path + "output/edge_info.csv",index=False)
        
        
        ## trajectory for all vehicles during the simulation time interval
        motion = pd.read_csv(result_path + "trajectories_outputmotionState.csv",sep=';',low_memory=False)
        vehtype = pd.read_csv(result_path + "trajectories_outputactorConfig.csv",sep=';')
        vehref = pd.read_csv(result_path + "trajectories_outputvehicle.csv",sep=';')
        
        # extract the output values for buses
        vehref['vehicle_ref'] = vehref['vehicle_ref'].astype('str')
        bus=vehref[vehref['vehicle_ref'].apply(lambda x: len(x)>20)]
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
        #write in csv files, bus trip name as the file name
        for key, df in trajectory.items():
            bus=key.replace(':','')
            with open(result_path + 'output/' + 'Trajectory_' + bus + '.csv', 'w', newline='') as oFile:
                df.to_csv(oFile, index = False)
            print("Finished writing: " + 'Trajectory_' + bus)
                