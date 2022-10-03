from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow

from MedRepo import MedRepo
from database.entities.Entity import Patient
from ui.ClientWindowUI import Ui_ClientWindow


class ClientWindow(QMainWindow, Ui_ClientWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.med_repo = MedRepo()
        self.patients = self.med_repo.get_patients_name()
        self._add_patients_to_list(self.patients)

    def _add_patients_to_list(self, patients_list: list[Patient]):
        model = QtGui.QStandardItemModel()
        self.patients_list.setModel(model)
        for patient in patients_list:
            item = QtGui.QStandardItem(patient.name)
            model.appendRow(item)
