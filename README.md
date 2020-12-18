# transit-simulator

## Procedure of transit simulation using [SUMO](https://sumo.dlr.de/docs/index.html)

<img src="https://github.com/hdemma/transit-simulator/blob/master/images/ChattanoogaSUMO.png" alt="alt text" width="550" height="320">

*Note:* The green boxes in the above diagram indicate the input information.

### Step 1. Correct network
Using GUI-based tool [NETEDIT](https://sumo.dlr.de/docs/netedit.html) to check the network and add links and junctions which are missing during the conversion from OSM map to SUMO network.
* The corrected network: [Chattanooga_SUMO_Network.net.xml](https://github.com/hdemma/transit-simulator/tree/master/SUMO_simulation/Chattanooga_SUMO_Network.net.zip)

### Step 2. Find bus stops' positions on network 
* Using [TraCI](https://sumo.dlr.de/docs/TraCI.html) to interact with SUMO ([convertGeo.py](https://github.com/smarttransit-ai/transit-simulator/blob/master/codes/convertGeo.py)).
* Get the position info of stops (including edge ID, lane position and lane index) based on geo coordinates in [GTFS](https://github.com/smarttransit-ai/transit-energy-dashboard/blob/master/app/data/raw/GTFS/gtfs_may_2020/stops.txt).

*Note:* Due to the nature of the automatic process, there would be many stops with incorrect positions converted through TraCI. The stops might be identified on a neighbor link with an opposite direction. For example, a stop should on edge ID '-123', and the lane position is 10, but it may be identified on edge ID '123' without the '-' sign, and the lane position is 90, have 10 distance to the end of the edge. This issue will cause buses to turn around fequently on their route. So it is necessary to find out these incorrect stops and revise them to the correct edge ID and lane position in the [busstops.xlsx](https://github.com/hdemma/transit-simulator/blob/master/data/busstops.xlsx). 

The edge lists in the later route file can supply the clue to check which stop is set on a wrong position on the route. It generally takes place when there are more than two edges with the same ID numbers but at least one is with “– “sign. 

### Step 3. Create bus stop additional xml
Automatically generate codes for bus stop additional file based on stop's positions converted by TraCI ([Def_BusStop_file.py](https://github.com/smarttransit-ai/transit-simulator/blob/master/codes/Def_BusStop_file.py)).
* Stop additional xml: [busStopsCARTA.add.xml](https://github.com/hdemma/transit-simulator/blob/master/SUMO_simulation/busStopsCARTA.add.xml).
### Step 4. Create bus trip xml
Automatically generate codes for bus trip file based on sequential bus stops along each trip in [Comprehensive_GTFS.xlsx](https://github.com/smarttransit-ai/transit-simulator/blob/master/data/Comprehensive_GTFS.xlsx) with correspongding position information ([Create_BusTrip_newfile.py](https://github.com/smarttransit-ai/transit-simulator/blob/master/codes/Create_BusTrip_newfile.py))
*Note:* Comprehensive_GTFS.xlsx is generated ([Match_GTFS.py](https://github.com/smarttransit-ai/transit-simulator/blob/master/codes/Match_GTFS.py)) from the [GTFS](https://github.com/smarttransit-ai/transit-energy-dashboard/tree/master/app/data/raw/GTFS/gtfs_may_2020) data.
* Bus trip xml: [BusLines.trips.xml](https://github.com/hdemma/transit-simulator/blob/master/SUMO_simulation/BusLines.trips.xml).

### Step 5. Genarate person trips xml
Use a SUMO tool [od2trips](https://sumo.dlr.de/docs/Demand/Importing_O/D_Matrices.html) to generate the person trips by incorporating [transportation demand (in O format)](https://github.com/smarttransit-ai/transit-simulator/blob/master/SUMO_simulation/OD_person.od) and [taz.xml](https://github.com/smarttransit-ai/transit-simulator/blob/master/SUMO_simulation/taz.xml). The command is shown as below.
```
od2trips -d OD_person.od --taz-files taz.xml --prefix person --persontrips --persontrips.modes public -o Person_trips.xml
```
**Option:**\
-d <FILE> (--od-matrix-files <FILE>)	Loads O/D-files from FILE(s)\
--taz-files <FILE>	Loads TAZ (districts; also from networks) from FILE(s)\
--prefix <STRING>	Defines the prefix for vehicle/person names\
--persontrips <BOOL>	Writes persontrips instead of vehicles; default: false\
--persontrips.modes	Add modes attribute to personTrips\
-o <FILE> (--output-file <FILE>)	Writes trip definitions into FILE

### Step 6. Create vehicle type additional xml
Automatically generate codes for bus trip file based on vehicel.xlsx. Here use a [sample](https://github.com/smarttransit-ai/transit-simulator/blob/master/data/BUS_type.xlsx) data ([Def_vehType_file.py](https://github.com/smarttransit-ai/transit-simulator/blob/master/codes/Def_vehType_file.py)).
* Vehicle type additional xml: [vehtype.add.xml](https://github.com/smarttransit-ai/transit-simulator/blob/master/SUMO_simulation/vehtype.add.xml).

### Step 7. Generate route file for bus and person
Use the tool [duarouter](https://sumo.dlr.de/docs/duarouter.html) to generate the route xml file for bus and person which includes detailed edge list for each bus route and detailed public transit plan for persons.
```
duarouter --route-files BusLines.trips.xml,person_trips.xml --net-file Chattanooga_SUMO_Network.net.xml --unsorted-input 
--additional-files busStopsCARTA.add.xml,vehtype.add.xml --ptline-routing --output-file busPerson.rou.xml --ignore-errors
```
**Option:**\
--route-files <FILE>	Read sumo routes, alternatives, flows, and trips from FILE(s)\
--net-file <FILE>	Use FILE as SUMO-network to route on\
--unsorted-input <BOOL>	Assume input is unsorted; default: false\
--ptline-routing <BOOL>	Route all public transport input; default: false\
--output-file <FILE>	Write generated routes to FILE\
--ignore-errors <BOOL>	Continue if a route could not be build; default: false
  
* The generated route file for bus and person: [busPerson.rou.xml](https://github.com/hdemma/transit-simulator/blob/master/SUMO_simulation/busPerson.rou.xml).

### Step 7. Define edge-based dump additional xml
To get the edge-based output, a [edge-based state dump](https://sumo.dlr.de/docs/Simulation/Output/Lane-_or_Edge-based_Traffic_Measures.html) is defined within an additional-file added to the sumo config as following:
```
<additional>
  <edgeData id="<MEASUREMENT_ID>" freq="<FREQUENCY>" file="<OUTPUT_FILE>" />
</additional>
```
Values within this output describe the situation within the network in terms of traffic by giving macroscopic values such as the mean vehicle speed, the mean density(#veh/km), the mean occupancy(%) of edge/lane. For lane-based dump, replace edgeData to laneData.

*Note:* An attribute named *freq* describes the aggregation period the values the detector collects shall be summed up. For example *freq="3600"* can be added in the above defination to get a aggregation output values in one hour.

### Step 8. Configure and run simulation
Set up the configuration file with output parameters: [newChatt_addBUS_wMEANoutput.sumocfg](https://github.com/hdemma/transit-simulator/blob/master/SUMO_simulation/newChatt_addBUS_wMEANoutput.sumocfg).
This configuration will generate three output files:
* Edge-based output mentioned in step 7.
* Bus stop output. This output contains the information about each vehicle's scheduled <stop>: time of arrival and departure, stopping place and number of persons that were loaded and unloaded. The information is generated every time a stop ends.
* Full output which contains informtation about every edge, lane, vehicle and traffic light for each time step

*Note:* [Chattanooga_Daily_Trips.rou.xml](https://vanderbilt365.sharepoint.com/sites/TransitHub/Shared%20Documents/simulation/SUMO_simulation) is in Teams

**Click the above blue highlight texts for more information.**

### Environment
SUMO 1.8.0

Python 3.8

