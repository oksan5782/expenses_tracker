from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QFormLayout, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()  
        self.setWindowTitle("Sign Up")

        self.setGeometry(300, 200, 300, 300)
        self.setWindowTitle("Registration Form")
        self.setStyleSheet('background-color: #F5FFFA')

        layout = QFormLayout()
        layout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)

        # Label names
        label_username = QLabel("Username:")
        label_password = QLabel("Password:")
        label_confirm_password = QLabel("Confirm Password:")
        label_username.setFont(QFont('Futura', 16))
        label_password.setFont(QFont('Futura', 16))
        label_confirm_password.setFont(QFont('Futura', 16))

        # QLine edits to enter input
        self.username_line_edit = QLineEdit()
        self.password_line_edit = QLineEdit()
        self.confirm_password_line_edit = QLineEdit()

        # Insert labels and line edits into layout
        layout.addRow(label_username, self.username_line_edit)
        layout.addRow(label_password, self.password_line_edit)
        layout.addRow(label_confirm_password, self.confirm_password_line_edit)

        # Register button
        log_in_button = QPushButton("Register")
        log_in_button.clicked.connect(lambda : self.register_user(self.username_line_edit.text(), self.password_line_edit.text(), self.confirm_password_line_edit.text()))
        log_in_button.setStyleSheet('background-color : #66CDAA; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')

        layout.addRow(log_in_button)

        self.setLayout(layout)

    def register_user(self, username, password, password_confirmation):
        print("Register " + username + " " + str(password) + " " + str(password_confirmation))
        # VALIDATE INPUT FIELDS (check for existing username)

        # INSERT USER INTO USERS TABLE

        # OPEN MAIN WINDOW