import numpy as np
import pandas as pd

dataset = pd.read_csv('Airplane_Crashes_and_Fatalities_Since_1908.csv')
dataset.head()
selection = dataset.iloc[3196:, 1:]  # take values from 1980-90 and take all columns except from the first

# print(len(selection))
# print(selection.nunique())

#dup = {x for x in flight_number if flight_number.count(x) > 1}
# print(dup)

###working on primary keys

import random

selection = selection.drop(labels='Flight #', axis=1)

flight_number = []

while len(flight_number) != 2072:
    n = random.randint(1000, 10000)
    if n not in flight_number:
        flight_number.append(n)


selection.insert(6, 'Flight#', flight_number)


serial_num = selection.loc[3196:, 'cn/In']
serial_num_ = list(serial_num)
selection = selection.drop(labels='cn/In', axis=1)

for x in range(len(serial_num_)):
    n = random.randint(100, 8000)
    if serial_num_[x] is np.nan:
        while n in serial_num:
            n = random.randint(100, 8000)
        serial_num_[x] = str(n)

selection.insert(8, 'serial#', serial_num_)


registration = selection.loc[3196:, 'Registration']
registration_ = list(registration)
selection = selection.drop(labels='Registration', axis=1)

import string
for r in range(len(registration_)):
    reg1 = ''.join(random.choice(string.ascii_uppercase) for x in range(2))
    reg2 = ''.join(random.choice(string.ascii_uppercase) for x in range(3))
    reg = reg1+'-'+reg2
    if reg not in registration_:
        registration_[r] = reg

selection.insert(7, 'Registration', registration_)

'''
null_val = selection.isnull().sum()
#print(selection)
#print('null values are:')
print(null_val)
'''

