# coding: utf-8
# In[ ]:

import pandas as pd
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
# To Convert the Rows to columns to create single entry based on setid (reading for every 3 mins)
emdata = EnergyMeter.pivot_table(index = ['gid','setid','timestamp'], columns='reg_name', values='reg_data')
print(emdata.head(10))
emdata.to_csv('converted_data.csv')

# In[ ]:

#Checking the Data frame for no of rows & columns    
emdata.shape

emdata.describe()

# In[ ]:

# To Write into CSV file for checking whether correctly formed or not.
#emdata.to_csv('emdata1.csv',sep=',' )

# In[ ]:

#writer = pd.ExcelWriter("D:/BABI/BABICS-master/Group8/New_EM_Dataset.xlsx",engine='xlsxwriter')
#emdata.to_excel(writer,sheet_name='Sheet1')
#writer.save()

# In[ ]:

#Linux/MAC code to read RTC COMMAND TABLE, uncomment and change file path accordingly
rtc_data = pd.read_csv("/Users/balajivr/Desktop/BABI/CapData/rtc_command_table.csv")

#Windows code to read RTC COMMAND TABLE, uncomment and change file path accordingly
#rtc_data = pd.read_csv("D:/BABI/BABICS-master/CapstoneData/rtc_command_table.csv")
print(rtc_data.head(10))
print(rtc_data.shape)

print(rtc_data.dtypes)


# In[ ]:

#Creating dataframe only with relevant fields, removed otherparams like offset
colnames =['gid','command','params', 'status','timestamp']
rtc_data = pd.DataFrame(rtc_data, columns=colnames)
print(rtc_data.head(5))
print(rtc_data.shape)

# In[ ]:
#Selection of only RTC_SCHEDULE which does reset and setting configuration of light intensity
rtc_data_final=rtc_data[rtc_data.command=='RTC_SCHEDULE']
print(rtc_data_final.head(5))

# In[ ]:
# Experimental code with merge_asof function
#RTCResetdf = pd.Dataframe
#df_merge_asof = pd.merge_asof(trades, quotes,
#              on='time',
#              by='ticker')
#df_merge_asof
#MergeEnergyRTC = pd.merge_asof(emdata, rtc_data_final, on='timestamp', by='gid')

#Merging 2 Dataframes Energymeter and rtc schedule data into single dataframe
MergeEnergyRTC = pd.merge(emdata, rtc_data_final, how='left',on=['gid','timestamp'])

#MergeEnergyRTC = pd.merge(emdata, rtc_data_final, on="timestamp")
print(MergeEnergyRTC.shape)
print(MergeEnergyRTC.head(10))
print(MergeEnergyRTC.tail(10))
# In[ ]:



# In[ ]:

#RTCReset[RTCReset.columns[4]]=RTCReset[RTCReset.columns[4]].str.strip()
#RTCReset[RTCReset.columns[4]]
#RTCReset[RTCReset.columns[6]]=RTCReset[RTCReset.columns[6]].str.strip()
#RTCReset[RTCReset.columns[6]]
#df= pd.DataFrame(columns=["gid","setid","Frequency", 
#                          "Voltage Phase R","Voltage Phase Y","Voltage Phase B",
#                          "Voltage Phase R to Y","Voltage Phase Y to B","Voltage Phase B to R",
#                          "Current Phase R","Current Phase Y","Current Phase B",
#                          "Power Factor R","Power Factor Y","Power Factor B","Total Power Factor",
#                          "Active Power R","Active Power Y","Active Power B","Total Active Power",
#                          "Active Energy","Load Hours","timestamp","rtc_reset"])
#df
#
## In[ ]:
#
#df.loc[i/WRAP_SIZE]=[gid,setid,freq, Volt_PhaseR,Volt_PhaseY,Volt_PhaseB,Volt_PhaseR2Y,Volt_PhaseY2B,Volt_PhaseB2R,
#                        Cur_PhaseR,Cur_PhaseY,Cur_PhaseB, Pow_FactR,Pow_FactY,Pow_FactB,Tot_Pow_Fact, Act_PowR,
#                        Act_PowY,Act_PowB, Tot_Act_Power, Act_Energy,Load_Hours, timestamp, 0]
#                        
#   
#   writer = pd.ExcelWriter("/Users/balajivr/Desktop/BABI/CapData/IoT_EnergyMeter_RTC_Data.xlsx",engine='xlsxwriter')
#   df.to_excel(writer,sheet_name='Sheet1')
#   writer.save()
#
## In[ ]:
#
#EnergyMeter
