
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


# bus stop output containing delay and person load information
stopO = pd.read_csv("/busstop_output24h.csv",sep=';')
stopO=stopO[["stopinfo_id","stopinfo_busStop","stopinfo_started","stopinfo_arrivalDelay",
             "stopinfo_ended","stopinfo_delay","stopinfo_initialPersons",
             "stopinfo_loadedPersons","stopinfo_unloadedPersons",
             "stopinfo_lane","stopinfo_pos","stopinfo_parking"]]
stopO['route']=stopO['stopinfo_id'].str[5:8]
stopO['route']=stopO['route'].replace('_','', regex=True)
stopO['route']=stopO['route'].replace('t','', regex=True)
stopO['trip']=stopO['stopinfo_id'].str[-8:]
stopO=stopO.sort_values(["trip","stopinfo_started"])


#hourly number of people at each bus stop
stopO['hour']=stopO['stopinfo_ended']//3600
stopbyH = dict(tuple(stopO.groupby([stopO['hour']])))


#boxplot of occupancy of each bus by trip over 24 hours
fig1st, oc = plt.subplots(figsize=(25, 10))
sns.set_style("ticks") 
sns.boxplot(x = 'trip', y = 'stopinfo_initialPersons', data = stopO, hue="route",
            linewidth=0.5, palette="Set3",
            flierprops = dict(markerfacecolor='0.75', markersize=4,linestyle='none'),
            dodge =False,width=0.6)
#sns.stripplot(x = 'trip', y = 'stopinfo_initialPersons', data = stopO, hue="route",
#             palette="Set3",dodge=True, jitter=True, zorder=1) 
oc.set_xlabel('Trips (sorted by departure time)',fontsize=28);
#oc.set(xticklabels=[]);
oc.set_xticks([0,184])
oc.set_xticklabels(["4:41:00","23:55:00"])
oc.set_ylabel('Occupancy (passenger amount)',fontsize=28);
oc.legend(fontsize=20,title="Route", title_fontsize = 20)
plt.setp(oc.get_xticklabels(), fontsize = 24)
plt.setp(oc.get_yticklabels(), fontsize = 24)
plt.show()

fig2, bo = plt.subplots(figsize=(25, 10))
sns.set_style("whitegrid")   
sns.boxplot(x = 'trip', y = 'stopinfo_loadedPersons', data = stopO, hue="route",
            linewidth=0.5, palette="Set3",
            flierprops = dict(markerfacecolor='0.75', markersize=4,linestyle='none'),
            dodge =False,width=0.6) 
#sns.stripplot(x = 'trip', y = 'stopinfo_loadedPersons', data = stopO, hue="route",
#             palette="Set3",dodge=True, jitter=True, zorder=1) 
bo.set_xlabel('Trips',fontsize=18);
bo.set_ylabel('Loaded Passengers',fontsize=18);
bo.legend(bbox_to_anchor=(1.04, 1.0),borderaxespad=0.).set_title('Route')
plt.setp(bo.get_xticklabels(), rotation=60, fontsize = 12)
plt.setp(bo.get_yticklabels(), fontsize = 12)
plt.show()

fig3, al = plt.subplots(figsize=(25, 10))
sns.set_style("whitegrid")   
sns.boxplot(x = 'trip', y = 'stopinfo_unloadedPersons', data = stopO, hue="route",
            linewidth=0.5, palette="Set3",
            flierprops = dict(markerfacecolor='0.75', markersize=4,linestyle='none'),
            dodge =False,width=0.6) 
#sns.stripplot(x = 'trip', y = 'stopinfo_unloadedPersons', data = stopO, hue="route",
#             palette="Set3",dodge=True, jitter=True, zorder=1) 
al.set_xlabel('Trips',fontsize=18);
al.set_ylabel('Unloaded Passengers',fontsize=18);
al.legend(bbox_to_anchor=(1.04, 1.0),borderaxespad=0.).set_title('Route')
plt.setp(al.get_xticklabels(), rotation=60, fontsize = 12)
plt.setp(al.get_yticklabels(), fontsize = 12)
plt.show()

