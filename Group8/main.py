import numpy as np
import pandas as pd
from datetime import datetime

import DataPrep as DP

# In[ ]:
path = "C:/Govi/BABI/Capstone/Wisys/CapstoneData/"
DP.init_scheduleinfo(path)
emeter_data = DP.init_energymeterdata(path)
print(emeter_data.head(5))

# In[ ]:
diffdf = emeter_data['expected power']-emeter_data['Total Active Power']
 