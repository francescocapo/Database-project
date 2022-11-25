import numpy as np
import pandas as pd

dataset = pd.read_csv('Airplane_Crashes_and_Fatalities_Since_1908.csv')
dataset.head()
selection = dataset.iloc[3196:]  # take values from 1980-90 and take all columns except from the first

# print(len(selection))
# print(selection.nunique())

#dup = {x for x in flight_number if flight_number.count(x) > 1}
# print(dup)

###working on primary keys
selection = selection.drop(labels='Flight #', axis=1)

#FLIGHT NUMBER

import random

flight_number = []

while len(flight_number) != 2072:
    n = random.randint(1000, 10000)
    if n not in flight_number:
        flight_number.append(n)


selection.insert(6, 'Flight#', flight_number)

#SERIAL NUMBER

serial_num = selection.loc[3196:, 'cn/In']
serial_num_ = list(serial_num)
selection = selection.drop(labels='cn/In', axis=1)

for x in range(len(serial_num_)):
    n = random.randint(100, 8000)
    if serial_num_[x] is np.nan:
        while n in serial_num:
            n = random.randint(100, 8000)
        serial_num_[x] = str(n)

selection.insert(9, 'serial#', serial_num_)


#REGISTRATION

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

selection.insert(8, 'Registration', registration_)


#TIME

import datetime
from datetime import datetime

times = selection['Time'].tolist()
t2 = []
for t in times:
    if type(t) != str:
            t2.append(0)
    else:
        allowed_characters = ['0','1','2','3','4','5','6','7','8','9',':']
        for i in t:
            if i not in allowed_characters or (i == ':' in (t[0] or t[-1])):
                t = t.replace(i,'')
        if ':' not in t:
            t = t[:len(t)//2]+':'+t[len(t)//2:]
        p = t.partition(':')
        if len(p[0]) > 2:
            t = t[1:]
        if len(p[2]) > 2:
            t = t[:-1]
        try:
            time = datetime.strptime(t, '%H:%M').time()
            t2.append(time)
        except:
            t2.append(0)
            continue
selection = selection.drop(labels='Time', axis=1)
selection.insert(2, 'Time', t2)


#DATE

date = selection.loc[3196:, 'Date']
date_ = list(date)
list = [datetime.strptime(x,'%m/%d/%Y').strftime('%Y/%m/%d') for x in date_]
print(list)
selection = selection.drop(labels='Date', axis=1)
selection.insert(1, 'Date', list)



null_val = selection.isnull().sum()
#print(selection)
#print('null values are:')
print(null_val)
