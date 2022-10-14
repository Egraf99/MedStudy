from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem

from MedRepo import MedRepo
from database.entities.Entity import Patient
from ui.ClientWindowUI import Ui_ClientWindow


def get_year_str(year: int) -> str:
    if year % 10 == 1:
        return f"{year} год"
    elif year % 10 in [2, 3, 4]:
        return f"{year} года"
    else:
        return f"{year} лет"


class ClientWindow(QMainWindow, Ui_ClientWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.med_repo = MedRepo()
        self._update_patients(self.med_repo.get_patients_name())
        self._connect_button()

    def _connect_button(self):
        self.patients_list.pressed.connect(lambda: self.delete_patient_button.setEnabled(True))
        self.delete_patient_button.clicked.connect(lambda: self._delete_selected_patient())

    def _delete_selected_patient(self):
        selected_item = self.patients_list.currentItem()
        self._delete_patient(selected_item.data(QtCore.Qt.UserRole))

    def _delete_patient(self, patient_id: int):
        self.med_repo.delete_patient(patient_id)
        self._update_patients(self.med_repo.get_patients_name())

    def _update_patients(self, patients_list: list[Patient]):
        self.patients_list.clear()
        self.patients = patients_list
        for patient in patients_list:
            item = QListWidgetItem(
                f"{patient.name}         {get_year_str(patient.age)}          {'муж.' if patient.male else 'жен.'}"
            )
            item.setData(QtCore.Qt.UserRole, patient.id)
            self.patients_list.addItem(item)
