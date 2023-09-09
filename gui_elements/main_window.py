from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QBrush, QColor, QPainter, QFontMetrics
from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QGridLayout, 
                            QHBoxLayout, QVBoxLayout, QFormLayout, QDialog,
                            QDialogButtonBox, QSpinBox, QFileDialog, QMessageBox)

from PyQt6.QtCharts import (QBarCategoryAxis, QStackedBarSeries, QBarSet, QChart, 
                            QChartView, QValueAxis, QPieSeries)

# GUI elements
from gui_elements.view_balance import ViewBalanceWindow
from gui_elements.add_expense import AddExpenseWindow
from gui_elements.add_income import AddIncomeWindow
from gui_elements.category_view import DisplayCategoryList
from gui_elements.single_group_view import DisplayGroupList
from gui_elements.add_new_group import AddGroupWindow
from gui_elements.calendar_view import CalendarView


# Import functions interacting with the database
import sys
sys.path.append('../helpers')
from helpers import (get_groups_list, get_top_10_category_expenses, get_recent_expenses,
                     upload_expense_csv_discover, upload_expense_csv_chase,
                     get_3_letters_for_last_6_month, get_this_month_expenses,
                     get_monthly_income)


class MainScreen(QWidget):
    def __init__(self, user_id):
        super().__init__()  
        self.user_id = user_id
        self.setWindowTitle("Expences Tracker")

        # Set size of the main window - position x, position y, width, height
        self.setGeometry(100, 100, 1240, 750)
        self.set_ui()


    # Create main layout 
    def set_ui(self):
        self.setStyleSheet('background-color: #F5FFFA')
        self.main_layout = QGridLayout()

        # Generate components
        self.generate_greeting_area()
        self.generate_charts_area()
        self.generate_categories_area()
        self.generate_buttons_area()
        self.generate_groups_area()

        # Add these 5 functional componets to the layout
        self.main_layout.addWidget(self.greeting_with_calender, 0, 0, 1, 4)
        self.main_layout.addWidget(self.placeholder_bar_chart, 1, 0, 3, 4)
        self.main_layout.addWidget(self.placeholder_categories, 4, 0, 2, 4)
        self.main_layout.addWidget(self.placeholder_add_buttons, 0, 4, 2, 2)
        self.main_layout.addWidget(self.placeholder_groups, 2, 4, 4, 2)

        self.setLayout(self.main_layout)


    # FUNCTIONAL AREA 1 in the top left of the grid box
    def generate_greeting_area(self):
        self.greeting_with_calender = QWidget()

        # First row
        title = QLabel("<h1>My Expenses</h1>")

        # Second row
        greeting = QLabel("Take a look at your current balance")
        greeting.setFont(QFont('Futura', 16))

        # View balance button 
        change_limit_button = AutoShrinkButton("View Balance Data", 220, "#FFB499")
        change_limit_button.clicked.connect(self.change_limit)

        # Create widgets called by button clicks
        self.balance_window = None
        self.calendar_window = None

        # View calender button
        calendar_button = StyledPushButton("Calendar", 150, "#ADD8E6", 18)
        calendar_button.clicked.connect(self.open_calender)

        # Add widgets to the horizontal layout 
        inner_greeting_layout = QHBoxLayout()
        inner_greeting_layout.addWidget(greeting)
        inner_greeting_layout.addWidget(change_limit_button)
        inner_greeting_layout.addWidget(calendar_button)

        # Set main layout of the area as vertical 
        v_greeting_layout = QVBoxLayout()
        v_greeting_layout.addWidget(title)
        v_greeting_layout.addLayout(inner_greeting_layout)

        self.greeting_with_calender.setLayout(v_greeting_layout)


    # FUNCTIONAL AREA 2 - user input section
    def generate_buttons_area(self):
        self.placeholder_add_buttons = QWidget()
        add_income_expence_layout = QVBoxLayout()

        # Add Income button
        add_income_button = StyledPushButton("Add Income", 160, "#E6E6FA", 15)
        add_income_button.clicked.connect(self.open_add_income)
        self.add_income_window = None

        # Add Expense Button
        add_expence_button = StyledPushButton("Add Expense", 160, "#B2CDD6", 15)
        add_expence_button.clicked.connect(self.open_add_expense)
        self.add_expense_window = None
    
        # Upload Chase Button
        upload_chase_button = AutoShrinkButton("Upload Chase .csv", 160, "#B2CDD6")
        upload_chase_button.clicked.connect(self.open_upload_expense_chase)

        # Upload Discover Button 
        upload_discover_button = AutoShrinkButton("Upload Discover .csv", 160, "#B2CDD6")
        upload_discover_button.clicked.connect(self.open_upload_expense_discover)

        # Insert buttons to the layout
        add_income_expence_layout.addWidget(add_income_button)
        add_income_expence_layout.insertSpacing(1, 10)
        add_income_expence_layout.addWidget(add_expence_button)
        add_income_expence_layout.addWidget(upload_chase_button)
        add_income_expence_layout.addWidget(upload_discover_button)

        self.placeholder_add_buttons.setLayout(add_income_expence_layout)


        # FUNCTIONAL AREA 3 - Groups section
    def generate_groups_area(self):
        self.placeholder_groups = None
        self.refresh_groups()

    # Update groups content called from outer functions
    def update_groups_area(self):
        self.refresh_groups()
        self.main_layout.removeWidget(self.placeholder_groups)
        self.main_layout.addWidget(self.placeholder_groups, 2, 4, 4, 2)
        self.setLayout(self.main_layout)

    # Create groups view
    def refresh_groups(self):
        self.placeholder_groups = QWidget()
        groups_layout = QVBoxLayout()
        groups_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Group title label
        groups_label = QLabel("Groups:")
        groups_label.setFont(QFont('Futura', 16))
        groups_layout.addWidget(groups_label)
        groups_layout.insertSpacing(1, 10)

        # Get list of the available groups with the total amount spent
        group_list = get_groups_list(self.user_id)

        if not group_list:
            single_group_layout = QHBoxLayout()
            no_groups_label = QLabel("No Groups Created")
            no_groups_label.setFont(QFont('Futura', 15))
            no_groups_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            single_group_layout.addWidget(no_groups_label)
            groups_layout.addLayout(single_group_layout)

        else:
            # Create buttons to view available groups
            for i in range(len(group_list)):
                single_group_layout = QHBoxLayout()

                # Button with title
                button_group_name = AutoShrinkButton(group_list[i][0], 200, "#D8BFD8")
                button_group_name.clicked.connect(lambda x, i=i : self.group_button_press(group_list[i][0]))

                # Label with the amount spent
                label_group_amount = QLabel(str(round(group_list[i][1], 2)))
                label_group_amount.setFont(QFont('Futura', 16))
                label_group_amount.setStyleSheet('background-color : #F0FFF0; font-weight: 550; border-radius : 5; padding: 5 0')
                label_group_amount.setAlignment(Qt.AlignmentFlag.AlignRight)

                # Add layouts for display
                single_group_layout.addWidget(button_group_name)
                single_group_layout.addWidget(label_group_amount)
                groups_layout.addLayout(single_group_layout)

        # Add last button to create a new group
        add_new_group_button = StyledPushButton("New Group", 150, "#D7C3C1", 14)
        add_new_group_button.clicked.connect(self.add_new_group)
        groups_layout.addWidget(add_new_group_button, alignment=Qt.AlignmentFlag.AlignLeft)

        self.placeholder_groups.setLayout(groups_layout)


    # FUNCTIONAL AREA 4 - Categories section
    def generate_categories_area(self):
        self.placeholder_categories = None
        self.refresh_categories()


    # Update categories content called from the outer functions
    def update_categories_area(self):
        self.refresh_categories()
        self.main_layout.removeWidget(self.placeholder_categories)
        self.main_layout.addWidget(self.placeholder_categories, 4, 0, 2, 4)
        self.setLayout(self.main_layout)


    # Create categories view
    def refresh_categories(self):   
        self.placeholder_categories = QWidget()
        self.categories_grid_layout = QGridLayout()

        # Add title to categories section
        categories_title_layout = QHBoxLayout()
        categories_title = QLabel("Categories")
        categories_title.setFont(QFont('Futura', 18))

        # Explanation on how categories work
        categories_description = QLabel("Press each category for more details. Button titles contain data for the last month only")
        categories_description.setFont(QFont('Futura', 15))

        # Add category labels and buttons to the view
        categories_title_layout.addWidget(categories_title)
        categories_title_layout.addWidget(categories_description)
        self.categories_grid_layout.addLayout(categories_title_layout, 0, 0, 1, 5)

        # Get top 10 categories from user's expenses (tuple: name, spent this month)
        TOP_CATEGORIES_LIST = get_top_10_category_expenses(self.user_id)

        if TOP_CATEGORIES_LIST:
        # Create buttons with categories
            for i in range(len(TOP_CATEGORIES_LIST)):

                # Categories outer box
                single_category_layout = QVBoxLayout()

                # Category item as a button
                button_name = TOP_CATEGORIES_LIST[i][0]+ "\n" + str(TOP_CATEGORIES_LIST[i][1])
                category_item_button = QPushButton(button_name)
                category_item_button.setCursor(Qt.CursorShape.PointingHandCursor)

                category_item_button.setStyleSheet('background-color : #FFEBCD; color: #2A3036; font-weight: 600; border-radius : 5; padding: 8 0')
                category_item_button.setFont(QFont('Futura', 16))

                category_item_button.clicked.connect(lambda x, i=i : self.category_button_press(TOP_CATEGORIES_LIST[i][0]))

                # Add items to the category box and align them
                single_category_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                single_category_layout.addWidget(category_item_button)
                self.categories_grid_layout.addLayout(single_category_layout, (i// 5) + 1, i % 5, 1, 1)

        else:
            no_categories_label = QLabel("No expenses in categories this month")
            no_categories_label.setFont(QFont('Futura', 15))
            no_categories_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.categories_grid_layout.addWidget(no_categories_label, 1, 0, 1, 5)
        
        self.placeholder_categories.setLayout(self.categories_grid_layout)


    # FUNCTIONAL AREA 5 - Bar chart and pie chart section
    def generate_charts_area(self):
        self.placeholder_bar_chart = QWidget()
        self.placeholder_bar_chart.setStyleSheet('background-color: #F0F8FF')

        charts_area_layout = QGridLayout()

        # Create stacked bar chart with expenses for the last 6 months
        self.stacked_bar_chart = StackedBarChart(self.user_id)
        charts_area_layout.addWidget(self.stacked_bar_chart, 0, 0, 1, 4)

        # Create donut chart with the monthly balance
        self.current_month_donut_chart = DonutChart(self.user_id)
        charts_area_layout.addWidget(self.current_month_donut_chart, 0, 4, 1, 2)

        self.placeholder_bar_chart.setLayout(charts_area_layout)


    """ FUNCTIONAL AREA 1 methods """

    # Open a window with calender view 
    def open_calender(self):
        self.calendar_window = CalendarView(self.user_id)
        self.calendar_window.show()

    # change monthly budget (limit)
    def change_limit(self):
        self.balance_window = ViewBalanceWindow(self.user_id, self)
        self.balance_window.show()


    """ FUNCTIONAL AREA 2 methods """ 

    # Open add income window
    def open_add_income(self):
        self.add_income_window = AddIncomeWindow(self.user_id, self)
        self.add_income_window.show()


    # Open add expense window
    def open_add_expense(self):
        self.add_expense_window = AddExpenseWindow(self.user_id, self)
        self.add_expense_window.show()


    # Open Discover file upload dialog
    def open_upload_expense_discover(self):

        # Use QFileDialog to open a window and select the file
        file_filter = "Text Files (*.csv)"
        file_dialog = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select a CSV file",
            directory="",
            filter=file_filter)
        
        # If no file is selected
        if not file_dialog[0]:
            no_file_selected_msg = QMessageBox.warning(self, "Information", "No file selected")
        
        # Process the file
        else:
            result, message = upload_expense_csv_discover(self.user_id, file_dialog[0])
            
            # If file cannot be uploaded
            if not result:
                cannot_add_msg = QMessageBox.information(self, "Information", message)
            else:            
                # Repaint widgets in the main window
                self.stacked_bar_chart.refresh_bar_chart()
                self.update_categories_area()
                self.current_month_donut_chart.refresh_donut_chart()

                # Display successful upload message
                upload_complete_msg = QMessageBox.information(self, "Information", message)


    # Open Chase file upload dialog
    def open_upload_expense_chase(self):

        # Use QFileDialog to open a window to select a file
        file_filter = "Text Files (*.csv)"
        file_dialog = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select a CSV file",
            directory="",
            filter=file_filter)
        
        # If no file has been selected
        if not file_dialog[0]:
            no_file_selected_msg = QMessageBox.warning(self, "Information", "No file selected")
        
        # Process the file
        else:
            result, message = upload_expense_csv_chase(self.user_id, file_dialog[0])
            
            # If file cannot be uploaded
            if not result:
                cannot_add_msg = QMessageBox.information(self, "Information", message)

            else:   
                # Repaint widgets in the maain window
                self.stacked_bar_chart.refresh_bar_chart()
                self.update_categories_area()
                self.current_month_donut_chart.refresh_donut_chart()

                # Display successful upload message
                upload_complete_msg = QMessageBox.information(self, "Information", message)

    
    """ FUNCTIONAL AREA 3 methods """ 

    # Should open a window with selection of the expences related to some group
    def group_button_press(self, name):        
        # Create a group view instance
        self.single_group_view = DisplayGroupList(self.user_id, name, self)
        # Display newly created instance
        self.single_group_view.show()

    # Should open a list of all transactions and allow user to put checkmark near some to add them to group
    def add_new_group(self):
        self.adding_new_group = AddGroupWindow(self.user_id, self)
        self.adding_new_group.show()
        

    """ FUNCTIONAL AREA 4 methods """
      
    # Should open a window with selection of the expences related to some category
    def category_button_press(self, name):

        # Create an instanse of Category view to fill it with data on the button click
        self.single_category_view = DisplayCategoryList(self.user_id, name, self)

        # Display newly created instance
        self.single_category_view.show()

   
