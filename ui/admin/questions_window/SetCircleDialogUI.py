# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'set_cicrcle.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SetCircleDialog(object):
    def setupUi(self, SetCircleDialog):
        SetCircleDialog.setObjectName("SetCircleDialog")
        SetCircleDialog.resize(587, 200)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(SetCircleDialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.question_comboBox = QtWidgets.QGroupBox(SetCircleDialog)
        self.question_comboBox.setObjectName("question_comboBox")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.question_comboBox)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.answer_label = QtWidgets.QLabel(self.question_comboBox)
        self.answer_label.setObjectName("answer_label")
        self.verticalLayout_3.addWidget(self.answer_label)
        self.answer_combo_box = QtWidgets.QComboBox(self.question_comboBox)
        self.answer_combo_box.setObjectName("answer_combo_box")
        self.verticalLayout_3.addWidget(self.answer_combo_box)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.start_label = QtWidgets.QLabel(self.question_comboBox)
        self.start_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.start_label.setIndent(0)
        self.start_label.setObjectName("start_label")
        self.verticalLayout.addWidget(self.start_label)
        self.start_comboBox = QtWidgets.QComboBox(self.question_comboBox)
        self.start_comboBox.setObjectName("start_comboBox")
        self.verticalLayout.addWidget(self.start_comboBox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.finish_label = QtWidgets.QLabel(self.question_comboBox)
        self.finish_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.finish_label.setObjectName("finish_label")
        self.verticalLayout_2.addWidget(self.finish_label)
        self.finish_comboBox = QtWidgets.QComboBox(self.question_comboBox)
        self.finish_comboBox.setObjectName("finish_comboBox")
        self.verticalLayout_2.addWidget(self.finish_comboBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.question_comboBox)
        self.label_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)
        self.verticalLayout_4.addWidget(self.question_comboBox)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.cycle_check_box = QtWidgets.QCheckBox(SetCircleDialog)
        self.cycle_check_box.setObjectName("cycle_check_box")
        self.horizontalLayout_2.addWidget(self.cycle_check_box)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.saveAndCancelButtonBox = QtWidgets.QDialogButtonBox(SetCircleDialog)
        self.saveAndCancelButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.saveAndCancelButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.saveAndCancelButtonBox.setObjectName("saveAndCancelButtonBox")
        self.verticalLayout_4.addWidget(self.saveAndCancelButtonBox)

        self.retranslateUi(SetCircleDialog)
        self.saveAndCancelButtonBox.accepted.connect(SetCircleDialog.accept) # type: ignore
        self.saveAndCancelButtonBox.rejected.connect(SetCircleDialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(SetCircleDialog)

    def retranslateUi(self, SetCircleDialog):
        _translate = QtCore.QCoreApplication.translate
        SetCircleDialog.setWindowTitle(_translate("SetCircleDialog", "Set circle"))
        self.question_comboBox.setTitle(_translate("SetCircleDialog", "Вопрос"))
        self.answer_label.setText(_translate("SetCircleDialog", "При ответе"))
        self.start_label.setText(_translate("SetCircleDialog", "Следующие вопросы с:"))
        self.finish_label.setText(_translate("SetCircleDialog", "По:"))
        self.label_2.setText(_translate("SetCircleDialog", "доступны"))
        self.cycle_check_box.setText(_translate("SetCircleDialog", "и повторяются"))