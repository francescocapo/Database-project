from time import strftime

import mysql.connector as mysql
from mysql.connector import Error
import pandas as pd
import numpy as np

dataset = pd.read_csv("Airplane_Crashes_and_Fatalities_Since_1908.csv")

db_name='airplane_crashes'
try:
    mydb = mysql.connect(host = 'localhost', user = 'root', password = 'password') # you can add the auth_plugin here too (ref line 26)
    if mydb.is_connected():
        mycursor = mydb.cursor()
        mycursor.execute('SHOW DATABASES')

        result = mycursor.fetchall()
        print(result)
        for x in result:
            if db_name == x[0]:
                mycursor.execute('DROP DATABASE ' + db_name) # delete old database
                mydb.commit() # make the changes official
                print("The database already exists! The old database has been deleted!")

        mycursor.execute("CREATE DATABASE " + db_name)
        print("Database is created")
except Error as e:
    print("Error while connecting to MySQL", e)

mycursor.execute('USE' + ' ' + db_name)

#CREATE TABLES

mycursor.execute(
      '''
        CREATE TABLE `Airplane` (
          `serial_number` varchar(100),
          `registration` varchar(100),
          `operator` varchar(100),
          `type` varchar(100),
          PRIMARY KEY (serial_number, registration)
        );
      '''
      )

mycursor.execute(
      '''
        CREATE TABLE Flight (
           flight_number varchar(100),
           aboard int,
           route varchar(100),
           serial_number varchar(100),
           registration varchar(100),
           PRIMARY KEY (flight_number),
           FOREIGN KEY (`serial_number`, `registration`) REFERENCES `Airplane` (`serial_number`, `registration`)
        );
      '''
      )

mycursor.execute(
    '''
        CREATE TABLE `Crash` (
          `index` int,
          `date` date NULL,
          `time` time NULL,
          `location` varchar(100),
          `serial_number` varchar(100),
          `registration` varchar(100),
          `number_of_fatalities` int,
          `ground` int,
          `summary` varchar(2000),
          PRIMARY KEY (`index`),
          FOREIGN KEY (`serial_number`, `registration`) REFERENCES `Airplane`(`serial_number`, `registration`)
        );
    '''
)

#We manipulate the data
selection = dataset.iloc[3196:] #take values from 1980-90 and take all columns except from the first
null_val = selection.isnull().sum()
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
serial_num = selection.loc[0:, 'cn/In']
serial_num_ = list(serial_num)
selection = selection.drop(labels='cn/In', axis=1)

for x in range(len(serial_num_)):
    n = random.randint(100, 8000)
    if serial_num_[x] is np.nan:
        while n in serial_num:
            n = random.randint(100, 8000)
        serial_num_[x] = str(n)

selection.insert(9, 'Serial#', serial_num_)


#REGISTRATION
registration = selection.loc[0:, 'Registration']
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

        time = datetime.strptime(t, '%H:%M').time()
        t2.append(time)

selection = selection.drop(labels='Time', axis=1)
selection.insert(2, 'Time', t2)


#DATE
date = selection.loc[0:, 'Date']
date_ = list(date)
list = [datetime.strptime(x,'%m/%d/%Y').strftime('%Y/%m/%d') for x in date_]
selection = selection.drop(labels='Date', axis=1)
selection.insert(1, 'Date', list)

##Insert the data into the tables
#Airplane
for attrib in ['Operator', 'Type']:
    selection[attrib] = selection[attrib].fillna('/')
for i,row in selection.iterrows():
    sql = "INSERT INTO airplane_crashes.Airplane VALUES (%s,%s,%s,%s)"
    mycursor.execute(sql, tuple([row['Serial#'], row['Registration'], row['Operator'], row['Type']]))
    mydb.commit()

#Flight
selection['Route'] = selection['Route'].fillna('/')
selection['Aboard'] = selection['Aboard'].fillna(0)
for i, row in selection.iterrows():
    sql = "INSERT INTO airplane_crashes.Flight VALUES (%s,%s,%s,%s,%s)"
    mycursor.execute(sql, tuple([row['Flight#'], row['Aboard'], row['Route'], row['Serial#'], row['Registration']]))
    mydb.commit()

#Crash
for attrib in ['Location', 'Summary']:
    selection[attrib] = selection[attrib].fillna('/')
for attrib1 in ['Fatalities', 'Ground']:
    selection[attrib1] = selection[attrib1].fillna(0)
selection['Date'] = selection['Date'].fillna('0000-00-00')
selection['Time'] = selection['Time'].fillna('00')
for i, row in selection.iterrows():
    sql = "INSERT INTO airplane_crashes.Crash VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    mycursor.execute(sql, tuple([row['index'], row['Date'], row['Time'], row['Location'],  row['Serial#'], row['Registration'],  row['Fatalities'], row['Ground'], row['Summary']]))
    mydb.commit()