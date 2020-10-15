#This code is to create busStopsCARTA.xml file.

library(readxl)
#Read xlsx file from folder named "data"
data = read_excel("stopsinf_CARTA.xlsx")

#Create new columns 'startpos' and 'endpos' in data based on the "lanepos" in "stopsinf_CARTA.xlsx"
data$startPos = round(data$lanepos,digit=2)
data$endPos = data$startPos+10

#Create busStopsCARTA.txt file to write in
fileStop<-file.create("busStopsCARTA.txt")

#Write the fist line in the .txt file
write(paste("<additional>"),file="busStopsCARTA.txt") 

#Write all the bus stop defination under the "<additional>" 
for (i in 1:length(data$edgeID)){
write(paste("\t<busStop id=\"busStop_", #Create id for busstop based on columns 'edgeID', 'laneind' and "ID" in data. e.g. busStop id="busStop_-1489_0_12"
              data[i,'edgeID'],"_",
              data[i,'laneind'],"_",
              data[i,'ID'],
              "\" lane=\"",             #Create lane name according to 'edgeID' and 'laneind'. e.g. lane="-1489_0"
              data[i,'edgeID'],"_",
              data[i,'laneind'],
              pos"\" startPos=\"",      #start position of busstop. e.g. startPos="33.25"
              data[i,'startPos'],
              "\" endPos=\"",
              data[i,'endPos'],         #end position of busstop. e.g. endPos="43.25"
              "\" friendlyPos=\"1",
              "\"/>",sep=""), file = "busStopsCARTA.txt", append=TRUE)
}

#Write the last line in the .txt file
write(paste("</additional>"),file="busStopsCARTA.txt",append=TRUE) 

