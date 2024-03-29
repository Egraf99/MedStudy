# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_answers.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AddAnswerDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(626, 696)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.answerGroupBox = QtWidgets.QGroupBox(Dialog)
        self.answerGroupBox.setObjectName("answerGroupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.answerGroupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.bool_answer_radioButton = QtWidgets.QRadioButton(self.answerGroupBox)
        self.bool_answer_radioButton.setChecked(True)
        self.bool_answer_radioButton.setObjectName("bool_answer_radioButton")
        self.gridLayout.addWidget(self.bool_answer_radioButton, 0, 0, 1, 1)
        self.int_answer_radio_Button = QtWidgets.QRadioButton(self.answerGroupBox)
        self.int_answer_radio_Button.setObjectName("int_answer_radio_Button")
        self.gridLayout.addWidget(self.int_answer_radio_Button, 0, 1, 1, 1)
        self.text_answer_radioButton = QtWidgets.QRadioButton(self.answerGroupBox)
        self.text_answer_radioButton.setObjectName("text_answer_radioButton")
        self.gridLayout.addWidget(self.text_answer_radioButton, 0, 3, 1, 1)
        self.single_answer_radioButton = QtWidgets.QRadioButton(self.answerGroupBox)
        self.single_answer_radioButton.setObjectName("single_answer_radioButton")
        self.gridLayout.addWidget(self.single_answer_radioButton, 1, 1, 1, 1)
        self.float_answer_radioButton = QtWidgets.QRadioButton(self.answerGroupBox)
        self.float_answer_radioButton.setObjectName("float_answer_radioButton")
        self.gridLayout.addWidget(self.float_answer_radioButton, 0, 2, 1, 1)
        self.many_answer_radioButton = QtWidgets.QRadioButton(self.answerGroupBox)
        self.many_answer_radioButton.setObjectName("many_answer_radioButton")
        self.gridLayout.addWidget(self.many_answer_radioButton, 1, 2, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.answerGroupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.measure_lineEdit = QtWidgets.QLineEdit(self.answerGroupBox)
        self.measure_lineEdit.setEnabled(False)
        self.measure_lineEdit.setObjectName("measure_lineEdit")
        self.horizontalLayout_4.addWidget(self.measure_lineEdit)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.add_answer_button = QtWidgets.QPushButton(self.answerGroupBox)
        self.add_answer_button.setEnabled(False)
        self.add_answer_button.setObjectName("add_answer_button")
        self.gridLayout_3.addWidget(self.add_answer_button, 0, 1, 1, 1)
        self.add_answer_lineEdit = QtWidgets.QLineEdit(self.answerGroupBox)
        self.add_answer_lineEdit.setEnabled(False)
        self.add_answer_lineEdit.setObjectName("add_answer_lineEdit")
        self.gridLayout_3.addWidget(self.add_answer_lineEdit, 0, 0, 1, 1)
        self.answers_list = QtWidgets.QListWidget(self.answerGroupBox)
        self.answers_list.setEnabled(False)
        self.answers_list.setObjectName("answers_list")
        self.gridLayout_3.addWidget(self.answers_list, 1, 0, 1, 1)
        self.delete_answer_button = QtWidgets.QPushButton(self.answerGroupBox)
        self.delete_answer_button.setEnabled(False)
        self.delete_answer_button.setObjectName("delete_answer_button")
        self.gridLayout_3.addWidget(self.delete_answer_button, 1, 1, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_3)
        self.verticalLayout.addWidget(self.answerGroupBox)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.bool_answer_radioButton.toggled['bool'].connect(self.measure_lineEdit.setDisabled) # type: ignore
        self.single_answer_radioButton.toggled['bool'].connect(self.measure_lineEdit.setEnabled) # type: ignore
        self.many_answer_radioButton.toggled['bool'].connect(self.measure_lineEdit.setEnabled) # type: ignore
        self.bool_answer_radioButton.toggled['bool'].connect(self.add_answer_button.setDisabled) # type: ignore
        self.bool_answer_radioButton.toggled['bool'].connect(self.answers_list.setDisabled) # type: ignore
        self.bool_answer_radioButton.toggled['bool'].connect(self.delete_answer_button.setDisabled) # type: ignore
        self.single_answer_radioButton.toggled['bool'].connect(self.add_answer_lineEdit.setEnabled) # type: ignore
        self.single_answer_radioButton.toggled['bool'].connect(self.add_answer_button.setEnabled) # type: ignore
        self.many_answer_radioButton.toggled['bool'].connect(self.add_answer_lineEdit.setEnabled) # type: ignore
        self.many_answer_radioButton.toggled['bool'].connect(self.add_answer_button.setEnabled) # type: ignore
        self.int_answer_radio_Button.toggled['bool'].connect(self.measure_lineEdit.setEnabled) # type: ignore
        self.int_answer_radio_Button.toggled['bool'].connect(self.add_answer_lineEdit.setDisabled) # type: ignore
        self.int_answer_radio_Button.toggled['bool'].connect(self.add_answer_button.setDisabled) # type: ignore
        self.int_answer_radio_Button.toggled['bool'].connect(self.delete_answer_button.setDisabled) # type: ignore
        self.int_answer_radio_Button.toggled['bool'].connect(self.answers_list.setDisabled) # type: ignore
        self.bool_answer_radioButton.toggled['bool'].connect(self.add_answer_lineEdit.setDisabled) # type: ignore
        self.text_answer_radioButton.toggled['bool'].connect(self.measure_lineEdit.setEnabled) # type: ignore
        self.text_answer_radioButton.toggled['bool'].connect(self.add_answer_lineEdit.setDisabled) # type: ignore
        self.text_answer_radioButton.toggled['bool'].connect(self.add_answer_button.setDisabled) # type: ignore
        self.text_answer_radioButton.toggled['bool'].connect(self.answers_list.setDisabled) # type: ignore
        self.text_answer_radioButton.toggled['bool'].connect(self.delete_answer_button.setDisabled) # type: ignore
        self.float_answer_radioButton.toggled['bool'].connect(self.measure_lineEdit.setEnabled) # type: ignore
        self.float_answer_radioButton.toggled['bool'].connect(self.add_answer_lineEdit.setDisabled) # type: ignore
        self.float_answer_radioButton.toggled['bool'].connect(self.answers_list.setDisabled) # type: ignore
        self.float_answer_radioButton.toggled['bool'].connect(self.add_answer_button.setDisabled) # type: ignore
        self.float_answer_radioButton.toggled['bool'].connect(self.delete_answer_button.setDisabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Добавить ответы"))
        self.answerGroupBox.setTitle(_translate("Dialog", "Ответ"))
        self.bool_answer_radioButton.setText(_translate("Dialog", "Да|Нет"))
        self.int_answer_radio_Button.setText(_translate("Dialog", "Числовой ответ"))
        self.text_answer_radioButton.setText(_translate("Dialog", "Текстовый ответ"))
        self.single_answer_radioButton.setText(_translate("Dialog", "Одиночный ответ"))
        self.float_answer_radioButton.setText(_translate("Dialog", "Десятичный ответ"))
        self.many_answer_radioButton.setText(_translate("Dialog", "Множественный ответ"))
        self.label_3.setText(_translate("Dialog", "Ед. измер."))
        self.add_answer_button.setText(_translate("Dialog", "Добавить"))
        self.delete_answer_button.setText(_translate("Dialog", "Удалить"))