fig4, al = plt.subplots(figsize=(25, 10))
#sns.set_style("whitegrid")   
sns.boxplot(x = 'trip', y = 'stopinfo_delay', data = stopO, hue="route",
            linewidth=0.5, palette="Set3",
            flierprops = dict(markerfacecolor='0.75', markersize=4,linestyle='none'),
            dodge =False,width=0.6) 
#sns.stripplot(x = 'trip', y = 'stopinfo_delay', data = stopO, hue="route",
#             palette="Set3",dodge=True, jitter=True, zorder=1) 
al.set_xlabel('Trips',fontsize=18);
al.set_ylabel('Delay Time of Buses on Each Stop',fontsize=18);
al.legend(bbox_to_anchor=(1.04, 1.0),borderaxespad=0.).set_title('Route')
plt.setp(al.get_xticklabels(), rotation=60, fontsize = 12)
plt.setp(al.get_yticklabels(), fontsize = 12)
plt.show()

stopO['tripid']=stopO['stopinfo_id'].str[-22:]
stop_byTrip=stopO.groupby('tripid').agg({'stopinfo_initialPersons': 'max',
                         'stopinfo_loadedPersons': 'sum',
                         'stopinfo_unloadedPersons': 'sum',
                         'stopinfo_delay': 'mean',
                         'route':'min'})
stop_byTrip.rename(columns={'stopinfo_initialPersons' : 'max_occupacy',
                            'stopinfo_loadedPersons':'totle_board',
                            'stopinfo_unloadedPersons':'totle_alight',
                            'stopinfo_delay': 'average_delay'},inplace = True)

#max passenger occupancy of each bus along the stops across 24h
fig11, ocr = plt.subplots(figsize=(8, 6))
sns.set_style("ticks")   
ocr=sns.boxplot(x = 'route', y = 'max_occupacy', data = stop_byTrip, hue="route",
            linewidth=1.5, palette="Set3",
            flierprops = dict(markerfacecolor='0.75', markersize=5,linestyle='none'),
            dodge =False,width=0.6) 
ocr.set_xlabel('Routes',fontsize=24);
ocr.set_ylabel('Max occupancy on each bus',fontsize=24);
#ocr.legend(bbox_to_anchor=(1.1, 1.0),borderaxespad=0.)
plt.legend([],[], frameon=False)
plt.setp(ocr.get_xticklabels(), fontsize = 18)
plt.setp(ocr.get_yticklabels(), fontsize = 18)
plt.show()

#Total boarding passengers of each bus
fig22, bor = plt.subplots(figsize=(8, 6))
sns.set_style("ticks")   
bor=sns.boxplot(x = 'route', y = 'totle_board', data = stop_byTrip, hue="route",
            linewidth=1.5, palette="Set3",
            flierprops = dict(markerfacecolor='0.75', markersize=5,linestyle='none'),
            dodge =False,width=0.6)  
bor.set_xlabel('Routes',fontsize=24);
bor.set_ylabel('Total boarding passengers',fontsize=24);
#bor.set(ylim=(0, 80))
#bor.legend(bbox_to_anchor=(1.1, 1.0),borderaxespad=0.)
plt.legend([],[], frameon=False)
plt.setp(bor.get_xticklabels(), fontsize = 18)
plt.setp(bor.get_yticklabels(), fontsize = 18)
plt.show()

#Total alighting passengers of each bus
fig33, alr = plt.subplots(figsize=(8, 6))
sns.set_style("whitegrid")   
alr=sns.boxplot(x = 'route', y = 'totle_alight', data = stop_byTrip, hue="route",
            linewidth=1.5, palette="Set3",
            flierprops = dict(markerfacecolor='0.75', markersize=5,linestyle='none'),
            dodge =False,width=0.6)  
alr.set_xlabel('Routes',fontsize=24);
alr.set_ylabel('Total alighting passengers',fontsize=24);
#alr.legend(bbox_to_anchor=(1.1, 1.0),borderaxespad=0.)
plt.legend([],[], frameon=False)
plt.setp(alr.get_xticklabels(), fontsize = 18)
plt.setp(alr.get_yticklabels(), fontsize = 18)
plt.show()

