import pandas as pd
import sumolib
import traci
import random
import copy
import math
from itertools import groupby
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--SUMO_PATH", type=str, default="/usr/bin/sumo", help="SUMO installation path")
parser.add_argument("--GTFS", type=str, default="c", help="GTFS folder")
parser.add_argument("--date", type=str, default="20210820", help="date")
parser.add_argument("--sim", type=str, default="transit-sim-date", help="simulation folder")
args = parser.parse_args()

SUMO_CMD = ["".format(args.SUMO_PATH)]
SUMO_CONFIG_FILE = ["-c", "{}/SUMO_configuration.sumocfg".format(args.sim)]
SUMO_CMD.extend(SUMO_CONFIG_FILE)
traci.start(SUMO_CMD, label=str(random.randint(10000, 50000)))

# read GTFS files
trip_df = pd.read_csv('{}/trips.txt'.format(args.GTFS))
trip_df['trip_id_short'] = trip_df['trip_id'].apply(lambda x: int(x/1000))
stop_time_df = pd.read_csv('{}/stop_times.txt'.format(args.GTFS)).sort_values(by=['arrival_time'])
stop_time_df['trip_id_short'] = stop_time_df['trip_id'].apply(lambda x: int(x/1000))
shape_df = pd.read_csv('{}/shapes.txt'.format(args.GTFS))
bus_stop_df = pd.read_csv('{}/stops.txt'.format(args.GTFS))

# remove trips with 10C shape
removed_shape_ids = [shape_id for shape_id in shape_df['shape_id'].unique() if '10C' in shape_id]
shape_df = shape_df[~shape_df['shape_id'].isin(removed_shape_ids)]
trip_df = trip_df[~trip_df['shape_id'].isin(removed_shape_ids)]

# read road network file
net = sumolib.net.readNet('{}/Chattanooga_SUMO_Network.net.xml'.format(args.sim))
PARKING_LOTS = {}
for parking_id in traci.parkingarea.getIDList():
    lane_id = traci.parkingarea.getLaneID(parking_id)
    PARKING_LOTS[parking_id] = {'lane_id': lane_id, 'edge_id': lane_id.split('_')[0]}

def get_opposite_edge(edge_id):
    edge = net.getEdge(edge_id)
    to_node, from_node = edge.getToNode(), edge.getFromNode()
    for edge_ in to_node.getOutgoing():
        if edge_.getToNode().getID() == from_node.getID():
            return edge_.getID()
    
    return 'None'

