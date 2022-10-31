from PyQt5.QtWidgets import QDialog

from MedRepo import MedRepo
from database.entities.Entity import Question
from ui.admin.questions_window.MoveQuestionDialog import MoveQuestionDialog
from ui.admin.questions_window.QuestionDialogUI import Ui_Dialog


class QuestionDialog(QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.med_repo = MedRepo()
        self._connection_signal_slot()

    def _connection_signal_slot(self):
        self.saveAndCloseButtonsBox.accepted.connect(self.save_question)

    def save_question(self):
        pass

    def _take_question_name(self) -> str:
        return self.question_lineEdit.text().strip()

    def _take_short_name(self) -> str:
        return self.short_question_lineEdit.text().strip()

    def _take_measure(self) -> str:
        return self.measure_lineEdit.text().strip()

    def _take_question_type(self) -> int:
        type_ = Question.TypeAnswer.BOOL.value
        if self.bool_answer_radioButton.isChecked():
            type_ = Question.TypeAnswer.BOOL.value
        elif self.single_answer_radioButton.isChecked():
            type_ = Question.TypeAnswer.SINGLE.value
        elif self.many_answer_radioButton.isChecked():
            type_ = Question.TypeAnswer.MANY.value
        elif self.int_answer_radio_Button.isChecked():
            type_ = Question.TypeAnswer.INTEGER.value
        elif self.float_answer_radioButton.isChecked():
            type_ = Question.TypeAnswer.FLOAT.value
        elif self.text_answer_radioButton.isChecked():
            type_ = Question.TypeAnswer.TEXT.value

        return type_

    def _create_question(self) -> Question:
        return Question(
            name=self._take_question_name(),
            short=self._take_short_name(),
            type_=self._take_question_type(),
            measure=self._take_measure(),
            require=self._take_require(),
            private=self._take_private(),
        )

    def _take_require(self) -> bool:
        return self.require_checkBox.isChecked()

    def _take_private(self) -> bool:
        return self.private_checkBox.isChecked()

    def _set_question_bool(self):
        self.bool_answer_radioButton.setChecked(True)

    def _set_question_single(self):
        self.single_answer_radioButton.setChecked(True)

    def _set_question_many(self):
        self.many_answer_radioButton.setChecked(True)

    def _set_question_integer(self):
        self.int_answer_radio_Button.setChecked(True)

    def _set_question_float(self):
        self.float_answer_radioButton.setChecked(True)

    def _set_question_text(self):
        self.text_answer_radioButton.setChecked(True)

    def _set_question_name(self, name: str):
        self.question_lineEdit.setText(name)

    def _set_short_name(self, short: str):
        self.short_question_lineEdit.setText(short)

    def _set_measure(self, measure: str):
        if self._take_question_type() != 0:
            self.measure_lineEdit.setText(measure)

    def _set_require(self, require: bool):
        self.require_checkBox.setChecked(require)

    def _set_private(self, private: bool):
        self.private_checkBox.setChecked(private)


class AddNewQuestionDialog(QuestionDialog):
    def __init__(self, after_save_func=None, parent=None):
        super().__init__(parent)
        self.after_save_func = after_save_func

    def save_question(self):
        question = self._create_question()
        self.med_repo.insert_question(question)
        self.after_save_func(self.med_repo.get_question_id_by_name(question.name))


class UpdateQuestionDialog(QuestionDialog):
    def __init__(self, question_id: int, after_update_func=None, parent=None):
        super().__init__(parent)
        self.after_update_func = after_update_func
        self.set_change_buttons()
        self.old_question = self.med_repo.get_question_by_id(question_id)
        self.set_values(self.old_question)
        self.update_question_name(self.old_question.name)

    def update_question_name(self, name: str):
        self.question_groupBox.setTitle(f"Вопрос: {name}")

    def _connection_signal_slot(self):
        super()._connection_signal_slot()
        self.move_button.clicked.connect(self._move_question_dialog_show)
        self.delete_button.clicked.connect(self._delete_button_clicked)

    def _move_question_dialog_show(self):
        MoveQuestionDialog(self.old_question.id_).exec()

    def _delete_button_clicked(self):
        self.med_repo.delete_question(self.old_question.id_)
        self.after_update_func()
        self.reject()

    def save_question(self):
        question = self._create_question()
        question.id_ = self.med_repo.get_question_id_by_name(self.old_question.name)
        if question.type_ != self.old_question.type_:
            self.med_repo.update_question_type(question, question.type_)
        self.med_repo.update_question(question)
        self.after_update_func()

    def set_values(self, question: Question):
        self._set_question_name(question.name)
        self._set_short_name(question.short)
        if question.type_ == Question.TypeAnswer.BOOL.value:
            self._set_question_bool()
        elif question.type_ == Question.TypeAnswer.SINGLE.value:
            self._set_question_single()
        elif question.type_ == Question.TypeAnswer.MANY.value:
            self._set_question_many()
        elif question.type_ == Question.TypeAnswer.INTEGER.value:
            self._set_question_integer()
        elif question.type_ == Question.TypeAnswer.FLOAT.value:
            self._set_question_float()
        elif question.type_ == Question.TypeAnswer.TEXT.value:
            self._set_question_text()
        self._set_measure(question.measure)
        self._set_private(question.private_bool)
        self._set_require(question.require_bool)
