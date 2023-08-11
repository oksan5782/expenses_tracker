from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QFormLayout, 
                            QMessageBox, QLineEdit)
from PyQt6.QtGui import QFont


# Import data insertion function
import sys
sys.path.append('../helpers')
from helpers import add_income_into_db


class AddIncomeWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()  
        self.user_id = user_id
        self.setWindowTitle("Add Income")
        self.setStyleSheet('background-color: #F5FFFA')

        layout = QFormLayout()

        # ROW 1 - date
        label_date = QLabel("Income Date (YYYY-MM-DD):")
        label_date.setFont(QFont('Futura', 16))

        # QLine edit to enter input
        self.label_date_line_edit = QLineEdit()
        self.label_date_line_edit.setStyleSheet('margin: 8 0')

        layout.addRow(label_date, self.label_date_line_edit)

        # Row 2 - Amount
        label_amount = QLabel("Income Amount ($):")
        label_amount.setFont(QFont('Futura', 16))

        # QLine edit to enter input
        self.amount_line_edit = QLineEdit()
        self.amount_line_edit.setStyleSheet('margin: 8 0')

        layout.addRow(label_amount, self.amount_line_edit)


        # Upload input button
        add_income_button = QPushButton("Add")
        add_income_button.clicked.connect(lambda : self.add_income(self.amount_line_edit.text(), self.label_date_line_edit.text()))
        add_income_button.setStyleSheet('background-color : #8CD9AF; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')
        layout.addRow(add_income_button)
        self.setLayout(layout)


    def add_income(self, amount_line_edit, date):
        print("Input value is " + str(amount_line_edit) + " " + str(date))
        # VALIDATE USER INPUT 

        # IF VALIDATION PASSED INSERT INCOME VALUE AND TIME TO THE RELEVANT TABLE
        sql_return_value = add_income_into_db(self.user_id, date, amount_line_edit)

        # Error message for invalid date
        if sql_return_value == 1:
            invalid_date_msg = QMessageBox.warning(self, "Information", "Invalid Date Format. Please use YYYY-MM-DD")

        # Error message for invalid amount input 
        if sql_return_value == 3:
            invalid_date_msg = QMessageBox.warning(self, "Information", "Invalid amount")

        # IF VALIDATION PASSED Flush change message
        if sql_return_value == 0:
            success_msg = QMessageBox.information(self, "Information", "Income value added")
            
            # GO BACK TO MAIN WINDOW
            self.close()
        