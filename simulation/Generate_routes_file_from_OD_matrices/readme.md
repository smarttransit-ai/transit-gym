# Generate routes file from OD matrices (background traffic)

## 1- Convert TAZ shapefile to Sumo polygon file with POLYCONVERT:
For this step we need TAZ shape files from the folder “tazshapefile_909_TAZ” and the Chattanooga network file with this command: 

`polyconvert --net-file Chattanooga_SUMO_Network.net.xml --shapefile-prefixes taz909  --shapefile.id-column TAZID --shapefile.add-param true --shapefile.fill false  --proj.utm true -o polygon.xml`


##2- convert Sumo polygon file to Sumo TAZ file with edges assigned to TAZs:

`$SUMO_HOME/tools/edgesInDistricts.py -n Chattanooga_SUMO_Network.net.xml -t polygon.xml  -o taz.xml'`

##3- Check generated TAZ file:

Fix incorrect TAZ ids by removing “#x” part. Remember that this step is only for TAZ ids not the other  part of the TAZ file such as edges.

##4- Convert given OD matrices to O-format for sumo shown below :
All of our ODs are in this format, but if not the ODs should be converted to this format.

$OR;D2
* From-Time  To-Time
7.00 8.00
* Factor
1.00
* some
* additional
* comments

         1          1       1.00
         
         1          2       2.00
         
         1          3       3.00
         
         2          1       4.00
         
         2          2       5.00
         
     

You need to create separate files for different vehicle types: passenger, single unit truck and multi-unit truck because OD2Trips process vehicle types separately. 
You might need to create different files for different times of day too because of "From-Time" and "To-Time" line in O-format.

##5- Generate trips using od2trips in Sumo for passenger, single unit truck and multi-unit truck files.
For doing this step we need 9 separate OD files: (op: off peak hours)
pass_am.txt
pass_pm.txt
pass_op.txt
mut_am.txt
mut_pm.txt
mut_op.txt
sut_am.txt
sut_pm.txt
sut_op.txt

`od2trips --taz-files taz.xml --od-matrix-files pass_am.txt --output-file trips_pass_am_xml.xml --prefix pass_am --vtype passenger --spread.uniform t`

`od2trips --taz-files taz.xml --od-matrix-files pass_pm.txt --output-file trips_pass_pm_xml.xml --prefix pass_pm --vtype passenger --spread.uniform t`

`od2trips --taz-files taz.xml --od-matrix-files pass_op.txt --output-file trips_pass_op_xml.xml --prefix pass_op --vtype passenger --spread.uniform t`

`od2trips --taz-files taz.xml --od-matrix-files sut_op.txt --output-file trips_sut_op_xml.trips.xml --prefix sut_op --vtype truck --spread.uniform t`

`od2trips --taz-files taz.xml --od-matrix-files sut_pm.txt --output-file trips_sut_pm_xml.trips.xml --prefix sut_pm --vtype truck --spread.uniform`

`od2trips --taz-files taz.xml --od-matrix-files sut_am.txt --output-file trips_sut_am_xml.trips.xml --prefix sut_am --vtype truck --spread.uniform`

`od2trips --taz-files taz.xml --od-matrix-files mut_pm.txt --output-file trips_mut_pm_xml.trips.xml --prefix mut_pm --vtype trailer --spread.uniform`

`od2trips --taz-files taz.xml --od-matrix-files mut_op.txt --output-file trips_mut_op_xml.trips.xml --prefix mut_op --vtype trailer --spread.uniform`

`od2trips --taz-files taz.xml --od-matrix-files mut_am.txt --output-file trips_mut_am_xml.trips.xml --prefix mut_am --vtype trailer --spread.uniform`

##6- Combine the different trips files into one trip file for sumo
A jupyter notebook  code file attached here to does this.

##7- Generating the routes file using  duaIterate:
This step depends on the demand file may takes time from one day to a month for 50 iteration. (https://sumo.dlr.de/docs/Demand/Dynamic_User_Assignment.html)

`$SUMO_HOME/tools/assign/duaIterate.py --net-file Chattanooga_SUMO_Network.net.xml -t combined_trips.xml –continue-on-unbuild  --time-to-teleport 50   --clean-alt `




