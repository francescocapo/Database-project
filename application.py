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

def load_data(dataset_fname: str):
	print("I loaded the dataset and built the database!\n")
	# dump the database to a file
	pass


def query_ground():
	min_engineCC = input("Please provide a minimum engine capacity: ")
	print(f"\n====\n<result of query_1 with minimum engine capacity {min_engineCC}>\n====")


def query_plane():
	print(f"<result of query_2>")


def query_fatalities():
	print(f"<result of query_3>")


def query_deaths():
	print(f"<result of query_4>")


def query_five():
	choicesq5 = ['shot down', 'engines failed', 'hijacked', 'crashed into a mountain', 'crashed into the jungle', 'midair collision', 'home']

	while True:

		choice5 = input('''\nSelect the reason why the airplane crashed or type 'home' to return to the query selection.
	The possible reason that you can select are the following:
	'shot down', 'engines failed', 'hijacked', 'crashed into a mountain', 'crashed into the jungle', 'midair collision'
	(note that all the letter must be in lower case).
			
	Choose a the reason or type 'home':
	
	>''')
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
					f"\n====\n<Details and summary of the crashes '{i[0]}', '{i[1]}', '{i[2]}' \n")
			continue

def query_war():
	print(f"<result of query_6>")



# MAIN
if __name__ == "__main__":
	print("Welcome to our project!\n")

	valid_choices = ['query1', 'query2', 'query3', 'query4', 'query5', 'query6', 'query7', 'quit']

	while True:

		choice = input('''\nChoose a query to execute from the one below or type 'quit' to quit.\n
	Choices:
	1. Select a country and find which airplane crashed there
	2. -
	3. Select the number of fatalities and see a which crash corresponds to
	4. Select a year and see the number of incidents
	5. Select a motivation and see which airplane crashed and why
	6. -
	quit
'cars' -> Get all the cars with engineCC greater than a given value
'members' -> Get all the members
'crash' -> Get all the rentals
 > ''')

		if choice not in valid_choices:
			print(f"Your choice '{choice}' is not valid. Please retry")
			continue

		if choice == "quit":
			break

		print(f"\nYou chose to execute query {choice}")
		if choice == 'cars':
			query_cars()
		elif choice == 'members':
			query_members()
		elif choice == 'crash':
			query_five()

		else:
			raise Exception("We should never get here!")


	print("\nGoodbye!\n")
