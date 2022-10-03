import sys
import traceback

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from ui.ClientWindow import ClientWindow
from ui.Window import Window


def main():
    app = QApplication(sys.argv)
    win = ClientWindow()
    win.show()
    sys.exit(app.exec())


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(tb)
    QtWidgets.QApplication.quit()             # !!! если вы хотите, чтобы событие завершилось


sys.excepthook = excepthook

if __name__ == '__main__':
    main()
