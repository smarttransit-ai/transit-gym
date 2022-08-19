The files have two batch files: One for Helics 2.8 version and one for HELICS 3.1. 
Depending on the version of the helics_broker that is being used, use the helics broker command propwerly, especially the part with loglevel definition int he helics broker command.
Key lines are commented "user-defined" that are associated withthe charging profiles and the charger load. 
In chargerLoad.py: Lines 42, 59 and 60
To vary the interval between charger load update and the computation of the Grid score, update line 492 in federate1.py.
Currently set to update every 300 sec (i.e., 5 min).
