from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton,
                            QFormLayout, QLineEdit, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Import my widgets
from gui_elements.main_window import MainScreen
from gui_elements.register import RegisterWindow

# Import data insertion function
import sys
sys.path.append('../helpers')
from helpers import log_in_check



class LogInWindow(QWidget):
    def __init__(self):
        super().__init__()  
        self.setGeometry(550, 300, 300, 300)
        self.setWindowTitle("Login Form")
        self.setStyleSheet('background-color: #F5FFFA')

        layout = QFormLayout()
        layout.setFormAlignment(Qt.AlignmentFlag.AlignCenter)

        # Label names
        label_username = QLabel("Username:")
        label_password = QLabel("Password:")
        label_username.setFont(QFont('Futura', 16))
        label_password.setFont(QFont('Futura', 16))

        # QLine edits to enter input
        self.username_line_edit = QLineEdit()
        self.password_line_edit = QLineEdit()
        # Make password field in echo mode - display *
        self.password_line_edit.setEchoMode(QLineEdit.EchoMode.Password)  

        # Insert labels and line edits into layout
        layout.addRow(label_username, self.username_line_edit)
        layout.addRow(label_password, self.password_line_edit)

        # Log in button
        log_in_button = QPushButton("Log In")
        log_in_button.setCursor(Qt.CursorShape.PointingHandCursor)
        log_in_button.clicked.connect(lambda: self.log_in_user(self.username_line_edit.text(), self.password_line_edit.text()))
        log_in_button.setStyleSheet('background-color : #D8BFD8; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')
        layout.addRow(log_in_button)

        # Register new user button
        register_button = QPushButton("New User")
        register_button.setCursor(Qt.CursorShape.PointingHandCursor)
        register_button.clicked.connect(self.register_user)
        register_button.setStyleSheet('background-color : #9FC4C6; font-weight: 600; font-size: 14px; border-radius : 5; padding: 5 0')
        layout.addRow(register_button)

        self.setLayout(layout)


    def log_in_user(self, username, password):

        result, message, user_id = log_in_check(username, password)

        if not result:
            no_login_possible_msg = QMessageBox.information(self, "Information", message)
            
        else:
            # Create main window object 
            main_window = MainScreen(user_id)
            main_window.show()
            self.close()
            
    

    def register_user(self):
        # TRANSFER USER TO A REGISTER WINDOW
        self.register_window = RegisterWindow(self)
        self.register_window.show()
        self.hide()