# Bar Chart with summary of the expenses for the last 6 months
class StackedBarChart(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.init_chart_ui()


    def init_chart_ui(self):
        self.bar_chart_layout = QVBoxLayout()

        # Create a button for setting Y-axis range
        self.range_button = QPushButton("Set Y-axis Range")
        self.range_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.range_button.setStyleSheet("background-color: #B3E0FF; border: none; border-radius: 5; padding: 5 0" )

        self.range_button.clicked.connect(self.show_range_dialog)
        self.bar_chart_layout.addWidget(self.range_button)

        self.chart_view = None  # Store the chart view widget
        self.no_results_label = None
        self.refresh_bar_chart()  # Initial chart creation or refresh if needed

        self.setLayout(self.bar_chart_layout)


    def refresh_bar_chart(self):

        # Get a dictionary of the recent expenses
        RECENT_EXPENSES = get_recent_expenses(self.user_id)

        # Remove the label with no results message, if painted
        if self.no_results_label:
            self.bar_chart_layout.removeWidget(self.no_results_label)
            self.no_results_label.deleteLater()

        # Delete the previous chart view
        if self.chart_view:
            self.bar_chart_layout.removeWidget(self.chart_view)
            self.chart_view.deleteLater()  
        
        if RECENT_EXPENSES:
            self.series = QStackedBarSeries()

            # Input the list of values in a dictionary of top 5 expense categories for the last 6 months into series
            for key in RECENT_EXPENSES:
                self.key = QBarSet(key)
                self.key.append(RECENT_EXPENSES[key])
                self.series.append(self.key)

            # Add series to the stacked bar chart
            self.chart = QChart()
            self.chart.addSeries(self.series)
            self.chart.setTitle("Last 6 month")

            # Get 3-letter names of the last 6 month ans set them as X axis
            self.categories = get_3_letters_for_last_6_month()
            self.axis_x = QBarCategoryAxis()
            self.axis_x.append(self.categories)
            self.chart.addAxis(self.axis_x, Qt.AlignmentFlag.AlignBottom)
            self.series.attachAxis(self.axis_x)

            # Create Y axis
            self.axis_y = QValueAxis()
            self.axis_y.setTickCount(6)
            self.axis_y.setLabelFormat("%d")
            self.axis_y.setRange(0, 5000)
            self.chart.addAxis(self.axis_y, Qt.AlignmentFlag.AlignLeft)
            self.series.attachAxis(self.axis_y)

            # Set alignment for the chart legend
            self.chart.legend().setVisible(True)
            self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignLeft)

            # Display the chart
            self.chart_view = QChartView(self.chart)
            self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
            self.bar_chart_layout.addWidget(self.chart_view)
        
        else:
            self.no_results_label = QLabel("No data in for the last 6 month")
            self.no_results_label.setFont(QFont('Futura', 15))
            self.no_results_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.bar_chart_layout.addWidget(self.no_results_label)


    # Allow user to update the range of Y axis
    def show_range_dialog(self):
        # Use Spin Box to set min and max values
        min_spinbox = QSpinBox()
        min_spinbox.setRange(0, 5000)
        min_spinbox.setValue(int(self.axis_y.min()))

        max_spinbox = QSpinBox()
        max_spinbox.setRange(0, 5000)
        max_spinbox.setValue(int(self.axis_y.max()))

        dialog = QDialog(self)
        dialog.setWindowTitle("Set Y-axis Range")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Minimum Value"))
        layout.addWidget(min_spinbox)
        layout.addWidget(QLabel("Maximum Value"))
        layout.addWidget(max_spinbox)

        # Display a message to modify the chart on "Ok" button press
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)

        layout.addWidget(button_box)
        dialog.setLayout(layout)

        if dialog.exec():
            min_value = min_spinbox.value()
            max_value = max_spinbox.value()
            self.axis_y.setRange(min_value, max_value)
            self.chart_view.repaint()


