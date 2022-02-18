# Transit-GYM

The following project describes the procedures necessary to simulate the public transit in the city of Chattanooga. The approach is generalizable and can be extended to other cities. The paper [TRANSIT-GYM: A Simulation and Evaluation Engine for Analysis of Bus Transit Systems](https://ieeexplore.ieee.org/abstract/document/9556290) provides details about the work. Refer to [Presentation-Transit-Gym-SmartComp2021.pdf] for a powerpoint presentation about the simulation framework. 

Below you will find the installation instructions and steps required to run a few example simulations. 
Please refer to [Manual Files](manual_files) if you are looking for **manual steps** to create the simulation environment. Otherwise follow the steps below that provide helper scripts. During these steps we refer to two different scenarios:

1. [Hello World](examples/HelloWorld/): a simple example that demonstrates the full functionality and usages.
2. [Chattanooga_CS](examples/Chattanooga_CS/): an environment for transit simulation within the Chattanooga area.
3. [examples/Chattanooga_CS_cal](examples/Chattanooga_CS_cal): an example that includes updated matrices that were calibrated using real traffic from streets. Refer to [calibration-poster.pdf](calibration-poster.pdf) for details.

A youtube presentation of this work is available at [https://youtu.be/Fw4UQGcB80o](https://youtu.be/Fw4UQGcB80o).

# Installation Instructions

## Step 1. Install package

In the directory src, create a python venv (or use install for all environments). Use the command "***pip install .***" to install the package into your environment. Note the version of python on your machine should be greater than 3.6 for dependencies to work.

Install required python packages from requirements.txt

## Step 2. Install SUMO

If you have not already done so, go to "https://sumo.dlr.de/docs/Installing/index.html" to install SUMO on your machine. Please install the latest version instead of the regular distribution.

## Step 3. Prepare files

Prepare the required files in a same file structure as shown in the files folder. The required files in the apporipriate folders are:

* /network/ - The network files.
* /taz/ - The taz.xml for transportation demand.
* /bus-stop/ - Configured bus stop excel file. Format should be same as example.
* /gtfs/ - Apporpriate GTFS files.
* /gui/ - gui.view.xml for sumo config.
* /travel-demand/ -.od file for transportation demand.
* /vehicle-types/ - Apporpriate excel file for vehicle stats.
* /routes/ - Routes to be included in the simulation if needed. (Optional)

## Step 4. Start Simulation

As shown in [driver.py](examples/driver.py), you can now use the package it to interpret your transsim program. Use run() to start the simulation. The result will be available in the running directory after it completes.

## For running Energy estimation 
Install jupyter-nbconvert to run pyhton notebooks. It can be done by entering **sudo apt install jupyter-nbconvert** in terminal.

# Example 1: Hello World

## Step 1. Install transsim package

Install the package into the python environment.<br>
For global installation, cd into the directory transit-simulator/src and run:

```
$ sudo pip3 install .
```

To install the package into your global python environment. 

## Step 2. Unzip network files
Unzip the network file contained in examples/HelloWorld/network .<br>
Run the following command in the directory examples/HelloWorld/network:

```
$ sudo apt-get install unzip
$ unzip Chattanooga_SUMO_Network.net.zip
```


## Step 3. Run test simulation

You are all set to run the helloworld example. cd into HelloWorld and run:

```
python3 driver.py
```

## Step 4. Collect results
The results will be put in HelloWorld/Simulation_1. Specifically, the trajectories and edge output files will be in the folder HelloWorld/Simulation_1/output/.


# Example 2 : Chattanooga Simulation - 24 Hours

Follow the instructions as before to install the system. However, we will use a different configuration file.

### Step 1. Prepare the Required Files for 24 Hours
Prepare the required files in a same file structure as shown in the files folder. The required files in the apporipriate folders are:


* /network/ - The network files.
* /taz/ - The taz.xml for transportation demand.
* /bus-stop/ - Configured bus stop excel file. Format should be same as example.
* /gtfs/ - Apporpriate GTFS files.
* /gui/ - gui.view.xml for sumo config.
* /travel-demand/ -.od file for transportation demand.
* /vehicle-types/ - Apporpriate excel file for vehicle stats.
* /routes/ - Routes to be included in the simulation. 


Now download the routes file (routes.Chattanooga_Daily_Trips.rou.xml) from (https://drive.google.com/file/d/17O9rhpYR1JWlh9vSRZvyCdIFsTKhLSZj/view?usp=sharing) and put in the /routes/ folder.

### Step 2. Start Simulation

Now you are ready to simulate for 24 hour from 00:00 AM - 12 PM. Note this takes a long time.

Change the simulation to a whole day or different time windows by changing the "time [0000:2359]" in [Chattanooga_CS_24_hours.transsim](https://github.com/smarttransit-ai/transit-simulator/tree/master/examples/Chattanooga_CS_24_hours).

cd into Chattanooga_CS_24_hours and run: python3 driver_24.py.  The result will be available in the running directory after it completes.

After this follow these steps.

1. Collect output. The output results are saved at examples/Chattanooga_CS_24_hours/output/. The example output of simulating for one hour from 00:00 AM - 12 PM is saved at https://drive.google.com/drive/u/1/folders/1w9hj8wMJOGemEWVHgJ4_zvXnMT2Htbv9. The output folder includes trajectories for buses, bus stop information, and edge information, all in csv format.
2. Compute Energy Estimates. Fill the corresponding folder name in the script and run [Energy_estimation.ipynb](https://github.com/smarttransit-ai/transit-simulator/blob/master/energy_estimation/Energy_estimation.ipynb). The energy estimation results are saved in your created folder.
3. Plot Energy Estimates across trajectories for vehicles. Run the script [plot_energy_estimation.ipynb](https://github.com/smarttransit-ai/transit-simulator/blob/master/energy_estimation/plot_energy_estimation.ipynb) with the energy estimation results.
4. Plot occupancy of buses. Read the "busstop_info.csv" from the simulation output folder and run the script [plot_occupancy.ipynb](https://github.com/smarttransit-ai/transit-simulator/blob/master/manual_files/output/visulization%20example/plot_occupancy.ipynb).
5. Plot congestion levels on the roads.


## Example 3 : Chattanooga Simulation - 0900 - 1000 hours with GTFS Changes
Using GTFS processor "https://github.com/smarttransit-ai/transit-simulator/blob/master/src/transsim/GTFS_processor.py" to generate new files and put the files in the GFTS folder. Prepare the required files in a same file structure as shown in the files folder. The required files in the apporipriate folders are:
* /network/ - The network files.
* /taz/ - The taz.xml for transportation demand.
* /bus-stop/ - Configured bus stop excel file. Format should be same as example.
* /gtfs/ - Apporpriate GTFS files.
* /gui/ - gui.view.xml for sumo config.
* /travel-demand/ -.od file for transportation demand.
* /vehicle-types/ - Apporpriate excel file for vehicle stats.
* /routes/ - Routes to be included in the simulation. 

1. Run the [Chattanooga_CS_900_1000](https://github.com/smarttransit-ai/transit-simulator/tree/master/examples/Chattanooga_CS_900_1000) example. 
2. Download the routes file (routes.Chattanooga_Daily_Trips.rou.xml) from (https://drive.google.com/file/d/17O9rhpYR1JWlh9vSRZvyCdIFsTKhLSZj/view?usp=sharing) and put in the /routes/ folder. 
3. Simulate for one hour from 9 AM - 10 AM. Change the simulation to a whole day or different time windows by changing the "time [0900:1000]" in [Chattanooga_CS.transsim](https://github.com/smarttransit-ai/transit-simulator/blob/master/examples/Chattanooga_CS/Chattanooga_CS.transsim).
4. Extract the zip file in /Chattanooga_CS_900_1000/network
5. cd into /Chattanooga_CS_900_1000 and run: python3 driver.py
6. Collect output. The output results are saved at Chattanooga_CS/Chattanooga_CS/output/. The example output of simulating for one hour from 9 AM - 10 AM is saved at https://drive.google.com/drive/u/1/folders/1w9hj8wMJOGemEWVHgJ4_zvXnMT2Htbv9. The output folder includes trajectories for buses, bus stop information, and edge information, all in csv format.
7. Compute Energy Estimates. Fill the corresponding folder name in the script and run [Energy_estimation.ipynb](https://github.com/smarttransit-ai/transit-simulator/blob/master/energy_estimation/Energy_estimation.ipynb). The energy estimation results are saved in your created folder.
8. Plot Energy Estimates across trajectories for vehicles. Run the script [plot_energy_estimation.ipynb](https://github.com/smarttransit-ai/transit-simulator/blob/master/energy_estimation/plot_energy_estimation.ipynb) with the energy estimation results.
9. Plot occupancy of buses. Read the "busstop_info.csv" from the simulation output folder and run the script [plot_occupancy.ipynb](https://github.com/smarttransit-ai/transit-simulator/blob/master/manual_files/output/visulization%20example/plot_occupancy.ipynb).
10. Plot congestion levels on the roads.


## Example 4 : Chattanooga Simulation - 24 Hours after calibration
The procedure is similar to "Installation Instructions", with the configuration file of 24 Hours. The configuration file and driver python file updated as "Chattanooga_CS_24_hours_cal" and "driver_24_cal" respectively at: [examples/Chattanooga_CS_cal](examples/Chattanooga_CS_cal)

**Note** - look at [calibration-poster.pdf](calibration-poster.pdf) for the calibration procedures that we used.

### Step 1. Prepare the Required Files for 24 Hours
Prepare the required files in a same file structure as shown in the files folder. The required files in the apporipriate folders are:


* /network/ - The network files.
* /taz/ - The taz.xml for transportation demand.
* /bus-stop/ - Configured bus stop excel file. Format should be same as example.
* /gtfs/ - Apporpriate GTFS files.
* /gui/ - gui.view.xml for sumo config.
* /travel-demand/ -.od file for transportation demand.
* /vehicle-types/ - Apporpriate excel file for vehicle stats.
* /routes/ - Routes to be included in the simulation. 


1. Download the calibrated routes file (Chattanooga_trips_cal.rou.xml) from (https://drive.google.com/file/d/1IxJPMDwjnMn5U5wSLA2PJ_J0WsePk_aN/view?usp=sharing) and put in the /routes/ folder.  
2. Run the [Chattanooga_CS_24_hours_cal.transsim](https://github.com/smarttransit-ai/transit-simulator/tree/master/examples/Chattanooga_CS_cal) example. cd into Chattanooga_CS and run: python3 driver.py
3. Simulate for 24 hour from 00:00 AM - 12 PM. Change the simulation to a whole day or different time windows by changing the "time [0000:2359]" in [Chattanooga_CS_24_hours_cal.transsim](https://github.com/smarttransit-ai/transit-simulator/tree/master/examples/Chattanooga_CS_cal).
4. Collect output. The output results are saved at Chattanooga_CS/Chattanooga_CS/output/. The output folder includes trajectories for buses, bus stop information, and edge information, all in csv format.
5. Compute Energy Estimates. Fill the corresponding folder name in the script and run [Energy_estimation.ipynb](https://github.com/smarttransit-ai/transit-simulator/blob/master/energy_estimation/Energy_estimation.ipynb). The energy estimation results are saved in your created folder.
6. Plot Energy Estimates across trajectories for vehicles. Run the script [plot_energy_estimation.ipynb](https://github.com/smarttransit-ai/transit-simulator/blob/master/energy_estimation/plot_energy_estimation.ipynb) with the energy estimation results.
7. Plot occupancy of buses. Read the "busstop_info.csv" from the simulation output folder and run the script [plot_occupancy.ipynb](https://github.com/smarttransit-ai/transit-simulator/blob/master/manual_files/output/visulization%20example/plot_occupancy.ipynb).
8. Plot congestion levels on the roads.


### Step 2. Start Simulation
As shown in [driver_24_cal.py](examples/driver_24.py), you can now use the package it to interpret your transsim program. Use run() to start the simulation. The result will be available in the running directory after it completes.


## Changing the Settings - Examples
1. Change the vehicle Assignment by changing the content of "vehicleassignment{}" in .transsim files in the respective example and run: python3 driver.py
3. Repeat steps 1-7 from above.


## Changing the Settings - Examples
1. Change the GTFS Schedule by changing "import "gtfs.20200816"" to other gtfs file name, such as "import "gtfs.20211024"" in [Chattanooga_CS.transsim](https://github.com/smarttransit-ai/transit-simulator/blob/master/examples/Chattanooga_CS/Chattanooga_CS.transsim) and run: python3 driver.py
2. Repeat steps 1-7 from above.




# Acknowledgement

This material is based upon work supported  by National Science Foundation under grants CNS-1952011, CNS-2029950 and Department of Energy, Office of Energy Efficiency and Renewable Energy (EERE), under Award Number DEEE0008467. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation or the Department of Energy.
