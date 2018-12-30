import pandas as pd
import numpy as np
import datetime as dt


def init_scheduleinfo(basepath):
      #Linux/MAC code to read RTC COMMAND TABLE, uncomment and change file path accordingly
    rtc_data = pd.read_csv(basepath +"rtc_command_table.csv")
    
    #Creating dataframe only with relevant fields, removed otherparams like offset
    colnames =['gid','command','params', 'status','timestamp']
    rtc_data = pd.DataFrame(rtc_data, columns=colnames)
      
    #Creating Dataframe without Null timestamp
    rtc_data =rtc_data[rtc_data['timestamp']!= '0000-00-00 00:00:00']
    
    #Converting the timestamp object to DateTime object    
    rtc_data['timestamp'] =  pd.to_datetime(rtc_data['timestamp'])
    
    #Selection of only RTC_SCHEDULE which does reset and setting configuration of light intensity
    global rtc_data_final
    rtc_data_final = rtc_data[((rtc_data.command=='RTC_SCHEDULE') & (rtc_data.status=='DONE'))]
      
    temp = pd.DatetimeIndex(rtc_data_final['timestamp'])
    rtc_data_final['date'] = temp.date
    rtc_data_final['time'] = temp.time
    
    rtc_data_final['date'] = pd.to_datetime(rtc_data_final['date'])

    
    #Spliting the Params into phaseline applied and what sindex configuration applied
    #rtc_data_final['phaseapplied']=rtc_data_final[rtc_data_final.params]
    # new data frame with split value columns 
    newcols = rtc_data_final['params'].str.split(":", n=1, expand = True) 
      
    # making seperate first name column from new data frame 
    rtc_data_final['phaseapplied'] = newcols[0] 
      
    # making seperate last name column from new data frame 
    rtc_data_final['sindex'] = newcols[1] 
    
    rtc_data_final = rtc_data_final.drop(columns=['command', 'params', 'status', 'timestamp'])
    
    # Reading the RTC Schedule configuration data
    #Linux/MAC code to read RTC COMMAND TABLE, uncomment and change file path accordingly
    global rtc_config_df
    rtc_config_df = pd.read_csv(basepath+"rtc_schedule_index.csv")
    
    rtc_config_df['time'] = rtc_config_df['time_hh'].astype(str) + ":" + rtc_config_df['time_mm'].astype(str) +":00"
    rtc_config_df['time'] = pd.to_datetime(rtc_config_df['time'], format='%H:%M:%S')
    
    rtc_config_df = rtc_config_df.drop(columns=['time_hh', 'time_mm','sid', 'stype', 'status'])

    return
    

# In[ ] :  
def get_scheduled_pwm(tstamp, gid=49):
    pwm = pd.Series()
    sch_applied = rtc_data_final[ rtc_data_final['date'] <= tstamp ]

    # Data is in Ascending order
    phase = sch_applied.tail(1)['phaseapplied']
    idx = sch_applied.tail(1)['sindex']
    
    ts2 = ts1.replace(year=1900, month=1, day=1)
    idx = int(idx.get_values()[0])
    rtc_config = rtc_config_df[ (rtc_config_df['sindex'] == idx) & (rtc_config_df['time'] <= ts2) ] 
    
    pwmval = int(rtc_config.tail(1)['pwm'].get_values()[0])
    
 
    phid = int(phase.get_values()[0])
    if(phid==0) :
        pwm = pwm.set_value(1, pwmval)
        pwm = pwm.set_value(2, pwmval)
        pwm = pwm.set_value(3, pwmval)
    elif(phid == 1 ):
        pwm = pwm.set_value(1, pwmval)
    elif(phid == 2 ):
        pwm = pwm.set_value(2, pwmval)
    elif(phid == 3 ):
       pwm = pwm.set_value(3, pwmval)

    return pwm

# In[ ] :
ts1 = pd.to_datetime("19-09-2018  16:45:00")
init_scheduleinfo("C:/Govi/BABI/Capstone/Wisys/CapstoneData/")    
pwms = get_scheduled_pwm(ts1)


