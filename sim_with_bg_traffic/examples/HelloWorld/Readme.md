## Steps to run the HelloWorld example

Note: All the below steps are executed on Ubuntu 20.04 LTS. Please make sure your python version >= 3.7

#### 1.Install SUMO

The package requires sumo ver >= 1.8.0. To install the latest version of SUMO, run

sudo **add**-apt-repository ppa:sumo/stable

sudo apt-**get** update

sudo apt-**get** install sumo sumo-tools sumo-doc

#### 2. Install transsim package

Install the package into the python environment.

For global installation, cd into the directory transit-simulator/src and run:

sudo **pip3** install .

To install the package into your global python environment. 

#### 3. Unzip network files

Unzip the network file contained in examples/HelloWorld/network.

Run the following command in the directory examples/HelloWorld/network:

sudo apt-**get** install unzip

**unzip** Chattanooga_SUMO_Network.net.zip

#### 4. Run test simulation

You are all set to run the helloworld example. cd into HelloWorld and run:

**python3** driver.py

#### 5. Collect results

The results will be put in HelloWorld/Simulation_1. Specifically, the trajectories and edge output files will be in the folder HelloWorld/Simulation_1/output/.







