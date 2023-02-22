import pandas as pd
import plotly.express as px
import traci
import random
import copy
import math
from itertools import groupby
import os
import pickle
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--date", type=str, default="20210820", help="date")
parser.add_argument("--sim", type=str, default="transit-sim-date", help="simulation folder")
parser.add_argument("--bgTraffic", type=str, default="combined_trips_100k_08-25_049.rou.xml", help="background traffic .rou.xml")
args = parser.parse_args()

SUMO_CMD = ["/usr/bin/sumo"]
SUMO_CONFIG_FILE = ["-c", "../{}/SUMO_configuration.sumocfg".format(args.sim), 
                    "-r", "../{}/routes-{}.rou.xml,{}/passenger-{}.rou.xml,{}/{}".format(args.sim, args.date, args.sim, args.date, args.sim, args.bgTraffic),
                    "-a", "../{}/busStop-{}.add.xml".format(args.sim, args.date)]

INTERVAL = 60

speed_obj = {}
while traci.simulation.getTime() < 3600*24:
    step = int(traci.simulation.getTime())
    # logged background traffic ------------------------------------------------                
    if (step % INTERVAL == 0):
        speed_obj[step] = {}
        for edge_id in traci.edge.getIDList():
            speed_obj[step][edge_id] = traci.edge.getLastStepMeanSpeed(edge_id)
    traci.simulationStep()
    # -------------------------------------------------------------------------
    if step % 600 == 0:
        print(step)
        
tmp_obj = {}
edge_data = {}
for step in speed_obj:
    if step not in edge_data:
        edge_data[step] = []
    for eid, espeed in speed_obj[step].items():
        if espeed < 1:
            continue
        if eid in tmp_obj:
            if espeed == tmp_obj[eid]:
                continue
        edge_data[step].append((eid, espeed))
        tmp_obj[eid] = espeed
        
pickle.dump(edge_data, open('./edge_speed_by_sim.pkl', 'wb'))
