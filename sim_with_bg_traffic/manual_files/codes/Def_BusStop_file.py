# python version of Def_BusStop_file.R

import pandas as pd
import os

# for testing
if os.path.exists('busStopsCARTA.add.xml'):
    os.remove("busStopsCARTA.add.xml")

#Read xlsx file from folder named "data"
data = pd.read_excel("../data/busstops.xlsx")

#Create new columns 'startpos' and 'endpos' in data based on the "lanepos" in "busstops.xlsx"
data['startPos'] = round(data["lanepos"] - 5, 2)
data['endPos'] = round(data['startPos'] + 5, 2)
data['startPos'][data['startPos']<0] = 0
#Create busStopsCARTA.txt file to write in
f = open("busStopsCARTA.add.xml", "x")
#Write the fist line in the .txt file
f.write("<additional>\n")

# helper function to parse data to html
def parser(r):
    return '\t<busStop id="busStop_' + r['edgeID']+ "_"\
        + r['laneind'] + "_" + r['ID']\
        + '" lane="' + r['edgeID'] + '_'\
        + r['laneind'] + '" startPos="'\
        + r['startPos'] + '" endpos="'\
        + r['endPos'] + '" friendlyPos="1"/>\n'
#Write all the bus stop defination under the "<additional>" 
data["export"] = data.apply(lambda x: parser(x.astype(str)), axis=1)
for index, row in data.iterrows():
    f.write(row['export'])

#Write the last line in the .txt file
f.write("</additional>")
f.close()


