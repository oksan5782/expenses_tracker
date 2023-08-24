
""" FUNCTIONS FOR MAIN WINDOW WIDGET """

from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd
import bcrypt 


"""CONSTANTS"""
#  Categories list for all categories view
ALL_POSSIBLE_CATEGORIES_LIST = ["Rent", "Transportation", "Groceries", "Utilities", "Eating Out", "Health", "Entertainment", "Subscriptions", "Sport", "Other"]
# Expense types
ALL_EXPENSE_TYPES = ["Credit", "Cash", "Check", "Foreign Currency"]


# DATETIME ONLY FUNCTIONS 
def get_last_day_of_current_month():
    # Get the current date
    current_date = datetime.now()

    # Get the first day of the next month
    first_day_of_next_month = datetime(current_date.year, current_date.month % 12 + 1, 1)

    # Subtract one day from the first day of the next month to get the last day of the current month
    last_day_of_current_month = first_day_of_next_month - timedelta(days=1)

    return last_day_of_current_month

# Get list of strings for the last 6 months in the format YYYY-MM
def get_last_6_months():

    today = datetime.today()

    first_day_of_current_month = today.replace(day=1)

    last_6_months = [first_day_of_current_month - timedelta(days=i*30) for i in range(6)][::-1]

    return [date.strftime("%Y-%m") for date in last_6_months]



def get_3_letters_for_last_6_month():
        now = datetime.now()
        result = [now.strftime("%B")[:3]]
        for _ in range(0, 5):
            now = now.replace(day=1) - timedelta(days=1)
            result.append(now.strftime("%B")[:3])
        result.reverse()
        return result

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

# CHECK IF the all recurring transactions were placed this month


# Get Recent Expenses for Stacked bar chart
def get_recent_expenses(user_id):
    sqliteConnection = sqlite3.connect('expense_tracker.db')
    try:
        cursor = sqliteConnection.cursor()
           # SQL query to get the list of 6 categories sorted by total amount of expenses
        categories_query = """
            SELECT category, SUM(amount) AS total_amount
            FROM expense
            GROUP BY category
            ORDER BY total_amount DESC
            LIMIT 6;
        """

        # Execute the first query to get the list of 6 categories
        cursor.execute(categories_query)
        top_6_categories = [row[0] for row in cursor.fetchall()]

        # Get the date range for the last 6 months and change its order
        last_6_months = get_last_6_months()
        # last_6_months.reverse()

        # SQL query to get the sum of "amount" grouped by each month and each category
        sum_query = """
            SELECT category, strftime('%Y-%m', date) AS month, SUM(amount) AS total_amount
            FROM expense
            WHERE user_id = {}
                AND strftime('%Y-%m', date) IN ({}) 
                AND category IN ({})
            GROUP BY category, month
            ORDER BY category, month;
        """.format(user_id,
                   ', '.join(['"{}"'.format(date) for date in last_6_months]),
                   ', '.join(['"{}"'.format(category) for category in top_6_categories]))

        cursor.execute(sum_query)
        sums_data = cursor.fetchall()
        cursor.close()
        if not sums_data:
            return None

        # Organize the results in a dictionary format
        result_dict = {}
        for category in top_6_categories:
            result_dict[category] = [0] * 6

        for category, month, total_amount in sums_data:
            result_dict[category][last_6_months.index(month)] = total_amount

        return result_dict
 
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()



# Functions for Balance area
def get_monthly_income(user_id):
    # PLACEHOLDER
    return 4000

