setwd("/Users/balajivr/Desktop/BABI/Capstone/Health")
getwd()

#install.packages("foreign")
#library(foreign)

# mydata <- read.xport("LLCP2017.XPT")
# summary(mydata)
# plot_missing(prData)
# create_report(prData)

library(DataExplorer)
library(Hmisc)

prData <- read.csv("new_cdc_data.csv", header = TRUE)
summary(prData)
diabData <- prData[1:18]

diabData$PE_freq<-ifelse((diabData$exeroft1>=100 & diabData$exeroft1 <200),((diabData$exeroft1%%100)/7)*30,(diabData$exeroft1%%200))
diabData$PE_freq<- round(diabData$PE_freq)

diabData$SE_freq<-ifelse((diabData$exeroft2>=100 & diabData$exeroft2 <200),((diabData$exeroft2%%100)/7)*30,(diabData$exeroft2%%200))
diabData$SE_freq<- round(diabData$SE_freq)

#Exploratary Data Analysis
head(diabData$diabete3,10)
tail(diabData$diabete3,10)
describe(diabData)
str(diabData)

#Checking Diabete3 values..
levels(diabData$diabete3)
frequency(diabData$diabete3)

#Data Preparation for Diabetes prediction by creating a diabetPred column from existing diabete3
diabData$diabetPred=diabData$diabete3
unique(diabData$diabetPred)

#Converting missing values
diabData$diabetPred[is.na(diabData$diabetPred)] <- 0
unique(diabData$diabetPred)

#Converting 0 and 1s from values ranging from 1 to 9 to do diabetes prediction
diabData$diabetPred=ifelse(diabData$diabetPred==1,1,0)
unique(diabData$diabetPred)
