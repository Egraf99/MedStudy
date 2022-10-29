# -*- coding: utf-8 -*-
from collections import deque

# Form implementation generated from reading ui file 'ui/qt/main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QColor, QFont

from MedRepo import MedRepo
from database.entities.Entity import Question


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(731, 513)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.new_question_button = QtWidgets.QPushButton(self.centralwidget)
        self.new_question_button.setObjectName("new_question_button")
        self.verticalLayout_2.addWidget(self.new_question_button)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.treeView = QuestionTree(self.centralwidget)
        self.treeView.setHeaderHidden(False)
        self.treeView.setObjectName("treeView")
        self.horizontalLayout.addWidget(self.treeView)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.change_question_button = QtWidgets.QPushButton(self.centralwidget)
        self.change_question_button.setEnabled(False)
        self.change_question_button.setObjectName("change_question_button")
        self.verticalLayout.addWidget(self.change_question_button)
        spacerItem = QtWidgets.QSpacerItem(20, 178, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.add_answer_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_answer_button.setEnabled(False)
        self.add_answer_button.setObjectName("add_answer_button")
        self.verticalLayout.addWidget(self.add_answer_button)
        self.set_branch_button = QtWidgets.QPushButton(self.centralwidget)
        self.set_branch_button.setEnabled(False)
        self.set_branch_button.setObjectName("set_branch_button")
        self.verticalLayout.addWidget(self.set_branch_button)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Med"))
        self.new_question_button.setText(_translate("MainWindow", "Новый вопрос"))
        self.change_question_button.setText(_translate("MainWindow", "Изменить"))
        self.add_answer_button.setText(_translate("MainWindow", "Добавить ответы"))
        self.set_branch_button.setText(_translate("MainWindow", "Добавить ветвление"))


class QuestionTree(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        super(QuestionTree, self).__init__(parent)
        self.med_repo = MedRepo()

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Имя', 'Тип'])
        self.header().setDefaultSectionSize(180)
        self.setModel(self.model)
        self.model.setRowCount(0)
        self.update()
        self.collapseAll()

    def update(self):
        seen = {}

        def place_question_and_next(question_id: int, root=None):
            if root is None:
                root = self.model.invisibleRootItem()

            chain = self.med_repo.get_next_questions(question_id)
            for question in chain:
                qsi = QStandardItem(question.name)
                qsi.setData(question_id, Qt.UserRole)
                root.appendRow([
                    qsi,
                    QStandardItem('вопрос'),
                ])
                seen[question.id_] = root.child(root.rowCount() - 1)

        def place_answer(name: str, root: QStandardItem) -> QStandardItem:
            root.appendRow([
                QStandardItem(name),
                QStandardItem('ответ'),
            ])
            return root.child(root.rowCount() - 1)

        start_question = self.med_repo.get_first_question_in_block(0)
        place_question_and_next(start_question.id_)

        # enable_answers = deque(enable_answers_)

        ea = self.med_repo.get_deque_enable_answers()
        enable_answers = deque(ea)

        while enable_answers:
            ea = enable_answers.popleft()
            root = seen.get(ea.question_id)
            if root is None:
                # нужный вопрос еще не добавлен в дерево
                enable_answers.append(ea)
                continue

            if ea.answer_id is None:
                place_question_and_next(ea.jump_to_question, root)
                continue

            if ea.answer_id is not None:
                answer_root = place_answer(ea.answer_name, root)
                if ea.jump_to_question is not None:
                    place_question_and_next(ea.jump_to_question, answer_root)