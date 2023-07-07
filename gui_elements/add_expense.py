from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QComboBox, 
                             QFormLayout, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import datetime

class AddExpenseWindow(QWidget):
    def __init__(self):
        super().__init__()  
        self.setWindowTitle("Add Expense")
        self.setStyleSheet('background-color: #F5FFFA')

        layout = QFormLayout()

        label_date = QLabel("Expense Date:")
        label_date.setFont(QFont('Futura', 16))

        # QLine edit to enter input
        self.date_line_edit = QLineEdit()
        self.date_line_edit.setStyleSheet('margin: 8 0')

        layout.addRow(label_date, self.date_line_edit)

        # Row 2 - Category
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
        # self.amount_line_edit.setStyleSheet('margin: 8 0')

        layout.addRow(label_amount, self.amount_line_edit)


        # Upload input button
        add_income_button = QPushButton("Add")
        add_income_button.clicked.connect(lambda : self.add_income(self.amount_line_edit.text(), self.date_line_edit.text(), self.category.currentText()))
        add_income_button.setStyleSheet('background-color : #D8BFD8; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')
        layout.addRow(add_income_button)
        self.setLayout(layout)


    def add_income(self, amount_line_edit, date, category):
        print("Input value is " + str(amount_line_edit) + " " + str(date) + " " + category)
        # VALIDATE USER INPUT 

        # INSERT INCOME VALUE AND TIME TO THE RELEVANT TABLE

        # GO BACK TO MAIN WINDOW