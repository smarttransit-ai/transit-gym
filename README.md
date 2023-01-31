# Transit-GYM

The following project describes the procedures necessary to simulate the public transit in the city of Chattanooga. The approach is generalizable and can be extended to other cities. The papers, [TRANSIT-GYM: A Simulation and Evaluation Engine for Analysis of Bus Transit Systems](https://ieeexplore.ieee.org/abstract/document/9556290), [BTE-Sim: Fast Simulation Environment For Public Transportation](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10020973) provides details about the work.

There are three main components of a transit simulation: the transit system, the background traffic, and the transportation infrastructure. The transit system includes the buses, busstops, and commuters that make up the public transportation system. The background traffic consists of other modes of transportation such as private vehicles, taxis, freight vehicles,and pedestrians. Both the transit system and the background traffic share the use of the transportation infrastructure, so they can affect each other. The transit system is made up of these individual components that can be controlled and configured to meet the needs of the population. This includes the number of buses, the routesthey run on, their schedule, and other factors. By simulating the transit system, users can visualize how these different components interact and how they affect the overall efficiency and effectiveness of the system.

By including the background traffic in the simulation, users can get a more accurate picture of how the transit system functions in the context of the overall transportation network, as described in [TRANSIT-GYM: A Simulation and Evaluation Engine for Analysis of Bus Transit Systems](https://ieeexplore.ieee.org/abstract/document/9556290). Refer to [Presentation-Transit-Gym-SmartComp2021.pdf](docs/Presentation-Transit-Gym-SmartComp2021.pdf) for a powerpoint presentation about the simulation framework. This method of simulation uses the exact details of all kinds of veicles plying on the roads and provides the exact replica of the scenario where all these vehicles would be moving on the road network. his methd is very accurate, and in turn, uses a lot of cmputation of time to arrive at the simualtion results. You can find the instructions to run this simulation process under [Sim with bg traffic](sim_with_bg_traffic). A youtube presentation of this work is available at [https://youtu.be/Fw4UQGcB80o](https://youtu.be/Fw4UQGcB80o).

For regular activities, or where fast changes needed to be implemented in any of the components of the simualtion, re-running the simualtion woud be temporlally and computationally expensive. To sort this issue, we have looked into the process of simulation where we eliminate all the background traffic (vehicles other than the ones we are concerned about, buses in our case). The paper, [BTE-Sim: Fast Simulation Environment For Public Transportation](https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=10020973), and the related recources [BTETransitSimReport.pdf](docs\BTETransitSimReport.pdf), [S06211-sen.pdf](docs\S06211-sen.pdf) explain the process. It does use the initial results that the background traffic simulation method generates and calibrates them to be used here. You can find the steps to run BTE-Sim under[ Sim without bg traffic](sim_without_bgtraffic).

Further, the simulations for energy usage from power grids can be done using the steps mentioned in [e-bench](archive/e-bench).

## Requirement: Install SUMO

If you have not already done so, go to [https://sumo.dlr.de/docs/Installing/index.html](https://sumo.dlr.de/docs/Installing/index.html) to install SUMO on your machine. Please install the **latest version** instead of the regular distribution.


## Files required for running simulation

Note for each of the simulation, the folder contains the following file structure

* /network/ - The network files. Note you need to **extract the zip file in the folder at the same location**. This network file describes chattanooga road map.
* /taz/ - The taz.xml for transportation demand.
* /bus-stop/ - Configured bus stop excel file. Format should be same as [example](sim_with_bg_traffic\examples\Chattanooga_CS_24_hours\bus-stop\busstops.xlsx).
* /gtfs/ - Apporpriate GTFS files (can be downloaded from [Transitfeeds](https://transitfeeds.com/))
* /gui/ - gui.view.xml for sumo config.
* /travel-demand/ -.od file for transportation demand.
* /vehicle-types/ - Apporpriate excel file for vehicle stats.
* /routes/ - Routes to be included in the simulation if needed. (Optional)

These files can be generated by following the steps in [manual_files](sim_with_bg_traffic\manual_files)

# Acknowledgement

This material is based upon work supported by National Science Foundation under grants CNS-1952011, CNS-2029950 and Department of Energy, Office of Energy Efficiency and Renewable Energy (EERE), under Award Number DEEE0008467. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation or the Department of Energy.
