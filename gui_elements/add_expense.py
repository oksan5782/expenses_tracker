from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QComboBox, 
                             QFormLayout, QLineEdit, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Import data insertion function
import sys
sys.path.append('../helpers')
from helpers import add_expense_into_db

class AddExpenseWindow(QWidget):
    def __init__(self, user_id, categories_list, types_list):
        super().__init__()  
        self.user_id = user_id
        self.types_list = types_list
        self.categories_list = categories_list
        self.setWindowTitle("Add Expense")
        self.setStyleSheet('background-color: #F5FFFA')

        layout = QFormLayout()

        # Row 1 - Name of the expense
        label_name = QLabel("Expense Name:")
        label_name.setFont(QFont('Futura', 16))
    
        # QLine edit to fill out name of the expense
        self.name_line_edit = QLineEdit()
        self.name_line_edit.setStyleSheet('margin: 8 0')

        layout.addRow(label_name, self.name_line_edit)

        # Row 2 - Date 
        label_date = QLabel("Expense Date. Format YYYY-MM-DD")
        label_date.setFont(QFont('Futura', 16))

        # QLine edit to enter input
        self.date_line_edit = QLineEdit()
        self.date_line_edit.setStyleSheet('margin: 8 0')

        layout.addRow(label_date, self.date_line_edit)

        # Row 3 - Type 
        label_type = QLabel("Expense Type:")
        label_type.setFont(QFont('Futura', 16))

        # Selection box to enter input
        self.type = QComboBox()
        # ADD MORE CATEGORIES
        self.type.addItems(self.types_list)
        # STYLE COMBOBOX
        self.type.setFixedHeight(25)
        self.type.setStyleSheet("QComboBox QAbstractItemView {"
                       "selection-color: #2E8B57"
                       "}")
        layout.addRow(label_type, self.type)


        # Row 4 - Category
        label_category = QLabel("Expense Category:")
        label_category.setFont(QFont('Futura', 16))
        
        # Selection box to enter input
        self.category = QComboBox()
        # ADD MORE CATEGORIES
        self.category.addItems(self.categories_list)
        # STYLE COMBOBOX
        self.category.setFixedHeight(25)
        self.category.setStyleSheet("QComboBox QAbstractItemView {"
                       "selection-color: #2E8B57"
                       "}")
        layout.addRow(label_category, self.category)

        # Row 5 - Amount
        label_amount = QLabel("Expense Amount:")
        label_amount.setFont(QFont('Futura', 16))

        # QLine edit to enter input
        self.amount_line_edit = QLineEdit()

        layout.addRow(label_amount, self.amount_line_edit)


        # Upload input button
        add_expense_button = QPushButton("Add")
        add_expense_button.clicked.connect(lambda : self.add_expense(self.name_line_edit.text(), self.amount_line_edit.text(), self.date_line_edit.text(), self.category.currentText(), self.type.currentText()))
        add_expense_button.setStyleSheet('background-color : #D8BFD8; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')
        layout.addRow(add_expense_button)
        self.setLayout(layout)


    def add_expense(self, name, amount_line_edit, date, category, type):
        # VALIDATE USER INPUT 

        # IF VALIDATION PASSED INSERT INCOME VALUE AND TIME TO THE RELEVANT TABLE
        sql_return_value = add_expense_into_db(self.user_id, type, name, date, category, amount_line_edit)

        # Error message for invalid date
        if sql_return_value == 1:
            invalid_date_msg = QMessageBox.warning(self, "Information", "Invalid Date Format. Please use YYYY-MM-DD")

        # Error message for invalid name input
        if sql_return_value == 2:
            invalid_date_msg = QMessageBox.warning(self, "Information", "Missing name")

        # Error message for invalid amount input 
        if sql_return_value == 3:
            invalid_date_msg = QMessageBox.warning(self, "Information", "Invalid amount")


        # IF VALIDATION PASSED Flush the message 
        elif sql_return_value == 0:
            success_msg = QMessageBox.information(self, "Information", "Expense added")
            
            # GO BACK TO MAIN WINDOW
            self.close()

