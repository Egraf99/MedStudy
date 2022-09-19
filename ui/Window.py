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
        self.connection_signal_slot()

    def connection_signal_slot(self):
        self.add_answer_button.clicked.connect(self.add_new_answer)
        self.delete_answer_button.clicked.connect(self.delete_answer_from_list)

    def add_new_answer(self):
        self.answers_list.addItem(self.add_answer_lineEdit.text())
        self.add_answer_lineEdit.clear()

    def delete_answer_from_list(self):
        listItems = self.answers_list.selectedItems()
        if not listItems: return
        for item in listItems:
            self.answers_list.takeItem(self.answers_list.row(item))
