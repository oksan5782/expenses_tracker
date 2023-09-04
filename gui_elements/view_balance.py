from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout,
                              QHBoxLayout, QLineEdit, QTableWidget, 
                              QHeaderView, QTableWidgetItem, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QBrush, QColor

# Import functions interacting with the database
import sys
sys.path.append('../helpers')
from helpers import (get_last_start_date_of_oldest_record, get_last_day_of_current_month, 
                    get_yearly_expenses_summary, get_yearly_income_summary,
                    get_monthly_expenses_summary, get_monthly_income_summary,
                    get_user_expenses, edit_record, remove_record,
                    get_user_income, edit_income_record, remove_income_record)


class ViewBalanceWindow(QWidget):
    def __init__(self, user_id, main_window):
        super().__init__()  
        self.user_id = user_id
        self.setWindowTitle("Balance")
        self.setStyleSheet('background-color: #F5FFFA')
        self.setGeometry(300, 150, 800, 500)
        self.main_window = main_window
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
        self.init_balance_ui()
        

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

        # Button to view list of expenses
        self.expense_list_button = QPushButton("View Expenses List")
        self.expense_list_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.expense_list_button.setFixedWidth(240)
        self.expense_list_button.setStyleSheet("background-color: #87cefa; border: none; border-radius: 5; padding: 5 0" )
        self.expense_list_button.setFont(QFont("Futura", 16))
        self.expense_list_button.clicked.connect(self.view_expense_list)

        left_layout.addWidget(self.expense_list_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Button to view the list of income records
        self.income_list_button = QPushButton("View Income List")
        self.income_list_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.income_list_button.setFixedWidth(240)
        self.income_list_button.setStyleSheet("background-color: #a3dcce; border: none; border-radius: 5; padding: 5 0" )
        self.income_list_button.setFont(QFont("Futura", 16))
        self.income_list_button.clicked.connect(self.view_income_list)
        left_layout.addWidget(self.income_list_button, alignment=Qt.AlignmentFlag.AlignCenter)

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


    # Insert values into the yearly table
    def fill_yearly_table(self):
        self.year_table.verticalHeader().setVisible(False)
        self.year_table.setStyleSheet(self.table_stylesheet)
        self.year_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.year_table.setColumnCount(4)
        self.year_table.setHorizontalHeaderLabels(["Year", "Income", "Expense", "Balance"])
        self.year_table.verticalHeader().setDefaultSectionSize(40)

        # If table is empty
        if not self.oldest_record[0]:
            self.year_table.setRowCount(1)
            self.year_table.setSpan(0, 0, 1, 4)
            self.year_table.setItem(0, 0, QTableWidgetItem("No Data"))
        else:
            # Get expense dictionaries
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
            
            # Populate yearly table
            for i, yearly_record in enumerate(combined_list):
                year = yearly_record[0]
                income = int(yearly_record[1])
                expense = int(yearly_record[2])
                difference = int(yearly_record[3])

                # Insert extracted data into the row
                self.year_table.setItem(i, 0, QTableWidgetItem(year))
                self.year_table.setItem(i, 1, QTableWidgetItem(str(income)))
                self.year_table.setItem(i, 2, QTableWidgetItem(str(expense)))
                self.year_table.setItem(i, 3, QTableWidgetItem(str(difference)))

            self.year_table.resizeColumnsToContents()


    # Insert data into a monthly table
    def fill_montly_table(self):
        self.monthly_table.verticalHeader().setVisible(False)
        self.monthly_table.setStyleSheet(self.table_stylesheet)
        self.monthly_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.monthly_table.setColumnCount(4)
        self.monthly_table.setHorizontalHeaderLabels(["Month", "Income", "Expense", "Balance"])
        self.monthly_table.verticalHeader().setDefaultSectionSize(42)

        # If table is empty
        if not self.oldest_record[0]:
            self.monthly_table.setRowCount(1)
            self.monthly_table.setSpan(0, 0, 1, 4)
            self.monthly_table.setItem(0, 0, QTableWidgetItem("No Data"))
        else:
            # Get expense dictionaries
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
            
            # Populate the monthly table
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

    # "View expense" button click
    def view_expense_list(self):
        self.expenses_list_window = ExpenseListWindow(self.user_id, self.table_stylesheet, self.main_window)
        self.expenses_list_window.show()

    # "View income" button click
    def view_income_list(self):
        self.income_list_window = IncomeListWindow(self.user_id, self.table_stylesheet, self.main_window)
        self.income_list_window.show()

    # Go back to the main window
    def close_balanse_window(self):
        self.close()


# Table with the list of expenses
class ExpenseListWindow(QWidget):
    def __init__(self, user_id, stylesheet, main_window):
        super().__init__()  
        self.user_id = user_id
        self.table_style = stylesheet
        self.main_window = main_window

        self.setWindowTitle("Expense")
        self.setStyleSheet('background-color: #F5FFFA')
        self.init_list_ui()


    def init_list_ui(self):
        outer_frame_layout = QVBoxLayout()

        self.setWindowTitle("Expenses")
        self.setGeometry(330, 250, 750, 450)

        self.table_widget = QTableWidget(self)

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget.setStyleSheet(self.table_style)
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(["Name", "Category", "Date", "Type", "Amount ($)", "Edit", "Delete"])
        self.table_widget.verticalHeader().setDefaultSectionSize(50)

        # Allow sorting by column header clicks
        header = self.table_widget.horizontalHeader()
        header.setSectionsClickable(True)
        header.sectionClicked.connect(self.header_clicked)

        # Get records from the database
        self.expenses_list = get_user_expenses(self.user_id)

        # Check for the absence of the records
        if not self.expenses_list:
            self.table_widget.setRowCount(1)
            self.table_widget.setSpan(0, 0, 1, 7)
            self.table_widget.setItem(0, 0, QTableWidgetItem("No Expense Data"))
        else:
            self.fill_table_content()

        outer_frame_layout.addWidget(self.table_widget)

        # Closing button
        closing_button = QPushButton("Close")
        closing_button.setCursor(Qt.CursorShape.PointingHandCursor)
        closing_button.setFixedWidth(150)
        closing_button.setStyleSheet("background-color: #B0C4DE; border: none; border-radius: 5; padding: 5 0" )
        closing_button.setFont(QFont("Futura", 16))
        closing_button.clicked.connect(self.close_expense_table)
        outer_frame_layout.addWidget(closing_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Set layout and display it
        self.setLayout(outer_frame_layout)  
        self.show()


    def fill_table_content(self):

        self.table_widget.clearContents()
        self.table_widget.setRowCount(len(self.expenses_list))

        for i, expense_record in enumerate(self.expenses_list):
            name = expense_record[0]
            category = expense_record[1]
            date = expense_record[2]
            transaction_type = expense_record[3]
            amount = expense_record[4]

            # Insert extracted data into the table row 
            self.table_widget.setItem(i, 0, QTableWidgetItem(name))
            self.table_widget.setItem(i, 1, QTableWidgetItem(category))
            self.table_widget.setItem(i, 2, QTableWidgetItem(date))
            self.table_widget.setItem(i, 3, QTableWidgetItem(transaction_type))
            self.table_widget.setItem(i, 4, QTableWidgetItem(str(amount)))

            # Button to edit the record
            edit_this_expense_record = QPushButton("Edit", self)
            edit_this_expense_record.setCursor(Qt.CursorShape.PointingHandCursor)
            edit_this_expense_record.setCheckable(True)
            edit_this_expense_record.setStyleSheet("background-color: #D9BFBF; border: none; border-radius: 5; padding: 5 0" )
            edit_this_expense_record.setFont(QFont("Futura", 16))
            edit_this_expense_record.clicked.connect(lambda checked, row=i: self.edit_this_expense_record(row, checked))

            # Button to remove the record from the database
            remove_this_expense_record = QPushButton("Delete", self)
            remove_this_expense_record.setCursor(Qt.CursorShape.PointingHandCursor)
            remove_this_expense_record.setStyleSheet("background-color: #DBC3A3; border: none; border-radius: 5; padding: 5 0" )
            remove_this_expense_record.setFont(QFont("Futura", 16))
            remove_this_expense_record.clicked.connect(lambda checked, row=i: self.remove_this_expense_record(row))

            self.table_widget.setCellWidget(i, 5, edit_this_expense_record)
            self.table_widget.setCellWidget(i, 6, remove_this_expense_record)

            # Set all labels as non-editable initially
            for column in range(5):
                label_item = self.table_widget.item(i, column)
                if label_item:
                    # The flags() method returns the current flags of the item, and we use a bitwise AND operation (&) with the complement (NOT) of the Qt.ItemFlag.ItemIsEditable flag to remove the Qt.ItemIsEditable flag from the item's flags.
                    label_item.setFlags(label_item.flags() & ~Qt.ItemFlag.ItemIsEditable)


    # Sort rows in the table according to the clicked column header
    def header_clicked(self, logical_index):
        # Sort by name
        if logical_index == 0:
            self.expenses_list = sorted(self.expenses_list, key=lambda x: x[0])
        # Sort by category
        if logical_index == 1:
            self.expenses_list = sorted(self.expenses_list, key=lambda x: x[1])
        # Sort by date
        if logical_index == 2:
            self.expenses_list = sorted(self.expenses_list, key=lambda x: x[2], reverse=True)
        # Sort by type
        if logical_index == 3:
            self.expenses_list = sorted(self.expenses_list, key=lambda x: x[3])
        # Sort by amount
        if logical_index == 4:
            self.expenses_list = sorted(self.expenses_list, key=lambda x: x[4], reverse=True)
        
        self.fill_table_content()


    # Remove current record from the database
    def remove_this_expense_record(self, row):

        # Collect data to find the record in the database
        row_data = [self.table_widget.item(row, column).text() for column in range(5)]
        sql_return_value = remove_record(self.user_id, row_data[0], row_data[1], row_data[2], row_data[3], row_data[4])
       
        # If the removal was successful
        if sql_return_value:
            success_msg = QMessageBox.information(self, "Information", "Record removed")

            # Repaint graph, categories view and balance widgets in the main window
            self.main_window.stacked_bar_chart.refresh_bar_chart()
            self.main_window.update_categories_area()
            self.main_window.update_groups_area()
            self.main_window.current_month_donut_chart.refresh_donut_chart()

            # Update expenses table
            self.table_widget.update()


    # Edit record and update it in the database
    def edit_this_expense_record(self, row_index, checked):
        if checked:  # When the "Edit" button is checked

            # Collect data to find the record in the database
            self.row_data_before_editing = []
            for column in range(5):
                label_item = self.table_widget.item(row_index, column)
                self.row_data_before_editing.append(label_item.text())
                if label_item:
                    label_item.setBackground(QBrush(QColor("#ADFF2F")))
                    label_item.setForeground(QBrush(QColor("#483D8B")))
                    label_item.setFlags(label_item.flags() | Qt.ItemFlag.ItemIsEditable)

            # Change text of the "Edit" button to "Apply"
            edit_button = self.table_widget.cellWidget(row_index, 5)
            edit_button.setText("Apply")

        else:  # When the "Apply" button is unchecked
            edited_row_data = []

            # Retrieve data from QTableWidgetItem
            for column in range(5):
                label_item = self.table_widget.item(row_index, column)
                if label_item:
                    edited_row_data.append(label_item.text())
                    label_item.setFlags(label_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    label_item.setBackground(QBrush(QColor("#F0FFF0")))
                    label_item.setForeground(QBrush(QColor("#000000")))  # Reset the text color

            # Change text of the "Apply" button to "Edit"
            edit_button = self.table_widget.cellWidget(row_index, 5)
            edit_button.setText("Edit")

            # Update the record in the database 
            result, message = edit_record(self.user_id, self.row_data_before_editing, edited_row_data)

            if not result:
                cannot_add_msg = QMessageBox.information(self, "Information", message)
            
            else:
                # If validation passed 
                success_msg = QMessageBox.information(self, "Information", message)

                # Repaint graph, categories view and balance widgets of the main window
                self.main_window.stacked_bar_chart.refresh_bar_chart()
                self.main_window.update_categories_area()
                self.main_window.update_groups_area()
                self.main_window.current_month_donut_chart.refresh_donut_chart()


    def close_expense_table(self):
        self.hide()


# Table with the list of income records
class IncomeListWindow(QWidget):
    def __init__(self, user_id, stylesheet, main_window):
        super().__init__()  
        self.user_id = user_id
        self.main_window = main_window
        self.setWindowTitle("Income")
        self.setStyleSheet('background-color: #F5FFFA')
        self.table_style = stylesheet
        self.init_list_ui()


    def init_list_ui(self):
        outer_frame_layout = QVBoxLayout()

        self.setWindowTitle("Income")
        self.setGeometry(450, 250, 600, 400)

        self.table_widget = QTableWidget(self)

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget.setStyleSheet(self.table_style)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Date", "Amount ($)", "Edit", "Delete"])
        self.table_widget.verticalHeader().setDefaultSectionSize(50)

        # Allow sorting by column header clicks
        header = self.table_widget.horizontalHeader()
        header.setSectionsClickable(True)
        header.sectionClicked.connect(self.header_clicked)

        # Get records from the database
        self.incomes_list = get_user_income(self.user_id)

        # If there are no records
        if not self.incomes_list:
            self.table_widget.setRowCount(1)
            self.table_widget.setSpan(0, 0, 1, 4)
            self.table_widget.setItem(0, 0, QTableWidgetItem("No Income Data"))
        else:
            self.fill_table_content()

        outer_frame_layout.addWidget(self.table_widget)

        # Closing button
        closing_button = QPushButton("Close")
        closing_button.setCursor(Qt.CursorShape.PointingHandCursor)
        closing_button.setFixedWidth(150)
        closing_button.setStyleSheet("background-color: #B0C4DE; border: none; border-radius: 5; padding: 5 0" )
        closing_button.setFont(QFont("Futura", 16))
        closing_button.clicked.connect(self.close_income_table)
        outer_frame_layout.addWidget(closing_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Set layout and display it
        self.setLayout(outer_frame_layout)  
        self.show()


    def fill_table_content(self):

        self.table_widget.clearContents()
        self.table_widget.setRowCount(len(self.incomes_list))

        for i, income_record in enumerate(self.incomes_list):
            date = income_record[0]
            amount = income_record[1]

            # Insert extracted data into the table row 
            self.table_widget.setItem(i, 0, QTableWidgetItem(date))
            self.table_widget.setItem(i, 1, QTableWidgetItem(str(amount)))

            # Button to edit the record
            edit_this_income_record = QPushButton("Edit", self)
            edit_this_income_record.setCursor(Qt.CursorShape.PointingHandCursor)
            edit_this_income_record.setCheckable(True)
            edit_this_income_record.setStyleSheet("background-color: #D9BFBF; border: none; border-radius: 5; padding: 5 0" )
            edit_this_income_record.setFont(QFont("Futura", 16))
            edit_this_income_record.clicked.connect(lambda checked, row=i: self.edit_this_income_record(row, checked))

            # Button to remove the record from the database
            remove_this_income_record = QPushButton("Delete", self)
            remove_this_income_record.setCursor(Qt.CursorShape.PointingHandCursor)
            remove_this_income_record.setStyleSheet("background-color: #DBC3A3; border: none; border-radius: 5; padding: 5 0" )
            remove_this_income_record.setFont(QFont("Futura", 16))
            remove_this_income_record.clicked.connect(lambda checked, row=i: self.remove_this_income_record(row))

            self.table_widget.setCellWidget(i, 2, edit_this_income_record)
            self.table_widget.setCellWidget(i, 3, remove_this_income_record)

            # Set all labels as non-editable initially
            for column in range(2):
                label_item = self.table_widget.item(i, column)
                if label_item:
                    # The flags() method returns the current flags of the item, and we use a bitwise AND operation (&) with the complement (NOT) of the Qt.ItemFlag.ItemIsEditable flag to remove the Qt.ItemIsEditable flag from the item's flags.
                    label_item.setFlags(label_item.flags() & ~Qt.ItemFlag.ItemIsEditable)


   # Sort rows in the table according to the clicked column header
    def header_clicked(self, logical_index):
        # Sort by date
        if logical_index == 0:
            self.incomes_list = sorted(self.incomes_list, key=lambda x: x[0], reverse=True)
        # Sort by amount
        if logical_index == 1:
            self.incomes_list = sorted(self.incomes_list, key=lambda x: x[1], reverse=True)
        
        self.fill_table_content()


    # Remove current record from the database
    def remove_this_income_record(self, row):

        # Collect data to find the record in the database
        row_data = [self.table_widget.item(row, column).text() for column in range(2)]
        sql_return_value = remove_income_record(self.user_id, row_data[0], row_data[1])
       
        # In case of successful removal
        if sql_return_value:
            success_msg = QMessageBox.information(self, "Information", "Record removed")

            # Repaint donut chart in the main window
            self.main_window.current_month_donut_chart.refresh_donut_chart()
            self.table_widget.update()


    # Edit record and update it in the database
    def edit_this_income_record(self, row_index, checked):
        if checked:  # When the "Edit" button is checked

            # Collect data to find the recird in the ddatabase 
            self.row_data_before_editing = []
            for column in range(2):
                label_item = self.table_widget.item(row_index, column)
                self.row_data_before_editing.append(label_item.text())
                if label_item:
                    label_item.setBackground(QBrush(QColor("#ADFF2F")))
                    label_item.setForeground(QBrush(QColor("#483D8B")))
                    label_item.setFlags(label_item.flags() | Qt.ItemFlag.ItemIsEditable)

            # Change text of the "Edit" button to "Apply"
            edit_button = self.table_widget.cellWidget(row_index, 2)
            edit_button.setText("Apply")

        else:  # When the "Apply" button is unchecked
            edited_row_data = []
            # Retrieve data from QTableWidgetItem and print the edited data
            for column in range(2):
                label_item = self.table_widget.item(row_index, column)
                if label_item:
                    edited_row_data.append(label_item.text())
                    label_item.setFlags(label_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    label_item.setBackground(QBrush(QColor("#F0FFF0")))
                    label_item.setForeground(QBrush(QColor("#000000")))  # Reset the text color

            # Change text of the "Apply" button to "Edit"
            edit_button = self.table_widget.cellWidget(row_index, 2)
            edit_button.setText("Edit")

            # Update the record in the database
            result, message = edit_income_record(self.user_id, self.row_data_before_editing, edited_row_data)

            if not result:
                cannot_add_msg = QMessageBox.information(self, "Information", message)
            
            else:
            # In case of successful edit
                success_msg = QMessageBox.information(self, "Information", message)

                # Repaint donut chart in the main window
                self.main_window.current_month_donut_chart.refresh_donut_chart()
                self.table_widget.update()


    def close_income_table(self):
        self.hide()