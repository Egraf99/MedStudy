from PyQt5.QtWidgets import QDialog

from MedRepo import MedRepo
from database.entities.Entity import Question, Answer
from ui.admin.questions_window.SetCircleDialogUI import Ui_SetCircleDialog


class SetCircleDialog(Ui_SetCircleDialog, QDialog):
    def __init__(self, question: Question, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.med_repo = MedRepo()
        self.question = question
        self._set_question_name(question)
        self._set_answers(question.type_, self.med_repo.get_enable_answers(question.id_))
        self._set_cycle(question.type_)
        self.next_questions = self.med_repo.get_jump(question.id_)
        print(self.next_questions)
        self._set_start_questions(self.next_questions["basic_block"][1])
        self._set_finish_questions(self.next_questions["basic_block"][1])
        self._connect_buttons()

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
        self.saveAndCancelButtonBox.accepted.connect(self._save_circle_in_db)

    def _save_circle_in_db(self):
        answer_id = self._take_answer_id()
        start_id = self._take_start_question_id()
        finish_id = self._take_finish_question_id()
        cycle = int(self.cycle_check_box.isChecked())
        self.med_repo.update_cycle(self.question.id_, answer_id, start_id, finish_id, cycle)

    def _take_answer_id(self) -> int:
        return self.answer_combo_box.currentData()

    def _take_start_question_id(self) -> int:
        return self.start_comboBox.currentData()

    def _take_finish_question_id(self) -> int:
        return self.finish_comboBox.currentData()

    def _set_question_name(self, question: Question):
        self.question_comboBox.setTitle(question.name)

    def _set_start_questions(self, list_questions: list[Question]):
        for question in list_questions:
            self.start_comboBox.addItem(question.name, question.id_)

    def _set_finish_questions(self, list_questions: list[Question]):
        for question in list_questions:
            self.finish_comboBox.addItem(question.name, question.id_)
