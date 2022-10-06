from PyQt5 import QtCore
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
            self.single_answer_radioButton.setChecked(True)

    def _update_measure(self, m: str):
        self.measure_lineEdit.setText(m)

    def _update_answers(self, list_answers: list[Answer]):
        if not list_answers: return
        for answer in list_answers:
            self.answers_list.addItem(answer.name)

    def _connection_signal_slot(self):
        self.add_answer_button.clicked.connect(lambda: self.add_new_answer(self.add_answer_lineEdit.text()))
        self.delete_answer_button.clicked.connect(self.delete_answer_from_list)

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
            self.answers_list.takeItem(self.answers_list.row(item))
