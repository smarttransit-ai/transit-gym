import xmltodict
import json
from collections import OrderedDict

BUS_WITH_PERSON_FILE = './transit_run/bus_withPerson.rou.xml'
OUTPUT_BUS_ROUTE_FILE = './transit_run/bus_routes_only.rou.xml'

with open(BUS_WITH_PERSON_FILE) as fd:
    doc = xmltodict.parse(fd.read())

new_dict = OrderedDict()
new_dict['routes'] = OrderedDict()
new_dict['routes']['route'] = []

new_dict['routes']['vType'] = doc['routes']['vType']
for veh in doc['routes']['vehicle']:
    route_ = OrderedDict()
    str1, str2, str3 = veh['@id'].split('_')
    route_['@id'] = str2[4:] +'_'+ str3
    depart = veh['@depart']
    route_['@depart'] = depart
    route_['@edges'] = veh['route']['@edges']
    route_['stop'] = veh['stop']
    for stop in route_['stop']:
        stop['@arrival'] = str(float(stop['@arrival']) - float(depart))
        stop['@until'] = str(float(stop['@until']) - float(depart))
    new_dict['routes']['route'].append(route_)
    
xml_format= xmltodict.unparse(new_dict,pretty=True)
text_file = open(OUTPUT_BUS_ROUTE_FILE, "w")
text_file.write(xml_format)
text_file.close()