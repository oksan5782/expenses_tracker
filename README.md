# Expense Tracker Application


## Overview

The Expense Tracker Application is a user-friendly desktop application created using PyQT6 and designed to organize and track expenses. It provides a streamlined interface for managing financial data, reading and categorizing expenses from various sources, and gaining insights into user's spending habits.


## Features


### 1. Data Organization

1.1 CSV File Import: Upload expense data in the format downloaded from Chase or Discover websites, making it easy to get started.

1.2 Expense Parsing: The application intelligently parses imported CSV files to extract essential details such as category, date, time, and item name.

1.3 Expense Categorization: Automatically categorize and arrange all expenses in chronological order, making it convenient to track spending over time.

1.4 Balance Summaries: View expense summaries including yearly and monthly totals as well as charts with comparisons.

1.5 User Input Integration: Seamlessly combine user-provided input with the manual input of the data, ensuring comprehensive expense tracking.

### 2. User-Friendly Interface

2.1 Multiple Views: Switch between different views to analyze expenses based on a category or date.

2.2 Simplicity: The main interface is designed to be straightforward and uncluttered

2.3 Clear Summaries: All expense and income data is presented in a clear and concise format for easy reference.

### 3. User Interaction

3.1 Category-Based Expense Overview: Easily view overall expenses based on categories.

3.2 Manual Expense Input: Add expenses manually to ensure all financial transactions are recorded.

3.3 Editing and Deletion: Edit or delete expense items as needed to maintain accurate records.

3.4 Income Tracking: Keep track of the income alongside expenses to maintain a complete financial overview.


### 4. Data Management

4.1 Input New Data: Add new financial data seamlessly to the expense tracker.

4.2 Session Persistence: Once user creates an account, the application locally stores all previous session changes and inputs, ensuring continuity and data integrity when reopened.


## Prerequisites

Before running the application, have the following dependencies installed:z

- PyQt6
- SQLite3
- pandas
- bcrypt

These dependencies could be installed using pip:

    'pip install PyQt6 pandas bcrypt sqlite3'


## Usage

- Upload expense data from Discover or Chase in CSV format or input expense record manually
- The application will automatically categorize and organize expenses.
- Explore financial data using the intuitive interface, switch between different views, check out graphs and analyze spending habits.
- Add, edit, or delete expense items manually as needed.
- Manage expenses in customized groups
- Keep track of the income to maintain a complete financial overview.

## Screenshots

Login and Registration Forms
<img width="1138" alt="Login and Registration Forms" src="https://github.com/oksan5782/expenses_tracker/assets/57775793/ddc84d51-b514-421c-8b60-cd5961403c4d">

Main Window View
<img width="1246" alt="Main Window" src="https://github.com/oksan5782/expenses_tracker/assets/57775793/8300966a-1109-4953-8a94-f0cd3a03c7b5">

Manual Insertion of the Expense/Income Record
<img width="1043" alt="Add Expense/Income" src="https://github.com/oksan5782/expenses_tracker/assets/57775793/d2b7ac0c-7077-4cbd-b51f-1c68254cc747">

Calendar Date View
<img width="1197" alt="Calendar" src="https://github.com/oksan5782/expenses_tracker/assets/57775793/bef2f0d7-9d10-47b0-a28b-e853b3f913aa">

One of the Categories View
<img width="1276" alt="Category View" src="https://github.com/oksan5782/expenses_tracker/assets/57775793/8b070343-f60c-4cfe-8a58-4a126baa54a1">

## License

This project is licensed under the MIT License

