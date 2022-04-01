# Background traffic elimination

## Steps:

1. Download [filtered-edge-data.pkl](https://drive.google.com/file/d/1uF-SDjassfoRxPayVo2iggGGhNH3DPJf/view?usp=sharing) and put into folder *background_traffic_elimination*

2. Add transit_run folder to background_traffic_elimination folder (change bus_withPerson.xml for new gtfs)
   a. You can change the simulation endtime by changing the value in line 16 in run-sim-with-background-traffic-elimination.py ```while traci.simulation.getTime() < <max duration>:```
   b. SImulation time can also be changed from the .sumocfg file
   
3. Copy the following files from background_traffic_elimination folder to manual_files/codes/:
	1. busstop_output.xml ```cp ./transit_run/busstop_output.xml ../manual_files/codes/```
	2. EdgeData.xml ```cp ./transit_run/EdgeData.xml ../manual_files/codes/```
	3. trajectories_output.xml ```cp ./transit_run/trajectories_output.xml ../manual_files/codes/```

4. Generate csv from xml for all the above files:
	```
   python3 /usr/share/sumo/tools/xml/xml2csv.py EdgeData.xml
	python3 /usr/share/sumo/tools/xml/xml2csv.py busstop_output.xml
	python3 /usr/share/sumo/tools/xml/xml2csv.py trajectories_output.xml -p
   ```
5. Change the first line of EdgeData.csv (to accomodate all the parameters - the default first line may not have all of them):
	In the terminal, type:
	```
   sed -i '48 i \\t \t<edge id="-78766" sampledSeconds="9.79" traveltime="9.24" overlapTraveltime="9.79" density="0.24" laneDensity="0.12" occupancy="0.09" waitingTime="0.00" timeLoss="0.15" speed="14.49" speedRelative="1.04" departed="0" arrived="0" entered="1" left="1" laneChangedFrom="0" laneChangedTo="0"/>' EdgeData.xml
   ```
6. Create output folder ```mkdir output```

7. Run the outputRocess.py file - .csv files for all the trajectories are stored in output folder

   ```python outputProcess.py ```
	

<!-- 1. Run "log-edge-data-in-normal-simulation.ipynb"
2. Run "log-bus-data-in-normal-simultion.ipynb"
3. Run "remove-background-traffic-and-log-bus-data"

Or download some available outputs at https://drive.google.com/file/d/1Kd-Xgml1kRq8CaaIIsMrqtFy_bsU9DgN/view?usp=sharing

## Visualization:
* bus-speed-visualization.ipynb
* 3d-trajectory-visualization.ipynb -->
