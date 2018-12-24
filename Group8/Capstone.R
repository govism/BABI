
#Library used for EDA
library(tidyr)
library(reshape2)
library(dplyr)
library(ggplot2)
library(data.table)
library(readxl)

#Set the Data files path used for Capstone Project 
sample <- read_excel("/Users/balajivr/Desktop/BABI/Capstone/Energy_Master.xlsx",sheet = 1, col_names = TRUE)

#Dcast function used to covert Rows to Columns based on the 20 parameters captured
sampleEM <- dcast(sample, gid+setid+timestamp~reg_name, value.var=c("reg_data"))

head(sampleEM,5) 

#Working with Full Dataset
setwd("/Users/balajivr/Desktop/BABI/CapData/")
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

head(newEM_df,5)

#Adding rtc_reset column to New EnergyMeter Dataframe
newEM_df$rtc_reset = 0


#Reading RTC SCHEDULE information RTC Command table
rtc_reset_df = read.csv2("rtc_command_table.csv", header = TRUE, sep=",")

#Structure of RTC Command table dataset
str(rtc_reset_df)

#Data Preparation only for RTC_SCHEDULE leaving other commands RTC_RELAY etc..
rtcShedule=subset(rtc_reset_df,command == "RTC_SCHEDULE")
rtcShedule

#merge(newEM_df, rtcShedule[, c("command", "params","status")], by=c("timestamp","gid"), all = TRUE)
newEM_df = merge(newEM_df, rtcShedule[, c("command", "params","status")], by.y="timestamp")

