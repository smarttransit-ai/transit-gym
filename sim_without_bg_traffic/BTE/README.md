# Instructions for generating edge speed data

## Approach 1. Using simulation with background traffic

File: edge_speed_by_sim.py

Inputs:
- date
- simulation folder
- background traffic

Command:
```
$ python edge_speed_by_sim.py --date 20210820 --sim transit-sim-date --bgTraffic combined_trips_100k_08-25_049.rou.xml
```

Outputs:
- edge_speed_by_sim.pkl

## Approach 2. Using INRIX

File: edge_speed_by_INRIX.py

Inputs:
- date
- simulation folder
- INRIX data
- INRIX geojson

Command:
```
$ python edge_speed_by_INRIX.py --date 20210820 --sim transit-sim-date --INRIX_data INRIX-data/part-00054-49075979-b38a-4685-b377-f8d38d569b56.c000.snappy.parquet --INRIX_geo INRIX-data/USA_Tennessee.geojson
```
Outputs:
- edge_speed_by_INRIX.pkl


## Approach 3. Using APC data

File: edge_speed_by_APC.py

Inputs:
- date
- simulation folder
- trips_from_blocks
- APC

Command:
```
$ python edge_speed_by_APC.py --date 20210820 --sim transit-sim-date --trips_from_blocks Post-processing/trips_from_blocks.csv --APC APC/202108.parquet
```
Outputs:
- edge_speed_by_APC.pkl

