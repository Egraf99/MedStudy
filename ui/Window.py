from PyQt5.QtWidgets import QMainWindow, QDialog, QTableWidgetItem

from MedRepo import MedRepo
from database.entities.Entity import Question
from ui.questions_window.QuestionDialogUI import Ui_Dialog
from ui.MainWindow import Ui_MainWindow
from ui.questions_window.QuestionDialogs import AddNewQuestionDialog, UpdateQuestionDialog


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.med_repo = MedRepo()
        self.order = -1
        self.update_table()
        self.connection_signal_slot()
        self.questions = []

    def connection_signal_slot(self):
        self.new_question_button.clicked.connect(self._add_question_show)
        self.questions_table.cellPressed.connect(self._active_change_buttons)
        self.change_question_button.clicked.connect(self._change_question)

    def _add_question_show(self):
        AddNewQuestionDialog(self.order, parent=self, after_save_func=self.update_table).exec()

    def _active_change_buttons(self):
        self.change_question_button.setEnabled(True)
        self.set_additional_button.setEnabled(True)
        self.set_cicle_button.setEnabled(True)

    def _change_question(self):
        UpdateQuestionDialog(self.questions_table.get_selected_question_order(), parent=self, after_save_func=self.update_table).exec()

    def update_table(self):
        self.order = self.med_repo.get_count_questions()
        self.questions = self.med_repo.get_questions()
        self._add_question_to_table(self.questions)

    def _add_question_to_table(self, question_list: list[Question]):
        self.questions_table.fill(question_list)
