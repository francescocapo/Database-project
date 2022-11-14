import pandas as pd
import numpy as np

dataset = pd.read_csv('Airplane_Crashes_and_Fatalities_Since_1908.csv')
dataset.head()
selection = dataset.iloc[3912:, 1:] #take values from 1990 and take all columns except from the first
#print(selection)
null_val = dataset.isnull().sum()
print(null_val)

df = dataset.value_counts()