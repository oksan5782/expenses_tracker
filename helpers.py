
""" FUNCTIONS FOR MAIN WINDOW WIDGET """

from datetime import datetime, timedelta 
import pandas as pd



# DATETIME ONLY FUNCTIONS 
def get_last_day_of_current_month():
    # Get the current date
    current_date = datetime.now()

    # Get the first day of the next month
    first_day_of_next_month = datetime(current_date.year, current_date.month % 12 + 1, 1)

    # Subtract one day from the first day of the next month to get the last day of the current month
    last_day_of_current_month = first_day_of_next_month - timedelta(days=1)

    return last_day_of_current_month



#setup sqlite3
import sqlite3
sqliteConnection = sqlite3.connect('database.db')


    # Upload expense TO DO LATER EXTRACT NEEDED DATA AND INSERT IT TO THE DATABASE
        # EXTRACT ONLY THE FILENAME AND PASS IT TO PANDAS


# Get Recent Expenses for Stacked bar chart
def get_recent_expenses(user_id):
    # SELECT DATA for top 5 + OTHER categories not in groups grouped by month
    recent_expenses = {"Rent" : [2000, 2000, 2000, 2000, 2000, 2000],
                "Utilities" : [300, 300, 300, 250, 300, 300],
                "Groceries" : [500, 650, 600, 550, 500, 530],
                "Eating Out" : [200, 100, 150, 50, 70, 80],
                "Online" : [50, 0, 200, 70, 10, 40],
                "Other" : [200, 600, 150, 550, 75, 260]}
    return recent_expenses


# Get monthly limit set by the user
def get_monthly_budget(user_id):
    # SELECT limit from users table by user_id
    monthly_limit = 4000  
    return monthly_limit  

def get_this_month_expenses(user_id):
    # Extract the sum of all expenses this month
    this_month_expenses = 3300
    return this_month_expenses

"""Functions for calendar block """
# Extracting the sum of expenses for a given date

def get_sum_expenses_by_date(user_id, date):
    # cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE date = ? and user = ?", (date, user)))
    # sum_expenses = cursor.fetchone()[0]
    # PLACEHOLDER
    sum_expenses = 0
    if user_id == 1:
        sum_expenses = 200
    return sum_expenses

# Extracting all expense records by date
def get_list_expenses_by_date(user_id, date):
    # PLACEHOLDER
    extracted_test_data = [("ABC", "Eating Out", 20.25), ("BCD", "Laundry", 15.22), ("GNU", "Groceries", 76.00), ("ABC", "Laundry", 20.25), ("BCD", "Laundry", 15.22), ("GNU", "Rent", 76.00)]
    return extracted_test_data

def get_last_start_date_of_oldest_record(user_id):
    # Select top oldest date record in the table by user_id (limit 1)
    # MIGHT NEED TO FIX DATE FORMATS TO QDATE IN gui_elements/calendar_view.py
    # PLACEHOLDER
    return (2022, 7, 11)


""" FUNCTIONS for groups area """
def create_group(group_name, list_of_group_records):
    print("Creating this group")
    print(group_name)
    print(list_of_group_records)
    
    # Create a new group with a title "group_name" (Check if this name already exists)
    # Get its index
    # Set this index in the group column for records table in a for loop
    # Return number as an error/no error code


def get_groups_list(user_id):
    # GROUP list contains a tuple with group title [0] and amout spent [1]
    group_list = [('Hawaii 22-23', 2000), ('Japan May 23', 2050), ('Japan Sep 23', 1500), ('Medical', 500), ('Dental', 100)]
    return group_list

def get_top_10_category_expenses(user_id): 
    # CATEGORIES SECTION Select top 10 of expenses categories with the amount spent this month
    top_categpries_list = [('Rent', 2000), ('Groceries', 500), ('Online Orders', 200), ('Eating Out', 150), ('Fitness', 100), ('Other', 100)]
    return top_categpries_list



# SELECT statement by the category, should return a list with records (description, date, amount). Category can be extracted as well
EXTRACTED_TEST_DATA = [("ABC", "02/03/2023", 20.25), ("BCD", "04/08/2018", 15.22), ("GNU", "15/11/2022", 76.00)]



