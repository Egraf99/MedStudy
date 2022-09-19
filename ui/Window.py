from PyQt5.QtWidgets import QMainWindow, QDialog

from MedRepo import MedRepo
from ui.AddQuestionDialog import Ui_Dialog
from ui.MainWindow import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.med_repo = MedRepo()
        self.connection_signal_slot()

    def connection_signal_slot(self):
        self.new_question_button.clicked.connect(self.add_question_show)

    def add_question_show(self):
        AddNewQuestionDialog(self).exec()


class AddNewQuestionDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