#Average delay time of buses
fig44, alr = plt.subplots(figsize=(8, 6))
sns.set_style("whitegrid")   
alr=sns.boxplot(x = 'route', y = 'average_delay', data = stop_byTrip, hue="route",
            linewidth=1.5, palette="Set3",
            flierprops = dict(markerfacecolor='0.75', markersize=5,linestyle='none'),
            dodge =False,width=0.6)  
alr.set_xlabel('Routes',fontsize=18);
alr.set_ylabel('Average delay time of buses (seconds)',fontsize=18);
#alr.legend(bbox_to_anchor=(1.1, 1.0),borderaxespad=0.)
plt.legend([],[], frameon=False)
plt.setp(alr.get_xticklabels(), fontsize = 14)
plt.setp(alr.get_yticklabels(), fontsize = 14)
plt.show()



stopO['delay']=stopO['stopinfo_delay']/60
stop_r4=stopO[stopO.route=='4']
stop_r4_6=stop_r4.loc[(stop_r4.stopinfo_started>=28800) & (stop_r4.stopinfo_ended<=32400)]
stop_r4_6['group']='08'
stop_r4_12=stop_r4.loc[(stop_r4.stopinfo_started>=43200) & (stop_r4.stopinfo_ended<=46800)]
stop_r4_12['group']='12'
stop_r4_18=stop_r4.loc[(stop_r4.stopinfo_started>=61200) & (stop_r4.stopinfo_ended<=64800)]
stop_r4_18['group']='17'
stop_r4_23=stop_r4.loc[(stop_r4.stopinfo_started>=82800) & (stop_r4.stopinfo_ended<=86400)]
stop_r4_23['group']='23'
stopR4=pd.concat([stop_r4_6,stop_r4_12,stop_r4_18,stop_r4_23])

#Distribution of bus occupancy on specific hours for route 4
times = ['08', '12','17']
for time in times:
    sns.set_style("ticks")
    subset = stopR4[stopR4['group'] == time]   
    ax=sns.distplot(subset['stopinfo_initialPersons'], hist = False, kde = True,
                 kde_kws = {'linewidth': 2},
                 label = time)   
ax.legend().set_title('Hour')
plt.xlabel('Occupancy of Buses',fontsize = 24)
plt.ylabel('Density',fontsize = 24)
ax.set(xlim=(0, 40))
plt.setp(ax.get_xticklabels(), fontsize = 18)
plt.setp(ax.get_yticklabels(), fontsize = 18)
ax.legend(fontsize=18,title="Hour",title_fontsize = 18)
#plt.title('Route 4',fontsize = 18)
plt.show()


##delay distribution
times = ['08', '12','17']
for time in times:
    sns.set_style("ticks")
    subset = stopR4[stopR4['group'] == time]   
    ax=sns.distplot(subset['delay'], hist = False, kde = True,
                 kde_kws = {'linewidth': 2},
                 label = time)   
ax.legend().set_title('Hour')
plt.xlabel('Delay Time of Buses (min)',fontsize = 24)
plt.ylabel('Density',fontsize = 24)
ax.set(xlim=(0, 900))
plt.setp(ax.get_xticklabels(), fontsize = 18)
plt.setp(ax.get_yticklabels(), fontsize = 18)
#plt.title('Route 4',fontsize = 18)
plt.show()


# edge based output with mean speed for each hour(3600s)
edgeO = pd.read_csv("/EdgeData24h.csv",sep=';')
edgeO=edgeO[["interval_begin","interval_end","edge_id","edge_speed",
             "edge_density","edge_laneDensity","edge_left",
             "edge_occupancy","edge_traveltime",
             "edge_waitingTime","edge_entered"]]
# UNIT: "edge_speed":m/s, "edge_density":#veh/km, "edge_occupancy":%
edgeO['time_begin'] = pd.to_datetime(edgeO['interval_begin'], unit='s').dt.strftime("%H")
edgeO['speed'] = 0.62137*3600*edgeO['edge_speed']/1000

edgeP=edgeO.loc[(edgeO.time_begin=='00') | (edgeO.time_begin=='08') | (edgeO.time_begin=='12') | (edgeO.time_begin=='17')]

