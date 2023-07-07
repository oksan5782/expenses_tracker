from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QFormLayout, QLineEdit)
from PyQt6.QtGui import QFont


class AddIncomeWindow(QWidget):
    def __init__(self):
        super().__init__()  
        self.setWindowTitle("Add Income")
        self.setStyleSheet('background-color: #F5FFFA')

        layout = QFormLayout()

        # ROW 1 - date
        label_date = QLabel("Income Date:")
        label_date.setFont(QFont('Futura', 16))

        # QLine edit to enter input
        self.label_date_line_edit = QLineEdit()
        self.label_date_line_edit.setStyleSheet('margin: 8 0')

        layout.addRow(label_date, self.label_date_line_edit)

        # Row 2 - Amount
        label_amount = QLabel("Income Amount:")
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

        # INSERT INCOME VALUE AND TIME TO THE RELEVANT TABLE

        # GO BACK TO MAIN WINDOW

        