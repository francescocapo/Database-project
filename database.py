import numpy as np
import pandas as pd

dataset = pd.read_csv('Airplane_Crashes_and_Fatalities_Since_1908.csv')
dataset.head()
selection = dataset.iloc[3196:, 1:] #take values from 1980-90 and take all columns except from the first

#print(len(selection))
#print(selection.nunique())

###working on primary keys

selection = selection.drop(labels='Flight #', axis=1)

import random
flight_number = []

while len(flight_number)!=2072:
    n = random.randint(1000, 10000)
    if n not in flight_number:
        flight_number.append(n)

dup = {x for x in flight_number if flight_number.count(x) >1}
#print(dup)
selection.insert(6,'Flight#', flight_number)



serial_num = selection.loc[3196:, 'cn/In']
#print(serial_num)
dataset = dataset.replace(np.nan,00)

n = random.randint(100, 8000)
if n not in serial_num:
    selection['cn/In'].fillna(n, inplace = True)

serial_num = selection.loc[3196:, 'cn/In']
serial_num_ = list(serial_num)
dup2 = {i for i in serial_num_ if serial_num_.count(i) >1}



null_val = selection.isnull().sum()
#print(selection)
#print('null values are:')
#print(null_val)