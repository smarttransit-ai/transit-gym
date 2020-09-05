# transit-simulator

## Procedure of transit simulation using [SUMO](https://sumo.dlr.de/docs/index.html)

<img src="https://github.com/hdemma/transit-simulator/blob/master/images/Procedure.png" alt="alt text" width="490" height="400">

The yellow boxes in above chart is the existing information at the begining.

### Step 1. Correct network
Using GUI-based tool [NETEDIT](https://sumo.dlr.de/docs/netedit.html) to check the network and add links and junctions which are missing during the conversion from OSM map to SUMO network.
* The corrected network: [Chattanooga_SUMO_Network.net.xml](https://github.com/hdemma/transit-simulator/tree/master/SUMO_simulation/Chattanooga_SUMO_Network.net.zip)

### Step 2. Find bus stops' positions on network
* Using [TraCI](https://sumo.dlr.de/docs/TraCI.html) to interact with SUMO
* Get the position info of stops (including edge ID, lane position and lane index) based on geo coordinates in [CARTA Summary Data](https://github.com/hdemma/transit-simulator/blob/master/data/CARTA%20Summary%20Route%20Data_Remix%20Feb%20Schedule.xlsx).

### Step 3. Create bus stop additional file
Automatically generate codes for bus stop additional file based on stop's positions converted by TraCI.

### Step 4. Create bus trip file
Automatically generate codes for bus trip file based on [sequential bus stops along each bus route](https://github.com/hdemma/transit-simulator/blob/master/data/buslines.xlsx) with correspongding position information.

### Step 5. Generate bus route file
Generate the bus route file which includes detailed edge list for each bus route computed by [duarouter](https://sumo.dlr.de/docs/duarouter.html).
```
duarouter --route-files BusLines.trips.xml --net-file Chattanooga_SUMO_Network.net.xml 
--additional-files busStopsCARTA.add.xml,vehtype.add.xml --output-file Bus.rou.xml
```
*Note:* The vehicle type 'bus' needs to be predefined in [the vehicle type additional file](https://github.com/hdemma/transit-simulator/blob/master/SUMO_simulation/vehtype.add.xml) or added in bus trip file before running the above command.

### Step 6. Correct bus stops' positions
As shown in above flow chart, check if all the stops are converted correctly by TraCI. If yes, go on to the next step, importing route file into the simulation or import bus trip file directly file into the simulation as an alternative. Both ways can run the simulation successfully and get the same result. If no, return to correct the bus stops' position information.

Due to the nature of the automatic process, there would be many stops with incorrect positions converted through TraCI. The stops might be identified on a neighbor link with an opposite direction. For example, a stop should on edge ID '-123', and the lane position is 10, but it may be identified on edge ID '123' without the '-' sign, and the lane position is 90, have 10 distance to the end of the edge. This issue will cause buses to turn around fequently on their route. So it is necessary to find out these incorrect stops and revise them to the correct edge ID and lane position in the [stops position info file](https://github.com/hdemma/transit-simulator/blob/master/data/stopsinf_CARTA.xlsx).

The edge lists in route file generated in **Step 5** can supply the clue to check which stop is set on a wrong position on the route. It takes place when there are more than two edges with the same ID numbers but at least one is with “– “sign. 

### Step 7. Regenerate route file
Based on revised bus stop position file, recreate stop additional file and bus trip file. And then get the bus route file in the same way shown in **Step 5**.
* Stop additional file: [busStopsCARTA.add.xml](https://github.com/hdemma/transit-simulator/blob/master/SUMO_simulation/busStopsCARTA.add.xml).
* Bus trip file: [BusLines.trips.xml](https://github.com/hdemma/transit-simulator/blob/master/SUMO_simulation/BusLines.trips.xml).
* Bus route file: [Bus.rou.xml](https://github.com/hdemma/transit-simulator/blob/master/SUMO_simulation/Bus.rou.xml).

### Step 8. Configure and run simulation
Set up the configuration file: [newChatt_addBUS.sumocfg](https://github.com/hdemma/transit-simulator/blob/master/SUMO_simulation/newChatt_addBUS.sumocfg).
