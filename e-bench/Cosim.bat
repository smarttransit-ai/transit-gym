
start "HELICS" helics_broker -f 2 --loglevel=connections --name=mainbroker
start "GridLAB-D" gridlabd DistributionSim_B2_G_1.glm
start "Python" python federate1.py


