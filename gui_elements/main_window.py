from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QBrush, QColor, QPainter, QFontMetrics
from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QGridLayout, 
                            QHBoxLayout, QVBoxLayout, QFormLayout, QMainWindow, 
                            QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem)

from PyQt6.QtCharts import (QBarCategoryAxis, QStackedBarSeries, QBarSet, QChart, 
                            QChartView, QValueAxis, QPieSeries, QPieSlice)

import datetime

# GUI elements

from gui_elements.change_limit import ChangeLimitWindow
from gui_elements.add_expense import AddExpenseWindow
from gui_elements.add_income import AddIncomeWindow
from gui_elements.category_view import DisplayCategoryList
from gui_elements.single_group_view import DisplayGroupList
from gui_elements.add_new_group import AddGroupWindow
from gui_elements.calendar_view import CalendarView


# Import data extaction functions
import sys
sys.path.append('../helpers')
import helpers 


#  Categories list for all categories view
ALL_POSSIBLE_CATEGORIES_LIST = ["Rent", "Utilities", "Grocery", "Eating Out", "Online Shopping", "Sport", "Charity", "Other"]
# Expense types
ALL_EXPENSE_TYPES = ["Credit", "Cash", "Foreign Currency"]

class MainScreen(QWidget):
    def __init__(self, user_id):
        super().__init__()  
        self.user_id = user_id
        self.setWindowTitle("Expences Tracker")

        # Set size of the main window - position x, position y, width, height
        self.setGeometry(100, 100, 1200, 750)
        self.setStyleSheet('background-color: #F5FFFA')
        
        # Create main layout 
        main_layout = QGridLayout()


        # FUNCTIONAL AREA 1 in the top left of the grid box
        greeting_with_calender = QWidget()

        # First row
        title = QLabel("<h1>My Expenses</h1>")

        # Second row
        greeting = QLabel("Take a look at your current balance")
        greeting.setFont(QFont('Futura', 16))

        # Cet budget button 
        change_limit_button = AutoShrinkButton("Change Monthly Budget", 220, "#FFB499")
        change_limit_button.clicked.connect(self.change_limit)

        self.limit_window = ChangeLimitWindow(self.user_id)
        self.calendar_window = None

        # Calender Button
        calendar_button = StyledPushButton("Calendar", 150, "#ADD8E6", 18)
        calendar_button.clicked.connect(self.open_calender)

        # Add widgets to the horizontal layout to make a button row
        inner_greeting_layout = QHBoxLayout()
        inner_greeting_layout.addWidget(greeting)
        inner_greeting_layout.addWidget(change_limit_button)
        inner_greeting_layout.addWidget(calendar_button)

        # Set main layout of the area as vertical and add title and second row to it
        v_greeting_layout = QVBoxLayout()
        v_greeting_layout.addWidget(title)
        v_greeting_layout.addLayout(inner_greeting_layout)

        greeting_with_calender.setLayout(v_greeting_layout)



        # FUNCTIONAL AREA 2 - user entry section
        placeholder_add_buttons = QWidget()
        add_income_expence_layout = QVBoxLayout()

        # Add Income button
        add_income_button = StyledPushButton("Add Income", 150, "#E6E6FA", 14)
        add_income_button.clicked.connect(self.open_add_income)
        # self.add_income_window = AddIncomeWindow(self.user_id)
        self.add_income_window = None

        # Add Expense Button
        add_expence_button = StyledPushButton("Add Expense", 150, "#B2CDD6", 14)
        add_expence_button.clicked.connect(self.open_add_expense)
        self.add_expense_window = None
    
        # Upload Expense Button
        upload_expence_button = StyledPushButton("Upload .xls", 150, "#B2CDD6", 14)
        upload_expence_button.clicked.connect(self.open_upload_expense)

        # Insert buttons to the layout
        add_income_expence_layout.addWidget(add_income_button)
        add_income_expence_layout.insertSpacing(1, 25)
        add_income_expence_layout.addWidget(add_expence_button)
        add_income_expence_layout.addWidget(upload_expence_button)

        placeholder_add_buttons.setLayout(add_income_expence_layout)



        # FUNCTIONAL AREA 3 - Groups section
        placeholder_groups = QWidget()
        groups_layout = QVBoxLayout()
        groups_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Group title label
        groups_label = QLabel("Groups:")
        groups_label.setFont(QFont('Futura', 16))
        groups_layout.addWidget(groups_label)
        groups_layout.insertSpacing(1, 10)

        # Get list of all available groups with the total amount spent
        GROUP_LIST = helpers.get_groups_list(self.user_id)

        # Create buttons to view available groups
        for i in range(len(GROUP_LIST)):
            single_group_layout = QHBoxLayout()

            # Button with title
            button_group_name = AutoShrinkButton(GROUP_LIST[i][0], 200, "#D8BFD8")
            button_group_name.clicked.connect(lambda x, i=i : self.group_button_press(GROUP_LIST[i][0]))
            # button_group_name.setStyleSheet('background-color : #D8BFD8; font-weight: 600; font-size: 14px; border-radius : 5; padding: 5 0')

            # Label with amount spent
            label_group_amount = QLabel(str(GROUP_LIST[i][1]))
            label_group_amount.setFont(QFont('Futura', 16))
            label_group_amount.setStyleSheet('background-color : #F0FFF0; font-weight: 550; border-radius : 5; padding: 5 0')
            label_group_amount.setAlignment(Qt.AlignmentFlag.AlignRight)

            # Add layouts
            single_group_layout.addWidget(button_group_name)
            single_group_layout.addWidget(label_group_amount)
            groups_layout.addLayout(single_group_layout)
            
        # Add last button to create a new group
        add_new_group_button = StyledPushButton("New Group", 150, "#D7C3C1", 14)
        add_new_group_button.clicked.connect(self.add_new_group)
        groups_layout.addWidget(add_new_group_button, alignment=Qt.AlignmentFlag.AlignLeft)

        placeholder_groups.setLayout(groups_layout)
            


        # FUNCTIONAL AREA 4 - Categories section
        placeholder_categories = QWidget()
        categories_grid_layout = QGridLayout()

        # Add title to Categories section
        categories_title_layout = QHBoxLayout()
        categories_title = QLabel("Categories")
        categories_title.setFont(QFont('Futura', 18))

        # Button to view all categories
        open_all_categories_button = StyledPushButton("All Categories", 150, "#DEB887", 16)
        open_all_categories_button.clicked.connect(self.open_all_categories)

        # Add categories label andd button to the view
        categories_title_layout.addWidget(categories_title)
        categories_title_layout.addWidget(open_all_categories_button)
        categories_grid_layout.addLayout(categories_title_layout, 0, 0, 1, 5)


        # Get top 10 categories in user's expenses (tuple: name, spent this  month)
        TOP_CATEGORIES_LIST = helpers.get_top_10_category_expenses(self.user_id)

        # Create buttons with categories
        for i in range(len(TOP_CATEGORIES_LIST)):

            # Categories outer box
            single_category_layout = QVBoxLayout()

            # Category item as a button
            button_name = TOP_CATEGORIES_LIST[i][0]+ "\n" + str(TOP_CATEGORIES_LIST[i][1])
            category_item_button = QPushButton(button_name)
            category_item_button.setStyleSheet('background-color : #FFEBCD; color: #2A3036; font-weight: 600; border-radius : 5; padding: 8 0')
            category_item_button.setFont(QFont('Futura', 16))

            category_item_button.clicked.connect(lambda x, i=i : self.category_button_press(TOP_CATEGORIES_LIST[i][0]))
            
            # Add items to category box and align them
            single_category_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            single_category_layout.addWidget(category_item_button)
            categories_grid_layout.addLayout(single_category_layout, (i// 5) + 1, i % 5, 1, 1)

        placeholder_categories.setLayout(categories_grid_layout)


        # FUNCTIONAL AREA 5 - Bar chart and pie chart section
        placeholder_bar_chart = QWidget()
        placeholder_bar_chart.setStyleSheet('background-color: #F0F8FF')

        charts_area_layout = QGridLayout()

        # Create stacked bar chart with excpenses for the last 6 months
        stacked_bar_chart = StackedBarChart(self.user_id)
        charts_area_layout.addWidget(stacked_bar_chart, 0, 0, 1, 4)

        # Create donut chart with monthly limit
        current_month_donut_chart = DonutChart(self.user_id)
        charts_area_layout.addWidget(current_month_donut_chart, 0, 4, 1, 2)

        placeholder_bar_chart.setLayout(charts_area_layout)

        
        # Add 5 FUNCTIONAL AREAS to the layout
        main_layout.addWidget(greeting_with_calender, 0, 0, 1, 4)
        main_layout.addWidget(placeholder_bar_chart, 1, 0, 3, 4)
        main_layout.addWidget(placeholder_categories, 4, 0, 2, 4)
        main_layout.addWidget(placeholder_add_buttons, 0, 4, 2, 2)
        main_layout.addWidget(placeholder_groups, 2, 4, 4, 2)

        self.setLayout(main_layout)


    # FUNCTION AREA 1 methods  

    # Open a window with calender view 
    def open_calender(self):
        self.calendar_window = CalendarView(self.user_id)
        self.calendar_window.show()

    # change monthly budget (limit)
    def change_limit(self):
        print("Change limit button clicked")
        self.limit_window.show()

    # FUNCTION AREA 2 methods 

    # Open a window with add income view
    def open_add_income(self):
        self.add_income_window = AddIncomeWindow(self.user_id)
        self.add_income_window.show()


    # Open a window with add expense view
    def open_add_expense(self):
        self.add_expense_window = AddExpenseWindow(self.user_id, ALL_POSSIBLE_CATEGORIES_LIST, ALL_EXPENSE_TYPES)
        self.add_expense_window.show()


    # Open a window with upload file view
    def open_upload_expense(self):
        print("Upload expense Button clicked")

        # Use QFileDialog to open a window to select a file
        file_filter = "Text Files (*.csv *.xls *.xlsx)"
        file_dialog = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select an Excel or CSV file",
            directory="",
            filter=file_filter)
        
        # RUN CHECKS if the file could be open
        with open(file_dialog[0], 'r') as f:
            for line in f:
                print(line.rstrip())

        # EXTRACT NEEDED DATA AND INSERT IT TO THE DATABASE
        # EXTRACT ONLY THE FILENAME AND PASS IT TO PANDAS

        # FLUSH A MESSAGE THAT FILE WAS UPLOADED
        # message box = parent, title, message
        upload_complete_msg = QMessageBox.information(self, "Information", "The file has been uploaded")

  
    
    # FUNCTION AREA 3 methods 

    # Should open a window with selection of the expences related to some group
    def group_button_press(self, name):
        print(name + " was pressed") 
        
        # Create a group view instance
        self.single_group_view = DisplayGroupList(self.user_id, name)
              # Display newly created instance
        self.single_group_view.show()

    # Should open a list of all transactions and allow user to put checkmark near some to add them to group
    def add_new_group(self):
        print("Add New Group Button pressed")
        self.adding_new_group = AddGroupWindow(self.user_id, ALL_POSSIBLE_CATEGORIES_LIST)
        self.adding_new_group.show()
        


    # FUNCTION AREA 4 methods
      
    # Should open a window with selection of the expences related to some category
    def category_button_press(self, name):
        print(f"{name} was pressed")

        # Create an instanse of Category view to fill it with data on the button click
        self.single_category_view = DisplayCategoryList(self.user_id, name)

        # Display newly created instance
        self.single_category_view.show()

        
        
    #close detailed category view window    
    #
    def close_this_categories(self):
        self.list_all_categories_widget.hide()


    def open_all_categories(self):
        print("View All Categories button pressed")

        # View the list of all categories
        self.list_all_categories_widget = QWidget()
        all_cat_layout = QFormLayout()

        self.list_all_categories_widget.setGeometry(500, 200, 600, 300)

        for index, name in enumerate(ALL_POSSIBLE_CATEGORIES_LIST):
            # Label names
            label_category_name = QLabel(name)
            label_category_name.setFont(QFont('Futura', 16))

            # QLine edits to enter input
            button_name = "View " + name
            view_single_category_button = AutoShrinkButton(button_name, 180, "#8FBC8F")
            view_single_category_button.clicked.connect(lambda x, name=name : self.category_button_press(name))

            # Insert labels and line edits into layout
            all_cat_layout.addRow(label_category_name, view_single_category_button)

        # Add closing button 
        close_all_categories_button = StyledPushButton("Close", 150, "#B0C4DE", 16)
        close_all_categories_button.clicked.connect(self.close_all_categories)
        
        placeholder = QLabel("")
        all_cat_layout.addRow(placeholder, close_all_categories_button)

        self.list_all_categories_widget.setLayout(all_cat_layout)
        self.list_all_categories_widget.show()

    def close_all_categories(self):
        self.list_all_categories_widget.hide()





# CREATE A LIST OF TOP 5 EXPENCE CATEGORIES per last 6 month and reverse month
class StackedBarChart(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.series = QStackedBarSeries()
        RECENT_EXPENCES = helpers.get_recent_expenses(self.user_id)

        # Input the list of values in a dictionary of top 5 expence categories for the last 6 months into series
        for key in RECENT_EXPENCES:
            self.key = QBarSet(key)
            self.key.append(RECENT_EXPENCES[key])
            self.series.append(self.key)

        # Add series to the stacked bar chart
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle("Last 6 month")

        # Get 3-letter names of the last 6 month ans set them as X axis
        self.categories = self.get_last_6_month()
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
        self.setCentralWidget(self.chart_view)

    # Get names of the last 6 months 
    def get_last_6_month(self):
        now = datetime.datetime.now()
        result = [now.strftime("%B")[:3]]
        for _ in range(0, 5):
            now = now.replace(day=1) - datetime.timedelta(days=1)
            result.append(now.strftime("%B")[:3])
        # result.reverse()
        return result
        

# Donut chart with the expences made on current month
class DonutChart(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        # Make a pie chart with a hole
        self.series = QPieSeries()
        self.series.setHoleSize(0.4)

        # Extract data
        MONTHLY_LIMIT = helpers.get_monthly_budget(self.user_id)
        THIS_MONTH_EXPENSES = helpers.get_this_month_expenses(self.user_id)


        # Create donut slices with data
        self.slice1 = self.series.append("Spent", THIS_MONTH_EXPENSES)
        self.slice1.setBrush(QBrush(QColor("#FCBCB5")))
        self.slice2 = self.series.append(str(THIS_MONTH_EXPENSES), MONTHLY_LIMIT - THIS_MONTH_EXPENSES)
        self.slice2.setBrush(QBrush(QColor("#F0F8FF")))

        # Upload series to the chart 
        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.setTitle("Current Budget is " + str(MONTHLY_LIMIT))

        # Display the chart and its legend
        self.chart_view = QChartView(self.chart)
        self.chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setCentralWidget(self.chart_view)


 # Style buttons to avoit repeated style modifications       
class StyledPushButton(QPushButton):
    def __init__(self, text, width, color, font_size):
        super().__init__(text)
        self.setFixedWidth(width)
        self.setStyleSheet(f"background-color: {color}; border: none; border-radius: 5; padding: 5 0" )
        self.setFont(QFont("Futura", font_size))




# Buttons that reduce font size if the title does not fit
class AutoShrinkButton(QPushButton):
    DEFAULT_FONT_SIZE = 15

    def __init__(self, text, width, color):
        super().__init__(text)
        self.original_font = self.font()
        self.setFontSize(self.DEFAULT_FONT_SIZE)
        self.setFixedWidth(width)
        self.setStyleSheet(f"background-color: {color}; font-weight: 550; border: none; border-radius: 5; padding: 5 0" )
        self.update_font_size()

    def setFontSize(self, size):
        font = QFont(self.original_font)
        font.setPointSize(size)
        self.setFont(font)
        self.updateGeometry()

    def resizeEvent(self, event):
        self.update_font_size()
        super().resizeEvent(event)

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


        

