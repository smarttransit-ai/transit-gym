## Energy estimation for simulated trips
This code is to estimated the energy consumption for simulated buses in 1HZ. The micro-energy prediction models are developed based on the real-time vehicle driving and energy consumption data at 1Hz frequency collected by CARTA. For more details about the model, please refer to the [micro-energy-prediction repo](https://github.com/smarttransit-ai/micro-energy-prediction) .

### 1. Output from transit-simulator 

Run the simulation and collect the output results, which includes the trajectories for each trip. Each trip id has one trajectory output, recording the instantaneous speed and acceleration in 1Hz.

Below is a sample for one trajectory file.

<img src="https://github.com/smarttransit-ai/transit-simulator/blob/master/energy_estimation/traj_sample.png" alt="alt text" width="600" height="120">

*time_ms: time of the day in millisecond.*\
*speed: unit is 0.01m/s.*\
*acceleration: unit is 0.001m/s^2.*


### 2. energy estimation
[Energy_estimation.ipynb](https://github.com/smarttransit-ai/transit-simulator/blob/master/energy_estimation/Energy_estimation.ipynb) is used to predict the energy consumption for trajectories in 1HZ. 
* Select scenario for weather (rainy, sunny, windy, and snowny)
* Load micro-energy prediction models
* Predict energy consumption for each trip in 1Hz

*Note:* The unit of predicted energy consumption for diesel and hybrid bus is gal/h, and for electric bus is kWh.
