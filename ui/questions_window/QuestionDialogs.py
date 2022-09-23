from PyQt5.QtWidgets import QDialog

from MedRepo import MedRepo
from database.entities.Entity import Question
from ui.questions_window.QuestionDialogUI import Ui_Dialog


class QuestionDialog(QDialog, Ui_Dialog):
    def __init__(self, number: int, after_save_func=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.number = number
        self.update_number(self.number)
        if after_save_func:
            self._after_save_func = after_save_func
        self.med_repo = MedRepo()
        self.connection_signal_slot()

    def update_number(self, number: int):
        self.question_groupBox.setTitle(f"Вопрос {number}")

    def connection_signal_slot(self):
        self.add_answer_button.clicked.connect(self.add_new_answer)
        self.delete_answer_button.clicked.connect(self.delete_answer_from_list)
        self.saveAndCloseButtonsBox.accepted.connect(self.save_button_clicked)

    def save_button_clicked(self):
        self._after_save_func()

    def add_new_answer(self):
        self.answers_list.addItem(self.add_answer_lineEdit.text())
        self.add_answer_lineEdit.clear()

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

    def _take_question_have_bool_answer(self) -> bool:
        return self.bool_answer_radioButton.isChecked()

    def _take_question_have_single_answer(self) -> bool:
        return self.single_answer_radioButton.isChecked()

    def _take_question_have_many_answer(self) -> bool:
        return self.many_answer_radioButton.isChecked()

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
        if self._take_question_have_bool_answer(): return
        self.measure_lineEdit.setText(measure)

    def _set_all_answers(self, answers: list[str]):
        for answer in answers:
            self.answers_list.addItem(answer)

    def _set_require(self, require: bool):
        self.require_checkBox.setChecked(require)

    def _set_private(self, private: bool):
        self.private_checkBox.setChecked(private)


class AddNewQuestionDialog(QuestionDialog):
    def save_button_clicked(self):
        super(AddNewQuestionDialog, self).save_button_clicked()
        self.save_question()

    def save_question(self):
        name: str = self._take_question_name()
        short: str = self._take_short_name()
        private: bool = self._take_private()
        require: bool = self._take_require()
        question = Question(
            name=name,
            short=short,
            require=require,
            private=private,
            order=self.number
        )

        bool_answer: bool = self._take_question_have_bool_answer()
        if not bool_answer:
            measure = self._take_measure()
            single_answer: bool = self._take_question_have_single_answer()
            if not single_answer:
                all_answers = self._take_all_answers()
                question.set_type(Question.TypeAnswer.MANY, measure, all_answers)
            else:
                question.set_type(Question.TypeAnswer.SINGLE, measure)

        self.med_repo.insert_question(question)
        self._after_save_func()


class UpdateQuestionDialog(QuestionDialog):
    def __init__(self, question: Question, after_save_func=None, parent=None):
        super().__init__(question.order, after_save_func, parent)
        self.question = question
        self.set_values(question)

    def set_values(self, question: Question):
        self._set_question_name(question.name)
        self._set_short_name(question.short)
        if question.type_ == Question.TypeAnswer.BOOL:
            self._set_question_bool()
        elif question.type_ == Question.TypeAnswer.SINGLE:
            self._set_question_single()
        elif question.type_ == Question.TypeAnswer.MANY:
            self._set_question_many()
        self._set_measure(question.measure)
        self._set_private(question.private_bool)
        self._set_require(question.require_bool)