# Donut chart with the balance for the current month
class DonutChart(QWidget):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.set_ui()

    def set_ui(self):
        # Make a pie chart with a hole
        self.series = QPieSeries()
        self.series.setHoleSize(0.4)
        donut_chart_layout = QVBoxLayout()

        # Upload series to the chart
        self.chart = QChart()
        self.chart.addSeries(self.series)

        self.refresh_donut_chart()

        # Display the chart and its legend
        self.chart_view = QChartView(self.chart)
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        donut_chart_layout.addWidget(self.chart_view)
        self.setLayout(donut_chart_layout)

    
    def refresh_donut_chart(self):
        # Clear the current series if any
        self.series.clear()

        # Extract monthly expense and income data from the database
        current_month_expense = round(get_this_month_expenses(self.user_id))
        current_month_income = round(get_monthly_income(self.user_id))
        
        # Create donut slices with data with the colors according to the balance
        if current_month_expense < current_month_income:
            self.chart.setTitle("Income > Expense")
            self.slice1 = self.series.append(str(current_month_expense), current_month_expense)
            self.slice1.setBrush(QBrush(QColor("#C6ECD9")))
            self.slice2 = self.series.append(str(current_month_income), current_month_income - current_month_expense)
            self.slice2.setBrush(QBrush(QColor("#79D2A6")))
        elif current_month_expense > current_month_income:
            self.chart.setTitle("Income &lt; Expense")
            self.slice1 = self.series.append(str(current_month_income), current_month_expense)
            self.slice1.setBrush(QBrush(QColor("#F2738C")))
            self.slice2 = self.series.append(str(current_month_expense), current_month_income - current_month_expense)
            self.slice2.setBrush(QBrush(QColor("#990000")))
        else:
            self.chart.setTitle("Income = Expense")
            self.slice1 = self.series.append(str(current_month_income), current_month_expense)
            self.slice1.setBrush(QBrush(QColor("#D9B3FF")))
            self.slice2 = self.series.append(str(current_month_expense), current_month_income - current_month_expense)
            self.slice2.setBrush(QBrush(QColor("#CCCCFF")))


