from PyQt6.QtWidgets import (QWidget, QMainWindow, QLabel, QPushButton, QComboBox, 
                             QVBoxLayout, QHBoxLayout, QFormLayout, 
                             QLineEdit, QCalendarWidget, QMessageBox,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QTextCharFormat, QColor

import datetime

# Import data and functions interacting with a database
import sys
sys.path.append('../helpers')
from helpers import get_expenses_by_category, get_expenses_by_date_range, create_group, ALL_POSSIBLE_CATEGORIES_LIST 


class AddGroupWindow(QMainWindow):
    def __init__(self, user_id, main_window):  
        super().__init__() 
        self.user_id = user_id
        self.main_window = main_window
        self.setWindowTitle("Create New Group")
        self.setStyleSheet('background-color: #F5FFFA')
        self.setGeometry(500, 200, 350, 300)

        # Get list of records to select the ones belonging to a new group
        self.group_selection_data = []

        # Store the name of the group before creation
        self.group_name = ""

        # Records that belong to the new group
        self.new_group_data = []

        self.create_widget()


    def create_widget(self):
        self.initial_creation = QWidget()

        initial_creation_layout = QFormLayout()
        initial_creation_layout.setSpacing(15)

        # Row 1 - Get user input for a group title
        label_group_name = QLabel("Group Name:")
        label_group_name.setFont(QFont('Futura', 16))
    
        self.name_group_line_edit = QLineEdit()
        self.name_group_line_edit.setStyleSheet('margin: 8 0')

        initial_creation_layout.addRow(label_group_name, self.name_group_line_edit)
        
        # Row 2 - Label to explain selection options
        selection_options = QLabel("Choose selection option")
        selection_options.setFont(QFont('Futura', 16))

        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(selection_options, alignment=Qt.AlignmentFlag.AlignCenter)

        initial_creation_layout.addRow(hbox_layout)

        # Row 3 - Buttons to choose by date or by category
        create_by_calendar_button = QPushButton("By Calendar")
        create_by_calendar_button.setCursor(Qt.CursorShape.PointingHandCursor)
        create_by_calendar_button.setFixedWidth(155)
        create_by_calendar_button.clicked.connect(self.select_group_by_calendar)
        create_by_calendar_button.setStyleSheet('background-color : #A8DCF0; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')

        create_by_category_button = QPushButton("By Category")
        create_by_category_button.setCursor(Qt.CursorShape.PointingHandCursor)
        create_by_category_button.setFixedWidth(155)
        create_by_category_button.clicked.connect(self.select_group_by_category)
        create_by_category_button.setStyleSheet('background-color : #A8DCF0; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')

        initial_creation_layout.addRow(create_by_calendar_button, create_by_category_button)

        self.initial_creation.setLayout(initial_creation_layout)
        self.setCentralWidget(self.initial_creation)


        # Calendar selection view
        self.calendar_selection = QWidget()
        calender_selection_layout = QVBoxLayout()

        calendar_label = QLabel("Select Date Range")
        calendar_label.setFont(QFont('Futura', 16))
        calender_selection_layout.addWidget(calendar_label)

        # Insert calendar widget 
        self.calendar = CustomCalendar()
        calender_selection_layout.addWidget(self.calendar)

        # Button to run search by dates
        search_by_date_button = QPushButton("Search")
        search_by_date_button.setCursor(Qt.CursorShape.PointingHandCursor)
        search_by_date_button.clicked.connect(self.generate_group_selection_list_by_date)
        search_by_date_button.setStyleSheet('background-color : #D8BFD8; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')
        calender_selection_layout.addWidget(search_by_date_button)

        self.calendar_selection.setLayout(calender_selection_layout)


        # Category selection view
        self.category_selection = QWidget()
        category_selection_layout = QVBoxLayout()
        category_selection_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        category_selection_layout.setSpacing(70)

        category_label = QLabel("Select Category")
        category_label.setFont(QFont('Futura', 16))
        category_selection_layout.addWidget(category_label)

        # Present category options with combo box
        self.list_expenses_selection = QComboBox()
        self.list_expenses_selection.addItems(ALL_POSSIBLE_CATEGORIES_LIST)

        # Style Combo Box
        self.list_expenses_selection.setFixedHeight(50)
        self.list_expenses_selection.setStyleSheet("QComboBox QAbstractItemView {""selection-color: #2E8B57""}")
        category_selection_layout.addWidget(self.list_expenses_selection)
        
        # Button to run search by category
        search_by_category_button = QPushButton("Search")
        search_by_category_button.setCursor(Qt.CursorShape.PointingHandCursor)
        search_by_category_button.clicked.connect(lambda : self.generate_group_selection_list_by_category(self.list_expenses_selection.currentText()))
        search_by_category_button.setStyleSheet('background-color : #D8BFD8; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')
        category_selection_layout.addWidget(search_by_category_button)

        self.category_selection.setLayout(category_selection_layout)
        

        # Table for selection values that belong to the group
        self.selection_table_window = QWidget()
    

    # Button press for choosing to create a group by calendar
    def select_group_by_calendar(self):
        if self.name_group_line_edit.text():
            self.group_name = self.name_group_line_edit.text()
            self.initial_creation.hide()
            self.setCentralWidget(self.calendar_selection)
        else: 
            no_group_name_msg = QMessageBox.information(self, "Information", "Group name is missing")


    # Button press to display expenses within selected date range
    def generate_group_selection_list_by_date(self):
        if self.calendar.from_date and self.calendar.to_date:

            # Update data format 
            from_date = datetime.date(self.calendar.from_date.year(), self.calendar.from_date.month(), self.calendar.from_date.day())
            to_date = datetime.date(self.calendar.to_date.year(), self.calendar.to_date.month(), self.calendar.to_date.day())

            # Extract data from the database
            extracted_data = get_expenses_by_date_range(self.user_id, from_date, to_date)
            self.group_selection_data = extracted_data

            # Hide this window and open a table with checkmarks
            self.calendar_selection.hide()
            self.create_table()

        else:
            no_date_range__selected_msg = QMessageBox.information(self, "Information", "No range selected")





    def create_table(self):
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
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Name", "Category", "Date", "Type", "Amount ($)", "Add"])
        self.table.verticalHeader().setDefaultSectionSize(50)

        header = self.table.horizontalHeader()

        # Allow sorting by column header clicks
        header.setSectionsClickable(True)
        header.sectionClicked.connect(self.header_clicked)
        self.fill_table_content()

        table_selection_layout.addWidget(self.table)

        # Button to create a group
        create_group_button = QPushButton("Create Group")
        create_group_button.setCursor(Qt.CursorShape.PointingHandCursor)
        create_group_button.clicked.connect(self.create_group)
        create_group_button.setStyleSheet('background-color : #D8BFD8; font-weight: 600; font-size: 16px; border-radius : 5; padding: 6 0')
        table_selection_layout.addWidget(create_group_button)

        self.selection_table_window.setLayout(table_selection_layout)

        self.setCentralWidget(self.selection_table_window)


    # Populate the table with data
    def fill_table_content(self):

        self.table.clearContents()

        # Set the size of the table
        self.table.setRowCount(len(self.group_selection_data))

        if self.group_selection_data:
            for i, expense_record in enumerate(self.group_selection_data):
                name = expense_record[0]
                category = expense_record[1]
                date = expense_record[2]
                transaction_type = expense_record[3]
                amount = expense_record[4]

                # Insert extracted data into a row 
                self.table.setItem(i, 0, QTableWidgetItem(name))
                self.table.setItem(i, 1, QTableWidgetItem(category))
                self.table.setItem(i, 2, QTableWidgetItem(date))
                self.table.setItem(i, 3, QTableWidgetItem(transaction_type))
                self.table.setItem(i, 4, QTableWidgetItem(str(amount)))

                # Checkbox to include a record into a group
                checkbox = QCheckBox("Add", self)
                checkbox.setStyleSheet("background-color: #F9EBD1; border: none; border-radius: 5; padding: 5 0" )
                self.table.setCellWidget(i, 5, checkbox)

                # Make cells besides checkbox non-editable
                for column in range(5):
                    label_item = self.table.item(i, column)
                    if label_item:
                        # The flags() method returns the current flags of the item, and we use a bitwise AND operation (&) with the complement (NOT) of the Qt.ItemFlag.ItemIsEditable flag to remove the Qt.ItemIsEditable flag from the item's flags.
                        label_item.setFlags(label_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        else:
            self.table.setRowCount(1)
            self.table.setSpan(0, 0, 1, 5)
            self.table.setItem(0, 0, QTableWidgetItem("No Data For This Date Range"))
    
    
    # Sort rows in the table according to the clicked column header
    def header_clicked(self, logical_index):
        # Sort by name
        if logical_index == 0:
            self.group_selection_data = sorted(self.group_selection_data, key=lambda x: x[0])
        # Sort by category
        if logical_index == 1:
            self.group_selection_data = sorted(self.group_selection_data, key=lambda x: x[1])
        # Sort by date
        if logical_index == 2:
            self.group_selection_data = sorted(self.group_selection_data, key=lambda x: x[2], reverse=True)
        # Sort by type
        if logical_index == 3:
            self.group_selection_data = sorted(self.group_selection_data, key=lambda x: x[3])
        # Sort by amount
        if logical_index == 4:
            self.group_selection_data = sorted(self.group_selection_data, key=lambda x: x[4], reverse=True)
        
        self.fill_table_content()

    # Button press for choosing to create a group by category
    def select_group_by_category(self):
        if self.name_group_line_edit.text():
            self.group_name = self.name_group_line_edit.text()
            self.initial_creation.hide()
            self.setCentralWidget(self.category_selection)
        else:
            no_group_name_msg = QMessageBox.information(self, "Information", "Group name is missing")


    # Button press to display expenses within selected caategory
    def generate_group_selection_list_by_category(self, category):

        # Extract data from the database 
        extracted_data = get_expenses_by_category(self.user_id, category)

        # Insert category into the records
        extracted_data_with_category = []
        for row in extracted_data:
            new_row = list(row)
            new_row.insert(1, category)
            extracted_data_with_category.append(new_row)
        self.group_selection_data = extracted_data_with_category

        # Hide this window and open a table with checkmarks
        self.category_selection.hide()
        self.create_table()


    # Creating a group - Adding group_id to the record rows with checked checkbox
    def create_group(self):
        row_count = self.table.rowCount()
        column_count = self.table.columnCount()
        selected_rows_data = []

        for row in range(row_count):
            # Get the state of the cell with checkbox
            checkbox = self.table.cellWidget(row, 5)
            if isinstance(checkbox, QCheckBox) and checkbox.isChecked():
                # Get record information and insert it into the grour records list
                row_data = [self.table.item(row, column).text() for column in range(5)]
                selected_rows_data.append(row_data)

        # Error message for lack of selection
        if not selected_rows_data:
            no_rows_selected_msg = QMessageBox.warning(self, "Information", "Nothing was selected")
        
        else:
            # Create a group by passing selected_rows_data and a group title
            sql_return_value = create_group(self.user_id, self.group_name, selected_rows_data)

            # If validation passed - flush the message 
            if sql_return_value == 0:

                # Update main window
                self.main_window.update_groups_area()

                success_msg = QMessageBox.information(self, "Information", "Group created")
                self.close()
        



# Modify calendar widget to allow date range selection
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

        # Adjust selection to pressed dates
        if self.from_date == date_value:
            self.from_date = None
            self.to_date = None
        elif self.from_date is None:
            self.from_date = date_value
        else:
            # If from_date is set, set to_date to the clicked date
            self.to_date = date_value
            self.highlight_range(self.highlighter_format)


    # Apply style to selected a time frame
    def highlight_range(self, format):
        if self.from_date and self.to_date:
            # Find out which date is earlier
            start = min(self.from_date, self.to_date)
            end = max(self.from_date, self.to_date)

            # Apply highlight format to the span of the date range
            while end >= start:
                self.setDateTextFormat(start, format)
                start = start.addDays(1)





