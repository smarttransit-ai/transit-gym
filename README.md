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

### Environment
SUMO 1.8.0

Python 3.7


## Examples: Chattanooga Simulation.

1. Do something
2. Simulate for one hour from 8AM - 9 AM. Describe how someone can change to whole day or a different time window.
3. Collect trajectories
4. Compute Energy Estimates
5. Plot Energy Estimates across trajectories for vehicles.
6. Plot occupancy of vehicles
7. Plot congestion levels on the roads.


## Changing the Settings - Examples
1. Change the vehicle Assignment
2. Repeat steps 1-7 from above.


## Changing the Settings - Examples
1. Change the GTFS Schedule
2. Repeat steps 1-7 from above.


## Link to videos and demonstrations
https://vanderbilt365.sharepoint.com/sites/TransitHub/Shared%20Documents/Forms/AllItems.aspx?FolderCTID=0x01200038D55CC5B8DD0640BBBA3F2E7A659561&id=%2Fsites%2FTransitHub%2FShared%20Documents%2Fsimulation%2FSmartComp&viewid=ba956da1%2D2d6b%2D4b8a%2D8eaa%2D9d2fb164d54c

# Explaining the transit simulation

 - what goes behings it.
 - Refer to the paper
 - Provide link to presentation and video of smart comp
 - Explain calibration process
 - When would the calibration process be repeated.

## Guide to transsim

Note: The steps discussed here are generic steps. Specific **examples** are:

**[Hello World](https://github.com/hdemma/transit-simulator/blob/master/examples/HelloWorld/)**: a simple example that demonstrates the full functionality and usages.

**[Chattanooga_CS](https://github.com/hdemma/transit-simulator/blob/master/examples/Chattanooga_CS/)**: a environment for transit simulation within the Chattanooga area.

Also, the simulator is an automation of manual steps. If you are looking for **manual steps** to create the simulation environment, please refer to [Manual Files](manual_files)


# Acknowledgement

This material is based upon work supported  by National Science Foundation under grants CNS-1952011, CNS-2029950 and Department of Energy, Office of Energy Efficiency and Renewable Energy (EERE), under Award Number DEEE0008467. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation or the Department of Energy.
