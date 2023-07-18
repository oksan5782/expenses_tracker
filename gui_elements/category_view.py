
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, 
                            QTableWidgetItem, QPushButton, QWidget, 
                            QVBoxLayout, QHeaderView)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


# Import data insertion function
import sys
sys.path.append('../helpers')
from helpers import get_expenses_by_category, remove_record


class DisplayCategoryList(QMainWindow):
    def __init__(self, user_id, name, new_expense_window):
        super().__init__()
        self.category_title = name
        self.user_id = user_id
        self.new_expense_window = new_expense_window(self.user_id)
        self.setWindowTitle(f"Category {self.category_title}")
        self.setStyleSheet('background-color: #F5FFFA')
        self.create_table()


    def create_table(self):
        outer_frame = QWidget()
        outer_frame_layout = QVBoxLayout()

        self.setWindowTitle(f"{self.category_title} Expenses")
        self.setGeometry(450, 250, 600, 400)

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
            background-color: #E8EFFC;

        }"""
        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table_widget.setStyleSheet(stylesheet)
        table_widget.setColumnCount(4)
        table_widget.setHorizontalHeaderLabels(["Name", "Date", "Amount", "Edit"])
        table_widget.verticalHeader().setDefaultSectionSize(50)
        table_widget.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        # GETTING DATA FROM THE DATABASE
        current_category_expenses_list = get_expenses_by_category(self.user_id, self.category_title)
        for i in range(len(current_category_expenses_list)):
            name = current_category_expenses_list[i][0]
            date = current_category_expenses_list[i][1]
            amount = current_category_expenses_list[i][2]
            edit_this_expense_button = QPushButton("Edit")
            edit_this_expense_button.setStyleSheet("background-color: #B3B3FF; border: none; border-radius: 5; padding: 5 0" )
            edit_this_expense_button.setFont(QFont("Futura", 16))
            edit_this_expense_button.clicked.connect(lambda x, i=i : self.edit_this_expense_record(self.user_id, current_category_expenses_list[i]))

            table_widget.insertRow(i)
            table_widget.setItem(i, 0, QTableWidgetItem(name))
            table_widget.setItem(i, 1, QTableWidgetItem(date))
            table_widget.setItem(i, 2, QTableWidgetItem(str(amount)))
            table_widget.setCellWidget(i, 3, edit_this_expense_button)

        outer_frame_layout.addWidget(table_widget)

        # Closing button
        closing_button = QPushButton("Close")
        closing_button.setFixedWidth(150)
        closing_button.setStyleSheet("background-color: #B0C4DE; border: none; border-radius: 5; padding: 5 0" )
        closing_button.setFont(QFont("Futura", 16))
        closing_button.clicked.connect(self.close_category_table)
        outer_frame_layout.addWidget(closing_button, alignment=Qt.AlignmentFlag.AlignCenter)
        outer_frame.setLayout(outer_frame_layout)
        
        self.setCentralWidget(outer_frame)

        self.show()
    
    def close_category_table(self):
        self.hide()
    
    # remove current record and display add new record window
    def edit_this_expense_record(self, user_id, record_tuple):
        
        # REMOVE CURRENT RECORD - user_id, category, name, date, amount
        remove_record(self.user_id, self.category_title, record_tuple[0], record_tuple[1], record_tuple[2])

        # SHOULD OPEN ADD EXPENSE RECORD WINDOW,
        self.new_expense_window.show()

        # Close category view window
        self.close()



