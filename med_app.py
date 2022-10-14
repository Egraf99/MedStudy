import sys
import traceback

from PyQt5.QtWidgets import QApplication

from ui.admin.Window import Window


def main():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print(tb)
    write_exception_in_file(tb)
    # QtWidgets.QApplication.quit()             # !!! если вы хотите, чтобы событие завершилось


def write_exception_in_file(text):
    file = open('error.txt', 'w')
    file.write(text)
    file.close()


sys.excepthook = excepthook

if __name__ == '__main__':
    main()
