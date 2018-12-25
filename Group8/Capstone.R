
#Library used for EDA
library(tidyr)
library(reshape2)
library(dplyr)
library(ggplot2)
library(data.table)
library(readxl)
#library(xlsx)
#install.packages("WriteXLS")
library(WriteXLS)

#Set the Data files path used for Capstone Project 
sample <- read_xlsx("/Users/balajivr/Desktop/BABI/Capstone/Energy_Master.xlsx",sheet = 1, col_names = TRUE)

#Dcast function used to covert Rows to Columns based on the 20 parameters captured
sampleEM <- dcast(sample, gid+setid+timestamp~reg_name, value.var=c("reg_data"))

#Looking at sampleEM data
head(sampleEM,5) 

#Structure of sampleEM Dataset
str(sampleEM)


#Working with Full Dataset
setwd("/Users/balajivr/Desktop/BABI/CapData/")
getwd()
energyMaster_df = read.csv2("energy_table.csv", header = TRUE, sep=",")

#Structure of the Full dataset to observe what data types are available
str(energyMaster_df)

#Summary of Dataset
summary(energyMaster_df)

# Check whether direct timestamp usage is easier for RTC_Reset calculations etc or splitting Date & Time required
# Splitting Timestamp into Date and Time
# energMeter$Date <- as.Date(energMeter$timestamp)
# energMeter$Time <- format(as.POSIXct(energMeter$timestamp) ,format = "%H:%M:%S")

#Using dcast from reshape2 package to convert the relevant row values into Columns based on setid and timestamp
newEM_df <- dcast(energyMaster_df, gid+setid+timestamp~reg_name, value.var=c("reg_data"))
#newEM_df <- dcast(energyMaster_df, ~reg_name, value.var=c("reg_data"))
remove(newEM_df)
head(newEM_df,5)

#Adding rtc_reset column to New EnergyMeter Dataframe
newEM_df$rtc_reset = 0
#newEM_df <- newEM_df %>% mutate(id = row_number())


#Reading RTC SCHEDULE information RTC Command table
rtc_reset_df = read.csv2("rtc_command_table.csv", header = TRUE, sep=",")

#Structure of RTC Command table dataset
str(rtc_reset_df)

#Data Preparation only for RTC_SCHEDULE leaving other commands RTC_RELAY etc..
rtcShedule=subset(rtc_reset_df,command == "RTC_SCHEDULE")
rtcShedule
#rtcShedule <- rtcShedule %>% mutate(id = row_number()+max(newEM_df$id))

new_df <- merge(x=newEM_df,y=rtcShedule[,c(2:5,7)],by.x = c("gid","timestamp"),by.y = c("gid","timestamp"),all = TRUE)
new_df
#Arranging the new dataset based on timestamp
arranged_df <- new_df[order(as.Date(new_df$timestamp)),]

#To check the sorted data based on timestamp, writing into a excel file
WriteXLS(arranged_df,"/Users/balajivr/Desktop/BABI/Capstone/New_data.xlsx")


#While Ending the Program, Removing all created dataframes 
remove(m1)
remove(new_df)
remove(rtc_reset_df)

#Detaching the attached libraries
detach(tidyr)
detach(reshape2)
detach(dplyr)
detach(ggplot2)
detach(data.table)
detach(readxl)