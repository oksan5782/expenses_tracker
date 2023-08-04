from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, 
                            QTableWidgetItem, QPushButton, QWidget, 
                            QVBoxLayout, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QBrush, QColor

# Import data insertion function
import sys
sys.path.append('../helpers')
from helpers import get_group_expenses, remove_record_from_the_group, edit_record


class DisplayGroupList(QMainWindow):
    def __init__(self, user_id, name):
        super().__init__()
        self.group_name = name
        self.user_id = user_id
        self.setWindowTitle(f"Category {self.group_name}")
        self.setStyleSheet('background-color: #F5FFFA')
        self.create_table()
        self.row_data_before_editing = []



    def create_table(self):
        outer_frame = QWidget()
        outer_frame_layout = QVBoxLayout()

        self.setWindowTitle(f"{self.group_name} Expenses")
        self.setGeometry(450, 250, 750, 500)

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
            background-color: #FCF5E8;
            color: #2F4F4F;

        }"""
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table_widget.setStyleSheet(stylesheet)
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(["Name", "Category", "Date", "Amount", "Edit", "Exclude"])
        self.table_widget.verticalHeader().setDefaultSectionSize(50)

        # GETTING DATA FROM THE DATABASE
        group_expenses_list = get_group_expenses(self.user_id, self.group_name)

         # Check for null
        if not group_expenses_list:
            self.table_widget.setRowCount(1)
            self.table_widget.setSpan(0, 0, 1, 6)
            self.table_widget.setItem(0, 0, QTableWidgetItem("No Data For This Group"))
        else:
            for i, expense_record in enumerate(group_expenses_list):
                name = expense_record[0]
                category = expense_record[1]
                date = expense_record[2]
                amount = expense_record[3]

                # Insert extracted data into a row 
                self.table_widget.insertRow(i)
                self.table_widget.setItem(i, 0, QTableWidgetItem(name))
                self.table_widget.setItem(i, 1, QTableWidgetItem(category))
                self.table_widget.setItem(i, 2, QTableWidgetItem(date))
                self.table_widget.setItem(i, 3, QTableWidgetItem(str(amount)))

                # Button to edit the record
                edit_this_group_record = QPushButton("Edit", self)
                edit_this_group_record.setCheckable(True)
                edit_this_group_record.setStyleSheet("background-color: #D9BFBF; border: none; border-radius: 5; padding: 5 0" )
                edit_this_group_record.setFont(QFont("Futura", 16))
                edit_this_group_record.clicked.connect(lambda checked, row=i: self.edit_this_expense_record(row, checked))


                # Button to remove record from the group
                remove_this_group_record = QPushButton("Remove", self)
                remove_this_group_record.setStyleSheet("background-color: #DBC3A3; border: none; border-radius: 5; padding: 5 0" )
                remove_this_group_record.setFont(QFont("Futura", 16))
                remove_this_group_record.clicked.connect(lambda checked, row=i: self.remove_this_expense_record(row))


                self.table_widget.setCellWidget(i, 4, edit_this_group_record)
                self.table_widget.setCellWidget(i, 5, remove_this_group_record)


                # Set all labels as non-editable initially
                for column in range(4):
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
        closing_button.clicked.connect(self.close_group_view)
        outer_frame_layout.addWidget(closing_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Set layout and display it
        outer_frame.setLayout(outer_frame_layout)
        self.setCentralWidget(outer_frame)
        self.show()
    
    # Usage of the button to close the window
    def close_group_view(self):
        self.hide()
    
    # Remove current record from the group only
    def remove_this_expense_record(self, row):
        # Collect data to find it in DB
        row_data = [self.table_widget.item(row, column).text() for column in range(4)]
        sql_return_value = remove_record_from_the_group(self.user_id, row_data[0], row_data[1], row_data[2], row_data[3])
       
        # Flush message about what was removed
        if sql_return_value == 0:
            success_msg = QMessageBox.information(self, "Information", "Records removed from the gro")

            # Update Group view
            self.table_widget.update()


    # Edit record and update it in DB
    def edit_this_expense_record(self, row_index, checked):
        if checked:  # When the "Edit" button is checked

            # Collect data to find the row in DB
            self.row_data_before_editing = []
            for column in range(4):
                label_item = self.table_widget.item(row_index, column)
                self.row_data_before_editing.append(label_item.text())
                if label_item:
                    label_item.setBackground(QBrush(QColor("#ADFF2F")))
                    label_item.setForeground(QBrush(QColor("#483D8B")))
                    label_item.setFlags(label_item.flags() | Qt.ItemFlag.ItemIsEditable)

            # Change text of the "Edit" button to "Apply"
            edit_button = self.table_widget.cellWidget(row_index, 4)
            edit_button.setText("Apply")

        else:  # When the "Apply" button is unchecked
            edited_row_data = []
            # Retrieve data from QTableWidgetItem and print the edited data
            for column in range(4):
                label_item = self.table_widget.item(row_index, column)
                if label_item:
                    edited_row_data.append(label_item.text())
                    label_item.setFlags(label_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    label_item.setBackground(QBrush(QColor("#F0FFF0")))
                    label_item.setForeground(QBrush(QColor("#000000")))  # Reset the text color

            # Change text of the "Apply" button to "Edit"
            edit_button = self.table_widget.cellWidget(row_index, 4)
            edit_button.setText("Edit")

            # Update record in DB 
            sql_return_value = edit_record(self.user_id, self.row_data_before_editing, edited_row_data)

             # Error message for invalid date
            if sql_return_value == 1:
                invalid_date_msg = QMessageBox.warning(self, "Information", "Invalid Date Format. Please use YYYY-MM-DD")

            # Error message for invalid name input
            if sql_return_value == 2:
                invalid_date_msg = QMessageBox.warning(self, "Information", "Missing name")

            # Error message for invalid amount input 
            if sql_return_value == 3:
                invalid_date_msg = QMessageBox.warning(self, "Information", "Invalid amount")


            # IF VALIDATION PASSED Flush the message 
            if sql_return_value == 0:
                success_msg = QMessageBox.information(self, "Information", "Record updated")

                # Update table value
                self.table_widget.update()


            
            # Update table after removal of the item
            self.table_widget.update()