def get_routes(edges):
    begining_edge, begining_dist = edges.pop(0)
    begining_opposite_edge = get_opposite_edge(begining_edge)
    while len(edges) > 0 and (begining_edge in edges[0][0] or begining_opposite_edge in edges[0][0]):
        edges.pop(0)
    
    last_id, last_opposite_id = begining_edge, begining_opposite_edge
    # new first edge logic -----------------------------------------------------------------------------
    if begining_opposite_edge != 'None':
        while len(edges) > 0:
            candidate_id, candidate_dist = edges.pop(0)
            opposite_id = get_opposite_edge(candidate_id)
            count = 1
            while len(edges) > 0 and (candidate_id in edges[0][0] or opposite_id in edges[0][0] or
                                     last_id in edges[0][0] or last_opposite_id in edges[0][0]): # noise located in last edge
                if candidate_id in edges[0][0] or opposite_id in edges[0][0]:
                    count += 1
                edges.pop(0)
            last_id, last_opposite_id = candidate_id, opposite_id
            if count < 4 or count * 24 < net.getEdge(candidate_id).getLength():
                continue
            break
        route_from_beginning = net.getShortestPath(net.getEdge(begining_edge), net.getEdge(candidate_id))
        route_from_beginning_opposite = net.getShortestPath(net.getEdge(begining_opposite_edge), net.getEdge(candidate_id))
        if route_from_beginning[1] <= route_from_beginning_opposite[1]:
            corrected_edges_id = [begining_edge]
            corrected_edges_dist = [begining_dist]
        else:
            corrected_edges_id = [begining_opposite_edge]
            corrected_edges_dist = [begining_dist]
            
        if opposite_id == 'None':
            route_to_candidate = net.getShortestPath(net.getEdge(corrected_edges_id[-1]), net.getEdge(candidate_id))
            for edge_ in route_to_candidate[0][1:]:
                corrected_edges_id.append(edge_.getID())
                corrected_edges_dist.append(-1)
            corrected_edges_dist[-1] = candidate_dist
        else:
            route_to_candidate = net.getShortestPath(net.getEdge(corrected_edges_id[-1]), net.getEdge(candidate_id))
            route_to_opposite = net.getShortestPath(net.getEdge(corrected_edges_id[-1]), net.getEdge(opposite_id))
            if route_to_candidate[1] <= route_to_opposite[1]:
                for edge_ in route_to_candidate[0][1:]:
                    corrected_edges_id.append(edge_.getID())
                    corrected_edges_dist.append(-1)
                corrected_edges_dist[-1] = candidate_dist
            else:
                for edge_ in route_to_opposite[0][1:]:
                    corrected_edges_id.append(edge_.getID())
                    corrected_edges_dist.append(-1)
                corrected_edges_dist[-1] = candidate_dist
    else:
        corrected_edges_id = [begining_edge]
        corrected_edges_dist = [begining_dist]
    # --------------------------------------------------------------------------------------------------
    
    # find remainning edges -----------------------------------------------------
    last_id, last_opposite_id = corrected_edges_id[-1], get_opposite_edge(corrected_edges_id[-1])
    while len(edges) > 0:
        candidate_id, candidate_dist = edges.pop(0)
        count = 1
        opposite_id = get_opposite_edge(candidate_id)
        while len(edges) > 0 and (candidate_id in edges[0][0] or opposite_id in edges[0][0] or
                                 last_id in edges[0][0] or last_opposite_id in edges[0][0]): # noise located in last edge
            if candidate_id in edges[0][0] or opposite_id in edges[0][0]:
                count += 1
            edges.pop(0)
        last_id, last_opposite_id = candidate_id, opposite_id
        if count < 4 or count * 24 < net.getEdge(candidate_id).getLength():
            continue
        if opposite_id != 'None':
            route_to_candidate = net.getShortestPath(net.getEdge(corrected_edges_id[-1]), net.getEdge(candidate_id))
            route_to_opposite = net.getShortestPath(net.getEdge(corrected_edges_id[-1]), net.getEdge(opposite_id))
            if route_to_candidate[1] <= route_to_opposite[1]:
                for edge_ in route_to_candidate[0][1:]:
                    corrected_edges_id.append(edge_.getID())
                    corrected_edges_dist.append(-1)
                corrected_edges_dist[-1] = candidate_dist
            else:
                for edge_ in route_to_opposite[0][1:]:
                    corrected_edges_id.append(edge_.getID())
                    corrected_edges_dist.append(-1)
                corrected_edges_dist[-1] = candidate_dist
        else:
            route_to_candidate = net.getShortestPath(net.getEdge(corrected_edges_id[-1]), net.getEdge(candidate_id))
            for edge_ in route_to_candidate[0][1:]:
                corrected_edges_id.append(edge_.getID())
                corrected_edges_dist.append(-1)    
            corrected_edges_dist[-1] = candidate_dist
    # ------------------------------------------------------------------------------
    
    # last edge --------------------------------------------------------------------
    if (candidate_id not in corrected_edges_id) and (opposite_id not in corrected_edges_id):
        if opposite_id == 'None':
            corrected_edges_id.append(candidate_id)
            corrected_edges_dist.append(candidate_dist)
        else:
            route_to_candidate = net.getShortestPath(net.getEdge(corrected_edges_id[-1]), net.getEdge(candidate_id))
            route_to_opposite = net.getShortestPath(net.getEdge(corrected_edges_id[-1]), net.getEdge(opposite_id))
            if route_to_candidate[1] <= route_to_opposite[1]:
                for edge_ in route_to_candidate[0][1:]:
                    corrected_edges_id.append(edge_.getID())
                    corrected_edges_dist.append(-1)
                corrected_edges_dist[-1] = candidate_dist
            else:
                for edge_ in route_to_opposite[0][1:]:
                    corrected_edges_id.append(edge_.getID())
                    corrected_edges_dist.append(-1)
                corrected_edges_dist[-1] = candidate_dist
    # ------------------------------------------------------------------------------
    
    return corrected_edges_id, corrected_edges_dist

def get_route_string(corrected_edges_id):
    # get .rou.xml -----------------------------------------------------------------
    s = str(corrected_edges_id[0])
    for edge in corrected_edges_id[1:]:
        s += ' ' + edge
    # ------------------------------------------------------------------------------
    return s

