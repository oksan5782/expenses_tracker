from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QFormLayout, 
                            QMessageBox, QLineEdit)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


# Import functions interacting with a database
import sys
sys.path.append('../helpers')
from helpers import add_income_into_db


class AddIncomeWindow(QWidget):
    def __init__(self, user_id, main_window):
        super().__init__()  
        self.user_id = user_id
        self.main_window = main_window
        self.setWindowTitle("Add Income")
        self.setStyleSheet('background-color: #F5FFFA')

        layout = QFormLayout()

        # ROW 1 - Get income date information
        label_date = QLabel("Income Date (YYYY-MM-DD):")
        label_date.setFont(QFont('Futura', 16))

        self.label_date_line_edit = QLineEdit()
        self.label_date_line_edit.setStyleSheet('margin: 8 0')

        layout.addRow(label_date, self.label_date_line_edit)

        # Row 2 - Get income amount information
        label_amount = QLabel("Income Amount ($):")
        label_amount.setFont(QFont('Futura', 16))

        self.amount_line_edit = QLineEdit()
        self.amount_line_edit.setStyleSheet('margin: 8 0')

        layout.addRow(label_amount, self.amount_line_edit)


        # Upload input button
        add_income_button = QPushButton("Add")
        add_income_button.setCursor(Qt.CursorShape.PointingHandCursor)
        add_income_button.clicked.connect(lambda : self.add_income(self.amount_line_edit.text(), self.label_date_line_edit.text()))
        add_income_button.setStyleSheet('background-color : #8CD9AF; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')
        layout.addRow(add_income_button)
        self.setLayout(layout)


    # Add income to the database and update the widgets accordingly
    def add_income(self, amount_line_edit, date):

        # Try inserting the values into the database
        result, message = add_income_into_db(self.user_id, date, amount_line_edit)

        # Display a fail reason message in case of a failure
        if not result:
            cannot_add_income_msg = QMessageBox.information(self, "Information", message)
            
        else:
            success_msg = QMessageBox.information(self, "Information", "Income value added")
            
            # Update balance
            self.main_window.current_month_donut_chart.refresh_donut_chart()
            
            # Go back to the main window
            self.close()
