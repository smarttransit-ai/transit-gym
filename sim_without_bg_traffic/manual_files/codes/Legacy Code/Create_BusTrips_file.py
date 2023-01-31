#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 02:43:23 2020

@author: danielgui
"""

import pandas as pd
import os
import random as rand

# testing
if os.path.exists('BusLines.xml'):
    os.remove("BusLines.xml")

# read from stopsinf
data = pd.read_excel("../data/stopsinf_CARTA.xlsx", index_col = "ID")
# read from buslines.xlsx into a dictionary of dataframes
busline = {}
xl = pd.ExcelFile("../data/buslines.xlsx")
for sheet in xl.sheet_names:
    busline[sheet] = pd.read_excel(xl, sheet_name=sheet, index_col = 'ID')
    
# join each of those dataframe with stopsinf
for tripid, df in busline.items():
    busline[tripid] = df.join(data, how='inner')
    
#Create BusLines.xml file to write in
f = open("BusLines.xml", "x")

# write first line
f.write("<routes>\n")

for tripid, df in busline.items():
    # FIXME: depart
    df['ID'] = df.index
    f.write('\t<trip id="'+tripid+'" type="BUS" depart="' + str(rand.randint(0, 3600)) +
            '" color="1,1,0" departPos="stop">\n')
    # helper function to parse data to html
    def parser(r):
        return '\t\t<stop busStop="busStop_' + r['edgeID']+ "_"\
            + r['laneind'] + "_" + r['ID']\
            + '" duration="2"/>\n'
    #Write all the bus stop defination under the "<additional>" 
    df["export"] = df.apply(lambda x: parser(x.astype(str)), axis=1)
    for index, row in df.iterrows():
        f.write(row['export'])
    f.write("\t</trip>")

f.write("</routes>")
f.close
    
        
    



    
