# Transit-GYM

The following project describes the procedures necessary to simulate the public transit in the city of Chattanooga. The approach is generalizable and can be extended to other cities. The paper [TRANSIT-GYM: A Simulation and Evaluation Engine for Analysis of Bus Transit Systems](https://ieeexplore.ieee.org/abstract/document/9556290) provides details about the work. Refer to [Presentation-Transit-Gym-SmartComp2021.pdf] for a powerpoint presentation about the simulation framework. 

Below you will find the installation instructions and steps required to run a few example simulations. 
Please refer to [Manual Files](manual_files) if you are looking for **manual steps** to create the simulation environment. Otherwise follow the steps below that provide helper scripts. During these steps we refer to two different scenarios:

1. [Hello World](examples/HelloWorld/): a simple example that demonstrates the full functionality and usages.
2. [Chattanooga_CS](examples/Chattanooga_CS/): an environment for transit simulation within the Chattanooga area.
3. [examples/Chattanooga_CS_cal](examples/Chattanooga_CS_cal): an example that includes updated matrices that were calibrated using real traffic from streets. Refer to [calibration-poster.pdf](calibration-poster.pdf) for details.

A youtube presentation of this work is available at [https://youtu.be/Fw4UQGcB80o](https://youtu.be/Fw4UQGcB80o).


# Docker Instructions

Assuming you have docker command line, follow these instructions

```
$ git clone https://github.com/smarttransit-ai/transit-gym.git 
$ cd transit-gym
$ docker build -t transit-gym-docker .
```

Now you can run various examples. create a directory where results will be stored and then launch docker into root and mount simulation_output to /simulation_output. The docker will provide a prompt into the container. The container number 37a93e9abef8 will be different on your machine.

```
$ mkdir simulation_output  # 
$ docker run -t -i -v `pwd`/simulation_output:/simulation_output transit-gym-docker bash  
root@37a93e9abef8:/# 
```

Now launch example

```
root@bf8aa1fdcd33:/# cd transit-gym/examples/HelloWorld/
root@bf8aa1fdcd33:/transit-gym/examples/HelloWorld# python driver.py 
```

The output will look like the following

```
root@bf8aa1fdcd33:/transit-gym/examples/HelloWorld# python driver.py 
Sun Feb 20 00:55:18 2022 : Generating Configuration files for Simulation from  helloworld.transsim
Sun Feb 20 00:55:18 2022 : running od2trips
Sun Feb 20 00:55:19 2022 : od2trips done
Sun Feb 20 00:55:19 2022 : running duarouter. Takes time.
Sun Feb 20 01:25:08 2022 : duarouter done

Config File Saved. Please find configured simulation file at: ./Simulation_1

Sun Feb 20 01:25:08 2022 : Done.
Sun Feb 20 01:25:08 2022 : Starting Simulation. Calling Sumo:  sumo ./Simulation_1/config.sumocfg
Sun Feb 20 01:28:51 2022 : Simulation Complete - Proceeding to output processing
/usr/local/lib/python3.9/dist-packages/transsim/Output_Processor.py:45: DtypeWarning: Columns (6) have mixed types. Specify dtype option on import or set low_memory=False.
  edgeO = pd.read_csv(result_path + "EdgeMean.csv",sep=';')
Sun Feb 20 01:29:13 2022 : All Done
```

Now move the results to host machine

```
root@bf8aa1fdcd33:/transit-gym/examples/HelloWorld# mv Simulation_1/ /simulation_output/HelloWorld_Simulation_1
root@bf8aa1fdcd33:/transit-gym/examples/HelloWorld# exit
exit

```

Now the simulation results will be in host machine.

```
(base) host-machine:simulation_output $ tree
.
└── HelloWorld_Simulation_1
    ├── EdgeMean.csv
    ├── EdgeMean.xml
    ├── Person_trips.xml
    ├── busstop_output.csv
    ├── busstop_output.xml
    ├── config.sumocfg
    ├── edge.dump.add.xml
    ├── error_warning_log.xml
    ├── final_routefile.alt.xml
    ├── final_routefile.xml
    ├── output
    │   ├── Trajectory_Route1.0_ALTON_PARK_block107.0_trip151657020.csv
    │   ├── busstop_info.csv
    │   └── edge_info.csv
    ├── raw_routefile.xml
    ├── stopfile.add.xml
    ├── trajectories_output.xml
    ├── trajectories_outputactorConfig.csv
    ├── trajectories_outputmotionState.csv
    ├── trajectories_outputvehicle.csv
    └── vehicle.add.xml

2 directories, 20 files
(base) host-machine:simulation_output $ 


```

# Regular Installation Instructions (without Docker)

### Step 1. Install packages

python >= 3.6 required for dependencies to work.

Optional : create a virtual environment
Install required python packages from requirements.txt
```
$ pip3 install -r requirements.txt
```
Navigate to /transit-gym/src, create a python venv (or use install for all environments). Use the command "***pip install .***" to install the package into your environment.
```
$ cd transit-gym/src
$ pip3 install .
```

### Step 2. Install SUMO

If you have not already done so, go to "https://sumo.dlr.de/docs/Installing/index.html" to install SUMO on your machine. Please install the latest version instead of the regular distribution.

### Step 3. Prepare files

Prepare the required files in a same file structure as shown in the files folder. The required files in the apporipriate folders are:

* /network/ - The network files
* /taz/ - The taz.xml for transportation demand.
* /bus-stop/ - Configured bus stop excel file. Format should be same as example.
* /gtfs/ - Apporpriate GTFS files.
* /gui/ - gui.view.xml for sumo config.
* /travel-demand/ -.od file for transportation demand.
* /vehicle-types/ - Apporpriate excel file for vehicle stats.
* /routes/ - Routes to be included in the simulation if needed. (Optional)
<br>
(These files are already present in the examples provided)

**N.B**:  You need to extract the zip files in /network/ folder in the examples provided

### Step 4. Start Simulation

As shown in [driver.py](examples/driver.py), you can now use the program to interpret your transsim program. We use the run() method in driver.py to start the simulation. 
```
$ python3 driver.py
```
The result will be available in the running directory after it completes.

### Step 5. For running Energy estimation 
Install jupyter-nbconvert to run python notebooks. 
```
$ sudo apt install jupyter-nbconvert
```

### Step 6. Post-processing on generated results[](#post-processing)
Here, perform 3 types of post-analysis
1. Compute the energy estimates.
  Fill the corresponding **folder names** in the script and run [Energy_estimation.ipynb](https://github.com/smarttransit-ai/transit-gym/blob/master/energy_estimation/Energy_estimation.ipynb).
```
$ jupyter nbconvert --execute Energy_estimation.ipynb
```
The output notebook is stored in a .html file. The energy estimation results are saved in your created folder<br>
2. Plot the energy estimates<br>
  Plot Energy Estimates across trajectories for vehicles. Run the script [plot_energy_estimation.ipynb](https://github.com/smarttransit-ai/transit-gym/blob/master/energy_estimation/plot_energy_estimation.ipynb) with the energy estimation results.
```
$ jupyter nbconvert --execute plot_energy_estimation.ipynb
```

3. Plot the occupancy of buses
  Plot occupancy of buses. Read the "busstop_info.csv" from the simulation output folder and run the script [plot_occupancy.ipynb](https://github.com/smarttransit-ai/transit-gym/blob/master/manual_files/output/visulization%20example/plot_occupancy.ipynb).
```
$ jupyter nbconvert --execute plot_occupancy.ipynb
```

### Optional: Step 7. Installing ubuntu unzipper
```
$ sudo apt-get install unzip
```

### Optional : Step 8. Updating GTFS files[](#new-gtfs)
Using [GTFS_processor.py]"https://github.com/smarttransit-ai/transit-gym/blob/master/src/transsim/GTFS_processor.py" to generate new files and put the files in the GFTS folder.
```
$ cd transit-gym/src/transsim
$ python3 GTFS_processor.py
```

## Example 1: Hello World

### Step 1. Unzip network files
Unzip the network file contained in examples/HelloWorld/network .<br>

```
$ cd network
$ unzip Chattanooga_SUMO_Network.net.zip
```


### Step 2. Run test simulation

You are all set to run the helloworld example. cd into HelloWorld and run:

```
$ python3 driver.py
```

### Step 3. Collect results
The results will be put in HelloWorld/Simulation_1. Specifically, the trajectories and edge output files will be in the folder HelloWorld/Simulation_1/output/.

## Example 2 : Chattanooga Simulation - 0900 - 1000 hours (uncalibrated) with GTFS Changes

Go to the [Chattanooga_CS_900_1000](https://github.com/smarttransit-ai/transit-simulator/tree/master/examples/Chattanooga_CS_900_1000) example folder. 

### Step 0. *Optional* Update with new GTFS files
GTFS files can be updated as shown in [Step 8. Generating GTFS files](#new-gtfs)

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

## Example 3 : Chattanooga Simulation - 24 Hours (Uncalibrated)
Go to the [Chattanooga_CS_24_hours](https://github.com/smarttransit-ai/transit-simulator/tree/master/examples/Chattanooga_CS_24_hours) example folder. 

### Step 1. Prepare the Required Files for 24 Hours
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



## Example 4 : Chattanooga Simulation - 24 Hours after calibration
Go to the [Chattanooga_CS_24_hours](https://github.com/smarttransit-ai/transit-simulator/tree/master/examples/Chattanooga_CS_24_hours) example folder. 

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


## Additional Steps. Changing the Settings - Examples
#### Changing the Vehicle Assignment
Change the vehicle Assignment by changing the content of "vehicleassignment{}" in .transsim files in the respective example and run: python3 driver.py

#### Changing the GTFS schedule[](#change-duration)
Change the GTFS Schedule by changing "import "gtfs.20200816"" to other gtfs file name, such as "import "gtfs.20211024"" in the transsim file. For example, in  [Chattanooga_CS.transsim](https://github.com/smarttransit-ai/transit-simulator/blob/master/examples/Chattanooga_CS/Chattanooga_CS.transsim) change **import "gtfs.20200816"** to **import "gtfs.20211024"**



# Acknowledgement

This material is based upon work supported  by National Science Foundation under grants CNS-1952011, CNS-2029950 and Department of Energy, Office of Energy Efficiency and Renewable Energy (EERE), under Award Number DEEE0008467. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation or the Department of Energy.
