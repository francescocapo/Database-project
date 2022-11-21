
import pandas as pd

dataset = pd.read_csv('Airplane_Crashes_and_Fatalities_Since_1908.csv')
dataset.head()
selection = dataset.iloc[3196:, 1:] #take values from 1980-90 and take all columns except from the first
null_val = selection.isnull().sum()
#print(selection)
#print('null values are:')
#print(null_val)
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
print(dup)



selection.insert(6,'Flight#', flight_number)