from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QComboBox, 
                             QFormLayout, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Import data insertion function
import sys
sys.path.append('../helpers')
sys.path.append('..\helpers')
from helpers import add_expense_into_db

class AddExpenseWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()  
        self.user_id = user_id
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
        label_date = QLabel("Expense Date:")
        label_date.setFont(QFont('Futura', 16))

        # QLine edit to enter input
        self.date_line_edit = QLineEdit()
        self.date_line_edit.setStyleSheet('margin: 8 0')

        layout.addRow(label_date, self.date_line_edit)

        # Row 3 - Category
        label_category = QLabel("Expense Category:")
        label_category.setFont(QFont('Futura', 16))
        

        # QLine edit to enter input
        self.category = QComboBox()
        # ADD MORE CATEGORIES
        self.category.addItems(["Rent", "Groceries", "Eating Out"])
        # STYLE COMBOBOX
        self.category.setFixedHeight(25)
        self.category.setStyleSheet("QComboBox QAbstractItemView {"
                       "selection-color: #2E8B57"
                       "}")

        layout.addRow(label_category, self.category)

        # Row 3 - Amount
        label_amount = QLabel("Expense Amount:")
        label_amount.setFont(QFont('Futura', 16))

        # QLine edit to enter input
        self.amount_line_edit = QLineEdit()

        layout.addRow(label_amount, self.amount_line_edit)


        # Upload input button
        add_expense_button = QPushButton("Add")
        add_expense_button.clicked.connect(lambda : self.add_expense(self.name_line_edit.text(), self.amount_line_edit.text(), self.date_line_edit.text(), self.category.currentText()))
        add_expense_button.setStyleSheet('background-color : #D8BFD8; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')
        layout.addRow(add_expense_button)
        self.setLayout(layout)


    def add_expense(self, name, amount_line_edit, date, category):
        # VALIDATE USER INPUT 

        # IF VALIDATION PASSED INSERT INCOME VALUE AND TIME TO THE RELEVANT TABLE
        add_expense_into_db(self.user_id, name, date, category, amount_line_edit)
        # IF VALIDATION PASSED Flush the message 

        # GO BACK TO MAIN WINDOW
        self.close()