# Add Expense after Add Expense button press
def add_expense_into_db(user_id, type, name, date, category, amount):
    try:
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")
        values = { 'transaction_type' : type,
                   'category' : category,
                   'date' : date,
                   'amount' : amount,
                   'recurring' : False,
                   'group_id' : None, 
                   'user_id' : user_id}
        query = """INSERT INTO expense
                (transaction_type, category, date, amount, recurring, group_id, user_id)
                VALUES (:transaction_type, :category, :date, :amount, :recurring, :group_id, :user_id)"""
    #   VALUES ('tokyo central', 'grocery', get_today_date(), 43.25, False, NULL, 1);"""
        cursor.execute(query, values)
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


        
# Add income after Add Income button press
def add_income_into_db(user_id, date, amount):
    print("Added income into the database")
    print("Input value is " + str(user_id) + " " + str(date) + " " + str(amount))


# Update monthly limit in users table
def set_new_limit(user_id, new_limit_value):
    print("Limit updated")
    print(str(user_id) + " " + str(new_limit_value))

# Select data by user_id and category as a tuple (expense name, expense date, amount)
def get_expenses_by_category(user_id, name):
    print(str(user_id) + " " + name)
    # Placeholder
    extracted_test_data = [("ABC", "02/03/2023", 20.25), ("BCD", "04/08/2018", 15.22), ("GNU", "15/11/2022", 76.00), ("ABC", "02/03/2023", 20.25), ("BCD", "04/08/2018", 15.22), ("GNU", "15/11/2022", 76.00), ("ABC", "02/03/2023", 20.25), ("BCD", "04/08/2018", 15.22), ("GNU", "15/11/2022", 76.00), ("ABC", "02/03/2023", 20.25), ("BCD", "04/08/2018", 15.22), ("GNU", "15/11/2022", 76.00)]
    return extracted_test_data


# Select data by user_id and date_range 
def get_expenses_by_date_range(user_id, start_date, end_date):
    # date_list = pd.date_range(start=start_date, end=end_date)
    
    # Run SELECT category by datarange
    # PLACEHOLDER
    data_by_date = [("ABC", "Eating Out", "02/03/2023", 20.25), ("BCD", "Eating Out", "04/08/2018", 15.22), ("GNU", "Eating Out", "15/11/2022", 76.00)]
    return data_by_date


def remove_record(user_id, category, name, date, amount):
    print("Removing")
    print(str(user_id) + " " + category + " " + name + " " + date + " " + str(amount))



def remove_record_from_the_group(user_id, group_name, expense_name, category, date, amount):
    # Update record in users table and set group to None
    print(user_id)
    print(group_name)
    print(expense_name)
    print(date)
    print(amount)


# Update record data to new values after searching fir it by previous values
def edit_record(user_id, record_before_editing_list, record_after_editing_list):
    # Parse values fron lists
    prev_name = record_before_editing_list[0]
    prev_category = record_before_editing_list[1]
    prev_date = record_before_editing_list[2]
    prev_amount = record_before_editing_list[3]

    new_name = record_after_editing_list[0]
    new_category = record_after_editing_list[1]
    new_date = record_after_editing_list[2]
    new_amount = record_after_editing_list[3]
    
    print(record_before_editing_list)
    print(record_after_editing_list)
    # COMPLETE THE REST

# Select date by user_id and group
def get_group_expenses(user_id, group_name):
    print("Getting group data")
    print(str(user_id) + " " + group_name)

    # Placeholder
    group_data = [("ABC", "Eating Out", "02/03/2023", 20.25), ("BCD", "Eating Out", "04/08/2018", 15.22), ("GNU", "Eating Out", "15/11/2022", 76.00)]
    return group_data






# AUTHENTICATION

# Log In
def log_in_check(username, password):
    print("Log In " + username + " " + password)
    # VALIDATE BOTH INPUT FIELDS
    # CONVERT PASSWORD TO HASH
    # LOOK FOR USERNAME IN THE USERS TABLE
    # SELECT PASSWORD HASH AND CHECK IF IT MATCHES
    # Return user_id if user found
    # Return 0 if user not found or there were errors (could be several error codes to flush different messages)

    # Placeholder function (TO BE REMOVED)
    if username == "me" and password == "123":
        return 1
    else:
        return 0
        

# Register new user
def register_user(username, password, password_confirmation):
    print("Register " + username + " " + str(password) + " " + str(password_confirmation))
       
    # VALIDATE INPUT FIELDS (check for existing username)
    # INSERT USER INTO USERS TABLE

    # PlaceHolder function
    passed = True
    return passed

