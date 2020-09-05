# transit-simulator

## Procedure

<img src="https://github.com/hdemma/transit-simulator/blob/master/images/Procedure.png" alt="alt text" width="490" height="400">

The yellow boxes in above chart is the existing information at the begining.

### Step 1. Correct network
Use GUI-based tool NETEDIT to check the network and add links and junctions which are missing during the conversion from OSM map to SUMO network.

### Step 2. Find bus stops' positions on network
* Utilize TraCI tool to interact with SUMO
* Get the position info of stops (including edge ID, lane position and lane index) based on geo coordinates.

### Step 3. Create bus stop additional file

### Step 4. Create bus trip file

### Step 5. Generate bus route file

### Step 6. Correct bus stops' positions

### Step 7. Regenerate route file

### Step 8. Configure and run simulation


