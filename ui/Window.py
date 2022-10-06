from PyQt5.QtWidgets import QMainWindow

from MedRepo import MedRepo
from database.entities.Entity import Question
from ui.MainWindowUI import Ui_MainWindow
from ui.questions_window.AddAnswerDialog import AddAnswerDialog
from ui.questions_window.JumpToAndCicleDialogs import JumpToDialog, SetCircleDialog
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
        self.add_answer_button.clicked.connect(self._add_answer_dialog_show)
        self.set_additional_button.clicked.connect(self._jump_to_dialog_show)
        self.set_circle_button.clicked.connect(self._set_circle_dialog_show)

    def _add_question_show(self):
        AddNewQuestionDialog(self.order, parent=self, after_update_func=self.update_table).exec()

    def _jump_to_dialog_show(self):
        question = self.questions_table.get_selected_question()
        JumpToDialog(question, parent=self).exec()

    def _add_answer_dialog_show(self):
        question = self.questions_table.get_selected_question()
        AddAnswerDialog(question, parent=self).exec()

    def _set_circle_dialog_show(self):
        question = self.questions_table.get_selected_question()
        SetCircleDialog(question, parent=self).exec()

    def _active_change_buttons(self):
        selected_question = self.questions_table.get_selected_question()
        self.change_question_button.setEnabled(True)
        self.set_circle_button.setEnabled(True)
        if selected_question.type_ != Question.TypeAnswer.BOOL.value:
            self.set_additional_button.setEnabled(True)
            self.add_answer_button.setEnabled(True)
        else:
            self.set_additional_button.setEnabled(False)
            self.add_answer_button.setEnabled(False)

    def _change_question(self):
        UpdateQuestionDialog(self.questions_table.get_selected_question(), parent=self,
                             after_save_func=self.update_table).exec()

    def update_table(self):
        self.order = self.med_repo.get_count_questions()
        self.questions = self.med_repo.get_questions()
        self._add_question_to_table(self.questions)

    def _add_question_to_table(self, question_list: list[Question]):
        self.questions_table.fill(question_list)
