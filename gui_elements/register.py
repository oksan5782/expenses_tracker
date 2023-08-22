from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QFormLayout, 
                             QMessageBox, QLineEdit)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Import data insertion function
import sys
sys.path.append('../helpers')
from helpers import register_user

class RegisterWindow(QWidget):
    def __init__(self, Login_Window):
        super().__init__()  
        self.setWindowTitle("Sign Up")
        self.setGeometry(550, 300, 300, 300)
        self.setWindowTitle("Registration Form")
        self.setStyleSheet('background-color: #F5FFFA')
        self.login_window = Login_Window

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

        # Set the hidden mode for passwords
        self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Password) 
        self.confirm_password_line_edit.setEchoMode(QLineEdit.EchoMode.Password) 

        # Insert labels and line edits into layout
        layout.addRow(label_username, self.username_line_edit)
        layout.addRow(label_password, self.password_line_edit)
        layout.addRow(label_confirm_password, self.confirm_password_line_edit)

        # Register button
        log_in_button = QPushButton("Register")
        log_in_button.clicked.connect(lambda : self.try_register_user(self.username_line_edit.text(), self.password_line_edit.text(), self.confirm_password_line_edit.text()))
        log_in_button.setStyleSheet('background-color : #66CDAA; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')
        layout.addRow(log_in_button)

        # Back to log in button
        back_to_login_button = QPushButton("Back to Log In")
        back_to_login_button.clicked.connect(self.back_to_login)
        back_to_login_button.setStyleSheet('background-color : #9FC4C6; font-weight: 600; font-size: 14px; border-radius : 5; padding: 5 0')
        layout.addRow(back_to_login_button)


        self.setLayout(layout)

    def try_register_user(self, username, password, password_confirmation):

        # Try to register user and flush message boxes with error codes
        result, message = register_user(username, password, password_confirmation)
        
        # If registration was not succesful
        if not result:
            no_register_possible = QMessageBox.information(self, "Information", message)
            
        else:
            # Flush confirmation message 
            registration_success_msg = QMessageBox.information(self, "Information", message)
            
            # OPEN MAIN WINDOW
            self.back_to_login()
            

    def back_to_login(self):
        self.close()
        self.login_window.show()