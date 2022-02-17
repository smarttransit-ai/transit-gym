## Steps to run the Chattanooga_CS example

Note: All the below steps are executed on Ubuntu 20.04 LTS. Please make sure your python version >= 3.7

#### 1.Install SUMO

The package requires sumo ver >= 1.8.0. To install the latest version of SUMO, run

sudo **add**-apt-repository ppa:sumo/stable

sudo apt-**get** update

sudo apt-**get** install sumo sumo-tools sumo-doc

#### 2. Install transsim package

Install the package into the python environment.

For global installation, cd into the directory transsim/src and run:

sudo **pip3** install .

To install the package into your global python environment. 

#### 3. Prepare network and route files

Unzip the network file contained in examples/Chattanooga_CS/network.

Run the following command in the directory examples/Chattanooga_CS/network:

sudo apt-**get** install unzip

**unzip** Chattanooga_SUMO_Network.net.zip

Then, go to

https://drive.google.com/file/d/18QYhq5gbh9ytAzwC9kSXwNHfwSljbp8s/view?usp=sharing

to download the route file and put in a new directory examples/Chattanooga_CS/routes

#### 4. Run simulation

You are all set to run the Chattanooga_CS example. cd into Chattanooga_CS and run:

**python3** driver.py

#### 5. Collect results

Chattanooga_CS/Chattanooga_CS/output/.