routes_dict = {}
for shape_id in shape_df['shape_id'].unique():
    print(shape_id)
    shape = shape_df[shape_df['shape_id'] == shape_id].sort_values(by=['shape_pt_sequence'])
    edges = []
    for _, point in shape.iterrows():
        edge_id, offset, laneIdx = traci.simulation.convertRoad(point['shape_pt_lon'], point['shape_pt_lat'], isGeo=True)
        if ':' not in edge_id:
            edges.append((edge_id, point['shape_dist_traveled']))
    corrected_edges_id, corrected_edges_dist = get_routes(copy.deepcopy(edges))
    routes_dict[shape_id] = [corrected_edges_id, corrected_edges_dist]

trip_assignment_df = pd.read_csv('./Pre-processing/trip-assignments/trip-asm-{}.csv'.format(args.date))
trip_assignment_df = trip_assignment_df[trip_assignment_df['trip_id'].isin(trip_df['trip_id_short'].unique())]

corrected_bus_stops = {}
xml = '<?xml version="1.0" encoding="utf-8"?>\n<routes>\n'
xml += '    <vType id="Gillig_105" length="10.67" minGap="3.00" maxSpeed="60.00" guiShape="bus" personCapacity="32" accel="1.4" decel="4.5" sigma="0.5" fuelType="Hybrid"></vType>\n\
    <vType id="Gillig_103" length="10.67" minGap="3.00" maxSpeed="60.00" guiShape="bus" personCapacity="35" accel="1.2" decel="4.3" sigma="0.5" fuelType="Gasoline"></vType>\n\
    <vType id="Gillig_101" length="10.67" minGap="3.00" maxSpeed="65.00" guiShape="bus" personCapacity="32" accel="1.2" decel="4.0" sigma="0.5" fuelType="Gasoline"></vType>\n\
    <vType id="Gillig_106" length="11.28" minGap="3.00" maxSpeed="60.00" guiShape="bus" personCapacity="35" accel="1.2" decel="4.0" sigma="0.5" fuelType="Hybrid"></vType>\n\
    <vType id="Gillig_102" length="10.67" minGap="3.00" maxSpeed="65.00" guiShape="bus" personCapacity="32" accel="1.3" decel="4.1" sigma="0.5" fuelType="Gasoline"></vType>\n\
    <vType id="Gillig_107" length="11.28" minGap="3.00" maxSpeed="65.00" guiShape="bus" personCapacity="35" accel="1.3" decel="4.1" sigma="0.5" fuelType="Gasoline"></vType>\n\
    <vType id="Gillig_104" length="11.28" minGap="3.00" maxSpeed="65.00" guiShape="bus" personCapacity="35" accel="1.3" decel="4.1" sigma="0.5" fuelType="Gasoline"></vType>\n\
    <vType id="Gillig_108" length="10.90" minGap="3.00" maxSpeed="62.50" guiShape="bus" personCapacity="33" accel="1.2" decel="4.3" sigma="0.5" fuelType="Electric"></vType>\n\n'

