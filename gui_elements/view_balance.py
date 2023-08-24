from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Import data insertion function
import sys
sys.path.append('../helpers')
from helpers import set_new_limit


class ViewBalanceWindow(QWidget):
    def __init__(self, user_id):
        super().__init__()  
        self.user_id = user_id
        self.setWindowTitle("Change Monthly Budget")
        self.setStyleSheet('background-color: #F5FFFA')

        # Add layout
        layout = QVBoxLayout()

        # Add title label
        label_budget = QLabel("Set New Budget:")
        label_budget.setFont(QFont('Futura', 16))
        layout.addWidget(label_budget)

        # Add Line edit area 
        self.new_budget = QLineEdit()
        self.new_budget.setStyleSheet('margin: 8 0')
        layout.addWidget(self.new_budget)

        # Add change limit button 
        change_limit_button = QPushButton("Set Budget")
        change_limit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        change_limit_button.clicked.connect(lambda: self.set_new_limit_value(self.new_budget.text()))
        change_limit_button.setStyleSheet('background-color : #C3BAF7; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')
        layout.addWidget(change_limit_button)

        # Apply layout
        self.setLayout(layout)

    # Limit validation
    def set_new_limit_value(self, new_budget):
        # VALIDATE INPUT

        # INSERT NEW BUDGET INTO USERS TABLE
        set_new_limit(self.user_id, new_budget)

        # GO BACK TO MAIN WINDOW
        self.close()


    