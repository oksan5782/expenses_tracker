from PyQt6.QtWidgets import (QCalendarWidget, QHBoxLayout, QVBoxLayout, 
                            QWidget, QTableWidget, QTableWidgetItem,
                            QHeaderView, QLabel, QAbstractItemView)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont

# Import functions interacting with a database
import sys
sys.path.append('../helpers')
from helpers import get_last_day_of_current_month, get_sum_expenses_by_date, get_list_expenses_by_date, get_last_start_date_of_oldest_record


# Allow date cell to store sum of expenses made on that day
class CustomCalendarCell(QTableWidgetItem):
    def __init__(self, sum_expenses):
        super().__init__(str(sum_expenses))
        self.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFlags(Qt.ItemFlag.ItemIsEnabled)

# Main calendar window
class CalendarView(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Calendar View')
        self.setGeometry(300, 200, 550, 450)

        self.layout = QHBoxLayout()
        self.layout.setSpacing(20)
        self.setLayout(self.layout)

        # Add calendar 
        self.calendar = CustomCalendarWidget(self.user_id) 
        self.calendar.selectionChanged.connect(self.calendar_date_changed)

        # Initialize the table to display list of expenses on a date cell click
        self.table = None

        self.layout.addWidget(self.calendar)


    # Create and display table of the daily expenses for the day clicked
    def calendar_date_changed(self):
        date_selected = self.calendar.selectedDate().toPyDate()

        # Clear previously created tables
        if self.table:
            self.table.deleteLater()

        # Make a new table with the selected date
        self.table = DateExpenseTable(self.user_id, date_selected)
        self.resize(900, 450)
        self.layout.addWidget(self.table)
        
        
class CustomCalendarWidget(QCalendarWidget):
    def __init__(self, user_id):
        super().__init__()  
        self.user_id = user_id

        # Remove vertical header with yearly week count
        self.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)

        # Get last day of the current month
        max_date = get_last_day_of_current_month()

        # Get first day of the month of the earliest record in the database
        min_date = get_last_start_date_of_oldest_record(self.user_id)[1]

        # Set min and max days to display in the calendar
        self.setMaximumDate(QDate(max_date.year, max_date.month, max_date.day))
        self.setMinimumDate(QDate(min_date.year, min_date.month, min_date.day))


    # Write sum of the expenses for a day
    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)

        # Get the sum of expenses for the current date
        date_str = date.toString("yyyy-MM-dd")
        sum_expenses = get_sum_expenses_by_date(self.user_id, date_str)
        if sum_expenses:
            sum_expenses = round(sum_expenses, 2)
        if not sum_expenses:
            sum_expenses = 0

        # Draw the sum of expenses directly in the cell below the date
        painter.drawText(rect, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, str(sum_expenses))



class DateExpenseTable(QWidget):
    def __init__(self, user_id, date):
        super().__init__()
        self.user_id = user_id
        self.date = date
        self.init_ui()

    def init_ui(self):
        # Create the QLabel to reflect selected date
        title_label = QLabel(f"Expenses for {self.date}")
        title_label.setFont(QFont('Futura', 16))

        # Create the QTableWidget 
        table = self.create_table()

        # Create a QVBoxLayout to arrange the QLabel and QTableWidget
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(table)

        # Set the layout for the main widget
        self.setLayout(layout)

    def create_table(self):

        self.table = QTableWidget(self) 

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

        self.table.setStyleSheet(stylesheet)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Name", "Date", "Amount ($)"])
        self.table.verticalHeader().setDefaultSectionSize(50)

        # Set horizontal headder to change mouse pointer on hover
        custom_header = HoverHeaderView(Qt.Orientation.Horizontal)
        self.table.setHorizontalHeader(custom_header)

        # Allow sorting by column header clicks
        custom_header.sectionClicked.connect(self.header_clicked)

        # Make table cells non-editable
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        # Extract data to populate the table 
        self.expenses_of_the_day = get_list_expenses_by_date(self.user_id, self.date)
        
        # If there is no expense information for this date
        if not self.expenses_of_the_day:
            self.table.setRowCount(1)
            self.table.setSpan(0, 0, 1, 3)
            self.table.setItem(0, 0, QTableWidgetItem("No Data For This Date"))

        else:
            self.fill_table_content()

        return self.table
        
    def fill_table_content(self):
        self.table.clearContents()

        # Set the size of the table
        self.table.setRowCount(len(self.expenses_of_the_day))

        for i, expense_record in enumerate(self.expenses_of_the_day):
            # Name, category, amount columns 
            name = expense_record[0]
            category = expense_record[1]
            amount = expense_record[2]

            # Insert extracted data into a row
            self.table.setItem(i, 0, QTableWidgetItem(name))
            self.table.setItem(i, 1, QTableWidgetItem(category))
            self.table.setItem(i, 2, QTableWidgetItem(str(amount)))


    # Sort rows in the table according to the clicked column header
    def header_clicked(self, logical_index):
        # Sort by name
        if logical_index == 0:
            self.expenses_of_the_day = sorted(self.expenses_of_the_day, key=lambda x: x[0])
        # Sort by category
        if logical_index == 1:
            self.expenses_of_the_day = sorted(self.expenses_of_the_day, key=lambda x: x[1])
                # Sort by amount
        if logical_index == 2:
            self.expenses_of_the_day = sorted(self.expenses_of_the_day, key=lambda x: x[2], reverse=True)
        
        self.fill_table_content()


# Custom header class to enable mouse cursor change
class HoverHeaderView(QHeaderView):
    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setSectionsClickable(True)
        self.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    # Define cursor change for all the column headers
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)

        if self.orientation() == Qt.Orientation.Horizontal:
            for logical_index in range(self.count()):
                if (
                    self.sectionPosition(logical_index) <= event.pos().x() <
                    self.sectionPosition(logical_index + 1)
                ):
                    self.setCursor(Qt.CursorShape.PointingHandCursor)
                    return
    
        self.setCursor(Qt.CursorShape.PointingHandCursor if self.orientation() == Qt.Orientation.Horizontal else Qt.CursorShape.ArrowCursor)