def get_this_month_expenses(user_id):
    # PLACEHOLDER
    return 3300

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

        # Create group name if its new one
        if not existing_group:
            insert_query = "INSERT INTO groups (name) VALUES (?);"
            cursor.execute(insert_query, (group_name,))
            # Get the newly created group_id
            existing_group = cursor.lastrowid
        else: 
            existing_group = existing_group[0]


        data_list = []
        # Create data list to update group_id
        if list_of_group_records:
            for row in list_of_group_records:
                dictionary = {
                    'group_id' : existing_group,
                    'user_id' : user_id,
                    'name' : row[0],
                    'category' : row[1],
                    'date' : row[2],
                    'transaction_type' : row[3],
                    'amount' : row[4]
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
            AND transaction_type = :transaction_type
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




def get_groups_list(user_id):
    sqliteConnection = sqlite3.connect('expense_tracker.db')

    try:
        cursor = sqliteConnection.cursor()
        values = {'user_id' : user_id}

        # SQL query to get group names and sum of amounts for the given user_id
        query = """
            SELECT g.name, COALESCE(SUM(e.amount), 0) AS total_amount
            FROM groups g
            LEFT JOIN expense e ON g.group_id = e.group_id
            WHERE e.user_id = :user_id
            GROUP BY g.group_id
            LIMIT 10
            """
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


def get_top_10_category_expenses(user_id): 
    # Get the current month and year
    current_month = datetime.now().strftime("%Y-%m")
    result = []

    sqliteConnection = sqlite3.connect('expense_tracker.db')

    try:
        cursor = sqliteConnection.cursor() 

        for category in ALL_POSSIBLE_CATEGORIES_LIST:
            values = {'user_id': user_id,
                    'category': category,
                    'current_month': current_month}
            query = """
                SELECT IFNULL(SUM(amount), 0)
                FROM expense
                WHERE user_id = :user_id 
                AND category = :category
                AND strftime('%Y-%m', date) = :current_month
            """
            cursor.execute(query, values)
            expense_sum = cursor.fetchone()[0]
            result.append((category, expense_sum))
    
        result.sort(key=lambda x: x[1], reverse=True)  # Sort by expense_sum
        return result

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()             


# Add Expense after Add Expense button press
def add_expense_into_db(user_id, type, name, date, category, amount):
    sqliteConnection = sqlite3.connect('expense_tracker.db')
    
    # Check if name is not missing
    if name == "":
        message = "Missing name"
        return (False, message)
    
    # Validate date format
    if not is_valid_datetime_format(date):
        message = "Invalid Date Format. Please use YYYY-MM-DD"
        return (False, message)
    
    # Check if amount is aa positive numeric value
    if not is_valid_numeral(amount):
        message = "Invalid amount"
        return (False, message)
    try:
        cursor = sqliteConnection.cursor()
        values = { 'transaction_type' : type,
                   'name' : name,
                   'category' : category,
                   'date' : date,
                   'amount' : float(amount),
                   'group_id' : None, 
                   'user_id' : user_id}
        query = """INSERT INTO expense
                (name, transaction_type, category, date, amount, group_id, user_id)
                VALUES (:name, :transaction_type, :category, :date, :amount, :group_id, :user_id)"""
        cursor.execute(query, values)
        sqliteConnection.commit()
        cursor.close()
        # Finally will be executed after 'finally' statements, so return can be made
        message = "Expense added"
        return (True, message)
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


# Check if is value already inserted into the table
def check_record_presence(user_id, name, category, amount, date):
    sqliteConnection = sqlite3.connect('expense_tracker.db')

    try:
        cursor = sqliteConnection.cursor()
        values = {'user_id' : user_id,
                  'name' : name,
                  'category': category,
                  'amount': amount,
                  'date': date}
        query = """SELECT expense_id
                    FROM expense 
        WHERE user_id = :user_id 
            AND name = :name
            AND category = :category
            AND amount = :amount
            AND date = :date"""
        cursor.execute(query, values)
        results = cursor.fetchone()
        cursor.close()
        # Return True if the record is present
        if results:
            return True
        # Return False if record is not added
        return False

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()




# Upload expenses from a file
def upload_expense_csv_chase(user_id, file):
    try:
        df = pd.read_csv(file)

        # Remove thank you - credit cover line 
        df_cover_credit_row_index = df[(df['Description'].str.contains('Payment Thank You')) & (df['Type'] == 'Payment')].index
        df.drop(df_cover_credit_row_index, inplace=True)

        # Update date values to strings 
        df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], format='%m/%d/%Y')
        df['Transaction Date'] = df['Transaction Date'].dt.strftime('%Y-%m-%d')

        # Update amount values to float type
        df['Amount'] = df['Amount'].astype(float)
        print(df)

        # Get positive values to upload them as income 
        df_returns_or_income = df[df['Amount'] > 0]

        # Insert these values as income using iterrows
        for index, row in df_returns_or_income.iterrows():
            add_income_into_db(user_id, row['Transaction Date'], row['Amount'])

        # Remove positive values from the DataFrame
        df.drop(df_returns_or_income.index, inplace=True)

        # Remove columns Post Date, Memo and Type and reindex DataFrame
        df = df.drop(['Post Date', 'Type', 'Memo'], axis=1)
        df.reset_index(drop=True, inplace=True)

        # Change sign for all negative amounts 
        df['Amount'] = df['Amount'] * -1

        # Standartize category names
        df['Category'] = df['Category'].str.replace('Bills & Utilities', 'Utilities')
        df['Category'] = df['Category'].str.replace('Food & Drink', 'Eating Out')
        df['Category'] = df['Category'].str.replace('Health & Wellness', 'Health')
        # Replace values not in the list with 'Other'
        df.loc[~df['Category'].isin(ALL_POSSIBLE_CATEGORIES_LIST), 'Category'] = 'Other'


        # Find last uploaded transaction:
        check_first_row = check_record_presence(user_id, df.loc[0, 'Description'], df.loc[0, 'Category'], df.loc[0, 'Amount'], df.loc[0, 'Transaction Date'])

        # If latest record is already added, all of the table content is already uploaded
        if check_first_row:
            message = "The file content was already added to the database"
            return (False, message)
    
        # Check if last record is uploaded
        last_row_index = df.tail(1).index[0]
        check_last_row = check_record_presence(user_id, df.loc[last_row_index, 'Description'], df.loc[last_row_index, 'Category'], df.loc[last_row_index, 'Amount'], df.loc[last_row_index, 'Transaction Date'])

        # If oldest value is in the database, attempting binary search to find where the division starts
        if check_last_row:
            top_row = 0
            bottom_row = last_row_index
            # Button floor will be last index 
            while top_row <= bottom_row:
                mid = (top_row + bottom_row) // 2

                if not check_record_presence(user_id, df.loc[mid, 'Description'], df.loc[mid, 'Category'], df.loc[mid, 'Amount'], df.loc[mid, 'Transaction Date']):
                    last_row_index = mid
                    top_row = mid + 1  # Move to the bottom to find the last occurrence
                else:
                    bottom_row = mid - 1
            df = df.iloc[:last_row_index + 1]

        # Upload all table values 
        for index, row in df.iterrows():
            add_expense_into_db(user_id, 'Credit', row['Description'], row['Transaction Date'], row['Category'], row['Amount'])
        message = "The file has been uploaded"
        return (True, message)
    except (IndexError, TypeError, NameError, ValueError, KeyError):
        message = "The file does not match Chase format"
        return (False, message)


