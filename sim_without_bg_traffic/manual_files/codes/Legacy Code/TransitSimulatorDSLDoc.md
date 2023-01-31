## TransitSimulatorDSL

### 0. Introduction

TransitSimulatorDSL is a DSL created specifically to address the configuration of input for traffic simulation. It can perform the functionality of automatic configuration of the input for a traffic simulation, including configuring specific values and selecting a subset of routes and vehicles based on existing route files.

### 1. Syntax

The general format of a program using this DSL is as follow. Parameter types ore values of choice are specified by the arrow notation

*begin*

​	*TimeStart **startValue ->INT***

​	*TimeEnd **endValue ->INT***

​	Network **networkFile ->STRING***

​	*Additional **additionalFile ->STRING***

​	OutputName **outputFile ->STRING***

​	DumpName **dumpFile ->STRING***

​	*RouteFileName **"fileName ->STRING"***

​		***"selectionParam -> INCLUDE, ALL, EXCLUDE"***

​		*vehicle **"vehicle ->STRING"***

​	*RouteFileName **"fileName"***

​		***"selectionParam"***

​		*vehicle **"vehicle"***

​		*...*

*end*

Note that we can have multiple routefilename and multiple vehicles specified (0..n). A sample program is shown below.

*begin*

​	*TimeStart 10*

​	*TimeEnd 100*

​	*Network "networkfile.xml"*

​	*Additional "additionalFile.xml"*

​	*OutputName "test.sumocfg"*

​	*DumpName "trajectory_output.xml"*

​	*RouteFileName "Bus.rou.xml"*

​		*"INCLUDE"*

​		*vehicle "1AltonPark_A_inbound"*

​		*vehicle "2AltonPark_A_inbound"*

​	*RouteFileName "hattanooga_Daily_Trips.rou.xml*

​		*"ALL"*

*end*

### 2. Parameter Specifications

The specific meanings of the parameters are listed below:

**startValue**: the starting time for the simulation in seconds

**endValue**: the end time for the simulation in seconds

**networkFile**: the file name for the traffic network of use

**additionalFile**: the file name for additional data file of use

**outputFile**: the file name for output sumocfg file

**dumpFile**: the file name for the dump file for SUMO simulation

**selectionParam**: the parameter for determining the means of selection. When taken the value "ALL", all of the vehicles in the file specified earlier will be used for the simulation; when taken the value "INCLUDE", only the vehicles specified below will be included in the simulation; when taken the value "EXCLUDE", only the vehicles specified below will be excluded in the simulation. All others are taken.

**vehicle**: the name of the vehicle specified

### 3. Usage

To run the application, open codes/DSLInterpreter.py, change the parameter in line 12 to your code's name (for example, test.ts). After you execute the script, the sumocfg file will be generated under the same directory, which we can then use to proceed to simulation.

### 4. Environments

Environments used for this demo:

Python 3.8.3

SUMO 1.7.0

Packages used for this demo:

textx 2.2.0

beautifulsoup4 4.9.1













​		



​	









