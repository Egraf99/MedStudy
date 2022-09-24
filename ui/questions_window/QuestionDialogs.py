from PyQt5.QtWidgets import QDialog

from MedRepo import MedRepo
from database.entities.Entity import Question, Answer
from ui.questions_window.QuestionDialogUI import Ui_Dialog


class QuestionDialog(QDialog, Ui_Dialog):
    def __init__(self, number: int, after_update_func=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.number = number
        self.update_number(self.number)
        if after_update_func:
            self._after_update_func = after_update_func
        self.med_repo = MedRepo()
        self.connection_signal_slot()

    def update_number(self, number: int):
        self.question_groupBox.setTitle(f"Вопрос {number}")

    def connection_signal_slot(self):
        self.add_answer_button.clicked.connect(self.add_new_answer)
        self.delete_answer_button.clicked.connect(self.delete_answer_from_list)
        self.saveAndCloseButtonsBox.accepted.connect(self.save_question)

    def add_new_answer(self):
        self.answers_list.addItem(self.add_answer_lineEdit.text())
        self.add_answer_lineEdit.clear()

    def save_question(self):
        pass

    def after_update_func(self):
        if self._after_update_func: self._after_update_func()

    def delete_answer_from_list(self):
        listItems = self.answers_list.selectedItems()
        if not listItems: return
        for item in listItems:
            self.answers_list.takeItem(self.answers_list.row(item))

    def _take_question_name(self) -> str:
        return self.question_lineEdit.text()

    def _take_short_name(self) -> str:
        return self.short_question_lineEdit.text()

    def _take_measure(self) -> str:
        return self.measure_lineEdit.text()

    def _take_question_type(self) -> int:
        type_ = 0
        if self.bool_answer_radioButton.isChecked():
            type_ = 0
        elif self.single_answer_radioButton.isChecked():
            type_ = 1
        elif self.many_answer_radioButton.isChecked():
            type_ = 2

        return type_

    def _take_require(self) -> bool:
        return self.require_checkBox.isChecked()

    def _take_private(self) -> bool:
        return self.private_checkBox.isChecked()

    def _take_all_answers(self) -> list[str]:
        qlist = self.answers_list
        answers = [qlist.item(x).text() for x in range(qlist.count())]
        return answers

    def _set_question_bool(self):
        self.bool_answer_radioButton.setChecked(True)

    def _set_question_single(self):
        self.single_answer_radioButton.setChecked(True)

    def _set_question_many(self):
        self.many_answer_radioButton.setChecked(True)

    def _set_question_name(self, name: str):
        self.question_lineEdit.setText(name)

    def _set_short_name(self, short: str):
        self.short_question_lineEdit.setText(short)

    def _set_measure(self, measure: str):
        if self._take_question_type() != 0:
            self.measure_lineEdit.setText(measure)

    def _set_enable_answers(self, answers: list[Answer]):
        for answer in answers:
            self.answers_list.addItem(answer.name)

    def _set_require(self, require: bool):
        self.require_checkBox.setChecked(require)

    def _set_private(self, private: bool):
        self.private_checkBox.setChecked(private)


class AddNewQuestionDialog(QuestionDialog):
    def save_question(self):
        type_ = self._take_question_type()
        question = Question(
            name=self._take_question_name(),
            short=self._take_short_name(),
            type_=type_,
            measure=self._take_measure(),
            require=self._take_require(),
            private=self._take_private(),
            order=self.number
        )

        if type_ == 2:
            question.set_enable_answers(self._take_all_answers())

        self.med_repo.insert_question(question)
        self.after_update_func()


class UpdateQuestionDialog(QuestionDialog):
    def __init__(self, question: Question, after_save_func=None, parent=None):
        super().__init__(question.order, after_save_func, parent)
        self.set_delete_button()
        self.old_question = question
        self.set_values(question)

    def connection_signal_slot(self):
        super().connection_signal_slot()
        self.delete_button.clicked.connect(self._delete_button_clicked)

    def _delete_button_clicked(self):
        self.med_repo.delete_question(self.old_question.id_)
        self.after_update_func()
        self.reject()

    def save_question(self):
        type_ = self._take_question_type()
        question = Question(
            name=self._take_question_name(),
            short=self._take_short_name(),
            type_=type_,
            measure=self._take_measure(),
            require=self._take_require(),
            private=self._take_private(),
            order=self.number
        )
        question.id_ = self.med_repo.get_question_id_by_name(self.old_question.name)

        if type_ == 2:
            question.set_enable_answers(self._take_all_answers())

        self.med_repo.update_question(question)
        super().save_question()

    def set_values(self, question: Question):
        self._set_question_name(question.name)
        self._set_short_name(question.short)
        if question.type_ == 0:
            self._set_question_bool()
        elif question.type_ == 1:
            self._set_question_single()
        elif question.type_ == 2:
            self._set_question_many()
        self._set_measure(question.measure)
        self._set_enable_answers(self.med_repo.get_enable_answers(question.id_))
        self._set_private(question.private_bool)
        self._set_require(question.require_bool)
