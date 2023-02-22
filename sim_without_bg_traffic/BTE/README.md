# Instructions for generating edge speed data

## 1. Using simulation with background traffic

File: edge_speed_by_sim.py

Inputs:
- date
- simulation folder
- background traffic

Command:

$ python edge_speed_by_sim.py --date 20210820 --sim transit-sim-date --bgTraffic combined_trips_100k_08-25_049.rou.xml

Outputs:
- edge_speed_by_sim.pkl
