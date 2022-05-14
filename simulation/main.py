import random
import traci
from background_traffic_elimination.BTE import BTE
from vehId_concept.BusGenerator import BusGenerator

END_TIMESTEP = 3600*24
USING_BACKGROUND_ELIMINATION = False
SUMO_CMD = ["/usr/bin/sumo", "-c", "./transit_run/Chattanooga_v21.sumocfg"]

traci.start(SUMO_CMD, label=str(random.randint(10000, 50000)))

bus_generator = BusGenerator(traci)
if USING_BACKGROUND_ELIMINATION:
    bte = BTE(traci)

step = 0
while step < END_TIMESTEP:
    step = int(traci.simulation.getTime())
    bus_generator.update()
    if USING_BACKGROUND_ELIMINATION:
        bte.update()
    traci.simulationStep()    
    if step % 200 == 0:
        print(step)