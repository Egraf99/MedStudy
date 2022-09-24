# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'first_med.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(665, 718)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setContentsMargins(1, 1, 11, 11)
        self.verticalLayout.setSpacing(7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.question_groupBox = QtWidgets.QGroupBox(self.frame)
        self.question_groupBox.setObjectName("question_groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.question_groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.question_lineEdit = QtWidgets.QLineEdit(self.question_groupBox)
        self.question_lineEdit.setObjectName("question_lineEdit")
        self.verticalLayout_2.addWidget(self.question_lineEdit)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.question_groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.short_question_lineEdit = QtWidgets.QLineEdit(self.question_groupBox)
        self.short_question_lineEdit.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.short_question_lineEdit.setObjectName("short_question_lineEdit")
        self.horizontalLayout_2.addWidget(self.short_question_lineEdit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout_5.addWidget(self.question_groupBox)
        self.groupBox = QtWidgets.QGroupBox(self.frame)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.bool_answer_radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.bool_answer_radioButton.setChecked(True)
        self.bool_answer_radioButton.setObjectName("bool_answer_radioButton")
        self.horizontalLayout.addWidget(self.bool_answer_radioButton)
        self.single_answer_radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.single_answer_radioButton.setObjectName("single_answer_radioButton")
        self.horizontalLayout.addWidget(self.single_answer_radioButton)
        self.many_answer_radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.many_answer_radioButton.setObjectName("many_answer_radioButton")
        self.horizontalLayout.addWidget(self.many_answer_radioButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.measure_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.measure_lineEdit.setEnabled(False)
        self.measure_lineEdit.setObjectName("measure_lineEdit")
        self.horizontalLayout_3.addWidget(self.measure_lineEdit)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.add_answer_button = QtWidgets.QPushButton(self.groupBox)
        self.add_answer_button.setEnabled(False)
        self.add_answer_button.setObjectName("add_answer_button")
        self.gridLayout_2.addWidget(self.add_answer_button, 0, 1, 1, 1)
        self.add_answer_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.add_answer_lineEdit.setEnabled(False)
        self.add_answer_lineEdit.setObjectName("add_answer_lineEdit")
        self.gridLayout_2.addWidget(self.add_answer_lineEdit, 0, 0, 1, 1)
        self.answers_list = QtWidgets.QListWidget(self.groupBox)
        self.answers_list.setEnabled(False)
        self.answers_list.setObjectName("answers_list")
        self.gridLayout_2.addWidget(self.answers_list, 1, 0, 1, 1)
        self.delete_answer_button = QtWidgets.QPushButton(self.groupBox)
        self.delete_answer_button.setEnabled(False)
        self.delete_answer_button.setObjectName("delete_answer_button")
        self.gridLayout_2.addWidget(self.delete_answer_button, 1, 1, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout_2)
        self.verticalLayout_5.addWidget(self.groupBox)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.private_checkBox = QtWidgets.QCheckBox(self.frame)
        self.private_checkBox.setObjectName("private_checkBox")
        self.verticalLayout_4.addWidget(self.private_checkBox)
        self.require_checkBox = QtWidgets.QCheckBox(self.frame)
        self.require_checkBox.setObjectName("require_checkBox")
        self.verticalLayout_4.addWidget(self.require_checkBox)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.gridLayout.addLayout(self.verticalLayout_5, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame)
        self.saveAndCloseButtonsBox = QtWidgets.QDialogButtonBox(Dialog)
        self.saveAndCloseButtonsBox.setOrientation(QtCore.Qt.Horizontal)
        self.saveAndCloseButtonsBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Save)
        self.saveAndCloseButtonsBox.setCenterButtons(False)
        self.saveAndCloseButtonsBox.setObjectName("saveAndCloseButtonsBox")
        self.verticalLayout.addWidget(self.saveAndCloseButtonsBox)

        self.retranslateUi(Dialog)
        self.saveAndCloseButtonsBox.accepted.connect(Dialog.accept) # type: ignore
        self.saveAndCloseButtonsBox.rejected.connect(Dialog.reject) # type: ignore
        self.single_answer_radioButton.toggled['bool'].connect(self.measure_lineEdit.setEnabled) # type: ignore
        self.many_answer_radioButton.toggled['bool'].connect(self.measure_lineEdit.setEnabled) # type: ignore
        self.bool_answer_radioButton.toggled['bool'].connect(self.measure_lineEdit.clear) # type: ignore
        self.many_answer_radioButton.toggled['bool'].connect(self.add_answer_lineEdit.setEnabled) # type: ignore
        self.many_answer_radioButton.toggled['bool'].connect(self.add_answer_button.setEnabled) # type: ignore
        self.many_answer_radioButton.toggled['bool'].connect(self.answers_list.setEnabled) # type: ignore
        self.many_answer_radioButton.toggled['bool'].connect(self.delete_answer_button.setEnabled) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.question_lineEdit, self.short_question_lineEdit)
        Dialog.setTabOrder(self.short_question_lineEdit, self.bool_answer_radioButton)
        Dialog.setTabOrder(self.bool_answer_radioButton, self.single_answer_radioButton)
        Dialog.setTabOrder(self.single_answer_radioButton, self.many_answer_radioButton)
        Dialog.setTabOrder(self.many_answer_radioButton, self.measure_lineEdit)
        Dialog.setTabOrder(self.measure_lineEdit, self.add_answer_lineEdit)
        Dialog.setTabOrder(self.add_answer_lineEdit, self.add_answer_button)
        Dialog.setTabOrder(self.add_answer_button, self.answers_list)
        Dialog.setTabOrder(self.answers_list, self.private_checkBox)
        Dialog.setTabOrder(self.private_checkBox, self.require_checkBox)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Добавить вопрос"))
        self.question_groupBox.setTitle(_translate("Dialog", "Вопрос"))
        self.label.setText(_translate("Dialog", "Коротко"))
        self.groupBox.setTitle(_translate("Dialog", "Ответ"))
        self.bool_answer_radioButton.setText(_translate("Dialog", "Да|Нет"))
        self.single_answer_radioButton.setText(_translate("Dialog", "Одиночный ответ"))
        self.many_answer_radioButton.setText(_translate("Dialog", "Множественный ответ"))
        self.label_2.setText(_translate("Dialog", "Ед. измер."))
        self.add_answer_button.setText(_translate("Dialog", "Добавить"))
        self.delete_answer_button.setText(_translate("Dialog", "Удалить"))
        self.private_checkBox.setText(_translate("Dialog", "&Указание на личность пациента"))
        self.require_checkBox.setText(_translate("Dialog", "&Обязательный вопрос"))
