import pandas as pd
import numpy as np
import datetime as dt


def init_scheduleinfo(basepath):
     #Read RTC COMMAND TABLE
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
    rtc_data_final['datetime'] = pd.to_datetime(rtc_data_final['timestamp'])

    
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
    global rtc_config_df
    rtc_config_df = pd.read_csv(basepath+"rtc_schedule_index.csv")
    
    rtc_config_df['time'] = rtc_config_df['time_hh'].astype(str) + ":" + rtc_config_df['time_mm'].astype(str) +":00"
    rtc_config_df['time'] = pd.to_datetime(rtc_config_df['time'], format='%H:%M:%S')
    
    rtc_config_df = rtc_config_df.drop(columns=['time_hh', 'time_mm','sid', 'stype', 'status'])

    return
    

# In[ ] :  
def get_scheduled_pwm(tstamp, gid=49):
    pwm = pd.Series()
    sch_applied = rtc_data_final[ rtc_data_final['datetime'] <= tstamp ]
    
    # Data is in Ascending order
    phase = sch_applied.tail(1)['phaseapplied']
    idx = sch_applied.tail(1)['sindex']
    
    ts2 = tstamp.replace(year=1900, month=1, day=1)
    idx = int(idx.get_values()[0])
    rtc_config = rtc_config_df[ (rtc_config_df['sindex'] == idx) & (rtc_config_df['time'] <= ts2) ] 
    
    pwmval = int(rtc_config.tail(1)['pwm'].get_values()[0])
    
 
    phid = int(phase.get_values()[0])
    if(phid==0) :
        pwm = pwm.set_value(1, pwmval)
        pwm = pwm.set_value(2, pwmval)
        pwm = pwm.set_value(3, pwmval)
    else:
        pwm = pwm.set_value(phid, pwmval)

    return pwm

# In[ ]:
    
def init_energymeterdata(basepath):
  
    EnergyMeter = pd.read_csv(basepath+ "energy_table.csv")
    
    #Removing the Sequence no and reg_offset data from energy meter table
    colnames = ['gid','setid','timestamp','reg_name','reg_data']
    em_orig = pd.DataFrame(EnergyMeter,columns = colnames)
    
    #Converting the timestamp object to DateTime Object
    em_orig['timestamp'] =  pd.to_datetime(em_orig['timestamp'], format='%Y%m%d %H:%M:%S')
    
    # To Convert the Rows to columns to create single entry based on setid (reading for every 3 mins)
    global emdata
    emdata = EnergyMeter.pivot_table(index = ['gid','setid','timestamp'], columns='reg_name', values='reg_data')
    
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

    pwm1 = []
    pwm2 = []
    pwm3 = []
    for index, row in emdata.iterrows():
        pwms = get_scheduled_pwm( row['timestamp'] )
        pwm1.append( pwms.get_values()[0] )
        pwm2.append( pwms.get_values()[1] )
        pwm3.append( pwms.get_values()[2] )
        if( (index%1000) == 0 ):
            print(".", end="")
       
    print("Done.")
    
    emdata['pwm1'] = pwm1  
    emdata['pwm2'] = pwm2 
    emdata['pwm3'] = pwm3  

    return




