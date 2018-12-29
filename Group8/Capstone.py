# coding: utf-8
# In[ ]:
import numpy as np
import pandas as pd
from datetime import datetime


# In[ ]:
WRAP_SIZE=20

#if you are running on Windows, then uncomment and change the file path 
#filename = "D:/BABI/BABICS-master/Group8/Energy_Master.xlsx"
#filename = "D:/BABI/BABICS-master/CapstoneData/energy_table.csv"

#if you are running on Linux/MAC, then uncomment and change the file path
#filename = "/Users/balajivr/Desktop/BABI/Capstone/Energy_Master.xlsx"
filename = "/Users/balajivr/Desktop/BABI/CapData/energy_table.csv"

#EnergyMeter = pd.read_excel(filename,0)
EnergyMeter = pd.read_csv(filename)
print(EnergyMeter.head(5))

# In[ ]:
#EnergyMeter.describe

#Datatypes of Energymeter dataset
EnergyMeter.dtypes

# In[ ]:
# can use Index location also to select the columns.
#em_orig = EnergyMeter.iloc[:,2:3,5:7]

#Removing the Sequence no and reg_offset data from energy meter table
colnames = ['gid','setid','timestamp','reg_name','reg_data']
em_orig = pd.DataFrame(EnergyMeter,columns = colnames)
print(em_orig.head(5))

# In[ ]:
#Converting the timestamp object to DateTime Object
em_orig['timestamp'] =  pd.to_datetime(em_orig['timestamp'], format='%Y%m%d %H:%M:%S')
print(em_orig.head(5))
print(em_orig.dtypes)

# In[ ]:
# To Convert the Rows to columns to create single entry based on setid (reading for every 3 mins)
emdata = EnergyMeter.pivot_table(index = ['gid','setid','timestamp'], columns='reg_name', values='reg_data')
print(emdata.head(10))
#emdata.to_csv('converted_data.csv')
#Checking the Data frame for no of rows & columns    
print(emdata.shape)
print(emdata.describe())

# In[ ]:
#Inorder to access the index column, doing the reset_index to access emdata['gid'], emdata['timestamp']
emdata.index.names
emdata.reset_index(inplace=True)
emdata.index.names

# In[ ]:
#Creating a New Column fro RTC_RESET 
emdata['rtc_reset']=0

# In[ ]:
#emdata['time'],emdata['date']= emdata['timestamp'].apply(lambda x:x.time()), emdata['timestamp'].apply(lambda x:x.date())
temp = pd.DatetimeIndex(emdata['timestamp'])
emdata['date'] = temp.date
emdata['time'] = temp.time
emdata['date'] = pd.to_datetime(emdata['date'])
emdata['timestamp'] = pd.to_datetime(emdata['timestamp'])
#emdata['time'] = pd.to_datetime(emdata['time'])
print(emdata.head(5))
#Checking the No of cols 
print(emdata.shape)
print(emdata.dtypes)

# In[ ]:
#  df = emdata['timestamp'] > '2017-12-01  09:42:59' 
#emdata[emdata.date.between('2017-12-12 04:40:44', '2017-12-12 04:52:50')]
# In[ ]:
# To Write into CSV file for checking whether correctly formed or not.
#emdata.to_csv('emdata1.csv',sep=',' )

#writer = pd.ExcelWriter("D:/BABI/BABICS-master/Group8/New_EM_Dataset.xlsx",engine='xlsxwriter')
#emdata.to_excel(writer,sheet_name='Sheet1')
#writer.save()

# In[ ]:

#Linux/MAC code to read RTC COMMAND TABLE, uncomment and change file path accordingly
rtc_data = pd.read_csv("/Users/balajivr/Desktop/BABI/CapData/rtc_command_table.csv")

#Windows code to read RTC COMMAND TABLE, uncomment and change file path accordingly
#rtc_data = pd.read_csv("D:/BABI/BABICS-master/CapstoneData/rtc_command_table.csv")
print(rtc_data.head(5))

print(rtc_data.dtypes)
print(rtc_data.params)
# In[ ]:

#Creating dataframe only with relevant fields, removed otherparams like offset
colnames =['gid','command','params', 'status','timestamp']
rtc_data = pd.DataFrame(rtc_data, columns=colnames)
print(rtc_data.head(5))
print(rtc_data.shape)

#Creating Dataframe without Null timestamp
rtc_data =rtc_data[rtc_data['timestamp']!= '0000-00-00 00:00:00']
print(rtc_data.head(5))

# In[ ]:
#Converting the timestamp object to DateTime object    
rtc_data['timestamp'] =  pd.to_datetime(rtc_data['timestamp'])
#rtc_data['timestamp'] =  pd.to_datetime(rtc_data['timestamp'], format='%Y%m%d %H:%M:%S')
print(rtc_data.dtypes)

# In[ ]:
#Selection of only RTC_SCHEDULE which does reset and setting configuration of light intensity
rtc_data_final=rtc_data[((rtc_data.command=='RTC_SCHEDULE') & (rtc_data.status=='DONE'))]
print(rtc_data_final.head(5))

# In[ ]:

temp = pd.DatetimeIndex(rtc_data_final['timestamp'])
rtc_data_final['date'] = temp.date
rtc_data_final['time'] = temp.time