for vid in trip_assignment_df['vid'].unique():
    stop_xml = ''
    vid_trip_df = trip_assignment_df[trip_assignment_df['vid'] == vid]
    num_trips = len(vid_trip_df)
    full_corrected_edges = []
    for i in range(num_trips):
        trip_id = vid_trip_df[['trip_id']].iloc[i].values[0]
        print(vid, trip_id)
        # get routes -------------------------------------------------------
        shape_id = trip_df[trip_df['trip_id_short'] == int(trip_id)].values[0][7]
        corrected_edges_id, corrected_edges_dist = routes_dict[shape_id]
        # --------------------------------------------------------------------
        
        # get depart time ----------------------------------------------------
        if i == 0:
            stop_df_filtered = stop_time_df[stop_time_df['trip_id_short'] == trip_id].sort_values(by=['stop_sequence'])
            stop_df_filtered['time_stamp'] = stop_df_filtered['departure_time'].apply(lambda s: 3600*int(s[:2]) 
                                                                                  + 60*int(s[3:5]) + int(s[6:]))
            depart = stop_df_filtered[['time_stamp']].values[0][0]
            veh_type = vid_trip_df['vehicle_type'].values[0]
        # --------------------------------------------------------------------
        elif i < num_trips - 1:
            if vid_trip_df.iloc[i-1, :]['gtfs_time_end'] == vid_trip_df.iloc[i, :]['gtfs_time_start']:
                if last_edges_id == corrected_edges_id[0]:
                    corrected_edges_id = corrected_edges_id[1:]
                else:
                    route_to_start_next_trip = net.getShortestPath(net.getEdge(last_edges_id), 
                                                                   net.getEdge(corrected_edges_id[0]))
                    edge_ids_, edge_dists_ = [], []
                    for edge_ in route_to_start_next_trip[0][1:]:
                        edge_ids_.append(edge_.getID())
                        edge_dists_.append(-1)
                    corrected_edges_id = edge_ids_ + corrected_edges_id
                    corrected_edges_dist = edge_dists_ + corrected_edges_dist
            else:
                # find closest parking------
                min_dist, min_parking_id, edges_in_route_from_parking = -1, None, []
                for parking_id in PARKING_LOTS:
                    route_from_parking = net.getShortestPath(net.getEdge(PARKING_LOTS[parking_id]['edge_id']), 
                                                           net.getEdge(corrected_edges_id[0]))
                    if (min_dist == -1) or (min_dist > route_from_parking[1]):
                        min_dist = route_from_parking[1]
                        min_parking_id = parking_id
                        edges_in_route_from_parking = route_from_parking[0]
                # --------------------------
                
                route_from_parking = net.getShortestPath(net.getEdge(PARKING_LOTS[min_parking_id]['edge_id']), 
                                       net.getEdge(corrected_edges_id[0]))
                route_to_parking = net.getShortestPath(net.getEdge(last_edges_id), 
                                                       net.getEdge(PARKING_LOTS[min_parking_id]['edge_id']))
                edge_ids_, edge_dists_ = [], []
                for edge_ in route_to_parking[0][1:]:
                    edge_ids_.append(edge_.getID())
                    edge_dists_.append(-1)
                for edge_ in edges_in_route_from_parking[1:]:
                    edge_ids_.append(edge_.getID())
                    edge_dists_.append(-1)
                corrected_edges_id = edge_ids_ + corrected_edges_id
                corrected_edges_dist = edge_dists_ + corrected_edges_dist
                s = vid_trip_df.iloc[i, :]['gtfs_time_start']
                parking_until = 3600*int(s[:2]) + 60*int(s[3:5]) + int(s[6:])
                stop_xml += '        <stop parkingArea="{}" until="{}"> </stop>\n'.format(min_parking_id, parking_until) 
                    
        # --------------------------------------------------------------------
        last_edges_id = corrected_edges_id[-1]
        full_corrected_edges.extend(corrected_edges_id)

    
        stop_df_filtered = stop_time_df[stop_time_df['trip_id_short'] == trip_id].sort_values(by=['stop_sequence'])
        stop_df_filtered['time_stamp'] = stop_df_filtered['departure_time'].apply(lambda s: 3600*int(s[:2]) 
                                                                              + 60*int(s[3:5]) + int(s[6:]))
        # stops ----------------------------------------------------------------------------    
        stop_ids = stop_df_filtered.stop_id.values
        stop_dists = stop_df_filtered.shape_dist_traveled.values
        stop_arrivals = stop_df_filtered.time_stamp.values
        stop_timepoints = stop_df_filtered.timepoint.values
        stop_coordinates = []
        stop_edges = []
        stop_offsets = []
        for stop_id in stop_ids:
            tmp_df = bus_stop_df[bus_stop_df['stop_id'] == stop_id][['stop_lat', 'stop_lon']]
            lat, lon = tmp_df.values[0]
            stop_coordinates.append([lat, lon])
            edge_id, offset, laneIdx = traci.simulation.convertRoad(lon, lat, isGeo=True)
            stop_edges.append(edge_id)
            stop_offsets.append(offset)

        idx, stop_idx = 0, 0
        while (idx < len(corrected_edges_id)) and (stop_idx < len(stop_ids)):
            max_idx = idx
            while max_idx < len(corrected_edges_id):
                if corrected_edges_dist[max_idx] > stop_dists[stop_idx] + 1000:
                    break
                max_idx += 1

            if stop_ids[stop_idx] not in corrected_bus_stops:
                corrected_bus_stops[stop_ids[stop_idx]] = []        
            flag = False
            for j, stop in enumerate(corrected_bus_stops[stop_ids[stop_idx]]):
                if stop['edge'] in corrected_edges_id[idx:max_idx]:
                    flag = True
                    idx = idx + corrected_edges_id[idx:max_idx].index(stop['edge'])
                    if stop_timepoints[stop_idx] == 1:
                        stop_xml += '        <stop busStop="{}-{}" arrival="{}" until="{}"> </stop>\n'.format(stop_ids[stop_idx], j, 
                                                                            stop_arrivals[stop_idx], stop_arrivals[stop_idx]+1)
                    else:
                        stop_xml += '        <stop busStop="{}-{}" arrival="{}" duration="1"> </stop>\n'.format(stop_ids[stop_idx], j, 
                                                                            stop_arrivals[stop_idx])                    
                    break
            if not flag:
                # find the nearest point in edges[idx:max_idx]
                if stop_edges[stop_idx] in corrected_edges_id[idx:max_idx]:
                    corrected_bus_stops[stop_ids[stop_idx]].append({'edge': stop_edges[stop_idx], 'pos': stop_offsets[stop_idx]})
                    if stop_timepoints[stop_idx] == 1:
                        stop_xml += '        <stop busStop="{}-{}" arrival="{}" until="{}"> </stop>\n'.format(stop_ids[stop_idx], 
                            len(corrected_bus_stops[stop_ids[stop_idx]])-1, stop_arrivals[stop_idx], stop_arrivals[stop_idx]+1)
                    else:
                        stop_xml += '        <stop busStop="{}-{}" arrival="{}" duration="1"> </stop>\n'.format(stop_ids[stop_idx], 
                            len(corrected_bus_stops[stop_ids[stop_idx]])-1, stop_arrivals[stop_idx])
                    idx = idx + corrected_edges_id[idx:max_idx].index(stop_edges[stop_idx])
                else:
                    lat, lon = stop_coordinates[stop_idx]
                    stop_x, stop_y = traci.simulation.convertGeo(lon, lat, fromGeo=True)
                    min_dist, min_edge, min_pos = -1, None, 0
                    for edge in corrected_edges_id[idx:max_idx]:
                        for pos in range(0, math.floor(traci.lane.getLength(edge + '_0'))):
                            x, y = traci.simulation.convert2D(edge, pos)
                            dist = (stop_x - x)**2 + (stop_y - y)**2
                            if min_dist == -1 or dist < min_dist:
                                min_dist, min_edge, min_pos = dist, edge, pos

                    corrected_bus_stops[stop_ids[stop_idx]].append({'edge': min_edge, 'pos': min_pos})
                    if stop_timepoints[stop_idx] == 1:
                        stop_xml += '        <stop busStop="{}-{}" arrival="{}" until="{}"> </stop>\n'.format(stop_ids[stop_idx], 
                                len(corrected_bus_stops[stop_ids[stop_idx]])-1, stop_arrivals[stop_idx], stop_arrivals[stop_idx] + 1)
                    else:
                        stop_xml += '        <stop busStop="{}-{}" arrival="{}" duration="1"> </stop>\n'.format(stop_ids[stop_idx], 
                                len(corrected_bus_stops[stop_ids[stop_idx]])-1, stop_arrivals[stop_idx])
                    idx = idx + corrected_edges_id[idx:max_idx].index(min_edge)

            stop_idx += 1
        # -------------------------------------------------------------------------------------------
    full_corrected_edges = [key for key, _group in groupby(full_corrected_edges)]
    route_str = get_route_string(full_corrected_edges)
    xml += '    <vehicle id="{}" type="{}" depart="{}"  departPos="stop" line="{}">\n'.format(vid, veh_type, depart, vid)
    xml += '        <route edges="{}" />\n'.format(route_str)
    xml += stop_xml
    xml += '    </vehicle>\n'
    
