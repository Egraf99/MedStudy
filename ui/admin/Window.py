from PyQt5.QtWidgets import QMainWindow

from MedRepo import MedRepo
from database.MedDatabase import QuestionNotFoundError
from database.entities.Entity import Question
from ui.admin.MainWindowUI import Ui_MainWindow, SelectNoQuestionError
from ui.admin.questions_window.AddAnswerDialog import AddAnswerDialog
from ui.admin.questions_window.JumpToAndCicleDialogs import SetCircleDialog
from ui.admin.questions_window.QuestionDialogs import AddNewQuestionDialog, UpdateQuestionDialog


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.med_repo = MedRepo()
        self.update_table()
        self.connection_signal_slot()
        self._update_last_question_id()

    def _update_last_question_id(self):
        try:
            self.last_question_id = self.med_repo.get_last_question_in_block(0).id_
        except QuestionNotFoundError:
            self.last_question_id = -1

    def connection_signal_slot(self):
        self.new_question_button.clicked.connect(self._add_question_show)
        self.question_tree.clicked.connect(self._active_change_buttons)
        self.update_tree_button.clicked.connect(self._update_tree)
        self.change_question_button.clicked.connect(self._change_question)
        self.add_answer_button.clicked.connect(self._add_answer_dialog_show)
        self.set_branch_button.clicked.connect(self._set_circle_dialog_show)

    def _update_tree(self):
        self.question_tree.update()
        self._disable_question_buttons()

    def _disable_question_buttons(self):
        self.change_question_button.setEnabled(False)
        self.set_branch_button.setEnabled(False)
        self.add_answer_button.setEnabled(False)

    def _add_question_show(self):
        AddNewQuestionDialog(parent=self, after_save_func=self.after_add_question).exec()

    def _add_answer_dialog_show(self):
        try:
            question_id = self.question_tree.get_selected_question_id()
        except SelectNoQuestionError:
            return
        question = self.med_repo.get_question_by_id(question_id)
        AddAnswerDialog(question, parent=self).exec()

    def _set_circle_dialog_show(self):
        try:
            question_id = self.question_tree.get_selected_question_id()
        except SelectNoQuestionError:
            return
        question = self.med_repo.get_question_by_id(question_id)
        SetCircleDialog(question, parent=self).exec()

    def _active_change_buttons(self):
        try:
            question_id = self.question_tree.get_selected_question_id()
        except SelectNoQuestionError:
            self._disable_question_buttons()
            return

        selected_question = self.med_repo.get_question_by_id(question_id)
        self.change_question_button.setEnabled(True)
        self.set_branch_button.setEnabled(True)
        if selected_question.type_ in [Question.TypeAnswer.SINGLE.value, Question.TypeAnswer.MANY.value]:
            self.add_answer_button.setEnabled(True)
        else:
            self.add_answer_button.setEnabled(False)

    def _change_question(self):
        try:
            question_id = self.question_tree.get_selected_question_id()
        except SelectNoQuestionError:
            return
        UpdateQuestionDialog(question_id, parent=self,
                             after_update_func=self.update_table).exec()

    def after_add_question(self, new_question_id: int):
        self.med_repo.update_next_question(self.last_question_id, new_question_id)
        self._update_last_question_id()
        self.update_table()

    def update_table(self):
        self.question_tree.update()
