
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, 
                            QTableWidgetItem, QPushButton, QWidget, 
                            QVBoxLayout, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QBrush, QColor


# Import data insertion function
import sys
sys.path.append('../helpers')
from helpers import get_expenses_by_category, edit_record


class DisplayCategoryList(QMainWindow):
    def __init__(self, user_id, name):
        super().__init__()
        self.category_title = name
        self.user_id = user_id
        self.setWindowTitle(f"Category {self.category_title}")
        self.setStyleSheet('background-color: #F5FFFA')
        self.create_table()
        self.row_data_before_editing = []


    def create_table(self):
        outer_frame = QWidget()
        outer_frame_layout = QVBoxLayout()

        self.setWindowTitle(f"{self.category_title} Expenses")
        self.setGeometry(450, 250, 600, 400)

        self.table_widget = QTableWidget(self)

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
            color: #2F4F4F;
        }"""

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget.setStyleSheet(stylesheet)
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(["Name", "Date", "Amount", "Edit"])
        self.table_widget.verticalHeader().setDefaultSectionSize(50)

        # GETTING DATA FROM THE DATABASE
        current_category_expenses_list = get_expenses_by_category(self.user_id, self.category_title)
        
        # Check for null
        if not current_category_expenses_list:
            self.table_widget.setRowCount(1)
            self.table_widget.setSpan(0, 0, 1, 4)
            self.table_widget.setItem(0, 0, QTableWidgetItem("No Data For This Category"))
        else:
            for i, expense_record in enumerate(current_category_expenses_list):
                name = expense_record[0]
                date = expense_record[1]
                amount = expense_record[2]

                # Insert extracted data into a row
                self.table_widget.insertRow(i)
                self.table_widget.setItem(i, 0, QTableWidgetItem(name))
                self.table_widget.setItem(i, 1, QTableWidgetItem(date))
                self.table_widget.setItem(i, 2, QTableWidgetItem(str(amount)))

                # Edit button
                edit_this_expense_button = QPushButton("Edit", self)
                edit_this_expense_button.setCheckable(True)
                edit_this_expense_button.setStyleSheet("background-color: #B3B3FF; border: none; border-radius: 5; padding: 5 0" )
                edit_this_expense_button.setFont(QFont("Futura", 16))
                edit_this_expense_button.clicked.connect(lambda checked, row=i: self.edit_this_expense_record(row, checked))
                self.table_widget.setCellWidget(i, 3, edit_this_expense_button)

                # Set all labels as non-editable initially
                for column in range(3):
                    label_item = self.table_widget.item(i, column)
                    if label_item:
                        # The flags() method returns the current flags of the item, and we use a bitwise AND operation (&) with the complement (NOT) of the Qt.ItemFlag.ItemIsEditable flag to remove the Qt.ItemIsEditable flag from the item's flags.
                        label_item.setFlags(label_item.flags() & ~Qt.ItemFlag.ItemIsEditable)


        outer_frame_layout.addWidget(self.table_widget)

        # Closing button
        closing_button = QPushButton("Close")
        closing_button.setFixedWidth(150)
        closing_button.setStyleSheet("background-color: #B0C4DE; border: none; border-radius: 5; padding: 5 0" )
        closing_button.setFont(QFont("Futura", 16))
        closing_button.clicked.connect(self.close_category_table)
        outer_frame_layout.addWidget(closing_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Set layout and display it
        outer_frame.setLayout(outer_frame_layout)  
        self.setCentralWidget(outer_frame)
        self.show()
    
    def close_category_table(self):
        self.hide()
    
    # Edit this record functionality
    def edit_this_expense_record(self, row_index, checked):
        if checked:  # When the "Edit" button is checked

            # Collect data to find the row in DB
            self.row_data_before_editing = []
            for column in range(3):
                label_item = self.table_widget.item(row_index, column)
                self.row_data_before_editing.append(label_item.text())
                if label_item:
                    label_item.setBackground(QBrush(QColor("#ADFF2F")))
                    label_item.setForeground(QBrush(QColor("#483D8B")))
                    label_item.setFlags(label_item.flags() | Qt.ItemFlag.ItemIsEditable)

            # Change text of the "Edit" button to "Apply"
            edit_button = self.table_widget.cellWidget(row_index, 3)
            edit_button.setText("Apply")

        else:  # When the "Apply" button is unchecked
            edited_row_data = []
            # Retrieve data from QTableWidgetItem and insert the edited data
            for column in range(3):
                label_item = self.table_widget.item(row_index, column)
                if label_item:
                    edited_row_data.append(label_item.text())
                    label_item.setFlags(label_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    label_item.setBackground(QBrush(QColor("#F0FFF0")))
                    label_item.setForeground(QBrush(QColor("#000000")))  # Reset the text color

            # Change text of the "Apply" button to "Edit"
            edit_button = self.table_widget.cellWidget(row_index, 3)
            edit_button.setText("Edit")

            
            # Add category to two list for updating in DB to match pattern
            # (user_id, name, category, date, amount)
            self.row_data_before_editing.insert(1, self.category_title)
            edited_row_data.insert(1, self.category_title)
            
            # Update record in DB 
            sql_return_value = edit_record(self.user_id, self.row_data_before_editing, edited_row_data)

             # Error message for invalid date
            if sql_return_value == 1:
                invalid_date_msg = QMessageBox.warning(self, "Information", "Invalid Date Format. Please use YYYY-MM-DD")

            # Error message for invalid name input
            if sql_return_value == 2:
                invalid_name_msg = QMessageBox.warning(self, "Information", "Missing name")

            # Error message for invalid amount input 
            if sql_return_value == 3:
                invalid_amount_msg = QMessageBox.warning(self, "Information", "Invalid amount")
            
            # Error message for invalid category
            if sql_return_value == 4:
                invalid_category_msg = QMessageBox.warning(self, "Information", "Invalid category. Try capitalizing the name or use Other")


            # IF VALIDATION PASSED Flush the message 
            if sql_return_value == 0:
                success_msg = QMessageBox.information(self, "Information", "Expense updated")

                # Update table value
                self.table_widget.update()



