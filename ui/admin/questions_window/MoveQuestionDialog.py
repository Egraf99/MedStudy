from PyQt5.QtWidgets import QDialog

from MedRepo import MedRepo
from ui.admin.questions_window.JumpToAndCicleDialogs import set_new_items_to_combobox
from ui.admin.questions_window.MoveQuestionDialogUI import Ui_MoveDialog


class MoveQuestionDialog(QDialog, Ui_MoveDialog):
    def __init__(self, question_id: int, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._med_repo = MedRepo()
        self.question = self._med_repo.get_question_by_id(question_id)
        self._update_question_title(self.question.name)
        self.other_questions = self._med_repo.get_questions()
        set_new_items_to_combobox(self.questions_combobox, self.other_questions)
        self._connected_buttons()

    def _update_question_title(self, title: str):
        self.question_groupbox.setTitle(title)

    def _connected_buttons(self):
        self.cancel_button.clicked.connect(self.close)
        self.move_button.clicked.connect(self._set_move)

    def _get_prev_question(self):
        return self.questions_combobox.currentData()

    def _set_move(self):
        prev_question_id = self._get_prev_question()
        if self.question.id_ == prev_question_id: return
        self._med_repo.set_prev_question(prev_question_id, self.question)
        self.close()

