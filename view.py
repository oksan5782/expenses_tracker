
# Import QApplication and all the required widgets from PyQT
from PyQt6 import QtWidgets

from gui_elements.log_in import LogInWindow

import sys
   
def main():
    app = QtWidgets.QApplication(sys.argv)

    # Start with Log In window object
    main_window = LogInWindow()

    #  Show the application's GUI
    main_window.show()

    # Run the application's event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()


