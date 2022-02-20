## Steps to run the Chattanooga_CS example

Note: All the below steps are executed on Ubuntu 20.04 LTS. Please make sure your python version >= 3.7

## Step 1. Prepare the Required Files for 24 Hours
The files are already arranged in the required structure. *Extract zip file in /network/ folder*<br>
1. Download the routes file (routes.Chattanooga_Daily_Trips.rou.xml) from https://drive.google.com/file/d/17O9rhpYR1JWlh9vSRZvyCdIFsTKhLSZj/view?usp=sharing and put in the Chattanooga_CS_24_hours/routes/ folder.
2. Extract the zip file in /Chattanooga_CS_24_hours/network
```
$ cd network
$ unzip Chattanooga_SUMO_Network.net.zip
```

### Step 2. Start Simulation
**Warning: This execution may take a long time (>24 hours)**<br>
**Note**: The simulation time can be changed to different durations by changing the "time [0000:2359]" in [Chattanooga_CS_24_hours.transsim](https://github.com/smarttransit-ai/transit-gym/tree/master/examples/Chattanooga_CS_24_hours/Chattanooga_CS_24_hours.transsim), as mentioned [here](#change-duration)<br>

1. Simulate for 24 hours from 12:00 AM - 12:00 AM (next day). 
```
$ cd transit-gym/examples/Chattanooga_CS_24_hours
$ python3 driver_24.py
```
2. The result are available in `/Simulation1/output`.  The output folder includes trajectories for buses, bus stop information, and edge information, all in csv format.

  *Optional* The example output of simulating for 24 hours from 12:00 AM - 12:00 AM(nextday) is saved at https://drive.google.com/drive/u/1/folders/1w9hj8wMJOGemEWVHgJ4_zvXnMT2Htbv9.

3. The *post-processing* can be performed on the collected data according to the steps mentioned [Step 6. Post-processing](#post-processing)
