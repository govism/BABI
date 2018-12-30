import numpy as np
import pandas as pd
from datetime import datetime

import DataPrep as DP

# In[ ]:
path = "C:/Govi/BABI/Capstone/Wisys/CapstoneData/"
DP.init_scheduleinfo(path)
emeter_data = DP.init_energymeterdata(path)
emeter_data['power diff'] = emeter_data['expected power']-emeter_data['Total Active Power']

# In[ ]:
 emeter_data.to_csv(path+"Final_data.csv")