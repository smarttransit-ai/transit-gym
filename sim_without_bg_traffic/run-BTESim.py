import traci
import random
import time
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--date", type=str, default="20210820", help="date")
parser.add_argument("--sim", type=str, default="transit-sim-date", help="simulation folder")
parser.add_argument("--BTE_data", type=str, default="BTE/edge_speed_by_sim.pkl", help="BTE data")
args = parser.parse_args()

SUMO_CMD = ["/usr/bin/sumo"]
SUMO_CONFIG_FILE = ["-c", "{}/SUMO_configuration.sumocfg".format(args.sim), 
                    "-r", "{}/routes-{}.rou.xml,{}/passenger-{}.rou.xml".format(args.sim, args.date, args.sim, args.date),
                    "-a", "{}/busStop-{}.add.xml".format(args.sim, args.date)]

USING_BACKGROUND_ELIMINATION = True

SUMO_CMD.extend(SUMO_CONFIG_FILE)

if USING_BACKGROUND_ELIMINATION:
    print("LOADING EDGE DATA ==================================  ")
    edge_data_by_step = pickle.load(open(args.BTE_data, 'rb'))
INTERVAL = 60

start = time.time()
print("LOADING .NET.XML ==================================  ")
traci.start(SUMO_CMD, label=str(random.randint(10000, 50000)))
# --------------------------------------------------------------

# SIMULATING :::::::::::::::::::::::::::::::::::::::::::::::::::
while traci.simulation.getTime() < 3600*24:
    step = int(traci.simulation.getTime())
        
    # mimic background traffic ------------------------------------------------                
    if (USING_BACKGROUND_ELIMINATION & (step % INTERVAL == 0)):
        if step in edge_data_by_step:
            for item in edge_data_by_step[step]:
                traci.edge.setMaxSpeed(item[0], item[1] + 5)
    traci.simulationStep()
    # -------------------------------------------------------------------------
#     if step % 200 == 0:
#         print(step)

end = time.time()

traci.close()
print("FINISH !!!!!")
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::