import pandas as pd
import os

# for testing
if os.path.exists('vehtype.add.xml'):
    os.remove("vehtype.add.xml")

#Read xlsx file from folder named "data"
data = pd.read_excel("../data/BUS_type.xlsx")
data['BusID']=data['BusID'].astype(str)
data['Capacity']=data['Capacity'].astype(str)
#Create vehtype.add.xml file to write in
f = open("vehtype.add.xml", "x")
#Write the fist line in the .txt file
f.write("<additional>\n")
# helper function to parse data to html
def parser(r):
    return '\t<vType id="Gillig_' + r['BusID']+ '" accel="'\
        + r['Accel'] + '" decel="'+ r['Decel'] + '" sigma="0.5" length="'\
        + r['Length']+'" minGap="3" maxSpeed="'+ r['maxSpeed']+'" personCapacity="'\
        + r['Capacity']+'" guiShape="bus"/>\n'
#Write all the bus type defination under the "<additional>" 
data["export"] = data.apply(lambda x: parser(x.astype(str)), axis=1)
for index, row in data.iterrows():
    f.write(row['export'])

#Write the last line in the .txt file
f.write("</additional>")
f.close()
