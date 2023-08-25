import sqlite3

# Establish connection
sqliteConnection = sqlite3.connect('expense_tracker.db')

# Get a curson
cur = sqliteConnection.cursor()

# Users table
cur.execute("""CREATE TABLE user (
    id INTEGER PRIMARY KEY NOT NULL,
    hash TEXT NOT NULL,
    username TEXT NOT NULL)""")

# Income table
cur.execute("""CREATE TABLE income (
    income_id INTEGER PRIMARY KEY NOT NULL,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id))""")

# Groups table
cur.execute("""CREATE TABLE groups (
    group_id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL)""")

# Expense table - Allow NULL values for recurring and group_id
cur.execute("""CREATE TABLE expense (
    expense_id INTEGER PRIMARY KEY NOT NULL,
    name TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    group_id INTEGER, 
    user_id INTEGER NOT NULL,
    FOREIGN KEY (group_id) REFERENCES groups (group_id),
    FOREIGN KEY (user_id) REFERENCES user (id))""")

# Save created tables
sqliteConnection.commit()

# Close connections
cur.close()
sqliteConnection.close()

