import pandas as pd
import datetime
import mysql.connector as mysql

# Write <dataset> to a new file 'reduced_dataset.csv'

host = "localhost"
user = "root"
password = "franci22"


db = mysql.connect(
 host = host,
 user = user,
 passwd = password
)

from mysql.connector import Error

import numpy as np

db_name='airplane_crashes'
try:
    mydb = mysql.connect(host=host, user=user, password=password, auth_plugin='mysql_native_password')
    if mydb.is_connected():
        mycursor = mydb.cursor()
        mycursor.execute('SHOW DATABASES')
        result = mycursor.fetchall()
        db_list = []
        for x in result:
            db_list.append(x[0])
        if db_name not in db_list:
            print('Error, database', db_name, 'is not found')
        else:
            mycursor.execute('USE ' + db_name)
            mydb.commit()
            print("Database is selected")

except Error as e:
    print("Error while connecting to MySQL", e)

f = open('selection.csv', "r")

def query_1():

	location = []
	sql = (mycursor.execute(
		'''select distinct SUBSTRING_INDEX(location,',',-1)
		from crash;
        '''))
	mycursor.execute(sql)
	result = mycursor.fetchall()
	for i in result:
		location.append(i[0])
	mydb.commit()
	print(location)
	choicesq1 = location[:]
	choicesq1.append('location')
	choicesq1.append('home')
	print(choicesq1)
	while True:
		choice1 = input('''\nChoose a country to check if one or more crashes have ever happened.
	If so, you will get the information about the crashes.
	(note that the first letter of the country must be in upper case).
		
		
	Choose the nation or type 'home':
		''')
		if choice1 not in choicesq1:
			print(f"\nInput not valid, check your syntax.\n")
			continue

		else:
			if choice1 == 'home':
				print('\nGoing back to query selection\n')
				break
			if choice1 == 'location':
				print(f'''Here you can find all the location among which you can choose:
{location}\n''')

			if choice1 in location:
				sql = (mycursor.execute(f'''select c.serial_number, c.registration, a.operator, c.number_of_fatalities
				from airplane as a, crash as c
				where a.registration = c.registration and a.serial_number = c.serial_number and c.location like '%{choice1}' '''))
				mycursor.execute(sql)
				result1 = mycursor.fetchall()
				print(f"These are all flights that crashed in  {choice1}:")
				for i in result1:
					print(
						f"\n - Serial number: '{i[0]}', Registration: '{i[1]}', Company: '{i[2]}', Number of fatalities: {i[3]} \n")

#def query_2():


#def query_3():

def query_4():
	mycursor.execute('''select c.serial_number, c.registration, a.type, count(*) as cn
	from crash as c, airplane as a
	where c.serial_number = a.serial_number and c.registration = a.registration
	group by c.serial_number, c.registration
	having cn>2''')
	result2 = mycursor.fetchall()
	print('There are no airplanes that crashed more than once.')

def query_5():
	choicesq5 = ['shot down', 'engines failed', 'hijacked', 'crashed into a mountain', 'crashed into the jungle', 'midair collision', 'home']
	while True:

		choice5 = input('''\nSelect the reason why the airplane crashed or type 'home' to return to the query selection.
	The possible reason that you can select are the following:
	'shot down', 'engines failed', 'hijacked', 'crashed into a mountain', 'crashed into the jungle', 'midair collision'
	(note that all the letter must be in lower case).
			
	Choose a the reason or type 'home':''')

		if choice5 not in choicesq5:
			print(f"\nInput not valid, check your syntax.\n")
			continue
		else:

			if choice5 == 'home':
				print('\nGoing back to query selection\n')
				break

			sql = (mycursor.execute(f'''select registration, serial_number, summary
				from crash
				where summary like '%{choice5}%' '''))
			mycursor.execute(sql)
			result1 = mycursor.fetchall()
			print(f"These are the flights crashed because of {choice5}\n====")
			for i in result1:
				print(
					f"\nDetails and summary of the crashes '{i[0]}', '{i[1]}', '{i[2]}' \n")

#def query_6():


#def query_7():


# MAIN
if __name__ == "__main__":
	print("Welcome to our project!\n")

	valid_choices = ['1', '2', '3', '4', '5', '6', '7', '8', 'quit']

	while True:

		choice = input('''\nChoose a query to execute from the one below or type 'quit' to quit.\n
	Choices:
	1. Select a country and find which airplane crashed there
	2. Select a year and see the number of incidents
	3. Select the number of fatalities and see a which crash corresponds to
	4. Check if an airplane has crashed more than once
	5. Select a motivation and see which airplane crashed and why
	6. -
	7. -
	quit
 > ''')

		if choice not in valid_choices:
			print(f"Your choice '{choice}' is not valid. Please be sure to select of the above choices")
			continue

		if choice == "quit":
			break
		print(f"\nYou chose to execute query {choice}")
		if choice == '1':
			query_1()
		elif choice == '2':
			query_2()
		elif choice == '3':
			query_3()
		elif choice == '4':
			query_4()
		elif choice == '5':
			query_5()
		elif choice == '6':
			query_6()
		elif choice == '7':
			query_7()


	print("\nGoodbye!\n")
