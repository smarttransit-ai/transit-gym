# Simulation with VehID concept
Default directory structure
```
sim_with_vehId_concept
│   generate-bus-route-file.py
│   run-with-vehID-concept.py
|   trips_vid_n_timebyGTFS_20220111.csv
|   filtered_edge_data.pkl
└───transit_run
│   │   busWithPerson.rou.xml
│   │   ...
```




# Background traffic elimination

## Steps:

1. Download [filtered-edge-data.pkl](https://drive.google.com/file/d/1uF-SDjassfoRxPayVo2iggGGhNH3DPJf/view?usp=sharing) and put into folder *background_traffic_elimination*
```
$ cd background_traffic_elimination
$ wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1uF-SDjassfoRxPayVo2iggGGhNH3DPJf' -O- | sed -rn 's/.*c
onfirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1uF-SDjassfoRxPayVo2iggGGhNH3DPJf" -O filte
red_edge_data.pkl && rm -rf /tmp/cookies.txt
```

2. Add transit_run folder here  (change **bus_withPerson.xml** for new gtfs)<br>

 Download transit_run.zip and extract it ( https://drive.google.com/file/d/1J8EN538uXquD76HHwHmT8AWNHc2ERG3z/view?usp=sharing ) 
 
   a. You can change the simulation endtime by changing the value in **line 16** in run-sim-with-background-traffic-elimination.py <br>
    "while traci.simulation.getTime() < (max duration): "<br>
   b. Simulation time can also be changed from the .sumocfg file
   
3. Generate bus_routes_only.rou.xml
Note that: *BUS_WITH_PERSON_FILE* and *OUTPUT_BUS_ROUTE_FILE* can be edited
> python3 generate-bus-route-file.py

4. Edit sumo configuration file 

Edit Line 7 of *transit_run/Chattanooga_SUMO.sumocfg* to
```
<route-files value="bus_routes_only.rou.xml"/>
```

5. Simulation
> python3 run-with-vehID-concept.py 



6. After the simulation is complete, copy the following files from /background_traffic_elimination to /manual_files/codes/:
	1. busstop_output.xml   ```cp ./transit_run/busstop_output.xml ../manual_files/codes/```
	2. EdgeData.xml   ```cp ./transit_run/EdgeData.xml ../manual_files/codes/```
	3. trajectories_output.xml   ```cp ./transit_run/trajectories_output.xml ../manual_files/codes/```

7. Change the first line of EdgeData.csv (to accomodate all the parameters - the default first line may not have all of them).<br>
	In the terminal, type:
```
$ sed -i '48 i \\t \t<edge id="0" sampledSeconds="0" traveltime="0" overlapTraveltime="0" density="0" laneDensity="0" occupancy="0" waitingTime="0" timeLoss="0" speed="0" speedRelative="0" departed="0" arrived="0" entered="0" left="0" laneChangedFrom="0" laneChangedTo="0"/>' EdgeData.xml
   ```
8. Generate csv from xml for all the above files:
	```
   	$ python /usr/share/sumo/tools/xml/xml2csv.py EdgeData.xml
	$ python /usr/share/sumo/tools/xml/xml2csv.py busstop_output.xml
	$ python /usr/share/sumo/tools/xml/xml2csv.py trajectories_output.xml -p
   ``` 
9. Create 'output' folder  ```mkdir output```

10. Run the outputRocess.py file - 
```
$ python outputProcess.py 
```
	

<br>
The required .csv files for all the trajectories are stored in /output folder


<!-- 1. Run "log-edge-data-in-normal-simulation.ipynb"
2. Run "log-bus-data-in-normal-simultion.ipynb"
3. Run "remove-background-traffic-and-log-bus-data"

Or download some available outputs at https://drive.google.com/file/d/1Kd-Xgml1kRq8CaaIIsMrqtFy_bsU9DgN/view?usp=sharing

## Visualization:
* bus-speed-visualization.ipynb
* 3d-trajectory-visualization.ipynb -->
