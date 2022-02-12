# transit-simulator

## Installation Instructions

### Step 1. Install package

In the directory src, create a python venv (or use install for all environments). Use the command "***pip install .***" to install the package into your environment. Note the version of python on your machine should be greater than 3.6 for dependencies to work.

### Step 2. Install SUMO

If you have not already done so, go to "https://sumo.dlr.de/docs/Installing/index.html" to install SUMO on your machine. Please install the latest version instead of the regular distribution.

### Step 3. Prepare files

Prepare the required files in a same file structure as shown in the files folder. The required files in the apporipriate folders are:

* /network/ - The network files.
* /taz/ - The taz.xml for transportation demand.
* /bus-stop/ - Configured bus stop excel file. Format should be same as example.
* /gtfs/ - Apporpriate GTFS files.
* /gui/ - gui.view.xml for sumo config.
* /travel-demand/ -.od file for transportation demand.
* /vehicle-types/ - Apporpriate excel file for vehicle stats.
* /routes/ - Routes to be included in the simulation if needed. (Optional)

### Step 4. Start Simulation

As shown in [driver.py](examples/driver.py), you can now use the package it to interpret your transsim program. Use run() to start the simulation. The result will be available in the running directory after it completes.

## Example 1: Hello World

### Step 1. Install transsim package

Install the package into the python environment.<br>
For global installation, cd into the directory transit-simulator/src and run:

sudo **pip3** install .

To install the package into your global python environment. 

### Step 2. Unzip network files
Unzip the network file contained in examples/HelloWorld/network.<br>
Run the following command in the directory examples/HelloWorld/network:

sudo apt-**get** install unzip

**unzip** Chattanooga_SUMO_Network.net.zip

### Step 3. Run test simulation

You are all set to run the helloworld example. cd into HelloWorld and run:

**python3** driver.py

### Step 4. Collect results
The results will be put in HelloWorld/Simulation_1. Specifically, the trajectories and edge output files will be in the folder HelloWorld/Simulation_1/output/.


## Example 2 : Chattanooga Simulation - 24 Hours
The procedure is similar to "Installation Instructions", with the configuration file of 24 Hours. The configuration file and driver python file updated as "Chattanooga_CS_24_hours" and "driver_24" respectively at: https://github.com/smarttransit-ai/transit-simulator/tree/master/examples/Chattanooga_CS
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


### Step 2. Start Simulation
As shown in [driver_24.py](examples/driver_24.py), you can now use the package it to interpret your transsim program. Use run() to start the simulation. The result will be available in the running directory after it completes.


* Describe the output files.
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



## Example 4 : Chattanooga Simulation - 24 Hours after calibration
The procedure is similar to "Installation Instructions", with the configuration file of 24 Hours. The configuration file and driver python file updated as "Chattanooga_CS_24_hours_cal" and "driver_24_cal" respectively at: https://github.com/smarttransit-ai/transit-simulator/tree/master/examples/Chattanooga_CS
Also, it needs to replace * /routes/ file with https://drive.google.com/file/d/1IxJPMDwjnMn5U5wSLA2PJ_J0WsePk_aN/view?usp=sharing with the previous route file and add vehicle type from https://drive.google.com/file/d/14WqszGqfpbP1awJhw9TFWamT7p6Uv-7d/view?usp=sharing .


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



### Step 2. Start Simulation
As shown in [driver_24_cal.py](examples/driver_24.py), you can now use the package it to interpret your transsim program. Use run() to start the simulation. The result will be available in the running directory after it completes.








## Examples: Chattanooga Simulation.

1. Run the [Chattanooga_CS](https://github.com/smarttransit-ai/transit-simulator/tree/master/examples/Chattanooga_CS) example. cd into Chattanooga_CS and run: python3 driver.py
2. Simulate for one hour from 9 AM - 10 AM. Change the simulation to a whole day or different time windows by changing the "time [0900:1000]" in [Chattanooga_CS.transsim](https://github.com/smarttransit-ai/transit-simulator/blob/master/examples/Chattanooga_CS/Chattanooga_CS.transsim).
4. Collect output. The output results are saved at Chattanooga_CS/Chattanooga_CS/output/. The example output of simulating for one hour from 9 AM - 10 AM is saved at https://drive.google.com/drive/u/1/folders/1w9hj8wMJOGemEWVHgJ4_zvXnMT2Htbv9. The output folder includes trajectories for buses, bus stop information, and edge information, all in csv format.
5. Compute Energy Estimates. Fill the corresponding folder name in the script and run [Energy_estimation.ipynb](https://github.com/smarttransit-ai/transit-simulator/blob/master/energy_estimation/Energy_estimation.ipynb). The energy estimation results are saved in your created folder.
6. Plot Energy Estimates across trajectories for vehicles. Run the script [plot_energy_estimation.ipynb](https://github.com/smarttransit-ai/transit-simulator/blob/master/energy_estimation/plot_energy_estimation.ipynb) with the energy estimation results.
7. Plot occupancy of buses. Read the "busstop_info.csv" from the simulation output folder and run the script [plot_occupancy.ipynb](https://github.com/smarttransit-ai/transit-simulator/blob/master/manual_files/output/visulization%20example/plot_occupancy.ipynb).
8. Plot congestion levels on the roads.


## Changing the Settings - Examples
1. Change the vehicle Assignment by changing the content of "vehicleassignment{}" in [Chattanooga_CS.transsim](https://github.com/smarttransit-ai/transit-simulator/blob/master/examples/Chattanooga_CS/Chattanooga_CS.transsim) and run: python3 driver.py
3. Repeat steps 1-7 from above.


## Changing the Settings - Examples
1. Change the GTFS Schedule by changing "import "gtfs.20200816"" to other gtfs file name, such as "import "gtfs.20211024"" in [Chattanooga_CS.transsim](https://github.com/smarttransit-ai/transit-simulator/blob/master/examples/Chattanooga_CS/Chattanooga_CS.transsim) and run: python3 driver.py
2. Repeat steps 1-7 from above.


# Explaining the transit simulation

 - This work is published in this paper: [TRANSIT-GYM: A Simulation and Evaluation Engine for Analysis of Bus Transit Systems](https://ieeexplore.ieee.org/abstract/document/9556290)
 - Find the presentation and video of the paper in this link: https://vanderbilt365.sharepoint.com/sites/TransitHub/Shared%20Documents/Forms/AllItems.aspx?FolderCTID=0x01200038D55CC5B8DD0640BBBA3F2E7A659561&id=%2Fsites%2FTransitHub%2FShared%20Documents%2Fsimulation%2FSmartComp&viewid=ba956da1%2D2d6b%2D4b8a%2D8eaa%2D9d2fb164d54c
 - Explain calibration process
 - When would the calibration process be repeated.

## Guide to transsim

Note: The steps discussed here are generic steps. Specific **examples** are:

**[Hello World](https://github.com/hdemma/transit-simulator/blob/master/examples/HelloWorld/)**: a simple example that demonstrates the full functionality and usages.

**[Chattanooga_CS](https://github.com/hdemma/transit-simulator/blob/master/examples/Chattanooga_CS/)**: a environment for transit simulation within the Chattanooga area.

Also, the simulator is an automation of manual steps. If you are looking for **manual steps** to create the simulation environment, please refer to [Manual Files](manual_files)


# Acknowledgement

This material is based upon work supported  by National Science Foundation under grants CNS-1952011, CNS-2029950 and Department of Energy, Office of Energy Efficiency and Renewable Energy (EERE), under Award Number DEEE0008467. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation or the Department of Energy.
