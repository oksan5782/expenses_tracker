from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout,
                              QHBoxLayout, QLineEdit, QTableWidget, 
                              QHeaderView, QTableWidgetItem)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Import data insertion function
import sys
sys.path.append('../helpers')
from helpers import (get_last_start_date_of_oldest_record, get_last_day_of_current_month, 
                    get_yearly_expenses_summary, get_yearly_income_summary,
                    get_monthly_expenses_summary, get_monthly_income_summary)


class ViewBalanceWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()  
        self.user_id = user_id
        self.setWindowTitle("Balance")
        self.setStyleSheet('background-color: #F5FFFA')
        self.setGeometry(300, 150, 800, 500)
        self.init_balance_ui()
        self.table_stylesheet = """
        QTableWidget {

            border-radius: 5px;
            font-family: Futura;
        }

            QTableWidget QHeaderView::section {
            color: #05132E;
            border: none;
            font-weight: 600;
            font-size: 16px;

        }

            QTableWidget::item {
            padding: 5px;
            background-color: #E8EFFC;
            color: #2F4F4F;
        }"""

    def init_balance_ui(self):

        # Add layout
        self.main_layout = QVBoxLayout()

        self.content_layout = QHBoxLayout()

        # Left section with year table and income/expense view
        left_layout = QVBoxLayout()
    
        # History time range
        self.oldest_record = get_last_start_date_of_oldest_record(self.user_id)

        self.latest_date = get_last_day_of_current_month()

        # Yearly summary table
        self.year_table = QTableWidget(self)
        self.fill_yearly_table()
        left_layout.addWidget(self.year_table)

        self.expense_list = QPushButton("View Expenses List")
        self.expense_list.setCursor(Qt.CursorShape.PointingHandCursor)
        self.expense_list.setFixedWidth(240)
        self.expense_list.setStyleSheet("background-color: #87cefa; border: none; border-radius: 5; padding: 5 0" )
        self.expense_list.setFont(QFont("Futura", 16))
        self.expense_list.clicked.connect(self.view_expense_list)

        left_layout.addWidget(self.expense_list, alignment=Qt.AlignmentFlag.AlignCenter)

        self.income_list = QPushButton("View Income List")
        self.income_list.setCursor(Qt.CursorShape.PointingHandCursor)
        self.income_list.setFixedWidth(240)
        self.income_list.setStyleSheet("background-color: #a3dcce; border: none; border-radius: 5; padding: 5 0" )
        self.income_list.setFont(QFont("Futura", 16))
        self.income_list.clicked.connect(self.view_income_list)
        left_layout.addWidget(self.income_list, alignment=Qt.AlignmentFlag.AlignCenter)

        self.content_layout.addLayout(left_layout)
        
        # Right part of the content layout - monthly summary table
        self.monthly_table = QTableWidget(self)
        self.fill_montly_table()
        self.content_layout.addWidget(self.monthly_table)

        self.main_layout.addLayout(self.content_layout)

        # Closing button
        self.closing_button = QPushButton("Close")
        self.closing_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.closing_button.setFixedWidth(150)
        self.closing_button.setStyleSheet("background-color: #B0C4DE; border: none; border-radius: 5; padding: 5 0" )
        self.closing_button.setFont(QFont("Futura", 16))
        self.closing_button.clicked.connect(self.close_balanse_window)
        self.main_layout.addWidget(self.closing_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Apply layout
        self.setLayout(self.main_layout)


    # Insert values into yearly table
    def fill_yearly_table(self):
        self.year_table.verticalHeader().setVisible(False)
        # self.year_table.setStyleSheet(self.table_stylesheet)
        self.year_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.year_table.setColumnCount(4)
        self.year_table.setHorizontalHeaderLabels(["Year", "Income", "Expense", "Balance"])
        self.year_table.verticalHeader().setDefaultSectionSize(40)

        # If table is empty return no data
        if not self.oldest_record[0]:
            self.year_table.setRowCount(1)
            self.year_table.setSpan(0, 0, 1, 4)
            self.year_table.setItem(0, 0, QTableWidgetItem("No Data"))
        else:
            # Get expenses dictionaries
            yearly_expense_summaries = get_yearly_expenses_summary(self.user_id, self.oldest_record[1], self.latest_date)

            # Get income dictionaries
            yearly_income_summaries = get_yearly_income_summary(self.user_id, self.oldest_record[1], self.latest_date)

            # Create a list to populate the table 
            combined_list = []

            for key in yearly_expense_summaries.keys():
                value_expense = yearly_expense_summaries[key]
                value_income = yearly_income_summaries[key]
                difference = value_income - value_expense
                combined_list.append([key, value_income, value_expense, difference])

            # Set the row count of the table
            num_rows = len(combined_list)

            self.year_table.setRowCount(num_rows)
            
            # Populate the table
            for i, yearly_record in enumerate(combined_list):
                year = yearly_record[0]
                income = int(yearly_record[1])
                expense = int(yearly_record[2])
                difference = int(yearly_record[3])

                # Insert extracted data into a row
                self.year_table.setItem(i, 0, QTableWidgetItem(year))
                self.year_table.setItem(i, 1, QTableWidgetItem(str(income)))
                self.year_table.setItem(i, 2, QTableWidgetItem(str(expense)))
                self.year_table.setItem(i, 3, QTableWidgetItem(str(difference)))

            self.year_table.resizeColumnsToContents()


    # Populate monthly table
    def fill_montly_table(self):
        self.monthly_table.verticalHeader().setVisible(False)
        # self.monthly_table.setStyleSheet(self.table_stylesheet)
        self.monthly_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.monthly_table.setColumnCount(4)
        self.monthly_table.setHorizontalHeaderLabels(["Month", "Income", "Expense", "Balance"])
        self.monthly_table.verticalHeader().setDefaultSectionSize(42)

            # If table is empty return no data
        if not self.oldest_record[0]:
            self.monthly_table.setRowCount(1)
            self.monthly_table.setSpan(0, 0, 1, 4)
            self.monthly_table.setItem(0, 0, QTableWidgetItem("No Data"))
        else:
            # Get expenses dictionaries
            monthly_expense_summaries = get_monthly_expenses_summary(self.user_id, self.oldest_record[1], self.latest_date)
            
            # Get income dictionaries
            monthly_income_summaries = get_monthly_income_summary(self.user_id, self.oldest_record[1], self.latest_date)

            # Create a list to populate the table 
            combined_list = []

            for key in monthly_expense_summaries.keys():
                value_expense = monthly_expense_summaries[key]
                value_income = monthly_income_summaries[key]
                difference = value_income - value_expense
                combined_list.append([key, value_income, value_expense, difference])

            # Set the row count of the table
            num_rows = len(combined_list)
            self.monthly_table.setRowCount(num_rows)
            
            # Populate the table
            for i, monthly_record in enumerate(combined_list):
                year = monthly_record[0]
                income = int(monthly_record[1])
                expense = int(monthly_record[2])
                difference = int(monthly_record[3])

                # Insert extracted data into a row
                self.monthly_table.setItem(i, 0, QTableWidgetItem(year))
                self.monthly_table.setItem(i, 1, QTableWidgetItem(str(income)))
                self.monthly_table.setItem(i, 2, QTableWidgetItem(str(expense)))
                self.monthly_table.setItem(i, 3, QTableWidgetItem(str(difference)))

            self.monthly_table.resizeColumnsToContents()

    def view_expense_list(self):
        ...

    def view_income_list(self):
        ...

    def close_balanse_window(self):
        # GO BACK TO MAIN WINDOW
        self.close()

