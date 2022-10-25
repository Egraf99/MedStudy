from PyQt5.QtWidgets import QMainWindow

from MedRepo import MedRepo
from database.entities.Entity import Question
from ui.admin.MainWindowUI import Ui_MainWindow
from ui.admin.questions_window.AddAnswerDialog import AddAnswerDialog
from ui.admin.questions_window.JumpToAndCicleDialogs import JumpToDialog, SetCircleDialog
from ui.admin.questions_window.QuestionDialogs import AddNewQuestionDialog, UpdateQuestionDialog


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.med_repo = MedRepo()
        self.update_table()
        self.connection_signal_slot()
        try:
            self.old_question_id = self.med_repo.get_questions()[-1].id_
        except IndexError:
            self.old_question_id = -1

    def connection_signal_slot(self):
        self.new_question_button.clicked.connect(self._add_question_show)
        self.questions_table.cellPressed.connect(self._active_change_buttons)
        self.change_question_button.clicked.connect(self._change_question)
        self.add_answer_button.clicked.connect(self._add_answer_dialog_show)
        self.set_branch_button.clicked.connect(self._set_circle_dialog_show)

    def _add_question_show(self):
        AddNewQuestionDialog(parent=self, after_save_func=self.after_add_question).exec()

    def _jump_to_dialog_show(self):
        question = self.questions_table.get_selected_question()
        JumpToDialog(question, parent=self).exec()

    def _add_answer_dialog_show(self):
        question_id = self.questions_table.get_selected_question_id()
        question = self.med_repo.get_question_by_id(question_id)
        AddAnswerDialog(question, parent=self).exec()

    def _set_circle_dialog_show(self):
        question_id = self.questions_table.get_selected_question_id()
        question = self.med_repo.get_question_by_id(question_id)
        SetCircleDialog(question, parent=self).exec()

    def _active_change_buttons(self):
        selected_question = self.med_repo.get_question_by_id(self.questions_table.get_selected_question_id())
        self.change_question_button.setEnabled(True)
        self.set_branch_button.setEnabled(True)
        if selected_question.type_ in [Question.TypeAnswer.SINGLE.value, Question.TypeAnswer.MANY.value]:
            self.add_answer_button.setEnabled(True)
        else:
            self.add_answer_button.setEnabled(False)

    def _change_question(self):
        UpdateQuestionDialog(self.questions_table.get_selected_question_id(), parent=self,
                             after_update_func=self.update_table).exec()

    def after_add_question(self, new_question_id: int):
        self.med_repo.update_next_question(self.old_question_id, new_question_id)
        self.old_question_id = new_question_id
        self.update_table()

    def update_table(self):
        self._add_question_to_table(self.med_repo.get_questions())

    def _add_question_to_table(self, question_list: list[Question]):
        self.questions_table.fill(question_list)
