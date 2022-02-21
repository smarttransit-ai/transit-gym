## Steps to run the Chattanooga_CS example

Note: All the below steps are executed on Ubuntu 20.04 LTS. Please make sure your python version >= 3.7

**Note**: Look at [calibration-poster.pdf](calibration-poster.pdf) for the calibration procedures that we used.

**Warning: This execution may take a long time (>24 hours)**

Remember to download the route file. Refer to the [instructions on main readme.md](https://github.com/smarttransit-ai/transit-gym#step-3-run-simulation). Assuming you are in parent folder Chattanooga_CS_cal you can follow these commands.

```
$ cd network
$ unzip Chattanooga_SUMO_Network.net.zip
$ cd ../routes
$ wget https://www.dropbox.com/s/1tn7an1rijfyafa/Chattanooga_trips_cal.rou.xml.tar.gz?dl=0
$ tar -xzvf Chattanooga_trips_cal.rou.xml.tar.gz 
```

check a file called Chattanooga_trips_cal.rou.xml is in the routes folder. 

```
check if MD5 (Chattanooga_trips_cal.rou.xml) = 9caba35a878d77c4700e9e3aad10b37f
```

Then get to the top folder Chattanooga_CS_cal

```
$ cd Chattanooga_CS_cal
$ python3 river.py
```

Result are available in `/Simulation1/output`.  The output folder includes trajectories for buses, bus stop information, and edge information, all in csv format. An example of the same is available at https://drive.google.com/drive/u/0/folders/1w9hj8wMJOGemEWVHgJ4_zvXnMT2Htbv9.

Now you can perform post processing as described in the [instructions on main readme.md](https://github.com/smarttransit-ai/transit-gym#step-4-post-processing-of-outputs) 

 
