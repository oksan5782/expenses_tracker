
# Import QApplication and all the required widgets from PyQT
from PyQt6 import QtCore, QtGui, QtWidgets
# import custom components 
from gui_elements.main_window import MainScreen
from gui_elements.log_in import LogInWindow
from gui_elements.register import RegisterWindow
from gui_elements.change_limit import ChangeLimitWindow
from gui_elements.add_income import AddIncomeWindow
from gui_elements.add_expense import AddExpenseWindow

import sys
   
def main():
    app = QtWidgets.QApplication(sys.argv)

    main_window = AddExpenseWindow()
    # main_window = AddIncomeWindow()
    # main_window = ChangeLimitWindow()
    # main_window = RegisterWindow()
    # main_window = LogInWindow()
    # main_window = MainScreen()
    #  Show the application's GUI
    main_window.show()
    # Run the application's event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()



