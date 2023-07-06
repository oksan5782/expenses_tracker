from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QBrush, QColor, QPainter
from PyQt6.QtWidgets import (QWidget, QLabel, QPushButton, QGridLayout, 
                            QHBoxLayout, QVBoxLayout, QMainWindow)

from PyQt6.QtCharts import (QBarCategoryAxis, QStackedBarSeries, QBarSet, QChart, 
                            QChartView, QValueAxis, QPieSeries, QPieSlice)

import datetime


import sys
sys.path.append('../main')
from main import RECENT_EXPENCES, GROUP_LIST, CATEGORIES_LIST, MONTHLY_LIMIT, THIS_MONTH_EXPENSES


class MainScreen(QWidget):
    def __init__(self):
        super().__init__()  
        self.setWindowTitle("Expences Tracker")

        # Set size of the main window - position x, position y, width, height
        self.setGeometry(100, 100, 1200, 750)
        self.setStyleSheet('background-color: #F5FFFA')
        
        # Create main layout 
        main_layout = QGridLayout()


        # FUNCTIONAL AREA 1 in the top left of the grid box
        greetingWithCalender = QWidget()

        # First row
        title = QLabel("<h1>My Expenses</h1>")
        # Second row
        greeting = QLabel("Take a look at your current balance")
        greeting.setFont(QFont('Futura', 16))

        # Cet budget button 
        changeLimitButtom = StyledPushButton("Change Monthly Budget", 200, "#FFB499", 16)
        changeLimitButtom.clicked.connect(self.change_limit)

        # Calender Button
        calendarButton = StyledPushButton("Calendar", 150, "#ADD8E6", 18)
        calendarButton.clicked.connect(self.open_calender)

        # Add widgets to the horizontal layout to make a button row
        innerGreetingLayout = QHBoxLayout()
        innerGreetingLayout.addWidget(greeting)
        innerGreetingLayout.addWidget(changeLimitButtom)
        innerGreetingLayout.addWidget(calendarButton)

        # Set main layout of the area as vertical and add title and second row to it
        vGreetingLayout = QVBoxLayout()
        vGreetingLayout.addWidget(title)
        vGreetingLayout.addLayout(innerGreetingLayout)

        greetingWithCalender.setLayout(vGreetingLayout)



        # FUNCTIONAL AREA 2 - user entry section
        placeholderAddButtons = QWidget()
        addIncomeExpenceLayout = QVBoxLayout()

        # Add Income button
        addIncomeButton = StyledPushButton("Add Income", 150, "#E6E6FA", 14)
        addIncomeButton.clicked.connect(self.open_add_income)

        # Add Expense Button
        addExpenceButton = StyledPushButton("Add Expense", 150, "#B2CDD6", 14)
        addExpenceButton.clicked.connect(self.open_add_expense)
    
        # Upload Expense Button
        uploadExpenceButton = StyledPushButton("Upload .xls", 150, "#B2CDD6", 14)
        uploadExpenceButton.clicked.connect(self.open_upload_expense)

        # Insert buttons to the layout
        addIncomeExpenceLayout.addWidget(addIncomeButton)
        addIncomeExpenceLayout.insertSpacing(1, 25)
        addIncomeExpenceLayout.addWidget(addExpenceButton)
        addIncomeExpenceLayout.addWidget(uploadExpenceButton)

        placeholderAddButtons.setLayout(addIncomeExpenceLayout)



        # FUNCTIONAL AREA 3 - Groups section
        placeholderGroups = QWidget()
        groups_layout = QVBoxLayout()
        groups_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Group title label
        groupsLabel = QLabel("Groups:")
        groupsLabel.setFont(QFont('Futura', 16))
        groups_layout.addWidget(groupsLabel)
        groups_layout.insertSpacing(1, 10)

        # Create buttons to view available groups
        for i in range(len(GROUP_LIST)):
            single_group_layout = QHBoxLayout()

            # Button with title
            button_group_name = QPushButton(GROUP_LIST[i][0])
            button_group_name.clicked.connect(lambda x, i=i : self.group_button_press(i))
            button_group_name.setStyleSheet('background-color : #D8BFD8; font-weight: 600; border-radius : 5; padding: 5 0')

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
        addNewGroupButton = StyledPushButton("New Group", 150, "#D7C3C1", 14)
        addNewGroupButton.clicked.connect(self.add_new_group)
        groups_layout.addWidget(addNewGroupButton, alignment=Qt.AlignmentFlag.AlignLeft)

        placeholderGroups.setLayout(groups_layout)
            


        # FUNCTIONAL AREA 4 - Categories section
        placeholderCategories = QWidget()
        categoriesGridLayout = QGridLayout()

        # Add title to Categories section
        categories_title_layout = QHBoxLayout()
        categoriesTitle = QLabel("Categories")
        categoriesTitle.setFont(QFont('Futura', 18))

        # Button to view all categories
        openAllCategoriesButton = StyledPushButton("All Categories", 150, "#DEB887", 16)
        openAllCategoriesButton.clicked.connect(self.open_all_categories)

        # Add categories label andd button to the view
        categories_title_layout.addWidget(categoriesTitle)
        categories_title_layout.addWidget(openAllCategoriesButton)
        categoriesGridLayout.addLayout(categories_title_layout, 0, 0, 1, 5)

        # Create buttons with categories
        for i in range(len(CATEGORIES_LIST)):

            # Categories outer box
            single_category_layout = QVBoxLayout()

            # Category item as a button
            button_name = CATEGORIES_LIST[i][0]+ "\n" + str(CATEGORIES_LIST[i][1])
            category_item_button = QPushButton(button_name)
            category_item_button.setStyleSheet('background-color : #FFEBCD; color: #2A3036; font-weight: 600; border-radius : 5; padding: 8 0')
            category_item_button.setFont(QFont('Futura', 16))

            category_item_button.clicked.connect(lambda x, i=i : self.category_button_press(i))
            
            # Add items to category box and align them
            single_category_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            single_category_layout.addWidget(category_item_button)
            categoriesGridLayout.addLayout(single_category_layout, (i// 5) + 1, i % 5, 1, 1)

        placeholderCategories.setLayout(categoriesGridLayout)



        # FUNCTIONAL AREA 5 - Bar chart and pie chart section
        placeholderBarChart = QWidget()
        placeholderBarChart.setStyleSheet('background-color: #F0F8FF')

        charts_area_layout = QGridLayout()

        # Create stacked bar chart with excpenses for the last 6 months
        stacked_bar_chart = StackedBarChart()
        charts_area_layout.addWidget(stacked_bar_chart, 0, 0, 1, 4)

        # Create donut chart with monthly limit
        current_month_donut_chart = DonutChart()
        charts_area_layout.addWidget(current_month_donut_chart, 0, 4, 1, 2)

        placeholderBarChart.setLayout(charts_area_layout)

        
        # Add 5 FUNCTIONAL AREAS to the layout
        main_layout.addWidget(greetingWithCalender, 0, 0, 1, 4)
        main_layout.addWidget(placeholderBarChart, 1, 0, 3, 4)
        main_layout.addWidget(placeholderCategories, 4, 0, 2, 4)
        main_layout.addWidget(placeholderAddButtons, 0, 4, 2, 2)
        main_layout.addWidget(placeholderGroups, 2, 4, 4, 2)

        self.setLayout(main_layout)


    # FUNCTION AREA 1 methods  

    # Open a window with calender view 
    def open_calender(self):
        print("Calender clicked")

    # change monthly budget (limit)
    def change_limit(self):
        print("Change limit button clicked")

    # FUNCTION AREA 2 methods 

    # Open a window with add income view
    def open_add_income(self):
        print("Add Income Button clicked")

    # Open a window with add expense view
    def open_add_expense(self):
        print("Add Expense Button clicked")

    # Open a window with upload file view
    def open_upload_expense(self):
        print("Upload expense Button clicked")

    
    # FUNCTION AREA 3 methods 

    # Should open a window with selection of the expences related to some group
    def group_button_press(self, i):
        print(str(i) + " was pressed") 

    # Should open a list of all transactions and allow user to put checkmark near some to add them to group
    def add_new_group(self):
        print("Add New Group Button pressed")


    # FUNCTION AREA 4 methods
      
    # Should open a window with selection of the expences related to some category
    def category_button_press(self, i):
        print((str(i) + " was pressed"))

    def open_all_categories(self):
        print("View All Categories button pressed")

    


# CREATE A LIST OF TOP 5 EXPENCE CATEGORIES per last 6 month and reverse month
class StackedBarChart(QMainWindow):
    def __init__(self):
        super().__init__()
        self.series = QStackedBarSeries()


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
    def __init__(self):
        super().__init__()
        # Make a pie chart with a hole
        self.series = QPieSeries()
        self.series.setHoleSize(0.4)

        # Create donut slices with data
        self.slice1 = self.series.append("Spent", THIS_MONTH_EXPENSES)
        self.slice1.setBrush(QBrush(QColor(252, 188, 181, 200)))
        self.slice2 = self.series.append(str(THIS_MONTH_EXPENSES), MONTHLY_LIMIT - THIS_MONTH_EXPENSES)
        self.slice2.setBrush(QBrush(QColor(240, 248, 255, 200)))

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
        