xml += '</routes>'
file = open("{}/routes-{}.rou.xml".format(args.sim, args.date), 'w')
file.write(xml)
file.close()

xml = '<additional>\n'
BUS_STOP_LENGTH = 10
for stop_id in corrected_bus_stops:
    for idx, stop in enumerate(corrected_bus_stops[stop_id]):
        lane = stop['edge'] + '_0'
        lane_length = traci.lane.getLength(lane)
        if lane_length <= BUS_STOP_LENGTH:
            xml += '    <busStop id="{}-{}" lane="{}" startPos="{}" endpos="{}" friendlyPos="1"/>\n'.format(
                                stop_id, idx, lane, 0, lane_length)
        elif stop['pos'] + BUS_STOP_LENGTH <= lane_length:
            xml += '    <busStop id="{}-{}" lane="{}" startPos="{}" endpos="{}" friendlyPos="1"/>\n'.format(
                                stop_id, idx, lane, lane_length-BUS_STOP_LENGTH, lane_length)
        else:
            xml += '    <busStop id="{}-{}" lane="{}" startPos="{}" endpos="{}" friendlyPos="1"/>\n'.format(
                                stop_id, idx, lane, stop['pos'], stop['pos'] + BUS_STOP_LENGTH)
xml += '</additional>'
file = open("{}/busStop-{}.add.xml".format(args.sim, args.date), 'w')
file.write(xml)
file.close()

traci.close()