
# Import QApplication and all the required widgets from PyQT
from PyQt6 import QtCore, QtGui, QtWidgets
# import custom components 
from gui_elements.main_window import MainScreen
import sys

       
def main():
    app = QtWidgets.QApplication(sys.argv)

    mainWindow = MainScreen()
    #  Show the application's GUI
    mainWindow.show()
    # Run the application's event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()



