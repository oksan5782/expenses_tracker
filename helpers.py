from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd
import bcrypt 
import sqlite3


"""CONSTANTS"""

#  Categories list 
ALL_POSSIBLE_CATEGORIES_LIST = ["Rent", "Transportation", "Groceries", "Utilities", "Eating Out", "Health", "Entertainment", "Subscriptions", "Sport", "Other"]

# Expense types
ALL_EXPENSE_TYPES = ["Credit", "Cash", "Check", "Foreign Currency"]


"""Date/Datetime Functions"""

def get_last_day_of_current_month():

    current_date = datetime.now()

    # Get the first day of the next month
    first_day_of_next_month = datetime(current_date.year, current_date.month % 12 + 1, 1)

    # Subtract one day from the first day of the next month to get the last day of the current month
    last_day_of_current_month = first_day_of_next_month - timedelta(days=1)

    return last_day_of_current_month


# Get the list of strings for the last 6 months in the format YYYY-MM
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


# Check if the date value is valid
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


# Get a dictionary of the expenses for the last 6 months
def get_recent_expenses(user_id):
    sqliteConnection = sqlite3.connect('expense_tracker.db')
    try:
        cursor = sqliteConnection.cursor()

        # SQL query to get the list of 6 categories sorted by total amount of expenses
        categories_query = """ SELECT category, SUM(amount) AS total_amount
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

        # If there are no records
        if not sums_data:
            return None

        # Organize results in a dictionary
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



# Get a sum of amounts of income grouped by months
def get_monthly_income(user_id):
    sqliteConnection = sqlite3.connect('expense_tracker.db')

    current_month = datetime.now().strftime("%Y-%m")  

    try:
        cursor = sqliteConnection.cursor()
        values = {
                   'current_month' : current_month,
                   'user_id' : user_id}
        query = """ SELECT IFNULL(SUM(amount), 0) 
                    FROM income 
                    WHERE user_id = :user_id 
                        AND strftime('%Y-%m', date) = :current_month"""
        cursor.execute(query, values)
        result = cursor.fetchone()[0]
        cursor.close()
        return result
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)      
    finally:
        if sqliteConnection:
            sqliteConnection.close()


# Get a sum of expenses for the current month
def get_this_month_expenses(user_id):
    sqliteConnection = sqlite3.connect('expense_tracker.db')

    current_month = datetime.now().strftime("%Y-%m") 
    try:
        cursor = sqliteConnection.cursor()
        values = {
                   'current_month' : current_month,
                   'user_id' : user_id}
        query = """ SELECT IFNULL(SUM(amount), 0) 
                    FROM expense 
                    WHERE user_id = :user_id 
                        AND strftime('%Y-%m', date) = :current_month"""
        cursor.execute(query, values)
        result = cursor.fetchone()[0]
        cursor.close()
        return result
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


# Get a list of all user expense records in descending order
def get_user_expenses(user_id):
    sqliteConnection = sqlite3.connect('expense_tracker.db')
    try:
        cursor = sqliteConnection.cursor()
        query = """ SELECT name, category, date, transaction_type, amount
                    FROM expense 
                    WHERE user_id = :user_id 
                    ORDER BY date DESC"""
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        cursor.close()
        return result
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


# Get a list of all user income records in descending order
def get_user_income(user_id):
    sqliteConnection = sqlite3.connect('expense_tracker.db')
    try:
        cursor = sqliteConnection.cursor()
        query = """ SELECT date, amount 
                    FROM income 
                    WHERE user_id = :user_id 
                    ORDER BY date DESC"""
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        cursor.close()
        return result
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


# Extract the sum of expenses for a given date
def get_sum_expenses_by_date(user_id, date):
    sqliteConnection = sqlite3.connect('expense_tracker.db') # No need to validate date sinse its taken from Calendar widget
    try:
        cursor = sqliteConnection.cursor()
        values = {
                   'date' : date,
                   'user_id' : user_id}
        query = """ SELECT SUM(amount) 
                    FROM expense 
                    WHERE user_id = :user_id 
                        AND date = :date"""
        cursor.execute(query, values)
        result = cursor.fetchone()[0]
        cursor.close()
        return result
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


# Extract all expense records for a given date
def get_list_expenses_by_date(user_id, date):
    sqliteConnection = sqlite3.connect('expense_tracker.db')
    try:
        cursor = sqliteConnection.cursor()
        values = {
                   'date' : date,
                   'user_id' : user_id}
        query = """ SELECT name, category, amount 
                    FROM expense
                    WHERE date = :date 
                        AND user_id = :user_id"""
        cursor.execute(query, values)
        results = cursor.fetchall()
        cursor.close()
        return results
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


 # Select the 1st date of the month of the first record by this user
def get_last_start_date_of_oldest_record(user_id):
    sqliteConnection = sqlite3.connect('expense_tracker.db')

    try:
        cursor = sqliteConnection.cursor()
        values = {'user_id' : user_id}
        query = """ SELECT MIN(date) 
                    FROM expense 
                    WHERE user_id = :user_id
                    LIMIT 1"""
        cursor.execute(query, values)
        results = cursor.fetchone()[0]
        cursor.close()

        # If there are no records return the first date of the current month
        if not results:
            today = datetime.today()
            first_date_of_month = today.replace(day=1)
            return (False, first_date_of_month)

        return (True, convert_to_date_time(results))
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


# Crate a group by adding a group_id to the list of selected records
def create_group(user_id, group_name, list_of_group_records):
    sqliteConnection = sqlite3.connect('expense_tracker.db')
    try:
        cursor = sqliteConnection.cursor()

        # Check if any group with this name already exists
        check_query = "SELECT group_id FROM groups WHERE name = ?;"
        cursor.execute(check_query, (group_name,))
        existing_group = cursor.fetchone()

        # Add group name to the groups table and get its group_id
        if not existing_group:
            insert_query = "INSERT INTO groups (name) VALUES (?);"
            cursor.execute(insert_query, (group_name,))

            # Get the newly created group_id
            existing_group = cursor.lastrowid
        else: 
            existing_group = existing_group[0]

        # Create data list to update group_id
        data_list = []

        # Prepare record values for the update SQL query
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
        
        # Execute an update query for each dictionary in the list
        for data_dict in data_list:
            cursor.execute(update_query, data_dict)

        # Commit changes and close the connection
        sqliteConnection.commit()
        cursor.close()
        return 0
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


# Get a tuple of the group name and total amount by user id
def get_groups_list(user_id):
    sqliteConnection = sqlite3.connect('expense_tracker.db')
    try:
        cursor = sqliteConnection.cursor()
        values = {'user_id' : user_id}

        # Get group names and sum of amounts for the given user_id
        query = """SELECT g.name, COALESCE(SUM(e.amount), 0) AS total_amount
                    FROM groups g
                    LEFT JOIN expense e ON g.group_id = e.group_id
                    WHERE e.user_id = :user_id
                    GROUP BY g.group_id
                    LIMIT 10 """
        cursor.execute(query, values)
        results = cursor.fetchall()
        cursor.close()
        return results
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

# Get a list of tuples for a category and expenses belonging to it for the current month
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


# Get a dictionary of the year and its total expenses sum
def get_yearly_expenses_summary(user_id, start_date, end_date):
    sqliteConnection = sqlite3.connect('expense_tracker.db')
    try:
        cursor = sqliteConnection.cursor() 
            
        query = """
            SELECT strftime('%Y', date) AS year, 
            SUM(amount) AS total_expenses
            FROM expense
            WHERE user_id = ? AND date >= ? AND date <= ?
            GROUP BY year
        """
        
        cursor.execute(query, (user_id, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
        expenses_sum = cursor.fetchall()
        expenses_by_year = {str(year): 0 for year in range(start_date.year, end_date.year + 1)}
        for row in expenses_sum:
            year, total_expenses = row
            expenses_by_year[year] = total_expenses
        return expenses_by_year

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close() 


# Get a dictionary of the year and its total income sum
def get_yearly_income_summary(user_id, start_date, end_date):
    sqliteConnection = sqlite3.connect('expense_tracker.db')

    try:
        cursor = sqliteConnection.cursor() 
            
        query = """
            SELECT strftime('%Y', date) AS year, 
            SUM(amount) AS total_expenses
            FROM income
            WHERE user_id = ? AND date >= ? AND date <= ?
            GROUP BY year
        """
        
        cursor.execute(query, (user_id, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
          
        income_sum = cursor.fetchall()
        income_by_year = {str(year): 0 for year in range(start_date.year, end_date.year + 1)}
        for row in income_sum:
            year, total_income = row
            income_by_year[year] = total_income
        return income_by_year

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


# Get a dictionary of the months and their total expenses sums      
def get_monthly_expenses_summary(user_id, start_date, end_date):
    sqliteConnection = sqlite3.connect('expense_tracker.db')
    try:
        cursor = sqliteConnection.cursor() 
            
        query = """
            SELECT strftime('%Y-%m', date) AS month, 
            SUM(amount) AS total_expenses
            FROM expense
            WHERE user_id = ? AND date >= ? AND date <= ?
            GROUP BY month
        """
        
        cursor.execute(query, (user_id, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
          
        expenses_sum = cursor.fetchall()

        # Create a defaultdict to store expenses by month
        expenses_by_month = defaultdict(float)

        # Create a set to store unique months
        unique_months = set()

        # Iterate through expenses_sum and update the unique_months set
        for month, _ in expenses_sum:
            unique_months.add(month)

        # Initialize missing months with zero expenses
        current_date = start_date
        while current_date <= end_date:
            year_month = current_date.strftime("%Y-%m")
            if year_month not in unique_months:
                expenses_sum.append((year_month, 0.0))
            current_date += timedelta(days=30)  # Assuming roughly 30 days per month

        # Iterate through expenses_sum and update the expenses_by_month dictionary
        for month, total_expenses in expenses_sum:
            expenses_by_month[month] += total_expenses

        expenses_dict_by_month = dict(sorted(expenses_by_month.items(), reverse=True))

        return expenses_dict_by_month

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close() 


# Get a dictionary of the months and their total income sums      
def get_monthly_income_summary(user_id, start_date, end_date):
    sqliteConnection = sqlite3.connect('expense_tracker.db')
    try:
        cursor = sqliteConnection.cursor() 
            
        query = """
            SELECT strftime('%Y-%m', date) AS month, 
            SUM(amount) AS total_expenses
            FROM income
            WHERE user_id = ? AND date >= ? AND date <= ?
            GROUP BY month
        """
        
        cursor.execute(query, (user_id, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")))
        income_sum = cursor.fetchall()

        # Create a defaultdict to store income sums by month
        income_by_month = defaultdict(float)

        # Create a set to store unique months
        unique_months = set()

        # Iterate through income_sum and update the unique_months set
        for month, _ in income_by_month:
            unique_months.add(month)

        # Initialize missing months with zero income
        current_date = start_date
        while current_date <= end_date:
            year_month = current_date.strftime("%Y-%m")
            if year_month not in unique_months:
                income_sum.append((year_month, 0.0))
            current_date += timedelta(days=30)  # Assuming roughly 30 days per month

        # Iterate through income_sum and update the income_by_month dictionary
        for month, total_income in income_sum:
            income_by_month[month] += total_income

        income_dict_by_month = dict(sorted(income_by_month.items(), reverse=True))
        
        return income_dict_by_month

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


# Add expense record into the database
def add_expense_into_db(user_id, type, name, date, category, amount):
    sqliteConnection = sqlite3.connect('expense_tracker.db')
    
    # Check if the name field is not missing
    if name == "":
        message = "Missing name"
        return (False, message)
    
    # Validate date format
    if not is_valid_datetime_format(date):
        message = "Invalid Date Format. Please use YYYY-MM-DD"
        return (False, message)
    
    # Check if amount is a positive numeric value
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
        message = "Expense added"
        return (True, message)
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


# Check whether the record is added to the database
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


# Upload expenses from a Chase .csv file
def upload_expense_csv_chase(user_id, file):
    try:
        df = pd.read_csv(file)

        # Remove "thank you" - credit cover line 
        df_cover_credit_row_index = df[(df['Description'].str.contains('Payment Thank You')) & (df['Type'] == 'Payment')].index
        df.drop(df_cover_credit_row_index, inplace=True)

        # Format date values to strings 
        df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], format='%m/%d/%Y')
        df['Transaction Date'] = df['Transaction Date'].dt.strftime('%Y-%m-%d')

        # Format amount values to float type
        df['Amount'] = df['Amount'].astype(float)

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

        # Find the last uploaded transaction:
        check_first_row = check_record_presence(user_id, df.loc[0, 'Description'], df.loc[0, 'Category'], df.loc[0, 'Amount'], df.loc[0, 'Transaction Date'])

        # If the latest record is already added, all of the table content has been already uploaded
        if check_first_row:
            message = "The file content was already added to the database"
            return (False, message)
    
        # Check if the last record has been uploaded
        last_row_index = df.tail(1).index[0]
        check_last_row = check_record_presence(user_id, df.loc[last_row_index, 'Description'], df.loc[last_row_index, 'Category'], df.loc[last_row_index, 'Amount'], df.loc[last_row_index, 'Transaction Date'])

        # If oldest value is in the database, attempting binary search to find where the division starts
        if check_last_row:
            top_row = 0
            bottom_row = last_row_index
            # Buttom row value will be last index 
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


# Upload expenses from a Discover .csv file
def upload_expense_csv_discover(user_id, file):
    try:
        df = pd.read_csv(file)

        # Remove "thank you" - credit cover line 
        df_cover_credit_row_index = df[(df['Description'].str.contains('THANK YOU')) & (df['Category'] == 'Payments and Credits')].index
        df.drop(df_cover_credit_row_index, inplace=True)

        # Update date values to strings 
        df['Trans. Date'] = pd.to_datetime(df['Trans. Date'], format='%m/%d/%Y')
        df['Trans. Date'] = df['Trans. Date'].dt.strftime('%Y-%m-%d')

        # Update amount values to float type
        df['Amount'] = df['Amount'].astype(float)

        # Get negative values to upload them as income 
        df_returns_or_income = df[df['Amount'] < 0]

        # Change the sign of return or income records  
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

        # Find the last uploaded transaction:
        check_first_row = check_record_presence(user_id, df.loc[0, 'Description'], df.loc[0, 'Category'], df.loc[0, 'Amount'], df.loc[0, 'Trans. Date'])

        # If latest record is already added, all of the table content has been already uploaded
        if check_first_row:
            message = "The file content was already added to the database"
            return (False, message)

        # Check if the last record has been uploaded
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


# Add income record
def add_income_into_db(user_id, date, amount):
    sqliteConnection = sqlite3.connect('expense_tracker.db')

    # Validate date format
    if not is_valid_datetime_format(date):
        message = "Invalid Date Format. Please use YYYY-MM-DD"
        return (False, message)
    
    # Check if the amount is a positive numeric value
    if not is_valid_numeral(amount):
        message = "Invalid amount"
        return (False, message)
    try:
        cursor = sqliteConnection.cursor()
        values = { 'date' : date,
                   'amount' : float(amount),
                   'user_id' : user_id}
        query = """INSERT INTO income
                (date, amount, user_id)
                VALUES (:date, :amount, :user_id)"""
        cursor.execute(query, values)
        sqliteConnection.commit()
        cursor.close()
        message = "Income value added"
        return (True, message)
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


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


# Set group_id of the selected record to None
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



# Update expense record with the new values 
def edit_record(user_id, record_before_editing_list, record_after_editing_list):

    # Map record values to the dictionary
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
    
    # Check if the name field is not missing
    if values['new_name'] == "":
        message = "Missing name"
        return (False, message)
    
    # Check if the transaction type of the updated record is valid
    if values['new_type'] not in ALL_EXPENSE_TYPES:
        message = "Invalid transaction type"
        return (False, message)
    
    # check if the amount is a positive numeric value
    if not is_valid_numeral(values['new_amount']):
        message = "Invalid amount"
        return (False, message)
    
    # Check if category is among the ones available
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
        message = "Expense updated"
        return (True, message)
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    

# Update income record with the new values 
def edit_income_record(user_id, record_before_editing_list, record_after_editing_list):
    # Map record values to the dictionary
    values = {
        'user_id' : user_id,
        'prev_date' : record_before_editing_list[0],
        'prev_amount' : record_before_editing_list[1],

        'new_date' : record_after_editing_list[0], 
        'new_amount' : record_after_editing_list[1]
    }

    # Validate date format
    if not is_valid_datetime_format(values['new_date']):
        message = "Invalid Date Format. Please use YYYY-MM-DD"
        return (False, message)

    # Check if the amount is a positive numeric value
    if not is_valid_numeral(values['new_amount']):
        message = "Invalid amount"
        return (False, message)

    sqliteConnection = sqlite3.connect('expense_tracker.db')
    try:
        cursor = sqliteConnection.cursor()
        query = """UPDATE income
                SET date = :new_date,
                    amount = :new_amount
                WHERE user_id = :user_id
                    AND date = :prev_date
                    AND amount = :prev_amount;
                        """
        cursor.execute(query, values)
        sqliteConnection.commit()
        cursor.close()
        message = "Income updated"
        return (True, message)
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


# Delete a record from the expense table of the database
def remove_record(user_id, expense_name, category, date, transaction_type, amount):
    sqliteConnection = sqlite3.connect('expense_tracker.db')

    try:
        cursor = sqliteConnection.cursor()

        values = {'user_id' : user_id,
                  'name' : expense_name,
                  'category': category,
                  'date' : date,
                  'transaction_type' : transaction_type,
                  'amount' : float(amount)
                  }

        delete_query = """
        DELETE FROM expense
        WHERE user_id = :user_id
            AND name = :name
            AND category = :category
            AND date = :date
            AND transaction_type = :transaction_type
            AND amount = :amount;
        """
        cursor.execute(delete_query, values)

        # Commit changes and close the connection
        sqliteConnection.commit()
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


# Delete a record from the income table of the database
def remove_income_record(user_id, date, amount):
    sqliteConnection = sqlite3.connect('expense_tracker.db')

    try:
        cursor = sqliteConnection.cursor()

        values = {'user_id' : user_id,
                  'date' : date,
                  'amount' : float(amount)
                  }

        delete_query = """
        DELETE FROM income
        WHERE user_id = :user_id
            AND date = :date
            AND amount = :amount;
        """
        cursor.execute(delete_query, values)

        # Commit changes and close the connection
        sqliteConnection.commit()
        cursor.close()
        return True
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


# Select records from the expense table by group and user ids
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


""" AUTHENTICATION """

# Log in user
def log_in_check(username, password):

    # Validate username input field 
    if username == "":
        message = "Missing username"
        return (False, message, 0)
    
    # Validate password input field 
    if password == "":
        message = "Missing password"
        return (False, message, 0)
    
    # Search for user name in the user table
    sqliteConnection = sqlite3.connect('expense_tracker.db')
    try:
        cursor = sqliteConnection.cursor()

        # Get user's id and password hash based on the username
        check_query = "SELECT id, hash FROM user WHERE username = ?;"
        cursor.execute(check_query, (username,))
        result_tuple = cursor.fetchone()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

    # If it does not exist - return False
    if not result_tuple:
        message = "No user found"
        return (False, message, 0)
    
    # Format the content of the password input field
    password_bytes = password.encode('utf-8')

    # Check if the password hash matches username_id record
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

        # Get user_id by username
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

    # Insert new user into the users table
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
