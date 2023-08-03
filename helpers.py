
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


# Convert SQL string of date into datetimr object
def convert_to_date_time(date_string):
    try:
        # Use datetime.strptime to parse the date_string into a datetime object
        datetime_object = datetime.strptime(date_string, '%Y-%m-%d')
        return datetime_object
    except ValueError:
        # If the date_string is not in the correct format, handle the exception
        return None


# Check if date value is valid
def is_valid_datetime_format(datetime_str):
    try:
        # Try to parse the input date string
        datetime.strptime(datetime_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


 # Check if expense/income amount is valid
def is_valid_numeral(number):
    try:
        numeric_result = float(number)
        if numeric_result > 0:
            return True
        else:
            return False
    except ValueError:
        return False


# Setup sqlite3
import sqlite3


    # Upload expense TO DO LATER EXTRACT NEEDED DATA AND INSERT IT TO THE DATABASE
        # EXTRACT ONLY THE FILENAME AND PASS IT TO PANDAS


    # CHECK IF the all recurring transactions were placed this month


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
    sqliteConnection = sqlite3.connect('expense_tracker.db')

    # No need to validate date sinse its taken from Calendar widget
    try:
        cursor = sqliteConnection.cursor()
        values = {
                   'date' : date,
                   'user_id' : user_id}
        query = """SELECT SUM(amount) FROM expense WHERE user_id = :user_id AND date = :date"""
        cursor.execute(query, values)
        result = cursor.fetchone()[0]
        cursor.close()
        # Finally will be executed after 'finally' statements, so return can be made
        return result
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


    # cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE date = ? and user = ?", (date, user)))
    # sum_expenses = cursor.fetchone()[0]
    # PLACEHOLDER
    sum_expenses = 0
    if user_id == 1:
        sum_expenses = 200
    return sum_expenses


# Extracting all expense records by date
def get_list_expenses_by_date(user_id, date):
    sqliteConnection = sqlite3.connect('expense_tracker.db')

    # No need to validate date sinse its taken from Calendar widget
    try:
        cursor = sqliteConnection.cursor()
        values = {
                   'date' : date,
                   'user_id' : user_id}
        query = """SELECT name, category, amount FROM expense WHERE date = :date AND user_id = :user_id"""
        cursor.execute(query, values)
        results = cursor.fetchall()
        cursor.close()
        # Finally will be executed after 'finally' statements, so return can be made
        return results
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()



 # Select top oldest date record in the table by user_id (limit 1)
def get_last_start_date_of_oldest_record(user_id):
    sqliteConnection = sqlite3.connect('expense_tracker.db')

    try:
        cursor = sqliteConnection.cursor()
        values = {'user_id' : user_id}
        query = """SELECT MIN(date) FROM expense WHERE user_id = :user_id LIMIT 1"""
        cursor.execute(query, values)
        results = cursor.fetchone()[0]
        cursor.close()

        # Check if result is not empty results
        if not results:
            today = datetime.today()
            first_date_of_month = today.replace(day=1)
            return first_date_of_month

        # Finally will be executed after 'finally' statements, so return can be made
        return convert_to_date_time(results)
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

""" FUNCTIONS for groups area """
def create_group(user_id, group_name, list_of_group_records):
    sqliteConnection = sqlite3.connect('expense_tracker.db')

    try:
        cursor = sqliteConnection.cursor()

        # Check if the group with this name already exists
        check_query = "SELECT group_id FROM groups WHERE name = ?;"
        cursor.execute(check_query, (group_name,))
        existing_group = cursor.fetchone()

        if existing_group:
            cursor.close()
            return 5
        
        # If the group name doesn't exist, insert the new group
        insert_query = "INSERT INTO groups (name) VALUES (?);"
        cursor.execute(insert_query, (group_name,))

        # Get the newly created group_id
        new_group_id = cursor.lastrowid

        data_list = []
        # Create data list to update group_id
        if list_of_group_records:
            for row in list_of_group_records:
                dictionary = {
                    'group_id' : new_group_id,
                    'user_id' : user_id,
                    'name' : row[0],
                    'category' : row[1],
                    'date' : row[2],
                    'amount' : row[3]
                }
                data_list.append(dictionary)


        # Set group value query 
        update_query = """
            UPDATE expense
            SET group_id = :group_id
            WHERE user_id = :user_id 
            AND name = :name
            AND category = :category
            AND date = :date
            AND amount = :amount;"""
        
        # Execute the update query for each dictionary in the list
        for data_dict in data_list:
            cursor.execute(update_query, data_dict)

        # Commit the changes and close the connection
        sqliteConnection.commit()
        cursor.close()

        # Finally will be executed after 'finally' statements, so return can be made
        return 0
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

    
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
    top_categpries_list = [('Rent', 2000), ('Grocery', 500), ('Online Orders', 200), ('Eating Out', 150), ('Sport', 100), ('Other', 100)]
    return top_categpries_list



# SELECT statement by the category, should return a list with records (description, date, amount). Category can be extracted as well
EXTRACTED_TEST_DATA = [("ABC", "02/03/2023", 20.25), ("BCD", "04/08/2018", 15.22), ("GNU", "15/11/2022", 76.00)]



# Add Expense after Add Expense button press
def add_expense_into_db(user_id, type, name, date, category, amount):
    sqliteConnection = sqlite3.connect('expense_tracker.db')
    # Validate date format
    if not is_valid_datetime_format(date):
        return 1
    # Check if name is not missing
    if name == "":
        return 2
    # check if amount is aa positive numeric value
    if not is_valid_numeral(amount):
        return 3
    try:
        cursor = sqliteConnection.cursor()
        values = { 'transaction_type' : type,
                   'name' : name,
                   'category' : category,
                   'date' : date,
                   'amount' : float(amount),
                   'recurring' : False,
                   'group_id' : None, 
                   'user_id' : user_id}
        query = """INSERT INTO expense
                (name, transaction_type, category, date, amount, recurring, group_id, user_id)
                VALUES (:name, :transaction_type, :category, :date, :amount, :recurring, :group_id, :user_id)"""
    #   VALUES ('tokyo central', 'grocery', get_today_date(), 43.25, False, NULL, 1);"""
        cursor.execute(query, values)
        sqliteConnection.commit()
        cursor.close()
        # Finally will be executed after 'finally' statements, so return can be made
        return 0
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()



        
# Add income after Add Income button press
def add_income_into_db(user_id, date, amount):
    print("Adding income into the database")
    sqliteConnection = sqlite3.connect('expense_tracker.db')

    # Validate date format
    if not is_valid_datetime_format(date):
        return 1
    # check if amount is aa positive numeric value
    if not is_valid_numeral(amount):
        return 3
    try:
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")
        values = { 'date' : date,
                   'amount' : float(amount),
                   'user_id' : user_id}
        query = """INSERT INTO income
                (date, amount, user_id)
                VALUES (:date, :amount, :user_id)"""
        cursor.execute(query, values)
        sqliteConnection.commit()
        cursor.close()
        # Finally will be executed after 'finally' statements, so return can be made
        return 0
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()



# Update monthly limit in users table
def set_new_limit(user_id, new_limit_value):
    print("Limit updated")
    print(str(user_id) + " " + str(new_limit_value))


# Select data by user_id and category as a tuple (expense name, expense date, amount)
def get_expenses_by_category(user_id, category):
    sqliteConnection = sqlite3.connect('expense_tracker.db')

    try:
        cursor = sqliteConnection.cursor()
        values = {'user_id' : user_id,
                  'category': category}
        query = """SELECT name, date, amount FROM expense WHERE user_id = :user_id and category = :category"""
        cursor.execute(query, values)
        results = cursor.fetchall()
        cursor.close()
        return results

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


# Select data by user_id and date_range 
def get_expenses_by_date_range(user_id, start_date, end_date):
    sqliteConnection = sqlite3.connect('expense_tracker.db')
    try:
        cursor = sqliteConnection.cursor()
        values = {'user_id' : user_id,
                  'start_date' : start_date,
                  'end_date': end_date}
        
        query = """SELECT name, category, date, amount 
                    FROM expense 
                    WHERE user_id = :user_id
                        AND date BETWEEN :start_date AND :end_date"""
        cursor.execute(query, values)
        results = cursor.fetchall()
        cursor.close()
        return results

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


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
    values = {
        'user_id' : user_id,
        'prev_name' : record_before_editing_list[0],
        'prev_category' : record_before_editing_list[1],
        'prev_date' : record_before_editing_list[2],
        'prev_amount' : record_before_editing_list[3],

        'new_name' : record_after_editing_list[0],
        'new_category' : record_after_editing_list[1],
        'new_date' : record_after_editing_list[2], 
        'new_amount' : record_after_editing_list[3]
    }

    # Validate date format
    if not is_valid_datetime_format(values['new_date']):
        return 1
    # Check if name is not missing
    if values['new_name'] == "":
        return 2
    # check if amount is aa positive numeric value
    if not is_valid_numeral(values['new_amount']):
        return 3

    sqliteConnection = sqlite3.connect('expense_tracker.db')
    try:
        cursor = sqliteConnection.cursor()
        query = """UPDATE expense
                SET name = :new_name,
                    date = :new_date,
                    amount = :new_amount
                WHERE user_id = :user_id
                    AND name = :prev_name
                    AND category = :prev_category
                    AND date = :prev_date
                    AND amount = :prev_amount;
                        """
        cursor.execute(query, values)
        sqliteConnection.commit()
        cursor.close()
        # Finally will be executed after 'finally' statements, so return can be made
        return 0
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    
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

