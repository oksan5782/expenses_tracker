from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, 
                            QTableWidgetItem, QPushButton, QWidget, 
                            QVBoxLayout, QHeaderView, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QBrush, QColor

# Import functions interacting with the database
import sys
sys.path.append('../helpers')
from helpers import get_group_expenses, remove_record_from_the_group, edit_record


class DisplayGroupList(QMainWindow):
    def __init__(self, user_id, name, main_window):
        super().__init__()
        self.group_name = name
        self.user_id = user_id
        self.main_window = main_window
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
        self.table_widget.setStyleSheet(stylesheet)
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(["Name", "Category", "Date", "Type", "Amount ($)", "Edit", "Exclude"])
        self.table_widget.verticalHeader().setDefaultSectionSize(50)

        # Set horizontal headder to change mouse pointer on hover
        custom_header = HoverHeaderView(Qt.Orientation.Horizontal)
        self.table_widget.setHorizontalHeader(custom_header)

        # Allow sorting by column header clicks
        custom_header.sectionClicked.connect(self.header_clicked)

        # Get group data from the database for current user
        self.group_expenses_list = get_group_expenses(self.user_id, self.group_name)

         # Check for null
        if not self.group_expenses_list:
            self.table_widget.setRowCount(1)
            self.table_widget.setSpan(0, 0, 1, 7)
            self.table_widget.setItem(0, 0, QTableWidgetItem("No Data For This Group"))
        else:
            self.fill_table_content()

        outer_frame_layout.addWidget(self.table_widget)

        # Closing button
        closing_button = QPushButton("Close")
        closing_button.setCursor(Qt.CursorShape.PointingHandCursor)
        closing_button.setFixedWidth(150)
        closing_button.setStyleSheet("background-color: #B0C4DE; border: none; border-radius: 5; padding: 5 0" )
        closing_button.setFont(QFont("Futura", 16))
        closing_button.clicked.connect(self.close_group_view)
        outer_frame_layout.addWidget(closing_button, alignment=Qt.AlignmentFlag.AlignCenter)
       
        # Set layout and display it
        outer_frame.setLayout(outer_frame_layout)
        self.setCentralWidget(outer_frame)

        self.show()
        

    def fill_table_content(self):
        self.table_widget.clearContents()
        self.table_widget.setRowCount(len(self.group_expenses_list))

        for i, expense_record in enumerate(self.group_expenses_list):
            name = expense_record[0]
            category = expense_record[1]
            date = expense_record[2]
            transaction_type = expense_record[3]
            amount = expense_record[4]

            # Insert extracted data into the table row 
            self.table_widget.setItem(i, 0, QTableWidgetItem(name))
            self.table_widget.setItem(i, 1, QTableWidgetItem(category))
            self.table_widget.setItem(i, 2, QTableWidgetItem(date))
            self.table_widget.setItem(i, 3, QTableWidgetItem(transaction_type))
            self.table_widget.setItem(i, 4, QTableWidgetItem(str(amount)))

            # Button to edit the record
            edit_this_group_record = QPushButton("Edit", self)
            edit_this_group_record.setCursor(Qt.CursorShape.PointingHandCursor)
            edit_this_group_record.setCheckable(True)
            edit_this_group_record.setStyleSheet("background-color: #D9BFBF; border: none; border-radius: 5; padding: 5 0" )
            edit_this_group_record.setFont(QFont("Futura", 16))
            edit_this_group_record.clicked.connect(lambda checked, row=i: self.edit_this_expense_record(row, checked))

            # Button to remove record from the group
            remove_this_group_record = QPushButton("Delete", self)
            remove_this_group_record.setCursor(Qt.CursorShape.PointingHandCursor)
            remove_this_group_record.setStyleSheet("background-color: #DBC3A3; border: none; border-radius: 5; padding: 5 0" )
            remove_this_group_record.setFont(QFont("Futura", 16))
            remove_this_group_record.clicked.connect(lambda checked, row=i: self.remove_this_expense_record(row))

            self.table_widget.setCellWidget(i, 5, edit_this_group_record)
            self.table_widget.setCellWidget(i, 6, remove_this_group_record)

            # Set all labels as non-editable initially
            for column in range(5):
                label_item = self.table_widget.item(i, column)
                if label_item:
                    # The flags() method returns the current flags of the item, and we use a bitwise AND operation (&) with the complement (NOT) of the Qt.ItemFlag.ItemIsEditable flag to remove the Qt.ItemIsEditable flag from the item's flags.
                    label_item.setFlags(label_item.flags() & ~Qt.ItemFlag.ItemIsEditable)


    # Sort rows in the table according to the clicked column header
    def header_clicked(self, logical_index):
        # Sort by name
        if logical_index == 0:
            self.group_expenses_list = sorted(self.group_expenses_list, key=lambda x: x[0])
        # Sort by category
        if logical_index == 1:
            self.group_expenses_list = sorted(self.group_expenses_list, key=lambda x: x[1])
        # Sort by date
        if logical_index == 2:
            self.group_expenses_list = sorted(self.group_expenses_list, key=lambda x: x[2], reverse=True)
        # Sort by type
        if logical_index == 3:
            self.group_expenses_list = sorted(self.group_expenses_list, key=lambda x: x[3])
        # Sort by amount
        if logical_index == 4:
            self.group_expenses_list = sorted(self.group_expenses_list, key=lambda x: x[4], reverse=True)
        
        self.fill_table_content()
    

    # Close window button
    def close_group_view(self):
        self.hide()
    

    # Remove current record from the group only
    def remove_this_expense_record(self, row):

        # Collect row data to find the record in the database
        row_data = [self.table_widget.item(row, column).text() for column in range(5)]
        sql_return_value = remove_record_from_the_group(self.user_id, row_data[0], row_data[1], row_data[2], row_data[3], row_data[4])
       
        if sql_return_value:
            # Flush message with the status
            success_msg = QMessageBox.information(self, "Information", "Records removed from the group")

            # Repaint group widget
            self.main_window.update_groups_area()

            # Update group view
            self.table_widget.update()


    # Edit record and update it in the database
    def edit_this_expense_record(self, row_index, checked):
        if checked:  # When the "Edit" button is checked

            # Collect row data to find the record in the database
            self.row_data_before_editing = []
            for column in range(5):
                label_item = self.table_widget.item(row_index, column)
                self.row_data_before_editing.append(label_item.text())
                if label_item:
                    label_item.setBackground(QBrush(QColor("#ADFF2F")))
                    label_item.setForeground(QBrush(QColor("#483D8B")))
                    label_item.setFlags(label_item.flags() | Qt.ItemFlag.ItemIsEditable)

            # Change text of the "Edit" button to "Apply"
            edit_button = self.table_widget.cellWidget(row_index, 5)
            edit_button.setText("Apply")

        else:  # When the "Apply" button is unchecked
            edited_row_data = []
            # Retrieve data from QTableWidgetItem and print the edited data
            for column in range(5):
                label_item = self.table_widget.item(row_index, column)
                if label_item:
                    edited_row_data.append(label_item.text())
                    label_item.setFlags(label_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    label_item.setBackground(QBrush(QColor("#F0FFF0")))
                    label_item.setForeground(QBrush(QColor("#000000")))  # Reset the text color

            # Change text of the "Apply" button to "Edit"
            edit_button = self.table_widget.cellWidget(row_index, 5)
            edit_button.setText("Edit")

            # Update record in the database 
            result, message = edit_record(self.user_id, self.row_data_before_editing, edited_row_data)

            if not result:
                cannot_add_msg = QMessageBox.information(self, "Information", message)
            
            else:
            # If the validation passed 
                success_msg = QMessageBox.information(self, "Information", message)

                # Repaint graph, categories view and balance widgets in the main window
                self.main_window.stacked_bar_chart.refresh_bar_chart()
                self.main_window.update_categories_area()
                self.main_window.update_groups_area()
                self.main_window.current_month_donut_chart.refresh_donut_chart()

            # Update table after removal of the item
            self.table_widget.update()


# Custom header class to enable mouse cursor change
class HoverHeaderView(QHeaderView):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setSectionsClickable(True)
        self.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    # Define mouse over cursor change for all the columns besides the last one
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if self.orientation() == Qt.Orientation.Horizontal:
            for logical_index in range(self.count() - 2):
                if (
                    self.sectionPosition(logical_index) <= event.pos().x() < 
                    self.sectionPosition(logical_index + 1)
                ):
                    self.setCursor(Qt.CursorShape.PointingHandCursor)
                    return
        self.setCursor(Qt.CursorShape.ArrowCursor)
