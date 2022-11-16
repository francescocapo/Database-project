import pandas as pd

dataset = pd.read_csv('Airplane_Crashes_and_Fatalities_Since_1908.csv')
dataset.head()
selection = dataset.iloc[3196:, 1:] #take values from 198-ò0 and take all columns except from the first
#print(selection)
null_val = selection.isnull().sum()
print('null values are:')
print(null_val)
print(len(selection))
print(selection.nunique())