rtc_data_final['date'] = pd.to_datetime(rtc_data_final['date'])
#rtc_data_final['time'] = pd.to_datetime(rtc_data_final['time']).time()
print(rtc_data_final.head(5))
#Checking the No of cols 
print(rtc_data_final.shape)

# In[ ]:
#Spliting the Params into phaseline applied and what sindex configuration applied
#rtc_data_final['phaseapplied']=rtc_data_final[rtc_data_final.params]
# new data frame with split value columns 
newcols = rtc_data_final['params'].str.split(":", n=1, expand = True) 
  
# making seperate first name column from new data frame 
rtc_data_final['phaseapplied'] = newcols[0] 
  
# making seperate last name column from new data frame 
rtc_data_final['sindex'] = newcols[1] 

print(rtc_data_final.head(5))
print(rtc_data_final.dtypes)

# In[ ]:
# Reading the RTC Schedule configuration data
#Linux/MAC code to read RTC COMMAND TABLE, uncomment and change file path accordingly
rtc_config_df = pd.read_csv("/Users/balajivr/Desktop/BABI/CapData/rtc_schedule_index.csv")

#Windows code to read RTC COMMAND TABLE, uncomment and change file path accordingly
#rtc_data = pd.read_csv("D:/BABI/BABICS-master/CapstoneData/rtc_command_table.csv")
rtc_config_df = rtc_config_df[['sindex','time_hh','time_mm', 'pwm']]
rtc_config_df['time_hh'] = rtc_config_df['time_hh'].astype(str)
rtc_config_df['time_mm'] = rtc_config_df['time_mm'].astype(str)

#rtc_config_df['time'] = datetime.time(rtc_config_df['time_hh'],rtc_config_df['time_mm'])
#rtc_config_df['time'] = datetime.datetime.combine(datetime.time(rtc_config_df['time_hh'],rtc_config_df['time_mm']))
rtc_config_df['time'] = rtc_config_df['time_hh'] + ":" + rtc_config_df['time_mm'] +":00"
#string.format(rtc_config_df['time'], '%H:%M:%S')
#rtc_config_df['time'] = format(rtc_config_df['time'], '%H:%M:%S')
rtc_config_df['time'] = pd.to_datetime(rtc_config_df['time'], format='%H:%M:%S')
#check how to convert to time object 
#rtc_config_df['time'] = pd.to_datetime(rtc_config_df['time'])
print(rtc_config_df.head(10))
print(rtc_config_df.shape)
# In[ ]:
print(rtc_config_df.dtypes)
print(rtc_data_final.dtypes)
print(emdata.dtypes)

# In[ ]:
sch_ts = []    
for index, row in rtc_data_final.iterrows():
    #emdata[emdata.date.between('2017-12-12 ', '2017-12-12')]
    print(row.sindex)
    startdate = row.date
    print (startdate)
    next = next(rtc_data_final.iterrows())
    temp_df = emdata[(emdata['timestamp'] > startdate) & (emdata['timestamp'] < next.date)]
#    temp_df = pd.date_range(startdate, nextstartdate)
    temp_df
    #temp_df = pd.date_range(emdata[row.date], emdata[row.date])
    #df[(df['dt'] > '2014-07-23 07:30:00') & (df['dt'] < '2014-07-23 09:00:00')]
    #print(len(temp_df))

# In[ ]:
#Merging all table data in single dataframe for building models
pwm=[]
phaseapplied=[]
sindex=[]
for index, row in rtc_data_final.iterrows():
    #print (row["timestamp"], row["gid"])
    #rtc_date=pd.to_datetime(row["timestamp"]).date()
    #print(row.date)
    emdata[emdata.date.between('2017-12-12 ', '2017-12-12')]
    temp_df = pd.date_range(emdata[row.date], emdata[row.date])
    temp_df = emdata[emdata['date']== row.date]
#    count = temp_df.count
    print(len(temp_df))
    if (len(temp_df) > 0):
        print("RTC Date: ", row.date)   
        for ind, emrow in emdata.iterrows():
            em_date = pd.to_datetime(emrow["date"]).date()
            #print("EnergyMeter Date:", em_date)
            if (em_date==row.date):
                print("Date is matching:", row.date)
                emrow.reset = 1
                sindex.append(row.sindex)
                phaseapplied.append(row.phaseapplied)
                timeschedule = rtc_config_df[rtc_config_df['sindex']]
                pwm.append()
            else:
                print("Date is not matching", row.date, em_date)

# In[ ]:
#Merging all table data in single dataframe for building models
#
for index, row in rtc_data_final.iterrows():
    #print (row["timestamp"], row["gid"])
    rtc_date=pd.to_datetime(row["date"]).date()
    print("RTC Date: ", rtc_date)

    for ind, emrow in emdata.iterrows():
        em_date = pd.to_datetime(emrow["timestamp"]).date()
        #print("EnergyMeter Date:", em_date)
        if (em_date==rtc_date):
            print("Date is matching:", rtc_date)
        else:
            print("Date is not matching", rtc_date, em_date)
            #row['reset']=1
            #if (pd.to_datetime(emrow["timestamp"]).date() > pd.to_datetime(row["timestamp"]).date()):
                #emrow['resettimediff'] = emrow['timestamp'] - row['timestamp']
                #print(emrow.difference)
    #print(date)
