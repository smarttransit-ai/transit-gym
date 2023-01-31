import xmltodict
import pandas as pd

BUS_ROUTE_FILE = './transit_run/bus_routes_only.rou.xml'
ROUTE_ASM_FILE = './vehID_concept/trip_assignment_20220111.csv'

def to_second(time_str):
    h, m, s = time_str.split(':')
    return int(h)*3600 + int(m)*60 + int(s)

class BusGenerator:
    def __init__(self, traci):
        self.traci = traci
        with open(BUS_ROUTE_FILE) as fd:
            doc = xmltodict.parse(fd.read())
        route_ids = {}
        for route in doc['routes']['route']:
            route_ids[route['@id']] = True
        route_asm_df = pd.read_csv(ROUTE_ASM_FILE)
        route_asm_df.loc[:, 'route_id'] = route_asm_df.apply(lambda row: str(row['trip_id']) + '020' + '_' + row['gtfs_time_start'], axis=1)
        route_asm_df.loc[:, 'sumo_vehID'] = route_asm_df.apply(lambda row: str(row['trip_id']) + '_' + row['gtfs_time_start'], axis=1)
        route_asm_df.loc[:, 'valid'] = route_asm_df['route_id'].apply(lambda x: x in route_ids)
        print('WARNING: There are {} invalid trips'.format(len(route_asm_df[route_asm_df['valid'] == False])))
        self.route_asm_df = route_asm_df[route_asm_df['valid']]
        self.route_asm_df.loc[:, 'depart'] = self.route_asm_df['gtfs_time_start'].apply(to_second)


        # Create a dict to monitor vehicles -------------------------------
        self.veh_obj = {}
        for veh_id in self.route_asm_df['vid'].unique():
            self.veh_obj[veh_id] = {}
            self.veh_obj[veh_id]['routes'] = []
            self.veh_obj[veh_id]['counter'] = 0
            df_veh = self.route_asm_df[self.route_asm_df['vid'] == veh_id]
            for idx, row in df_veh.iterrows():
                self.veh_obj[veh_id]['routes'].append({'route_id': row['route_id'], 'depart': row['depart'], 
                    'sumo_vehID': row['sumo_vehID'], 'veh_type': row['vehicle_type']})
        # -----------------------------------------------------------------

    def update(self):
        step = int(self.traci.simulation.getTime())
        # if any trip is finished, add the next trip -----------------------------
        for veh_id_sim in self.traci.simulation.getArrivedIDList():
            veh_id = int(veh_id_sim.split('-')[0])
            veh_routes, veh_counter = self.veh_obj[veh_id]['routes'], self.veh_obj[veh_id]['counter']
            if veh_counter < len(veh_routes):
                new_veh_id = '{}-{}_{}'.format(veh_id, veh_counter, veh_routes[veh_counter]['sumo_vehID'])
                self.traci.vehicle.add(new_veh_id, veh_routes[veh_counter]['route_id'],
                                            depart=veh_routes[veh_counter]['depart'],  typeID=veh_routes[veh_counter]['veh_type'], departPos='stop')
                if step > veh_routes[veh_counter]['depart']:
                    delta = step - veh_routes[veh_counter]['depart']
                    for stop in self.traci.vehicle.getStops(new_veh_id):
                        stop_dict = stop.__dict__
                        new_until = stop_dict['until'] - delta
                        new_arrival = stop_dict['intendedArrival'] - delta
                        self.traci.vehicle.setBusStop(new_veh_id, stop_dict['stoppingPlaceID'], duration=1, until=new_until, flags=8)
                self.veh_obj[veh_id]['counter'] += 1
        # -------------------------------------------------------------------------