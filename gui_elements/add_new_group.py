from PyQt6.QtWidgets import (QWidget, QMainWindow, QLabel, QPushButton, QComboBox, 
                             QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QCalendarWidget, QMessageBox,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QDialog, QCheckBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QTextCharFormat, QColor

import datetime


# Import data insertion function
import sys
sys.path.append('../helpers')
from helpers import get_expenses_by_category, get_expenses_by_date_range, create_group 

class AddGroupWindow(QMainWindow):
    updated = pyqtSignal()
    def __init__(self, user_id, all_categories_list):  
        super().__init__() 
        self.user_id = user_id
        self.new_group_data = []
        self.categories_list = all_categories_list
        self.setWindowTitle("Create New Group")
        self.setStyleSheet('background-color: #F5FFFA')
        self.setGeometry(500, 200, 350, 300)
        self.group_selection_data = []
        self.group_name = ""
        self.create_widget()


    def create_widget(self):
        self.initial_creation = QWidget()

        initial_creation_layout = QFormLayout()
        initial_creation_layout.setSpacing(15)

        # Row 1 - create a title
        label_group_name = QLabel("Group Name:")
        label_group_name.setFont(QFont('Futura', 16))
    
        # QLine edit to fill out name of the expense
        self.name_group_line_edit = QLineEdit()
        self.name_group_line_edit.setStyleSheet('margin: 8 0')

        initial_creation_layout.addRow(label_group_name, self.name_group_line_edit)
        
        # Row 2 - label to explain selection
        selection_options = QLabel("Choose selection option")
        selection_options.setFont(QFont('Futura', 16))
        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(selection_options, alignment=Qt.AlignmentFlag.AlignCenter)

        initial_creation_layout.addRow(hbox_layout)

        # Row 3 - buttons to choose by date or by category
        create_by_calendar_button = QPushButton("By Calendar")
        create_by_calendar_button.setFixedWidth(155)
        create_by_calendar_button.clicked.connect(self.select_group_by_calendar)
        create_by_calendar_button.setStyleSheet('background-color : #A8DCF0; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')

        create_by_category_button = QPushButton("By Category")
        create_by_category_button.setFixedWidth(155)
        create_by_category_button.clicked.connect(self.select_group_by_category)
        create_by_category_button.setStyleSheet('background-color : #A8DCF0; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')

        initial_creation_layout.addRow(create_by_calendar_button, create_by_category_button)

        self.initial_creation.setLayout(initial_creation_layout)
        self.setCentralWidget(self.initial_creation)


        # Calendar selection view
        self.calendar_selection = QWidget()
        calender_selection_layout = QVBoxLayout()

        # Label
        calendar_label = QLabel("Select Date Range")
        calendar_label.setFont(QFont('Futura', 16))
        calender_selection_layout.addWidget(calendar_label)

        # Calendar itself
        self.calendar = CustomCalendar()
        calender_selection_layout.addWidget(self.calendar)

        # Button to run search by dates
        search_by_date_button = QPushButton("Search")
        search_by_date_button.clicked.connect(self.generate_group_selection_list_by_date)
        search_by_date_button.setStyleSheet('background-color : #D8BFD8; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')
        calender_selection_layout.addWidget(search_by_date_button)

        self.calendar_selection.setLayout(calender_selection_layout)



        # Category selection view
        self.category_selection = QWidget()
        category_selection_layout = QVBoxLayout()
        category_selection_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        category_selection_layout.setSpacing(70)

        # Label
        category_label = QLabel("Select Category")
        category_label.setFont(QFont('Futura', 16))
        category_selection_layout.addWidget(category_label)

        # QComboBox selection itself
        self.list_expenses_selection = QComboBox()
        self.list_expenses_selection.addItems(self.categories_list)
        # Style Combobox
        self.list_expenses_selection.setFixedHeight(50)
        self.list_expenses_selection.setStyleSheet("QComboBox QAbstractItemView {""selection-color: #2E8B57""}")
        category_selection_layout.addWidget(self.list_expenses_selection)
        
        # Button to run search by category
        search_by_category_button = QPushButton("Search")
        search_by_category_button.clicked.connect(lambda : self.generate_group_selection_list_by_category(self.list_expenses_selection.currentText()))
        search_by_category_button.setStyleSheet('background-color : #D8BFD8; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')
        category_selection_layout.addWidget(search_by_category_button)

        self.category_selection.setLayout(category_selection_layout)
        


        # Table for selection values that belong to the group
        self.selection_table_window = QWidget()
    


    def select_group_by_calendar(self):
        if self.name_group_line_edit.text():
            self.group_name = self.name_group_line_edit.text()
            self.initial_creation.hide()
            self.setCentralWidget(self.calendar_selection)
        else: 
            no_group_name_msg = QMessageBox.information(self, "Information", "Group name is missing")


    def generate_group_selection_list_by_date(self):
        if self.calendar.from_date and self.calendar.to_date:

            # FIX DATA FORMAT to pass to a search function
            from_date = datetime.date(self.calendar.from_date.year(), self.calendar.from_date.month(), self.calendar.from_date.day())
            to_date = datetime.date(self.calendar.to_date.year(), self.calendar.to_date.month(), self.calendar.to_date.day())

            # Select data 
            extracted_data = get_expenses_by_date_range(self.user_id, from_date, to_date)
            self.group_selection_data = extracted_data

            # Hide this window and open a table with checkmarks
            self.calendar_selection.hide()
            self.resize(600, 350)

            table_selection_layout = QVBoxLayout()

            # Insert a table
            self.table = QTableWidget()
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
            self.table.setStyleSheet(stylesheet)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.table.setColumnCount(5)
            self.table.setHorizontalHeaderLabels(["Name", "Category", "Date", "Amount", "Add"])
            self.table.verticalHeader().setDefaultSectionSize(50)

            # Populate table with data
            if self.group_selection_data:
                for i, expense_record in enumerate(self.group_selection_data):
                    name = expense_record[0]
                    category = expense_record[1]
                    date = expense_record[2]
                    amount = expense_record[3]

                    # Insert extracted data into a row 
                    self.table.insertRow(i)
                    self.table.setItem(i, 0, QTableWidgetItem(name))
                    self.table.setItem(i, 1, QTableWidgetItem(category))
                    self.table.setItem(i, 2, QTableWidgetItem(date))
                    self.table.setItem(i, 3, QTableWidgetItem(str(amount)))

                    # Checkbox to include a record into a group
                    checkbox = QCheckBox("Add", self)
                    checkbox.setStyleSheet("background-color: #F9EBD1; border: none; border-radius: 5; padding: 5 0" )
                    self.table.setCellWidget(i, 4, checkbox)

                    # Make cells besides checkbox non-editable
                    for column in range(4):
                        label_item = self.table.item(i, column)
                        if label_item:
                            # The flags() method returns the current flags of the item, and we use a bitwise AND operation (&) with the complement (NOT) of the Qt.ItemFlag.ItemIsEditable flag to remove the Qt.ItemIsEditable flag from the item's flags.
                            label_item.setFlags(label_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            else:
                self.table.setRowCount(1)
                self.table.setSpan(0, 0, 1, 5)
                self.table.setItem(0, 0, QTableWidgetItem("No Data For This Date Range"))

            table_selection_layout.addWidget(self.table)

            # Button to create a group
            create_group_button = QPushButton("Create Group")
            create_group_button.clicked.connect(self.create_group)
            create_group_button.setStyleSheet('background-color : #D8BFD8; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')
            table_selection_layout.addWidget(create_group_button)

            self.selection_table_window.setLayout(table_selection_layout)

            self.setCentralWidget(self.selection_table_window)

        # Show list with a checkbox selected by date
        else:
            no_date_range__selected_msg = QMessageBox.information(self, "Information", "No range selected")




    def select_group_by_category(self):
        # Show categories list with buttons or QComboBox, let user choose
        if self.name_group_line_edit.text():
            self.group_name = self.name_group_line_edit.text()
            self.initial_creation.hide()
            self.setCentralWidget(self.category_selection)
        else:
            no_group_name_msg = QMessageBox.information(self, "Information", "Group name is missing")



    def generate_group_selection_list_by_category(self, category):
        # Select data 
        extracted_data = get_expenses_by_category(self.user_id, category)
        self.group_selection_data = extracted_data

        # Hide this window and open a table with checkmarks
        self.category_selection.hide()
        self.resize(500, 350)
        
        table_selection_layout = QVBoxLayout()

        # Insert a table
        self.table = QTableWidget()
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
        self.table.setStyleSheet(stylesheet)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Name", "Category", "Date", "Amount", "Add"])
        self.table.verticalHeader().setDefaultSectionSize(50)
        
        # Populate table with data
        if self.group_selection_data:
            for i, expense_record in enumerate(self.group_selection_data):
                name = expense_record[0]
                date = expense_record[1]
                amount = expense_record[2]

                # Insert extracted data into a row 
                self.table.insertRow(i)
                self.table.setItem(i, 0, QTableWidgetItem(name))
                self.table.setItem(i, 1, QTableWidgetItem(category))
                self.table.setItem(i, 2, QTableWidgetItem(date))
                self.table.setItem(i, 3, QTableWidgetItem(str(amount)))

                # Checkbox to include a record into a group
                checkbox = QCheckBox("Edit", self)
                checkbox.setStyleSheet("background-color: #F9EBD1; border: none; border-radius: 5; padding: 5 0" )
                self.table.setCellWidget(i, 4, checkbox)
            
                # Make cells besides checkbox non-editable
                for column in range(4):
                    label_item = self.table.item(i, column)
                    if label_item:
                        # The flags() method returns the current flags of the item, and we use a bitwise AND operation (&) with the complement (NOT) of the Qt.ItemFlag.ItemIsEditable flag to remove the Qt.ItemIsEditable flag from the item's flags.
                        label_item.setFlags(label_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        else: 
            self.table.setRowCount(1)
            self.table.setSpan(0, 0, 1, 5)
            self.table.setItem(0, 0, QTableWidgetItem("No Data For This Date Range"))

        table_selection_layout.addWidget(self.table)

        # Button to create a group
        create_group_button = QPushButton("Create Group")
        create_group_button.clicked.connect(self.create_group)
        create_group_button.setStyleSheet('background-color : #D8BFD8; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')
        table_selection_layout.addWidget(create_group_button)

        self.selection_table_window.setLayout(table_selection_layout)

        self.setCentralWidget(self.selection_table_window)
        

    # Creating a group - marking rows with the group_id
    def create_group(self):
        row_count = self.table.rowCount()
        column_count = self.table.columnCount()
        selected_rows_data = []

        for row in range(row_count):
            # I is the column with checkbox
            checkbox = self.table.cellWidget(row, 4)
            if isinstance(checkbox, QCheckBox) and checkbox.isChecked():
                row_data = [self.table.item(row, column).text() for column in range(4)]
                selected_rows_data.append(row_data)

        # Error message for lack of selection
        if not selected_rows_data:
            no_rows_selected_msg = QMessageBox.warning(self, "Information", "Nothing was selected")
        
        else:
            # Get name of the group and create it create group by passing selected_rows_data and group title
            sql_return_value = create_group(self.user_id, self.group_name, selected_rows_data)
            # IF VALIDATION PASSED Flush the message 
            if sql_return_value == 0:
                success_msg = QMessageBox.information(self, "Information", "Group created")
                self.close()


class CustomCalendar(QCalendarWidget):
    def __init__(self):
        super().__init__()
        self.from_date = None
        self.to_date = None

        self.highlighter_format = QTextCharFormat()

        # Get default background and text color
        self.highlighter_format.setBackground(QColor("#4169E1"))
        self.highlighter_format.setForeground(QColor("#F8F8FF"))

        # Connect selection with clicking
        self.clicked.connect(self.select_day_range)

    # Select day range
    def select_day_range(self, date_value):
        self.highlight_range(QTextCharFormat())   

        # Check if modifier is pressed
        if self.from_date == date_value:
            self.from_date = None
            self.to_date = None
        elif self.from_date is None:
            self.from_date = date_value
        else:
            # If from_date is set, set to_date to the clicked date
            self.to_date = date_value
            self.highlight_range(self.highlighter_format)


    # Apply style to selected time frame
    def highlight_range(self, format):
        if self.from_date and self.to_date:
            # Find out which one is smaller
            start = min(self.from_date, self.to_date)
            end = max(self.from_date, self.to_date)

            # Apply format
            while end >= start:
                self.setDateTextFormat(start, format)
                start = start.addDays(1)





