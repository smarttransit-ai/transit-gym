library(readxl)
library(dplyr)
#Read "stopsinf_CARTA.xlsx" (see folder named "data")
data = read_excel("stopsinf_CARTA.xlsx")

#Function to read all sheets from an xlsx file
read_excel_allsheets <- function(filename, tibble = FALSE) {
  sheets <- readxl::excel_sheets(filename)
  x <- lapply(sheets, function(X) readxl::read_excel(filename, sheet = X))
  if(!tibble) x <- lapply(x, as.data.frame)
  names(x) <- sheets
  x
}

#buslines.xlsx is the file extracting busstop ID in sequence along each route from 'CARTA Summary Route Data_Remix Feb Schedule.xlsx'.
#Each route is in each sheet, the sheet name is just the route name.
#Read all the sheets
mysheets <- read_excel_allsheets("buslines.xlsx")

#change the format of mysheets to a dataframe named 'busline'
busline = list()
for(k in mysheets){
  busline[[length(busline)+1]] = k %>% mutate(ID = as.character(ID))
}

#Get the extra busstop information along each route by matching the busstop ID between data and busline.
listBL = list()
for(i in busline){
  join = left_join(i,data,by="ID")
  listBL[[length(listBL)+1]] = join[!is.na(join$edgeID),]
}
#get name of each route based on sheet name              
names(listBL) = names(mysheets)             
nams = names(listBL)     
#randomly set departing time
depart = sample(0:3600,95)

#create a file to write in              
fileAPAin<-file.create("BusLines.txt")
              
#write the first line on the file              
write(paste("<routes>"), file = "BusLines.txt", append=TRUE)
#write the trip family for each trip    
#e.g. <trip id="1AltonPark_A_inbound" type="BUS" depart="0" color="1,1,0" departPos="stop">
for (i in seq_along(listBL)){
  write(paste("\t<trip id=\"", 
              nams[i],
              "\" type=\"BUS",
              "\" depart=\"",
              depart[i],
              "\" color=\"1,1,0",
              "\" departPos=\"stop",
              "\">",
              sep=""), file = "BusLines.txt", append=TRUE)
  
  #write sequential stop id and duration time under the trip family 
  #e.g. <stop busStop="busStop_-29660_0_95" duration="2"/>
  for (j in 1:length(listBL[[i]]$ID)){
  write(paste("\t\t<stop busStop=\"busStop_",
              listBL[[i]][j,'edgeID'],"_",
              listBL[[i]][j,'laneind'],"_",
              listBL[[i]][j,'ID'],
              "\" duration=\"2",
              "\"/>",
              sep=""), file = "BusLines.txt", append=TRUE)
  }
  write(paste("\t</trip>"), file = "BusLines.txt", append=TRUE)
}

#write the last line on the file
write(paste("</routes>"), file = "BusLines.txt", append=TRUE)