# Upload Discover csv
def upload_expense_csv_discover(user_id, file):
    try:
        df = pd.read_csv(file)

        # Remove thank you - credit cover line 
        df_cover_credit_row_index = df[(df['Description'].str.contains('THANK YOU')) & (df['Category'] == 'Payments and Credits')].index
        df.drop(df_cover_credit_row_index, inplace=True)

        # Update date values to strings 
        df['Trans. Date'] = pd.to_datetime(df['Trans. Date'], format='%m/%d/%Y')
        df['Trans. Date'] = df['Trans. Date'].dt.strftime('%Y-%m-%d')

        # Update amount values to float type
        df['Amount'] = df['Amount'].astype(float)

        # Get NEGATIVE values to upload them as income 
        df_returns_or_income = df[df['Amount'] < 0]

        # Change sign these all negative amounts 
        if not df_returns_or_income.empty:
            df_returns_or_income['Amount'] = df_returns_or_income['Amount'] * -1

            # Insert these values as income using iterrows
            for index, row in df_returns_or_income.iterrows():
              add_income_into_db(user_id, row['Trans. Date'], row['Amount'])

            # Remove positive values from the DataFrame
            df.drop(df_returns_or_income.index, inplace=True)

        # Remove extra columns Post Date, Memo and Type and reindex DataFrame
        df = df.drop(['Post Date'], axis=1)
        df.reset_index(drop=True, inplace=True)

        # Standartize category names
        df['Category'] = df['Category'].str.replace('Warehouse Clubs', 'Groceries')
        df['Category'] = df['Category'].str.replace('Supermarkets', 'Groceries')
        df['Category'] = df['Category'].str.replace('Gasoline', 'Transportation')
        df['Category'] = df['Category'].str.replace('Travel/ Entertainment', 'Transportation')
        df['Category'] = df['Category'].str.replace('Medical Services', 'Health')


        df['Category'] = df['Category'].str.replace('Restaurants', 'Eating Out')

        # Replace values not in the list with 'Other'
        df.loc[~df['Category'].isin(ALL_POSSIBLE_CATEGORIES_LIST), 'Category'] = 'Other'

        # Find last uploaded transaction:
        check_first_row = check_record_presence(user_id, df.loc[0, 'Description'], df.loc[0, 'Category'], df.loc[0, 'Amount'], df.loc[0, 'Trans. Date'])

        # If latest record is already added, all of the table content is already uploaded
        if check_first_row:
            message = "The file content was already added to the database"
            return (False, message)

        # Check if last record is uploaded
        last_row_index = df.tail(1).index[0]
        check_last_row = check_record_presence(user_id, df.loc[last_row_index, 'Description'], df.loc[last_row_index, 'Category'], df.loc[last_row_index, 'Amount'], df.loc[last_row_index, 'Trans. Date'])

        # If oldest value is in the database, attempting binary search to find where the division starts
        if check_last_row:
            top_row = 0
            bottom_row = last_row_index
            # Button floor will be last index 
            while top_row <= bottom_row:
                mid = (top_row + bottom_row) // 2

            if not check_record_presence(user_id, df.loc[mid, 'Description'], df.loc[mid, 'Category'], df.loc[mid, 'Amount'], df.loc[mid, 'Trans. Date']):
                last_row_index = mid
                top_row = mid + 1  # Move to the bottom to find the last occurrence
            else:
                bottom_row = mid - 1
        df = df.iloc[:last_row_index + 1]

        # Upload all table values 
        for index, row in df.iterrows():
           add_expense_into_db(user_id, 'Credit', row['Description'], row['Trans. Date'], row['Category'], row['Amount'])
        message = "The file has been uploaded"
        return (True, message)
    except (IndexError, TypeError, NameError, ValueError, KeyError):
        message = "The file does not match Discover format"
        return (False, message)



