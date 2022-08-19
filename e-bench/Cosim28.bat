
start "HELICS" helics_broker -f 2 --loglevel=3 --name=mainbroker
start "GridLAB-D" gridlabd DistributionSim_B2_G_1.glm
start "PSS/E" python federate1.py


