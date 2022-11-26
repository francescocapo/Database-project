# Write <dataset> to a new file 'reduced_dataset.csv'

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


def query_demonstrations():
	print(f"<result of query_5>")


def query_war():
	print(f"<result of query_6>")


# MAIN
if __name__ == "__main__":
	print("Welcome to our project!\n")
	load_data("mydataset.txt")

	valid_choices = ['cars', 'members', 'rentals', 'quit']

	while True:

		choice = input('''\n\nChoose a query to execute by typing 'cars', 'members', or 'rentals', or type 'quit' to quit.\n
'cars' -> Get all the cars with engineCC greater than a given value
'members' -> Get all the members
'rentals' -> Get all the rentals
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
		elif choice == 'rentals':
			query_rentals()

		else:
			raise Exception("We should never get here!")


	print("\nGoodbye!\n")