# Add income after Add Income button press
def add_income_into_db(user_id, date, amount):
    sqliteConnection = sqlite3.connect('expense_tracker.db')

    # Validate date format
    if not is_valid_datetime_format(date):
        message = "Invalid Date Format. Please use YYYY-MM-DD"
        return (False, message)
    # CCheck if amount is a positive numeric value
    if not is_valid_numeral(amount):
        message = "Invalid amount"
        return (False, message)
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
        message = "Income value added"
        return (True, message)
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
        query = """SELECT name, date, transaction_type, amount 
                    FROM expense 
                    WHERE user_id = :user_id 
                        AND category = :category
                    ORDER BY date DESC"""
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
        
        query = """SELECT name, category, date, transaction_type, amount 
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



def remove_record_from_the_group(user_id, expense_name, category, date, transaction_type, amount):
    sqliteConnection = sqlite3.connect('expense_tracker.db')
    try:
        cursor = sqliteConnection.cursor()
        values = {'user_id' : user_id,
                  'group_id' : None,
                  'expense_name' : expense_name,
                  'category': category,
                  'date' : date,
                  'transaction_type' : transaction_type,
                  'amount' : amount
                }
        update_query = """
            UPDATE expense
            SET group_id = :group_id
            WHERE user_id = :user_id 
            AND name = :expense_name
            AND category = :category
            AND date = :date
            AND transaction_type = :transaction_type
            AND amount = :amount;"""

        cursor.execute(update_query, values)
        sqliteConnection.commit()
        cursor.close()
        return True

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()



# Update record data to new values after searching fir it by previous values
def edit_record(user_id, record_before_editing_list, record_after_editing_list):
    # Parse values fron lists
    values = {
        'user_id' : user_id,
        'prev_name' : record_before_editing_list[0],
        'prev_category' : record_before_editing_list[1],
        'prev_date' : record_before_editing_list[2],
        'prev_type' : record_before_editing_list[3],
        'prev_amount' : record_before_editing_list[4],

        'new_name' : record_after_editing_list[0],
        'new_category' : record_after_editing_list[1],
        'new_date' : record_after_editing_list[2], 
        'new_type' : record_after_editing_list[3],
        'new_amount' : record_after_editing_list[4]
    }

    # Validate date format
    if not is_valid_datetime_format(values['new_date']):
        message = "Invalid Date Format. Please use YYYY-MM-DD"
        return (False, message)
    # Check if name is not missing
    if values['new_name'] == "":
        message = "Missing name"
        return (False, message)
    # Check if the type is valid
    if values['new_type'] not in ALL_EXPENSE_TYPES:
        message = "Invalid transaction type"
        return (False, message)
    # check if amount is a positive numeric value
    if not is_valid_numeral(values['new_amount']):
        message = "Invalid amount"
        return (False, message)
    # check if category is among the ones available
    if values['new_category'] not in ALL_POSSIBLE_CATEGORIES_LIST:
        message = "Invalid category. Try capitalizing the name or use Other"
        return (False, message)

    sqliteConnection = sqlite3.connect('expense_tracker.db')
    try:
        cursor = sqliteConnection.cursor()
        query = """UPDATE expense
                SET name = :new_name,
                    date = :new_date,
                    transaction_type = :new_type,
                    category = :new_category,
                    amount = :new_amount
                WHERE user_id = :user_id
                    AND name = :prev_name
                    AND category = :prev_category
                    AND transaction_type = :prev_type
                    AND date = :prev_date
                    AND amount = :prev_amount;
                        """
        cursor.execute(query, values)
        sqliteConnection.commit()
        cursor.close()
        # Finally will be executed after 'finally' statements, so return can be made
        message = "Expense updated"
        return (True, message)
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    
    print(record_before_editing_list)
    print(record_after_editing_list)


# Select date by user_id and group
def get_group_expenses(user_id, group_name):
    sqliteConnection = sqlite3.connect('expense_tracker.db')
    try:
        cursor = sqliteConnection.cursor()

        # Get group_id
        check_query = "SELECT group_id FROM groups WHERE name = ?;"
        cursor.execute(check_query, (group_name,))
        current_group = cursor.fetchone()[0]

        # Get values from the group
        values = {'user_id' : user_id,
                  'group_id' : current_group}
        
        query = """SELECT name, category, date, transaction_type, amount 
                    FROM expense 
                    WHERE user_id = :user_id
                        AND group_id = :group_id"""
        cursor.execute(query, values)
        results = cursor.fetchall()
        cursor.close()
        return results

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()






# AUTHENTICATION

# Log In
def log_in_check(username, password):
    # Validate both input fields if they are not empty
    if username == "":
        message = "Missing username"
        return (False, message, 0)
    
    if password == "":
        message = "Missing password"
        return (False, message, 0)
    
    # Search for user name in a table
    sqliteConnection = sqlite3.connect('expense_tracker.db')
    try:
        cursor = sqliteConnection.cursor()

        # Get group_id
        check_query = "SELECT id, hash FROM user WHERE username = ?;"
        cursor.execute(check_query, (username,))
        result_tuple = cursor.fetchone()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

    # If it does not exist - return 
    if not result_tuple:
        message = "No user found"
        return (False, message, 0)
    
    # Format hash
    password_bytes = password.encode('utf-8')

    # Check if password hash matches username_id record
    if bcrypt.checkpw(password_bytes, result_tuple[1]):
        return (True, "", result_tuple[0])

    # If password hash does not match 
    message = "Password does not match"
    return (False, message, 0)

        

# Register new user
def register_user(username, password, password_confirmation):    
    # Validate input fields
    if username == "":
        message = "Missing username"
        return (False, message)
    
    if password == "":
        message = "Missing password"
        return (False, message)
    
    if password_confirmation == "":
        message = "Missing password confirmation"
        return (False, message)
    
    if password != password_confirmation:
        message = "Passwords do not match"
        return (False, message)

    # Check if username already exists
    sqliteConnection = sqlite3.connect('expense_tracker.db')
    try:
        cursor = sqliteConnection.cursor()

        # Get group_id
        check_query = "SELECT id FROM user WHERE username = ?;"
        cursor.execute(check_query, (username,))
        result = cursor.fetchone()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

    if result:
        message = "Username already exists"
        return (False, message)

    # Generate salt and hash the password
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    # Insert user into users table
    sqliteConnection = sqlite3.connect('expense_tracker.db')
    try:
        cursor = sqliteConnection.cursor()

        values = { 'hash' : hashed_password,
                   'username' : username}
        query = """INSERT INTO user
                (hash, username)
                VALUES (:hash, :username)"""
        cursor.execute(query, values)
        sqliteConnection.commit()
        cursor.close()
        message = "New user added"
        return (True, message)

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

    return 1
