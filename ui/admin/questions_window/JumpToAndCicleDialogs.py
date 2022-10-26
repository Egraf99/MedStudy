from typing import Any, Union, Tuple, List

from PyQt5.QtWidgets import QDialog, QComboBox

from MedRepo import MedRepo
from database.entities.Entity import Question, Answer, NoAnswer
from ui.admin.questions_window.SetCircleDialogUI import Ui_SetCircleDialog


def _get_answer(d: dict[Answer, list[bool, list[Question]]], answer_id: int) -> list[bool, list[Question]]:
    """Return list with answer, where key is given key."""
    for k, v in d.items():
        if answer_id is None:
            return d.get(NoAnswer, list())
        if answer_id == k.id_:
            return v
    return list()


def set_new_items_to_combobox(combobox: QComboBox, list_questions: list[Question], enable: bool = True):
    combobox.clear()
    for question in list_questions:
        combobox.addItem(question.name, question.id_)
    combobox.setEnabled(enable)


class SetCircleDialog(Ui_SetCircleDialog, QDialog):
    def __init__(self, question: Question, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.med_repo = MedRepo()
        self.question = question
        self._update_next_questions()
        self._set_question_title(question.name)
        self._set_answers(question.type_, (self.answers_branch.keys()))
        self._set_cycle(question.type_)
        self._set_choose_questions()
        self._connect_buttons()

    def _update_next_questions(self):
        next_questions = self.med_repo.get_jump(self.question.id_)
        self.basic_block = next_questions.pop("basic_block")
        self.answers_branch = next_questions

    def _set_answers(self, question_type: int, answers_list: list[Answer]):
        # если вопрос числовой, то в блокируем поле ответов для выбора
        if question_type in [Question.TypeAnswer.INTEGER.value,
                             Question.TypeAnswer.FLOAT.value,
                             Question.TypeAnswer.TEXT.value]:
            self.answer_label.setText("При ответе пользователя")
            self.answer_combo_box.setEnabled(False)

        else:
            for answer in answers_list:
                self.answer_combo_box.addItem(answer.name, answer.id_)

    def _set_cycle(self, question_type: int):
        if question_type == Question.TypeAnswer.INTEGER.value:
            self.cycle_check_box.setEnabled(True)
        else:
            self.cycle_check_box.setEnabled(False)

    def _connect_buttons(self):
        self.answer_combo_box.currentIndexChanged.connect(self._set_choose_questions)
        self.start_comboBox.currentIndexChanged.connect(
            lambda: self._update_finish_combobox(self.start_comboBox.currentData()))
        self.deleteBranch_button.clicked.connect(self._delete_branch)
        self.save_button.clicked.connect(self._save_circle_in_db)
        self.cancel_button.clicked.connect(self.close)

    def _update_ui(self):
        self._update_next_questions()
        self._set_choose_questions()

    def _delete_branch(self):
        answer_id = self._take_answer_id()
        self.med_repo.delete_branch(self.question, answer_id)
        self._update_ui()

    def _update_finish_combobox(self, question_id: int):
        if question_id is None: return
        set_new_items_to_combobox(self.finish_comboBox, self.med_repo.get_next_questions(question_id))

    def _save_circle_in_db(self):
        answer_id = self._take_answer_id()
        start_id = self._take_start_question_id()
        finish_id = self._take_finish_question_id()
        cycle = int(self.cycle_check_box.isChecked())
        self.med_repo.update_cycle(self.question.id_, answer_id, start_id, finish_id, cycle)
        self._update_ui()

    def _take_answer_id(self) -> int:
        return self.answer_combo_box.currentData()

    def _take_start_question_id(self) -> int:
        return self.start_comboBox.currentData()

    def _take_finish_question_id(self) -> int:
        return self.finish_comboBox.currentData()

    def _set_question_title(self, title: str):
        self.question_comboBox.setTitle(title)

    def _set_choose_questions(self):
        """Выставляет доступные для ветвления вопросы
          или показывает уже используемое ветвление для выбранного ответа
         (или для всего вопроса, если доступных ответов нет)."""
        choose_answer = self._take_answer_id()
        self.question_list = _get_answer(self.answers_branch, choose_answer)
        if len(self.question_list) == 0 or len(self.question_list[1]) == 0:
            # нет доступных ответов или нет ветвлений от выбранного ответа
            set_new_items_to_combobox(self.start_comboBox, self.basic_block[1], enable=True)
            set_new_items_to_combobox(self.finish_comboBox, self.basic_block[1], enable=True)
            self.save_button.setEnabled(True)
            self.deleteBranch_button.setEnabled(False)
        elif len(self.question_list) != 0:
            # есть ветвление от выбранного ответа
            set_new_items_to_combobox(self.start_comboBox, [self.question_list[1][0]], enable=False)
            set_new_items_to_combobox(self.finish_comboBox, [self.question_list[1][-1]], enable=False)
            self.save_button.setEnabled(False)
            self.deleteBranch_button.setEnabled(True)