# Style buttons with borders and fond    
class StyledPushButton(QPushButton):
    def __init__(self, text, width, color, font_size):
        super().__init__(text)
        self.setFixedWidth(width)
        self.setStyleSheet(f"background-color: {color}; border: none; border-radius: 5; padding: 5 0" )
        self.setFont(QFont("Futura", font_size))
        self.setCursor(Qt.CursorShape.PointingHandCursor)


# Buttons that reduce font size if the title does not fit
class AutoShrinkButton(QPushButton):
    DEFAULT_FONT_SIZE = 15

    def __init__(self, text, width, color):
        super().__init__(text)
        # self.original_font = self.font()
        self.setFont(QFont("Futura", self.DEFAULT_FONT_SIZE))
        # self.setFontSize(self.DEFAULT_FONT_SIZE)
        self.setFixedWidth(width)
        self.setStyleSheet(f"background-color: {color}; font-weight: 550; border: none; border-radius: 5; padding: 5 0" )
        self.update_font_size()
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    # Set font size 
    def setFontSize(self, size):
        font = QFont(self.original_font)
        font.setPointSize(size)
        self.setFont(font)
        self.updateGeometry()


    def resizeEvent(self, event):
        self.update_font_size()
        super().resizeEvent(event)

    # Reduce font size if the text overflows the button width
    def update_font_size(self):
        metrics = QFontMetrics(self.font())
        text_width = metrics.horizontalAdvance(self.text())
        button_width = self.width()

        if text_width > button_width:
            font = self.font()
            font_size = self.font().pointSize()
            while text_width > button_width and font_size > 10:
                font_size -= 1
                font.setPointSize(font_size)
                metrics = QFontMetrics(font)
                text_width = metrics.horizontalAdvance(self.text())

            self.setFont(font)


        

