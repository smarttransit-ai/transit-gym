## Steps to run the Chattanooga_CS example

Note: All the below steps are executed on Ubuntu 20.04 LTS. Please make sure your python version >= 3.7

**Note**: Look at [calibration-poster.pdf](calibration-poster.pdf) for the calibration procedures that we used.

### Step 1. Prepare the Required Files for 24 Hours
The files are already arranged in the required structure. *Extract zip file in /network/ folder*<br>
1. Download the calibrated routes file (Chattanooga_trips_cal.rou.xml) from https://drive.google.com/file/d/1IxJPMDwjnMn5U5wSLA2PJ_J0WsePk_aN/view?usp=sharing and put in the /routes/ folder. 
2. Extract the zip file in /network folder 



### Step 2. Start Simulation
**Warning: This execution may take a long time (>24 hours)**<br>
**Note**: The simulation time can be changed to different durations by changing the "time [0000:2359]" in [Chattanooga_CS_24_hours.transsim](https://github.com/smarttransit-ai/transit-gym/tree/master/examples/Chattanooga_CS_24_hours/Chattanooga_CS_cal.transsim).<br>

1. Simulate for 24 hours from 12:00 AM - 12:00 AM (next day). 
```
$ cd transit-gym/examples/Chattanooga_CS_cal
$ python3 driver.py
```
2. The result are available in `/Simulation1/output`.  The output folder includes trajectories for buses, bus stop information, and edge information, all in csv format.

  *Optional* The example output of simulating for 24 hours from 12:00 AM - 12:00 AM(nextday) is saved at https://drive.google.com/drive/u/1/folders/1w9hj8wMJOGemEWVHgJ4_zvXnMT2Htbv9.

3. The *post-processing* can be performed on the collected data according to the steps mentioned [Step 6. Post-processing](#post-processing)

