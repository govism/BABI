#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 30 10:27:25 2018

@author: balajivr
"""
import numpy as np
import pandas as pd
from datetime import datetime

import EnergyMeterInfo as EMI
import ScheduleInfo as SI


def init():
    EMI.init_energymeterdata()
    SI.init_scheduleinfo()
    return
    
#Calling Initialization to create EnergyMeter, Schedule and Configuration dataframe    
init()