library(readxl)
library(dplyr)
#Stop information got from TraCI
data = read_excel("stopsinf_CARTA.xlsx")

read_excel_allsheets <- function(filename, tibble = FALSE) {
  sheets <- readxl::excel_sheets(filename)
  x <- lapply(sheets, function(X) readxl::read_excel(filename, sheet = X))
  if(!tibble) x <- lapply(x, as.data.frame)
  names(x) <- sheets
  x
}
#Stops on each bus route with stop ID in their orders
mysheets <- read_excel_allsheets("buslines.xlsx")

busline = list()
for(k in mysheets){
  busline[[length(busline)+1]] = k %>% mutate(ID = as.character(ID))
}

listBL = list()
for(i in busline){
  join = left_join(i,data,by="ID")
  listBL[[length(listBL)+1]] = join[!is.na(join$edgeID),]
}
names(listBL) = names(mysheets)
nams = names(listBL)
depart = sample(0:3600,95)

fileAPAin<-file.create("BusLines.txt")
write(paste("<routes>"), file = "BusLines.txt", append=TRUE)
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
write(paste("</routes>"), file = "BusLines.txt", append=TRUE)





