import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--GTFS", type=str, default="../GTFS/20210815", help="GTFS folder")
parser.add_argument("--date", type=str, default="20210820", help="date")
parser.add_argument("--APC", type=str, default="../APC/202108.parquet", help="APC file")

args = parser.parse_args()

def vid_to_veh_type(veh_id):    
    if veh_id>=101 and veh_id<=110:
        return 'Gillig_104'
    elif veh_id>=111 and veh_id<=134:
        return 'Gillig_103'
    elif veh_id>=135 and veh_id<=144:
        return 'Gillig_102'
    elif veh_id>=145 and veh_id<=146:
        return 'Gillig_107'
    elif veh_id>=147 and veh_id<=155:
        return 'Gillig_101'
    elif veh_id>=501 and veh_id<=502:
        return 'Gillig_106'
    elif veh_id>=503 and veh_id<=506:
        return 'Gillig_105'
    elif veh_id>=700 and veh_id<=753:
        return 'Gillig_108'
    
    return 'None'

APC_df = pd.read_parquet(args.APC, engine='pyarrow')
gtfs_stop_df = pd.read_csv('{}/stop_times.txt'.format(args.GTFS))
gtfs_stop_df['trip_id_short'] = gtfs_stop_df['trip_id'].apply(lambda x: int(x/1000))

date_str = '{}-{}-{}'.format(args.date[:4], args.date[4:6], args.date[6:])
trip_asm = []
APC_date = APC_df[(APC_df['transit_date'] == date_str) & (APC_df['time_actual_arrive'].notnull())]
for trip_id in APC_date['trip_id'].unique():
    APC_trip = APC_date[APC_date['trip_id'] == trip_id]
    trip_id = int(trip_id)
    veh_id = APC_trip.vehicle_id.values[0]
    veh_type = vid_to_veh_type(veh_id)
    gtfs_trip_stop_times = gtfs_stop_df[gtfs_stop_df['trip_id_short'] == trip_id].sort_values(by='arrival_time')
    start_time, end_time = gtfs_trip_stop_times.arrival_time.values[0], gtfs_trip_stop_times.arrival_time.values[-1]
    trip_asm.append({'trip_id': trip_id, 'vid': veh_id, 'vehicle_type': veh_type,
                        'gtfs_time_start': start_time, 'gtfs_time_end': end_time})

trip_asm = pd.DataFrame(trip_asm).sort_values(by='gtfs_time_start').reset_index()
trip_asm.to_csv('./trip-assignments/trip-asm-{}.csv'.format(args.date), index=None)