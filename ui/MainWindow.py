# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


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
        self.questions_table = QtWidgets.QTableWidget(self.centralwidget)
        self.questions_table.setEnabled(True)
        self.questions_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.questions_table.setProperty("showDropIndicator", True)
        self.questions_table.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.questions_table.setDefaultDropAction(QtCore.Qt.CopyAction)
        self.questions_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.questions_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.questions_table.setCornerButtonEnabled(True)
        self.questions_table.setColumnCount(3)
        self.questions_table.setObjectName("questions_table")
        self.questions_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.questions_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.questions_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.questions_table.setHorizontalHeaderItem(2, item)
        self.horizontalLayout.addWidget(self.questions_table)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.change_question_button = QtWidgets.QPushButton(self.centralwidget)
        self.change_question_button.setEnabled(False)
        self.change_question_button.setObjectName("change_question_button")
        self.verticalLayout.addWidget(self.change_question_button)
        spacerItem = QtWidgets.QSpacerItem(20, 178, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.set_additional_button = QtWidgets.QPushButton(self.centralwidget)
        self.set_additional_button.setEnabled(False)
        self.set_additional_button.setObjectName("set_additional_button")
        self.verticalLayout.addWidget(self.set_additional_button)
        self.set_cicle_button = QtWidgets.QPushButton(self.centralwidget)
        self.set_cicle_button.setEnabled(False)
        self.set_cicle_button.setObjectName("set_cicle_button")
        self.verticalLayout.addWidget(self.set_cicle_button)
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
        item = self.questions_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Вопрос"))
        item = self.questions_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Коротко"))
        item = self.questions_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Порядок"))
        self.change_question_button.setText(_translate("MainWindow", "Изменить"))
        self.set_additional_button.setText(_translate("MainWindow", "Установить доп. вопросы"))
        self.set_cicle_button.setText(_translate("MainWindow", "Установить цикл"))
