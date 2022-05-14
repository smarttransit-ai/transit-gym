## Steps:

1. Download [filtered-edge-data.pkl](https://drive.google.com/file/d/1uF-SDjassfoRxPayVo2iggGGhNH3DPJf/view?usp=sharing) and put into folder *background_traffic_elimination*
```
$ cd background_traffic_elimination
$ wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1uF-SDjassfoRxPayVo2iggGGhNH3DPJf' -O- | sed -rn 's/.*c
onfirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1uF-SDjassfoRxPayVo2iggGGhNH3DPJf" -O filte
red_edge_data.pkl && rm -rf /tmp/cookies.txt
```

2. Download Chattanooga_SUMO_Network.net.xml and put into folder transit_run

<!-- 2. Add transit_run folder to /background_traffic_elimination  (change **bus_withPerson.xml** for new gtfs)<br>

```
$ wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1TDb9rhMw7DU5aU0keUPkA7Jf05UoRSKN' -O- | sed -rn 's/.*c
onfirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1TDb9rhMw7DU5aU0keUPkA7Jf05UoRSKN" -O trans
it_run.zip && rm -rf /tmp/cookies.txt
```
 -->
<!-- 3. Modify the route file
```
python ./vehId_concept/preprocessing/generate-bus-route-file.py
```
Then, make sure that the sumocfg file is using ```<route-files value="bus_routes_only.rou.xml"/>``` (line 6)
 -->
 
3. Run main.py
   &emsp; a. You can change the simulation endtime by changing the value in **line 6** in main.py 
    &emsp; &emsp; "END_TIMESTEP = 3600*24 "
   &emsp; b. Simulation time can also be changed from the .sumocfg file
```
$ python main.py
```

4. After the simulation is complete, copy the following files from /transit_run to /manual_files/codes/:
	1. busstop_output.xml   ```cp ./transit_run/busstop_output.xml ../manual_files/codes/```
	2. EdgeData.xml   ```cp ./transit_run/EdgeData.xml ../manual_files/codes/```
	3. trajectories_output.xml   ```cp ./transit_run/trajectories_output.xml ../manual_files/codes/```

6. Change the first line of EdgeData.csv (to accomodate all the parameters - the default first line may not have all of them).<br>
	In the terminal, type:
```
$ sed -i '48 i \\t \t<edge id="0" sampledSeconds="0" traveltime="0" overlapTraveltime="0" density="0" laneDensity="0" occupancy="0" waitingTime="0" timeLoss="0" speed="0" speedRelative="0" departed="0" arrived="0" entered="0" left="0" laneChangedFrom="0" laneChangedTo="0"/>' EdgeData.xml
   ```
7. Generate csv from xml for all the above files:
	```
   	$ python /usr/share/sumo/tools/xml/xml2csv.py EdgeData.xml
	$ python /usr/share/sumo/tools/xml/xml2csv.py busstop_output.xml
	$ python /usr/share/sumo/tools/xml/xml2csv.py trajectories_output.xml -p
   ``` 
8. temporary fix : replace 'trajectories_output.csvactorConfig.csv' with [https://drive.google.com/file/d/1d82N7x5gRQsgwuw3c5PmwK5ZnBsAsDx5/view?usp=sharing] 

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
