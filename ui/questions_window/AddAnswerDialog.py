from PyQt5 import QtCore, QtGui, Qt
from PyQt5.QtWidgets import QDialog, QListWidgetItem

from MedRepo import MedRepo
from database.entities.Entity import Question, Answer
from ui.questions_window.AddAnswersDialogUI import Ui_AddAnswerDialog


class AddAnswerDialog(Ui_AddAnswerDialog, QDialog):
    def __init__(self, question: Question, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.med_repo = MedRepo()
        self.question = question
        self._update_question(question)
        self._connection_signal_slot()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.type() == 6:
            return
        super(AddAnswerDialog, self).keyPressEvent(event)

    def _update_question(self, question: Question):
        self._update_name(question.name)
        self._update_type(question.type_)
        self._update_measure(question.measure)
        self._update_answers(self.med_repo.get_enable_answers(question.id_))

    def _update_name(self, s: str):
        self.answerGroupBox.setTitle(s)

    def _update_type(self, t: int):
        if t == Question.TypeAnswer.BOOL.value:
            self.bool_answer_radioButton.setChecked(True)
        elif t == Question.TypeAnswer.SINGLE.value:
            self.single_answer_radioButton.setChecked(True)
        elif t == Question.TypeAnswer.MANY.value:
            self.many_answer_radioButton.setChecked(True)

    def _update_measure(self, m: str):
        self.measure_lineEdit.setText(m)

    def _update_answers(self, list_answers: list[Answer]):
        if not list_answers: return
        for answer in list_answers:
            item = QListWidgetItem(answer.name)
            item.setData(QtCore.Qt.UserRole, answer.id_)
            self.answers_list.addItem(item)

    def _connection_signal_slot(self):
        self.add_answer_button.clicked.connect(lambda: self.add_new_answer(self.add_answer_lineEdit.text()))
        self.delete_answer_button.clicked.connect(self.delete_answer_from_list)
        self.buttonBox.accepted.connect(self._save_type_and_measure_question)

    def _save_type_and_measure_question(self):
        self.question.type_ = self._take_question_type()
        self.question.measure = self._take_measure()
        self.med_repo.update_question(self.question)

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

        return type_

    def add_new_answer(self, answer: str):
        if answer == "": return
        answer_id = self.med_repo.add_answer_to_question(answer, self.question.id_)
        item = QListWidgetItem(answer)
        item.setData(QtCore.Qt.UserRole, answer_id)
        self.answers_list.addItem(item)
        self.add_answer_lineEdit.clear()

    def delete_answer_from_list(self):
        listItems = self.answers_list.selectedItems()
        if not listItems: return
        for item in listItems:
            answer_id = int(item.data(QtCore.Qt.UserRole))
            self.med_repo.delete_question_with_answer(self.question.id_, answer_id)
            self.answers_list.takeItem(self.answers_list.row(item))
