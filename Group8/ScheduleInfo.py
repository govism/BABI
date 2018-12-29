
import pandas as pd
import numpy as np
import datetime as dt



def init_scheduleinfo():

    #Linux/MAC code to read RTC COMMAND TABLE, uncomment and change file path accordingly
    rtc_data = pd.read_csv("/Users/balajivr/Desktop/BABI/CapData/rtc_command_table.csv")
    
    #Windows code to read RTC COMMAND TABLE, uncomment and change file path accordingly
    #rtc_data = pd.read_csv("D:/BABI/BABICS-master/CapstoneData/rtc_command_table.csv")
    print(rtc_data.head(5))
    
    print(rtc_data.dtypes)
    print(rtc_data.params)

    #Creating dataframe only with relevant fields, removed otherparams like offset
    colnames =['gid','command','params', 'status','timestamp']
    rtc_data = pd.DataFrame(rtc_data, columns=colnames)
    print(rtc_data.head(5))
    print(rtc_data.shape)
    
    #Creating Dataframe without Null timestamp
    rtc_data =rtc_data[rtc_data['timestamp']!= '0000-00-00 00:00:00']
    print(rtc_data.head(5))
    
    #Converting the timestamp object to DateTime object    
    rtc_data['timestamp'] =  pd.to_datetime(rtc_data['timestamp'])
    #rtc_data['timestamp'] =  pd.to_datetime(rtc_data['timestamp'], format='%Y%m%d %H:%M:%S')
    print(rtc_data.dtypes)
    
    #Selection of only RTC_SCHEDULE which does reset and setting configuration of light intensity
    global rtc_data_final
    rtc_data_final = rtc_data[((rtc_data.command=='RTC_SCHEDULE') & (rtc_data.status=='DONE'))]
    print(rtc_data_final.head(5))
    
    temp = pd.DatetimeIndex(rtc_data_final['timestamp'])
    rtc_data_final['date'] = temp.date
    rtc_data_final['time'] = temp.time
    
    rtc_data_final['date'] = pd.to_datetime(rtc_data_final['date'])
    #rtc_data_final['time'] = pd.to_datetime(rtc_data_final['time']).time()
    print(rtc_data_final.head(5))
    #Checking the No of cols 
    print(rtc_data_final.shape)
    
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
    
    # Reading the RTC Schedule configuration data
    #Linux/MAC code to read RTC COMMAND TABLE, uncomment and change file path accordingly
    global rtc_config_df
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
    return
    

# In[ ] :    
init_scheduleinfo()    
    
#def defaultArg( dateime, gid = 49):
#    listpwm = []
#    return listpwm
    
