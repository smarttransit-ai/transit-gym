import traci
import pandas as pd
import random
import time
import pickle

sumo_cmd = ["/usr/bin/sumo"]
sumo_config = ["-c", "./Sim/network-bus.sumocfg"]
sumo_cmd.extend(sumo_config)
edge_data_by_step = pickle.load(open('filtered_edge_data.pkl', 'rb'))

INTERVAL = 60
print("START LOADING .NET.XML ==================================  ")
traci.start(sumo_cmd, label=str(random.randint(10000, 50000)))

while traci.simulation.getTime() < 86400:
    step = int(traci.simulation.getTime())
    if step % 200 == 0:
        print("Step: :", step)
    
    if step % INTERVAL == 0:
        if step in edge_data_by_step:
            for item in edge_data_by_step[step]:
                traci.edge.setMaxSpeed(item['edge_id'], item['edge_speed'])    
    traci.simulationStep()
    
traci.close()
print("FINISH !!!!!")
