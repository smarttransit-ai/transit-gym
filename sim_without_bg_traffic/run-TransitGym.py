import traci
import pandas as pd
import random
import time
import pickle
import xmltodict
import json
from collections import OrderedDict
import datetime


import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--date", type=str, default="20210820", help="date")
parser.add_argument("--sim", type=str, default="transit-sim-date", help="simulation folder")
parser.add_argument("--bgTraffic", type=str, default="combined_trips_100k_08-25_049.rou.xml", help="background traffic .rou.xml")
args = parser.parse_args()

SUMO_CMD = ["/usr/bin/sumo"]
SUMO_CONFIG_FILE = ["-c", "{}/SUMO_configuration.sumocfg".format(args.sim), 
                    "-r", "{}/routes-{}.rou.xml,{}/passenger-{}.rou.xml,{}/{}".format(args.sim, args.date, args.sim, args.date, args.sim, args.bgTraffic),
                    "-a", "{}/busStop-{}.add.xml".format(args.sim, args.date)]

USING_BACKGROUND_ELIMINATION = True

SUMO_CMD.extend(SUMO_CONFIG_FILE)

start = time.time()
print("LOADING .NET.XML ==================================  ")
traci.start(SUMO_CMD, label=str(random.randint(10000, 50000)))
# --------------------------------------------------------------

# SIMULATING :::::::::::::::::::::::::::::::::::::::::::::::::::
while traci.simulation.getTime() < 3600*24:        
    traci.simulationStep()

end = time.time()

traci.close()
print("FINISH !!!!!")
# ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::