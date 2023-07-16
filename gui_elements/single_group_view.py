from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, 
                            QTableWidgetItem, QPushButton, QWidget, 
                            QVBoxLayout, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Import data insertion function
import sys
sys.path.append('../helpers')
from helpers import get_group_expenses, remove_record


class DisplayGroupList(QMainWindow):
    def __init__(self, user_id, name):
        super().__init__()
        self.group_name = name
        self.user_id = user_id
        self.setWindowTitle(f"Category {self.group_name}")
        self.setStyleSheet('background-color: #F5FFFA')
        self.create_table()


    def create_table(self):
        outer_frame = QWidget()
        outer_frame_layout = QVBoxLayout()

        self.setWindowTitle(f"{self.group_name} Expenses")
        self.setGeometry(450, 250, 700, 400)

        table_widget = QTableWidget(self)

        stylesheet = """
        QTableWidget {

            border-radius: 5px;
            font-family: Futura;
        }

            QTableWidget QHeaderView::section {
            color: #05132E;
            border: none;
            font-weight: 600;
            font-size: 16px;

        }

            QTableWidget::item {
            padding: 5px;
            background-color: #FCF5E8;

        }"""
        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table_widget.setStyleSheet(stylesheet)
        table_widget.setColumnCount(5)
        table_widget.setHorizontalHeaderLabels(["Name", "Category", "Date", "Amount", "Remove Record"])
        table_widget.verticalHeader().setDefaultSectionSize(50)
        table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # GETTING DATA FROM THE DATABASE
        group_expenses_list = get_group_expenses(self.user_id, self.group_name)

        for i in range(len(group_expenses_list)):
            name = group_expenses_list[i][0]
            category = group_expenses_list[i][1]
            date = group_expenses_list[i][2]
            amount = group_expenses_list[i][3]
            remove_this_group_record = QPushButton("Remove")
            remove_this_group_record.setStyleSheet("background-color: #DBC3A3; border: none; border-radius: 5; padding: 5 0" )
            remove_this_group_record.setFont(QFont("Futura", 16))
            remove_this_group_record.clicked.connect(lambda x, i=i : self.remove_this_expense_record(group_expenses_list[i]))

            table_widget.insertRow(i)
            table_widget.setItem(i, 0, QTableWidgetItem(name))
            table_widget.setItem(i, 1, QTableWidgetItem(category))
            table_widget.setItem(i, 2, QTableWidgetItem(date))
            table_widget.setItem(i, 3, QTableWidgetItem(str(amount)))
            table_widget.setCellWidget(i, 4, remove_this_group_record)

        outer_frame_layout.addWidget(table_widget)

        # Closing button
        closing_button = QPushButton("Close")
        closing_button.setFixedWidth(150)
        closing_button.setStyleSheet("background-color: #B0C4DE; border: none; border-radius: 5; padding: 5 0" )
        closing_button.setFont(QFont("Futura", 16))
        closing_button.clicked.connect(self.close_group_view)
        outer_frame_layout.addWidget(closing_button, alignment=Qt.AlignmentFlag.AlignCenter)
        outer_frame.setLayout(outer_frame_layout)
        
        self.setCentralWidget(outer_frame)
        self.show()
    
    def close_group_view(self):
        self.hide()
    
    def remove_this_expense_record(self, record_tuple):
        # SHOULD OPEN ADD EXPENSE RECORD WINDOW,
        # REMOVE CURRENT RECORD AND INSERT AN UPDATE AS A NEW RECORD
        print(record_tuple)

