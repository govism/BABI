#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 18:12:19 2018

@author: balajivr
"""

# coding: utf-8
# In[ ]:
import numpy as np
import pandas as pd
from datetime import datetime

def init_energymeterdata():
        
    #if you are running on Windows, then uncomment and change the file path 
    #filename = "D:/BABI/BABICS-master/Group8/Energy_Master.xlsx"
    #filename = "D:/BABI/BABICS-master/CapstoneData/energy_table.csv"
    
    #if you are running on Linux/MAC, then uncomment and change the file path
    #filename = "/Users/balajivr/Desktop/BABI/Capstone/Energy_Master.xlsx"
    filename = "/Users/balajivr/Desktop/BABI/CapData/energy_table.csv"
    
    #EnergyMeter = pd.read_excel(filename,0)
    EnergyMeter = pd.read_csv(filename)
    print(EnergyMeter.head(5))
    
    #EnergyMeter.describe
    
    #Datatypes of Energymeter dataset
    EnergyMeter.dtypes
    
    # can use Index location also to select the columns.
    #em_orig = EnergyMeter.iloc[:,2:3,5:7]
    
    #Removing the Sequence no and reg_offset data from energy meter table
    colnames = ['gid','setid','timestamp','reg_name','reg_data']
    em_orig = pd.DataFrame(EnergyMeter,columns = colnames)
    print(em_orig.head(5))
    
    #Converting the timestamp object to DateTime Object
    em_orig['timestamp'] =  pd.to_datetime(em_orig['timestamp'], format='%Y%m%d %H:%M:%S')
    print(em_orig.head(5))
    print(em_orig.dtypes)
    
    # To Convert the Rows to columns to create single entry based on setid (reading for every 3 mins)
    global emdata
    emdata = EnergyMeter.pivot_table(index = ['gid','setid','timestamp'], columns='reg_name', values='reg_data')
    print(emdata.head(10))
    #emdata.to_csv('converted_data.csv')
    #Checking the Data frame for no of rows & columns    
    print(emdata.shape)
    print(emdata.describe())
    
    #Inorder to access the index column, doing the reset_index to access emdata['gid'], emdata['timestamp']
    emdata.index.names
    emdata.reset_index(inplace=True)
    emdata.index.names
    
    #Creating a New Column fro RTC_RESET 
    emdata['rtc_reset']=0
    
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
    return


# In[ ]:
init_energymeterdata()
