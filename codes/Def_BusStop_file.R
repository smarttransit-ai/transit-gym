library(readxl)
data = read_excel("stopsinf_CARTA.xlsx")
data$startPos = round(data$lanepos,digit=2)
data$endPos = data$startPos+10
#Create txt file to write in
fileStop<-file.create("busStopsCARTA.txt")
write(paste("<additional>"),file="busStopsCARTA.txt") 
for (i in 1:length(data$edgeID)){
write(paste("\t<busStop id=\"busStop_",
              data[i,'edgeID'],"_",
              data[i,'laneind'],"_",
              data[i,'ID'],
              "\" lane=\"",
              data[i,'edgeID'],"_",
              data[i,'laneind'],
              "\" startPos=\"",
              data[i,'startPos'],
              "\" endPos=\"",
              data[i,'endPos'],
              "\" friendlyPos=\"1",
              "\"/>",sep=""), file = "busStopsCARTA.txt", append=TRUE)
}
write(paste("</additional>"),file="busStopsCARTA.txt",append=TRUE) 

