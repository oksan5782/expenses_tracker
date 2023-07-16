
# FUNCTIONS FOR MAIN WINDOW WIDGET

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
def add_expense_into_db(user_id, name, date, category, amount):
    print("Added expense into the database")
    print("Input value is " + str(user_id) + str(name) + " " + str(date) + " " + category + " " + str(amount))


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


def remove_record(user_id, category, name, date, amount):
    print("Removing")
    print(str(user_id) + " " + category + " " + name + " " + date + " " + str(amount))


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

