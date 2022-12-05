import pandas as pd
import datetime
import mysql.connector as mysql

# Write <dataset> to a new file 'reduced_dataset.csv'

host = "localhost"
user = "root"
password = "Magda2004."

db = mysql.connect(
    host=host,
    user=user,
    passwd=password
)

from mysql.connector import Error

db_name = 'airplane_crashes'
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


def query_1():
    location = []
    sql = (mycursor.execute(
        '''select distinct SUBSTRING_INDEX(location,', ',-1)
		from crash
        '''))
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for i in result:
        location.append(i[0])
    mydb.commit()

    choicesq1 = location[:]
    choicesq1.append('location')
    choicesq1.append('home')

    while True:
        choice1 = input('''--\nChoose a country to check if one or more crashes have ever happened.
	If so, you will get the information about the crashes.
	(note that the first letter of the country must be in upper case).
	Hint: if you type 'location' you will get a list with all the possible location.
		
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
                print(f"These are all flights that crashed in  {choice1}:\n--")
                for i in result1:
                    print(
                        f"\n\n - Serial number: '{i[0]}', Registration: '{i[1]}', Company: '{i[2]}', Date: {i[3]}, Number of fatalities: {i[4]}")


def query_2():
    location = []
    sql = (mycursor.execute(
        '''select distinct SUBSTRING_INDEX(location,', ',-1)
		from crash;
        '''))
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for i in result:
        location.append(i[0])
    mydb.commit()
    choicesq2 = location[:]
    choicesq2.append('location')
    choicesq2.append('home')
    while True:
        choice2 = input('''--\nChoose a country to check where crashes happened and the number of total victims.
    The 1st row is the accident with more deaths.
	(note that the first letter of the country must be in upper case).
    Hint: if you type 'location' you will get a list with all the possible location.
    
	Choose the nation or type 'home': ''')
        if choice2 not in choicesq2:
            print(f"\nInput not valid, check your syntax.\n")
            continue

        else:
            if choice2 == 'home':
                print('\nGoing back to query selection\n')
                break
            if choice2 == 'location':
                print(f'''Here you can find all the location among which you can choose:
{location}\n''')

            if choice2 in location:
                sql = (mycursor.execute(f'''SELECT DISTINCT f.flight_number,SUBSTRING_INDEX(c.location,',',1) AS CityLocation, c.date,c.number_of_fatalities+c.ground as TotalVictims 
                                        FROM Flight as f, Airplane as a, Crash as c
                                        WHERE a.serial_number = c.serial_number and a.registration = c.registration and f.serial_number = a.serial_number and f.registration = c.registration and c.location LIKE '%{choice2}' 
                                        ORDER BY c.number_of_fatalities+c.ground DESC;'''))
                mycursor.execute(sql)
                result2 = mycursor.fetchall()
                print(f"These are all the details of the flights that crashed in {choice2}:\n--")
                for i in result2:
                    print(
                        f"\n \n- Flight number: '{i[0]}', CityLocation: '{i[1]}', Date: '{i[2]}', TotalVictims: {i[3]}")


def query_3():
    fatalities = []
    sql = (mycursor.execute(
        '''select distinct number_of_fatalities from crash'''))
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for i in result:
        fatalities.append(str(i[0]))
    mydb.commit()
    choicesq3 = fatalities[:]
    choicesq3.append('home')

    while True:
        choice3 = input('''--\nSelect a number between 0 and 520, indicating the number of fatalities of the crash you want to get the details, if it exists.

	Choose the number or type 'home':	''')

        if choice3 not in choicesq3:
            print(f"\n    There are no crashes with {choice3} fatalities, please try again with a different number.")
            continue
        else:

            if choice3 == 'home':
                print('\nGoing back to query selection\n')
                break

            if choice3 in fatalities:
                sql = (mycursor.execute(f'''select a.serial_number, a.registration, a.operator
				from crash as c , airplane as a 
				where a.registration=c.registration and a.serial_number = c.serial_number and c.number_of_fatalities='%{choice3}%' '''))
                mycursor.execute(sql)
                result1 = mycursor.fetchall()
                print(f"These are the flights crashed with {choice3} fatalities\n--")
                for i in result1:
                    print(f"\n\nDetails of the crashes: '{i[0]}', '{i[1]}', '{i[2]}'")


def query_4():
    mycursor.execute('''select c.serial_number, c.registration, a.type, count(*) as cn
	from crash as c, airplane as a
	where c.serial_number = a.serial_number and c.registration = a.registration
	group by c.serial_number, c.registration
	having cn>2''')
    result = mycursor.fetchall()
    print('\n--\nThere are no airplanes that crashed more than once.\n--\n')


def query_5():
    choicesq5 = ['shot down', 'engines failed', 'hijacked', 'crashed into a mountain', 'crashed into the jungle',
                 'midair collision', 'home']
    while True:

        choice5 = input('''--\nSelect the reason why the airplane crashed or type 'home' to return to the query selection.
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
            result = mycursor.fetchall()
            print(f"These are the flights crashed because of {choice5}\n--")
            for i in result:
                print(
                    f"Details and summary of the crashes '{i[0]}', '{i[1]}', '{i[2]}'\n\n")


def query_6():
    yearslist = [str(i) for i in range(1980, 2009)]
    yearslist.append('home')
    #print(yearslist)
    while True:
        choice6 = input('''--\nSelect an year from 1980 up to 2009 and you will get the aircrafts crashed in the same route.
         
	Choose the year or type 'home':''')

        if choice6 not in yearslist:
            print(f"\nInput not valid, check your syntax.\n")
            continue
        else:
            if choice6 == 'home':
                print('\nGoing back to query selection\n')
                break
            sql = (mycursor.execute(f'''select a.serial_number, a.registration, a.operator, c.date , f.route 
                                        from airplane as a join flight as f on a.serial_number = f.serial_number and a.registration = f.registration join crash c on f.registration = c.registration 
                                        where year(c.date)={choice6} and f.route in (select f.route 
                                                                                from flight f join crash c on f.registration = c.registration and f.serial_number = c.serial_number 
                                                                                where year(c.date)={choice6} 
                                                                                group by f.route 
                                                                                having count(f.route) > 1) and f.route <> '/';'''))
            mycursor.execute(sql)
            result6 = mycursor.fetchall()
            if result6 == []:
                print('--\nThere are no flights that crashed with the same route in this year.')
            else:
                print(f"These are the flights that crashed in {choice6}\n--")
            for i in result6:
                print(
                    f"\nAircraft's serial number: '{i[0]}', Aircraft registration: '{i[1]}', Aircraft operator: '{i[2]}', Crash date: {i[3]}, Route: {i[4]} \n")


def query_7():
    mycursor.execute('''select a.operator, sum(c.number_of_fatalities) as total_fatalities 
	from airplane as a , crash as c 
	where a.serial_number=c.serial_number and a.registration=c.registration 
	group by a.operator
	having count(a.operator) >= all(select count(*)
									from airplane group by operator );
	''')
    result = mycursor.fetchall()
    for i in result:
        print(f"\n--\nThe most frequent operator is: '{i[0]}', total number of fatalities: {i[1]} \n--\n")


def query_8():
    import matplotlib.pyplot as plt
    mycursor.execute('''select year(date), count(*) from crash group by year(date);''')
    result = mycursor.fetchall()
    years = []
    crashes = []
    for i in result:
        years.append(i[0])
        crashes.append(i[1])
    fig, ax = plt.subplots()
    plot = plt.bar(years, crashes, alpha=0.5, linewidth=5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('#DDDDDD')
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color='#EEEEEE')
    ax.xaxis.grid(False)
    ax.set_xlabel('Years', fontsize=13, fontweight='black', color = '#333F4B')
    ax.set_ylabel('Number of crashes', fontsize=12, fontweight='black', color = '#333F4B')
    fig.tight_layout()
    plt.show()



# MAIN
if __name__ == "__main__":
    print("\nWelcome to our project!\n")

    valid_choices = ['1', '2', '3', '4', '5', '6', '7', '8', 'Quit']

    while True:

        choice = input('''Choose a query to execute from the one below or type 'quit' to quit.
	Choices:
	1. Select a country and find which airplane crashed there
	2. Find information about a crash based on the country
	3. Select the number of fatalities and see to which crash it corresponds
	4. Check if an airplane has crashed more than once
	5. Select a motivation and see which airplane crashed and why
	6. Insert a year and find the information about the crashes happened on the same route in that year
	7. Get the most frequent company with its total number of fatalities
	8. Plot the number of crashes for all the years
	Quit
 > ''')

        if choice not in valid_choices:
            print(f"Your choice '{choice}' is not valid. Please be sure to select one of the numbers below")
            continue

        elif choice == "Quit":
            break
        elif choice == '1':
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
        elif choice == '8':
            query_8()

print("\nGoodbye!\n")
