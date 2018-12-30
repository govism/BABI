import numpy as np
import pandas as pd
from datetime import datetime

import DataPrep as DP

def init():
    path = "C:/Govi/BABI/Capstone/Wisys/CapstoneData/"
    DP.init_scheduleinfo(path)
    DP.init_energymeterdata(path)
    return
    
#Calling Initialization to create EnergyMeter, Schedule and Configuration dataframe    
init()