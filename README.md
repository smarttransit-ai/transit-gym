# transit-simulator

## Procedure of transit simulation using [SUMO](https://sumo.dlr.de/docs/index.html) (Version 1.8.0)

<img src="https://github.com/hdemma/transit-simulator/blob/master/images/ChattanoogaSUMO.png" alt="alt text" width="550" height="320">

The green boxes in above chart indicate the input information.

### Step 1. Correct network
Using GUI-based tool [NETEDIT](https://sumo.dlr.de/docs/netedit.html) to check the network and add links and junctions which are missing during the conversion from OSM map to SUMO network.
* The corrected network: [Chattanooga_SUMO_Network.net.xml](https://github.com/hdemma/transit-simulator/tree/master/SUMO_simulation/Chattanooga_SUMO_Network.net.zip)

### Step 2. Find bus stops' positions on network
* Using [TraCI](https://sumo.dlr.de/docs/TraCI.html) to interact with SUMO
* Get the position info of stops (including edge ID, lane position and lane index) based on geo coordinates in [GTFS](https://github.com/smarttransit-ai/transit-energy-dashboard/blob/master/app/data/raw/GTFS/gtfs_may_2020/stops.txt).

*Note:* Due to the nature of the automatic process, there would be many stops with incorrect positions converted through TraCI. The stops might be identified on a neighbor link with an opposite direction. For example, a stop should on edge ID '-123', and the lane position is 10, but it may be identified on edge ID '123' without the '-' sign, and the lane position is 90, have 10 distance to the end of the edge. This issue will cause buses to turn around fequently on their route. So it is necessary to find out these incorrect stops and revise them to the correct edge ID and lane position in the [busstops.xlsx](https://github.com/hdemma/transit-simulator/blob/master/data/busstops.xlsx). 

The edge lists in the later route file can supply the clue to check which stop is set on a wrong position on the route. It generally takes place when there are more than two edges with the same ID numbers but at least one is with “– “sign. 

### Step 3. [Create bus stop additional xml](https://github.com/smarttransit-ai/transit-simulator/blob/master/codes/Def_BusStop_file.py)
Automatically generate codes for bus stop additional file based on stop's positions converted by TraCI.
* Stop additional xml: [busStopsCARTA.add.xml](https://github.com/hdemma/transit-simulator/blob/master/SUMO_simulation/busStopsCARTA.add.xml).
### Step 4. [Create bus trip xml](https://github.com/smarttransit-ai/transit-simulator/blob/master/codes/Create_BusTrip_newfile.py)
Automatically generate codes for bus trip file based on sequential bus stops along each trip in [Comprehensive_GTFS.xlsx](https://github.com/smarttransit-ai/transit-simulator/blob/master/data/Comprehensive_GTFS.xlsx) with correspongding position information.
*Note:* Comprehensive_GTFS.xlsx is [generated](https://github.com/smarttransit-ai/transit-simulator/blob/master/codes/Match_GTFS.py) from the [GTFS](https://github.com/smarttransit-ai/transit-energy-dashboard/tree/master/app/data/raw/GTFS/gtfs_may_2020) data.
* Bus trip xml: [BusLines.trips.xml](https://github.com/hdemma/transit-simulator/blob/master/SUMO_simulation/BusLines.trips.xml).

### Step 5. Genarate person trips xml
Use a SUMO tool [od2trips](https://sumo.dlr.de/docs/Demand/Importing_O/D_Matrices.html) to generate the person trips by incorporating [transportation demand (in O format)](https://github.com/smarttransit-ai/transit-simulator/blob/master/SUMO_simulation/OD_person.od) and [taz.xml](https://github.com/smarttransit-ai/transit-simulator/blob/master/SUMO_simulation/taz.xml). The command is shown as below.
```
od2trips -d OD_person.od --taz-files taz.xml --prefix person --persontrips --persontrips.modes public -o Person_trips.xml
```

### Step 6. [Create vehicle type additional xml](https://github.com/smarttransit-ai/transit-simulator/blob/master/codes/Def_vehType_file.py)
Automatically generate codes for bus trip file based on vehicel.xlsx. Here use a [sample](https://github.com/smarttransit-ai/transit-simulator/blob/master/data/BUS_type.xlsx) data.
* Vehicle type additional xml: [vehtype.add.xml](https://github.com/smarttransit-ai/transit-simulator/blob/master/SUMO_simulation/vehtype.add.xml).

### Step 7. Generate route file for bus and person
Use the tool [duarouter](https://sumo.dlr.de/docs/duarouter.html) to generate the route xml file for bus and person which includes detailed edge list for each bus route and detail public transit plan for persons.
```
duarouter --route-files BusLines.trips.xml,person_trips.xml --net-file Chattanooga_SUMO_Network.net.xml --unsorted-input 
--additional-files busStopsCARTA.add.xml,vehtype.add.xml --ptline-routing --output-file busPerson.rou.xml --ignore-errors
```
* The route file for bus and person: [busPerson.rou.xml](https://github.com/hdemma/transit-simulator/blob/master/SUMO_simulation/busPerson.rou.xml).

### Step 7. Define edge-based dump additional xml
Based on revised bus stop position file, recreate stop additional file and bus trip file. 

### Step 8. Configure and run simulation
Set up the configuration file: [newChatt_addBUS.sumocfg](https://github.com/hdemma/transit-simulator/blob/master/SUMO_simulation/newChatt_addBUS.sumocfg).

*Note:* [Chattanooga_Daily_Trips.rou.xml](https://vanderbilt365.sharepoint.com/sites/TransitHub/Shared%20Documents/simulation/SUMO_simulation) is in Teams
