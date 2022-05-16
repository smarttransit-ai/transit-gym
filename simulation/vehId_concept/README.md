# Simulation with VehID concept
Default directory structure
```
sim_with_vehId_concept
└───preprocessing
│   |   generate-bus-route-file.py
│   run-with-vehID-concept.py
|   trips_vid_n_timebyGTFS_20220111.csv
|   filtered_edge_data.pkl
└───transit_run
│   │   busWithPerson.rou.xml
│   │   ...
```

#### Step 1: Generate bus_routes_only.rou.xml
Note that: *BUS_WITH_PERSON_FILE* and *OUTPUT_BUS_ROUTE_FILE* can be edited
> python3 generate-bus-route-file.py

#### Step 2: Edit sumo configuration file 

Edit Line 7 of *transit_run/Chattanooga_..sumocfg* to
```
<route-files value="bus_routes_only.rou.xml"/>
```

#### Step 3: Simulation
> python3 run-with-vehID-concept.py 
