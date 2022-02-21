## Steps to run the Chattanooga_CS example

Note: All the below steps are executed on Ubuntu 20.04 LTS. Please make sure your python version >= 3.7
### Step 0. *Optional* Generate new GTFS files
New GTFS files can be generated as shown in [Step 8. Generating GTFS files](#new-gtfs)

### Step 1. Prepare the Required Files

1. Download the routes file (routes.Chattanooga_Daily_Trips.rou.xml) from (https://drive.google.com/file/d/17O9rhpYR1JWlh9vSRZvyCdIFsTKhLSZj/view?usp=sharing) and put in the /routes/ folder. 
2. Extract the zip file in /Chattanooga_CS_900_1000/network
```
$ cd network
$ unzip Chattanooga_SUMO_Network.net.zip
```

### Step 2. Start Simulation

1. Simulating for one hour from 9 AM - 10 AM. The duration in driver.py is changed: 0900 to 1000 hrs
```
$ python3 driver.py
```
2. The result are available in `/Simulation1/output`.  The output folder includes trajectories for buses, bus stop information, and edge information, all in csv format. 
<pre>  *Optional* The example output of simulating for one hour from 9 AM - 10 AM is stored at https://drive.google.com/drive/u/1/folders/1w9hj8wMJOGemEWVHgJ4_zvXnMT2Htbv9</pre>
3. The *post-processing* can be performed on the collected data according to the steps mentioned [Step 6. Post-processing](#post-processing)
