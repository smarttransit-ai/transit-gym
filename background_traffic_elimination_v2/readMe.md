# 0. Unzip the SUMO network file

```bat
$ unzip transit-sim-date/Chattanooga_SUMO_Network.net.xml.zip
```

# 1. Generate trip-assignment files

File: Pre-processing/generate-trip-assignment.py

Inputs:

- GTFS
- APC
- date

Command:

```bat
$ cd Pre-processing
$ python generate-trip-assignment.py --GTFS ../GTFS/20210815 --APC ../APC/202108.parquet --date 20210820
```

Output:

- Pre-processing/trip-assignments/trip-asm-20210820.csv

# 2. Generate bus route files

File: generate-route.py

Inputs:

- GTFS
- date
- simulation folder

Command:

```bat
$ python generate-route.py --GTFS GTFS/20210815 --date 20210820 --sim transit-sim-date
```

Outputs:

- transit-sim-date/routes-20210820.rou.xml
- transit-sim-date/busStop-20210820.add.xml

# 3. Generate transit demand file

We will use the duarouter feature, which is packaged with SUMO.

$ cd transit-sim-date

```bat
$ duarouter --route-files routes-**{DATE}**.rou.xml,Person_trips.xml --net-file Chattanooga_SUMO_Network.net.xml --unsorted-input --additional-files busStop-**{DATE}**.add.xml,parking.add.xml  --output-file passenger-**{DATE}**.rou.xml --ignore-errors
```

Example:

```bat
$ duarouter --route-files routes-20210820.rou.xml,Person_trips.xml --net-file Chattanooga_SUMO_Network.net.xml --unsorted-input --additional-files busStop-20210820.add.xml,parking.add.xml  --output-file passenger-20210820.rou.xml --ignore-errors
```

Outputs:

- transit-sim-date/passenger-20210820.rou.xml

# 4. Run simulation with BTE

## 4.1 Mode 1 -- simulation with background traffic

File: run-TransitGym.py

Inputs:

- date
- simulation folder
- background traffic

Command:

```bat
$ python run-TransitGym.py --date 20210820 --sim transit-sim-date --bgTraffic combined_trips_100k_08-25_049.rou.xml
```

Outputs:

- transit-sim-date/busstop_output.xml
- transit-sim-date/trajectory_output.xml

## 4.2 Mode 2 -- simulation with BTE

File: run-BTESim.py now

Inputs:

- date
- simulation folder
- background traffic

Command:

```bat
$ python run-BTESim.py --date 20210820 --sim transit-sim-date --BTE_data BTE/edge_speed_by_sim.pkl
```

Outputs:

- transit-sim-date/busstop_output.xml
- transit-sim-date/trajectory_output.xml

# 5. Postprocessing - from block-level to trip level

File: Post-processing/outputProcess.py

Inputs:

- date

Command:

```bat
$ python Post-processing/outputProcess.py --date 2021-08-20
```

Outputs

- Post-processing/trip-level-output/busstop_info.csv
- Post-processing/trip-level-output/trajectory-{trip_id}.csv

These outputs contain the trip level information of each simulated trip, during the given time period.
