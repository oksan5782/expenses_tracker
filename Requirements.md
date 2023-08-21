'''
App to organize expenses
     -read excel/csv file downloaded from credit card websites
     -parse excel for category of expenses
        -allow user to input key words into categories OR use dictionary of synonyms to try and capture similar labeling
    -categorize all expenses, order by date time
        -separate views for year, month
    -total sums for year, month, week (overall expenses)
        -option to see overall expenses based on category
        -option to add income and check net balance
    -save data for quick access next time
        -able to add on to existing data
    -able to manually input expense (category, date/time, etc)
    -able to add notes to individual expenses

GUI Notes
    -Calender style view w/ side window

Requirements:
x.x - App shall help user organize and track expenses
    1.0 - App shall read and organize data
        1.1 - App shall read excel/csv files that user uploads in a format downloaded from credit card websites
        1.2 - App shall parse excel file for category of expenses, date, time, and name of item
        1.3 - App shall categorize all expenses and order by date time
        1.4 - App shall calculate expenses for year, month
        1.5 - App shall read user input and combine with excel/csv inputs
    2.0 - App shall have a freindly user interface
        2.1 - App shall have different views for year, month
        2.2 - Main interface shall be simple and not over crowded
        2.3 - Any buttons for user input shall be clear on the function
        2.4 - App shall show all data (sums of expenses) in a clear and consice format
    3.0 - App shall respond to user input
        3.1 - App shall have option to be able to see overall expenses based on category
        3.2 - App shall allow manual input of expense
        3.3 - App shall allow notes to be added to any item
        3.4 - App shall allow items to be deleted or edited
        3.5 - App shall allow income to be added
    4.0 - App shall allow data to be saved
        4.1 - App shall allow new data to be inputed
        4.2 - App shall show all previous session changes and inputs when re-opened
'''

