from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QComboBox, 
                             QFormLayout, QLineEdit, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


# Import data and functions interacting with a database
import sys
sys.path.append('../helpers')
from helpers import add_expense_into_db, ALL_POSSIBLE_CATEGORIES_LIST, ALL_EXPENSE_TYPES


class AddExpenseWindow(QWidget):
    def __init__(self, user_id, main_window):
        super().__init__()  
        self.user_id = user_id
        self.main_window = main_window
        self.setWindowTitle("Add Expense")
        self.setStyleSheet('background-color: #F5FFFA')

        layout = QFormLayout()

        # Row 1 - Get name of the expense from the user
        label_name = QLabel("Expense Name:")
        label_name.setFont(QFont('Futura', 16))
    
        self.name_line_edit = QLineEdit()
        self.name_line_edit.setStyleSheet('margin: 8 0')

        layout.addRow(label_name, self.name_line_edit)

        # Row 2 - Get exoense date from the user
        label_date = QLabel("Expense Date (YYYY-MM-DD)")
        label_date.setFont(QFont('Futura', 16))

        self.date_line_edit = QLineEdit()
        self.date_line_edit.setStyleSheet('margin: 8 0')

        layout.addRow(label_date, self.date_line_edit)

        # Row 3 - Get expense type from the user 
        label_type = QLabel("Expense Type:")
        label_type.setFont(QFont('Futura', 16))

        self.type = QComboBox()

        # Add type options
        self.type.addItems(ALL_EXPENSE_TYPES)

        # Style type selection combo box
        self.type.setFixedHeight(25)
        self.type.setStyleSheet("QComboBox QAbstractItemView {"
                       "selection-color: #2E8B57"
                       "}")
        layout.addRow(label_type, self.type)

        # Row 4 - Get expense category data from the user
        label_category = QLabel("Expense Category:")
        label_category.setFont(QFont('Futura', 16))
        
        self.category = QComboBox()

        # Add categories options
        self.category.addItems(ALL_POSSIBLE_CATEGORIES_LIST)

        # Style combo box
        self.category.setFixedHeight(25)
        self.category.setStyleSheet("QComboBox QAbstractItemView {"
                       "selection-color: #2E8B57"
                       "}")
        layout.addRow(label_category, self.category)

        # Row 5 - Get expense amount data from the user 
        label_amount = QLabel("Expense Amount ($):")
        label_amount.setFont(QFont('Futura', 16))

        self.amount_line_edit = QLineEdit()
        layout.addRow(label_amount, self.amount_line_edit)

        # Upload input button
        add_expense_button = QPushButton("Add")
        add_expense_button.setCursor(Qt.CursorShape.PointingHandCursor)
        add_expense_button.clicked.connect(lambda : self.add_expense(self.name_line_edit.text(), self.amount_line_edit.text(), self.date_line_edit.text(), self.category.currentText(), self.type.currentText()))
        add_expense_button.setStyleSheet('background-color : #D8BFD8; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')
        layout.addRow(add_expense_button)
        self.setLayout(layout)

    # Add expense to the database and update the widgets accordingly
    def add_expense(self, name, amount_line_edit, date, category, type):

        # Try inserting the record into database
        result, message = add_expense_into_db(self.user_id, type, name, date, category, amount_line_edit)

        # Display a fail reason message in case of a failure
        if not result:
            cannot_add_msg = QMessageBox.information(self, "Information", message)
            
        else:
            # If validation was  sucessful - flush the message 
            success_msg = QMessageBox.information(self, "Information", message)
            
            # Repaint graph, categories view and balance windows
            self.main_window.stacked_bar_chart.refresh_bar_chart()
            self.main_window.update_categories_area()
            self.main_window.current_month_donut_chart.refresh_donut_chart()

            # Go back to the main window
            self.close()

