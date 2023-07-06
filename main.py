
# GROUP list contains a tuple with group title [0] and amout spent [1]
GROUP_LIST = [('Hawaii 22-23', 2000), ('Japan May 23', 2050), ('Japan Sep 23', 1500), ('Medical', 500), ('Dental', 100)]


# CATEGORIES SECTION Select top 10 of expenses categories with the amount spent this month
CATEGORIES_LIST = [('Rent', 2000), ('Groceries', 500), ('Online Orders', 200), ('Eating Out', 150), ('Fitness', 100), ('Other', 100)]


# EXTRACT DATA for top 5 + OTHER categories not in groups grouped by month
RECENT_EXPENCES = {"Rent" : [2000, 2000, 2000, 2000, 2000, 2000],
                   "Utilities" : [300, 300, 300, 250, 300, 300],
                   "Groceries" : [500, 650, 600, 550, 500, 530],
                   "Eating Out" : [200, 100, 150, 50, 70, 80],
                   "Online" : [50, 0, 200, 70, 10, 40],
                   "Other" : [200, 600, 150, 550, 75, 260]}

# Extract monthly limit set for current month
MONTHLY_LIMIT = 4000

# Extract the sum of all expenses this month
THIS_MONTH_EXPENSES = 3300