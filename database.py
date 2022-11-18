"""
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
"""

import mysql.connector as mysql
from mysql.connector import Error
import pandas as pd


dataset = pd.read_csv("Airplane_Crashes_and_Fatalities_Since_1908.csv")

db_name='airplane_crashe'
try:
    mydb = mysql.connect(host='localhost', user='root', password='franci22',
                         auth_plugin='mysql_native_password')  # you can add the auth_plugin here too (ref line 26)
    if mydb.is_connected():
        mycursor = mydb.cursor()
        mycursor.execute('SHOW DATABASES')
        result = mycursor.fetchall()
        print(result)
        for x in result:
            if db_name == x[0]:
                mycursor.execute('DROP DATABASE ' + db_name)  # delete old database
                mydb.commit()  # make the changes official
                print("The database already exists! The old database has been deleted!)")

        mycursor.execute("CREATE DATABASE " + db_name)
        print("Database is created")
except Error as e:
    print("Error while connecting to MySQL", e)


mycursor.execute("USE" + db_name)

mycursor.execute(
    '''
    SELECT 'mysql' dbms,t.TABLE_SCHEMA,t.TABLE_NAME,c.COLUMN_NAME,c.ORDINAL_POSITION,c.DATA_TYPE,c.CHARACTER_MAXIMUM_LENGTH,n.CONSTRAINT_TYPE,k.REFERENCED_TABLE_SCHEMA,k.REFERENCED_TABLE_NAME,k.REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.TABLES t LEFT JOIN INFORMATION_SCHEMA.COLUMNS c ON t.TABLE_SCHEMA=c.TABLE_SCHEMA AND t.TABLE_NAME=c.TABLE_NAME LEFT JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE k ON c.TABLE_SCHEMA=k.TABLE_SCHEMA AND c.TABLE_NAME=k.TABLE_NAME AND c.COLUMN_NAME=k.COLUMN_NAME LEFT JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS n ON k.CONSTRAINT_SCHEMA=n.CONSTRAINT_SCHEMA AND k.CONSTRAINT_NAME=n.CONSTRAINT_NAME AND k.TABLE_SCHEMA=n.TABLE_SCHEMA AND k.TABLE_NAME=n.TABLE_NAME WHERE t.TABLE_TYPE='BASE TABLE' AND t.TABLE_SCHEMA NOT IN('INFORMATION_SCHEMA','mysql','performance_schema');
    '''
      )