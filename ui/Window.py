from PyQt5.QtWidgets import QMainWindow, QDialog, QTableWidgetItem

from MedRepo import MedRepo
from database.entities.Entity import Question
from ui.AddQuestionDialog import Ui_Dialog
from ui.MainWindow import Ui_MainWindow


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.med_repo = MedRepo()
        self.order = -1
        self.update_table()
        self.connection_signal_slot()
        self.questions = []

    def connection_signal_slot(self):
        self.new_question_button.clicked.connect(self._add_question_show)
        self.questions_table.cellPressed.connect(self._active_change_buttons)

    def _add_question_show(self):
        AddNewQuestionDialog(self.order, parent=self, after_save_func=self.update_table).exec()

    def _active_change_buttons(self):
        self.change_question_button.setEnabled(True)
        self.set_additional_button.setEnabled(True)
        self.set_cicle_button.setEnabled(True)

    def update_table(self):
        self.order = self.med_repo.get_count_questions()
        self.questions = self.med_repo.get_questions()
        self._add_question_to_table(self.questions)

    def _add_question_to_table(self, question_list: list[Question]):
        self.questions_table.setRowCount(0)
        for question in question_list:
            row = self.questions_table.rowCount()
            self.questions_table.insertRow(row)
            self.questions_table.setItem(row, 0, QTableWidgetItem(question.name))
            self.questions_table.setItem(row, 1, QTableWidgetItem(question.short))
            self.questions_table.setItem(row, 2, QTableWidgetItem(str(question.order)))


class AddNewQuestionDialog(QDialog, Ui_Dialog):
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
        self.saveAndCloseButtonsBox.accepted.connect(self.save_question)

    def add_new_answer(self):
        self.answers_list.addItem(self.add_answer_lineEdit.text())
        self.add_answer_lineEdit.clear()

    def delete_answer_from_list(self):
        listItems = self.answers_list.selectedItems()
        if not listItems: return
        for item in listItems:
            self.answers_list.takeItem(self.answers_list.row(item))

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

    def _take_require(self) -> bool:
        return self.require_checkBox.isChecked()

    def _take_private(self) -> bool:
        return self.private_checkBox.isChecked()

    def _take_all_answers(self) -> list[str]:
        qlist = self.answers_list
        answers = [qlist.item(x).text() for x in range(qlist.count())]
        return answers
