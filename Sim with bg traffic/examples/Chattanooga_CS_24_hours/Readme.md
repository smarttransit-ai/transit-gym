
**Warning: This execution may take a long time (>24 hours)**

Remember to download the route file. Refer to the [instructions on main readme.md](https://github.com/smarttransit-ai/transit-gym#step-3-run-simulation). Assuming you are in parent folder Chattanooga_CS_24_hours you can follow these commands.

```
$ cd network
$ unzip Chattanooga_SUMO_Network.net.zip
$ cd ../routes
$ wget https://www.dropbox.com/s/6sr0w60d96098v3/Chattanooga_Daily_Trips.rou.xml.tar.gz?dl=0
$ tar -xzvf Chattanooga_Daily_Trips.rou.xml.tar.gz
```

check a file called Chattanooga_Daily_Trips.rou.xml is in the routes folder. 

```
check if MD5 (Chattanooga_Daily_Trips.rou.xml) = dfbd1bc3bd889f58d179d268132708a9
```

Then get to the top folder Chattanooga_CS_24_hours

```
$ cd Chattanooga_CS_24_hours
$ python3 driver_24.py 
```

Result are available in `/Simulation1/output`.  The output folder includes trajectories for buses, bus stop information, and edge information, all in csv format. An example of the same is available at https://drive.google.com/drive/u/1/folders/1w9hj8wMJOGemEWVHgJ4_zvXnMT2Htbv9.

Now you can perform post processing as described in the [instructions on main readme.md](https://github.com/smarttransit-ai/transit-gym#step-4-post-processing-of-outputs) 

