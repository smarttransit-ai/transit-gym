##charger load from SOC

import math
import Bus_Read as br
Filepath = 'charge_sch.csv'

bus_info=br.Busread(Filepath)
#granted_time=55500+1*60
print("this is returned \n",bus_info)
location1=[]
soc1=[]
ch_start_time1=[]

##

for bus in bus_info:
    #if bus_info[bus]['charger_loc'] =='1':
    soc1.append(bus_info[bus]['soc'])
    location1.append(bus_info[bus]['charger_loc'])
    hours=float(bus_info[bus]['hh'])
    min=float(bus_info[bus]['mm'])
    st_time=hours*3600+min*60
    ch_start_time1.append(st_time)

## For
# location2=[]
# soc2=[]
# ch_start_time2=[]
# for bus in bus_info:
#     if bus_info[bus]['charger_loc'] =='2':
#         soc2.append(bus_info[bus]['soc'])
#         location1.append(bus_info[bus]['charger_loc'])
#         hours=float(bus_info[bus]['hh'])
#         min=float(bus_info[bus]['mm'])
#         st_time=hours*3600+min*60
#         ch_start_time1.append(st_time)

ch_end_time1 =[]

for i in range(len(ch_start_time1)):
    #if location[i]=='1':
    end_time=round((-53.846*float(soc1[i])+43.077)*60+ch_start_time1[i]) # user defined based on charger profile
    ch_end_time1.append(end_time)

##For charger location 2
# for i in range(len(ch_start_time2)):
#     if location[i]=='2':
#         end_time=round((-53.846*float(soc2[i])+43.077)*60+ch_start_time2[i]) # user defined based on charger profile
#         ch_end_time2.append(end_time)

# # introduce a flag for a forced end time and overwrite the flagged buses and times.

#realtime charger load function
def Chload1(granted_time):
    ch_load1=0
    for i in range(len(ch_start_time1)):
        #if location[i]=='1':
        if granted_time>ch_start_time1[i] and granted_time<ch_end_time1[i]:
            soc_current=0.0186*((granted_time-ch_start_time1[i])/60)+float(soc1[i]) # user defined- based on how SOC evolved during charging
            ch_load1=ch_load1+(-4.2488*soc_current*100+412.61) # user defined - based on how the charger load is determined based on soc value
    print ("charger load 1 being sent to Gridlabd is ", ch_load1)
    return ch_load1

## Charger load for location 2
# def Chload2(granted_time):
#     ch_load2=0
#     for i in range(len(ch_start_time1)):
#         if location[i]=='2':
#             if granted_time>ch_start_time1[i] and granted_time<ch_end_time1[i]:
#                 soc_current=0.0186*((granted_time-ch_start_time1[i])/60)+float(soc2[i]) # user defined- based on how SOC evolved during charging
#                 ch_load2=ch_load2+(-4.2488*soc_current*100+412.61) # user defined - based on how the charger load is determined based on soc value
#     print ("chargerload being sent to Gridlabd is ", ch_load2)
#     return ch_load2


#print(ch_load)

#print ("Done reading charger load function")

