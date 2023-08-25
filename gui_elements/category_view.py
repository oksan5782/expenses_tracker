
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
    def __init__(self, user_id, name, main_window):
        super().__init__()
        self.category_title = name
        self.user_id = user_id
        self.main_window = main_window
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
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["Name", "Date", "Type", "Amount ($)", "Edit"])
        self.table_widget.verticalHeader().setDefaultSectionSize(50)

        header = self.table_widget.horizontalHeader()
        header.setSectionsClickable(True)
        header.sectionClicked.connect(self.header_clicked)

        # GETTING DATA FROM THE DATABASE
        self.current_category_expenses_list = get_expenses_by_category(self.user_id, self.category_title)
        
        # Check for null
        if not self.current_category_expenses_list:
            self.table_widget.setRowCount(1)
            self.table_widget.setSpan(0, 0, 1, 5)
            self.table_widget.setItem(0, 0, QTableWidgetItem("No Data For This Category"))
        else:
            self.fill_table_content()

        outer_frame_layout.addWidget(self.table_widget)

        # Closing button
        closing_button = QPushButton("Close")
        closing_button.setCursor(Qt.CursorShape.PointingHandCursor)
        closing_button.setFixedWidth(150)
        closing_button.setStyleSheet("background-color: #B0C4DE; border: none; border-radius: 5; padding: 5 0" )
        closing_button.setFont(QFont("Futura", 16))
        closing_button.clicked.connect(self.close_category_table)
        outer_frame_layout.addWidget(closing_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # Set layout and display it
        outer_frame.setLayout(outer_frame_layout)  
        self.setCentralWidget(outer_frame)
        self.show()
    

    def header_clicked(self, logical_index):
        # Sort by Name
        if logical_index == 0:
            self.current_category_expenses_list = sorted(self.current_category_expenses_list, key=lambda x: x[0])
        # Sort by Date
        if logical_index == 1:
            self.current_category_expenses_list = sorted(self.current_category_expenses_list, key=lambda x: x[1], reverse=True)
        # Sort by type
        if logical_index == 2:
            self.current_category_expenses_list = sorted(self.current_category_expenses_list, key=lambda x: x[2])
        # Sort by amount
        if logical_index == 3:
            self.current_category_expenses_list = sorted(self.current_category_expenses_list, key=lambda x: x[3], reverse=True)
        
        self.table_widget.clearContents()
        self.fill_table_content()
    

    def fill_table_content(self):
        self.table_widget.clearContents()
        self.table_widget.setRowCount(len(self.current_category_expenses_list))
    
        for i, expense_record in enumerate(self.current_category_expenses_list):
            name = expense_record[0]
            date = expense_record[1]
            transaction_type = expense_record[2]
            amount = expense_record[3]

            # Insert extracted data into a row
            self.table_widget.setItem(i, 0, QTableWidgetItem(name))
            self.table_widget.setItem(i, 1, QTableWidgetItem(date))
            self.table_widget.setItem(i, 2, QTableWidgetItem(transaction_type))
            self.table_widget.setItem(i, 3, QTableWidgetItem(str(amount)))

            # Edit button
            edit_this_expense_button = QPushButton("Edit", self)
            edit_this_expense_button.setCursor(Qt.CursorShape.PointingHandCursor)
            edit_this_expense_button.setCheckable(True)
            edit_this_expense_button.setStyleSheet("background-color: #B3B3FF; border: none; border-radius: 5; padding: 5 0" )
            edit_this_expense_button.setFont(QFont("Futura", 16))
            edit_this_expense_button.clicked.connect(lambda checked, row=i: self.edit_this_expense_record(row, checked))
            self.table_widget.setCellWidget(i, 4, edit_this_expense_button)

        # Set all labels as non-editable initially
        for column in range(4):
            label_item = self.table_widget.item(i, column)
            if label_item:
                # The flags() method returns the current flags of the item, and we use a bitwise AND operation (&) with the complement (NOT) of the Qt.ItemFlag.ItemIsEditable flag to remove the Qt.ItemIsEditable flag from the item's flags.
                label_item.setFlags(label_item.flags() & ~Qt.ItemFlag.ItemIsEditable)



    def close_category_table(self):
        self.hide()
    
    # Edit this record functionality
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
            # Retrieve data from QTableWidgetItem and insert the edited data
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

            
            # Add category to two list for updating in DB to match pattern
            # (user_id, name, category, date, amount)
            self.row_data_before_editing.insert(1, self.category_title)
            edited_row_data.insert(1, self.category_title)
            
            # Update record in DB 
            result, message = edit_record(self.user_id, self.row_data_before_editing, edited_row_data)

            if not result:
                cannot_edit_msg = QMessageBox.information(self, "Information", message)
            
            # If validaation passed 
            else:
                success_msg = QMessageBox.information(self, "Information", message)

                # Repaint graph, categories view and balance windows
                self.main_window.stacked_bar_chart.refresh_bar_chart()
                self.main_window.update_categories_area()
                self.main_window.current_month_donut_chart.refresh_donut_chart()

                # Update table value
                self.table_widget.update()



