# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/qt/move_question.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MoveDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(402, 121)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.question_groupbox = QtWidgets.QGroupBox(Dialog)
        self.question_groupbox.setObjectName("question_groupbox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.question_groupbox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.question_groupbox)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.questions_combobox = QtWidgets.QComboBox(self.question_groupbox)
        self.questions_combobox.setObjectName("questions_combobox")
        self.horizontalLayout_2.addWidget(self.questions_combobox)
        self.verticalLayout.addWidget(self.question_groupbox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.move_button = QtWidgets.QPushButton(Dialog)
        self.move_button.setObjectName("move_button")
        self.horizontalLayout.addWidget(self.move_button)
        self.cancel_button = QtWidgets.QPushButton(Dialog)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout.addWidget(self.cancel_button)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Move"))
        self.question_groupbox.setTitle(_translate("Dialog", "Вопрос"))
        self.label.setText(_translate("Dialog", "Установить после"))
        self.move_button.setText(_translate("Dialog", "Установить"))
        self.cancel_button.setText(_translate("Dialog", "Отмена"))
