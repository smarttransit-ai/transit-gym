import pandas as pd
import os

# for testing
if os.path.exists('detector.add.xml'):
    os.remove("detector.add.xml")

#Read xlsx file from folder named "data"
data = pd.read_excel("../data/sumoCoordinate.xlsx")
data['Name_id']=data['Name_id'].astype(str)
data['Final_Edge_Id']=data['Final_Edge_Id'].astype(str)
data['lanepos']=data['lanepos'].astype(str)



#Create vehtype.add.xml file to write in
f = open("detector.add.xml", "x")
#Write the fist line in the .txt file
f.write("<additional>\n")
# helper function to parse data to html
def parser(r):
    return '\t<inductionLoop id="' + r['Name_id']+ '" lene="'\
        + r['Final_Edge_Id'] + '" pos="'+ r['lanepos'] + '" file="'+ 'out.xml' +'" freq="300" friendlyPos="True"/>\n'
#Write all the detector coordiates defination under the "<additional>"
data["export"] = data.apply(lambda x: parser(x.astype(str)), axis=1)
for index, row in data.iterrows():
    f.write(row['export'])

#Write the last line in the .txt file
f.write("</additional>")
f.close()
