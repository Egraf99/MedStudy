from PyQt5.QtWidgets import QDialog

from MedRepo import MedRepo
from database.entities.Entity import Question
from ui.questions_window.JumpToDialogUI import Ui_JumpToDialog
from ui.questions_window.SetCircleDialogUI import Ui_SetCircleDialog


class JumpToDialog(Ui_JumpToDialog, QDialog):
    def __init__(self, question: Question, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.med_repo = MedRepo()
        self.question = question
        self._connect_button()
        self._set_question_name(question)
        self._set_answers(self.med_repo.get_enable_answers(question.id_))
        self._set_jump_questions(self.med_repo.get_question_witch_more_than_order(question.order))

    def _set_answers(self, answers_list):
        for answer in answers_list:
            self.answer_comboBox.addItem(answer.name, answer.id_)

    def _set_jump_questions(self, question_list: list[Question]):
        for question in question_list:
            self.jump_comboBox.addItem(f"{question.order}) {question.name}", question.id_)

    def _set_question_name(self, question: Question):
        self.question_comboBox.setTitle(f"{question.order}) {question.name}")

    def _connect_button(self):
        self.saveAndCancelButtonBox.accepted.connect(self._update_jump)

    def _update_jump(self):
        answer_id = self._take_answer_id()
        destination_id = self._take_destination()
        self.med_repo.update_jump(self.question.id_, answer_id, destination_id)

    def _take_answer_id(self) -> int:
        return self.answer_comboBox.currentData()

    def _take_destination(self) -> int:
        return self.jump_comboBox.currentData()


class SetCircleDialog(Ui_SetCircleDialog, QDialog):
    def __init__(self, question: Question, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.med_repo = MedRepo()
        self.question = question
        self._set_question_name(question)
        self._set_start_questions(self.med_repo.get_question_witch_more_than_order(question.order))
        self._set_finish_questions(self.med_repo.get_question_witch_more_than_order(question.order))
        self._connect_buttons()

    def _connect_buttons(self):
        self.saveAndCancelButtonBox.accepted.connect(self._save_circle_in_db)

    def _save_circle_in_db(self):
        start_id = self._take_start_question_id()
        finish_id = self._take_finish_question_id()
        self.med_repo.update_circle(self.question.id_, start_id, finish_id)

    def _take_start_question_id(self) -> int:
        return self.start_comboBox.currentData()

    def _take_finish_question_id(self) -> int:
        return self.finish_comboBox.currentData()

    def _set_question_name(self, question: Question):
        self.question_comboBox.setTitle(f"{question.order}) {question.name}")

    def _set_start_questions(self, list_questions: list[Question]):
        for question in list_questions:
            self.start_comboBox.addItem(f"{question.order}) {question.name}", question.id_)

    def _set_finish_questions(self, list_questions: list[Question]):
        for question in list_questions:
            self.finish_comboBox.addItem(f"{question.order}) {question.name}", question.id_)
