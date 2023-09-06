# Expense Tracker Application


## Overview

The Expense Tracker Application is a user-friendly desktop applicatio designed to help users to organize and track their expenses effectively. It provides a streamlined interface for managing their financial data, reading and categorizing expenses from various sources, and gaining insights into their spending habits.


## Features


### 1. Data Organization

    1.1 CSV File Import: Upload expense data in the format downloaded from Chase or Discover websites, making it easy to get started.

    1.2 Expense Parsing: The application intelligently parses imported CSV files to extract essential details such as category, date, time, and item name.

    1.3 Expense Categorization: Automatically categorize and arrange all expenses in chronological order, making it convenient to track your spending over time.

    1.4 Balance Summaries: View expense summaries including yearly and monthly totals.

    1.5 User Input Integration: Seamlessly combine user-provided input with imported data, ensuring comprehensive expense tracking.

### 2. User-Friendly Interface

    2.1 Multiple Views: Switch between different views, allowing you to analyze expenses based on a category or date.

    2.2 Simplicity: The main interface is designed to be straightforward and uncluttered, providing a hassle-free experience.

    2.3 Clear Functionality: Buttons for user input are labeled clearly, ensuring you understand their purpose.

    2.4 Clear Summaries: All expense and income data, is presented in a clear and concise format for easy reference.

### 3. User Interaction

    3.1 Category-Based Expense Overview: Easily view overall expenses based on categories, helping you identify where your money is going.

    3.2 Manual Expense Input: Add expenses manually to ensure all financial transactions are recorded.

    3.3 Editing and Deletion: Edit or delete expense items as needed to maintain accurate records.

    3.4 Income Tracking: Keep track of your income alongside your expenses to maintain a complete financial overview.


### 4. Data Management

    4.1 Input New Data: Add new financial data seamlessly to your expense tracker.

    4.2 Session Persistence: Once user creates an account, the application locally stores all previous session changes and inputs, ensuring continuity and data integrity when reopened.


## Prerequisites

Before running the application, ensure you have the following dependencies installed:

    - PyQt6
    - SQLite3
    - pandas
    - bcrypt

These dependencies could be installed using pip:

    'pip install PyQt6 pandas bcrypt sqlite3'


## Usage

    - Upload your expense data from Discover or Chase in CSV format or input expence record manually
    - The application will automatically categorize and organize your expenses.
    - Explore your financial data using the intuitive interface, switch between different views, check out graphs and analyze your spending habits.
    - Add, edit, or delete expense items manually as needed.
    - Manage expenses in customized groups
    - Keep track of your income to maintain a complete financial overview.
    - Enjoy a seamless experience with data persistence across sessions.


## License

This project is licensed under the MIT License