times = ['00', '08', '12','17']
for time in times:
    sns.set_style("ticks")
    subset = edgeP[edgeP['time_begin'] == time]   
    ax=sns.distplot(subset['edge_speed'], hist = False, kde = True,
                 kde_kws = {'linewidth': 3},
                 label = time)   
ax.legend().set_title('Hour')
plt.xlabel('Segment average speed (mph)',fontsize = 14)
plt.ylabel('Density',fontsize = 14)
ax.set(xlim=(0, 40))
plt.setp(ax.get_xticklabels(), fontsize = 14)
plt.setp(ax.get_yticklabels(), fontsize = 14)
plt.show()

for time in times:
    sns.set_style("ticks")
    subset = edgeP[edgeP['time_begin'] == time]   
    oc=sns.distplot(subset['edge_occupancy'], hist = False, kde = True,
                 kde_kws = {'linewidth': 3},
                 label = time)   
oc.legend().set_title('Hour')
plt.xlabel('Segment average occupancy (%)',fontsize = 14)
plt.ylabel('Density',fontsize = 14)
oc.set(ylim=(0, 1))
oc.set(xlim=(0, 100))
plt.setp(oc.get_xticklabels(), fontsize = 14)
plt.setp(oc.get_yticklabels(), fontsize = 14)
plt.show()

for time in times:
    sns.set_style("ticks")
    subset = edgeP[edgeP['time_begin'] == time]   
    de=sns.distplot(subset['edge_density'], hist = False, kde = True,
                 kde_kws = {'linewidth': 3},
                 label = time)   
de.legend().set_title('Hour')
plt.xlabel('Segment average density (#Veh/km)',fontsize = 14)
plt.ylabel('Density',fontsize = 14)
de.set(ylim=(0, 0.1))
de.set(xlim=(0, 700))
plt.setp(de.get_xticklabels(), fontsize = 14)
plt.setp(de.get_yticklabels(), fontsize = 14)
plt.show()


figedge1, speed = plt.subplots(figsize=(8, 6))
sns.set_style("whitegrid")   
sns.boxplot(x = 'time_begin', y = 'speed', data = edgeO, hue="time_begin",
            linewidth=1.5,palette="Set2",
            flierprops = dict(markerfacecolor='0.75', markersize=4,linestyle='none'),
            dodge =False,width=0.6) 
speed.set_xlabel('Time',fontsize=18);
speed.set_ylabel('Segment Average Speed (km/h)',fontsize=18);
speed.legend(bbox_to_anchor=(1.12, 1.0),borderaxespad=0.).set_title('Hour')
speed.set(ylim=(0, 110))
plt.setp(speed.get_xticklabels(), fontsize = 14)
plt.setp(speed.get_yticklabels(), fontsize = 14)
plt.show()

figedge2, occup = plt.subplots(figsize=(8, 6))
sns.set_style("whitegrid")   
occup=sns.boxplot(x = 'time_begin', y = 'edge_occupancy', data = edgeO, hue="time_begin",
            linewidth=1.5, palette="Set2",
            flierprops = dict(markerfacecolor='0.75', markersize=4,linestyle='none'),
            dodge =False,width=0.6)  
occup.set_xlabel('Time',fontsize=18);
occup.set_ylabel('Segment Average Occupancy (%)',fontsize=18);
occup.legend(bbox_to_anchor=(1.12, 1.0),borderaxespad=0.).set_title('Hour')
plt.setp(occup.get_xticklabels(), fontsize = 14)
plt.setp(occup.get_yticklabels(), fontsize = 14)
plt.show()

figedge3, density = plt.subplots(figsize=(8, 6))
sns.set_style("whitegrid")   
density=sns.boxplot(x = 'time_begin', y = 'edge_density', data = edgeO, hue="time_begin",
            linewidth=1.5, palette="Set2",
            flierprops = dict(markerfacecolor='0.75', markersize=4,linestyle='none'),
            dodge =False,width=0.6)  
density.set_xlabel('Time',fontsize=18);
density.set_ylabel('Segment Average Density (#veh/km)',fontsize=18);
density.legend(bbox_to_anchor=(1.12, 1.0),borderaxespad=0.).set_title('Hour')
plt.setp(density.get_xticklabels(), fontsize = 14)
plt.setp(density.get_yticklabels(), fontsize = 14)
plt.show()


