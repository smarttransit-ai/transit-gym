## Energy estimation for simulated trips

### 1. Output from transit-simulator 

Run the simulation and collect the output results, which includes the trajectories for each trip. Each trip id has one trajectory output, recording the instantaneous speed and acceleration in 1Hz.

Below is a sample for one trajectory file.

<img src="https://github.com/smarttransit-ai/transit-simulator/blob/master/energy_estimation/traj_sample.png" alt="alt text" width="550" height="120">

*time_ms: time of the day in millisecond.*\
*speed: unit is 0.01m/s.*\
*acceleration: unit is 0.001m/s^2.*


### 2. energy estimation
[Energy-estimation.ipynb](https://github.com/smarttransit-ai/transit-simulator/blob/master/energy_estimation/Energy-estimation.ipynb) is used to predict the energy consumption for trajectories in 1HZ. 
* Select scenario for weather (rainy, sunny, windy, and snowny) and vehicle class (diesel, hybrid, and electric)
* Load the micro-energy prediction model 
* Predict energy consumption of each trip
