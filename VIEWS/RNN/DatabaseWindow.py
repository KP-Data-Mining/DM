# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RNN/Database.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DatabaseWindow(object):
    def setupUi(self, DatabaseWindow):
        DatabaseWindow.setObjectName("DatabaseWindow")
        DatabaseWindow.resize(650, 420)
        DatabaseWindow.setMinimumSize(QtCore.QSize(650, 420))
        DatabaseWindow.setMaximumSize(QtCore.QSize(650, 420))
        self.verticalLayoutWidget = QtWidgets.QWidget(DatabaseWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 651, 421))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.modelsTable = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.modelsTable.setColumnCount(4)
        self.modelsTable.setObjectName("modelsTable")
        self.modelsTable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.modelsTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.modelsTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.modelsTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.modelsTable.setHorizontalHeaderItem(3, item)
        self.verticalLayout.addWidget(self.modelsTable)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setMinimumSize(QtCore.QSize(55, 20))
        self.label.setMaximumSize(QtCore.QSize(55, 20))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBox = QtWidgets.QSpinBox(self.verticalLayoutWidget)
        self.spinBox.setMinimumSize(QtCore.QSize(60, 20))
        self.spinBox.setMaximumSize(QtCore.QSize(60, 20))
        self.spinBox.setObjectName("spinBox")
        self.horizontalLayout.addWidget(self.spinBox)
        self.deleteButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.deleteButton.setMinimumSize(QtCore.QSize(75, 20))
        self.deleteButton.setMaximumSize(QtCore.QSize(75, 20))
        self.deleteButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.deleteButton.setObjectName("deleteButton")
        self.horizontalLayout.addWidget(self.deleteButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(DatabaseWindow)
        QtCore.QMetaObject.connectSlotsByName(DatabaseWindow)

    def retranslateUi(self, DatabaseWindow):
        _translate = QtCore.QCoreApplication.translate
        DatabaseWindow.setWindowTitle(_translate("DatabaseWindow", "DatabaseWindow"))
        item = self.modelsTable.horizontalHeaderItem(0)
        item.setText(_translate("DatabaseWindow", "Id"))
        item = self.modelsTable.horizontalHeaderItem(1)
        item.setText(_translate("DatabaseWindow", "Name"))
        item = self.modelsTable.horizontalHeaderItem(2)
        item.setText(_translate("DatabaseWindow", "From"))
        item = self.modelsTable.horizontalHeaderItem(3)
        item.setText(_translate("DatabaseWindow", "To"))
        self.label.setText(_translate("DatabaseWindow", "Id модели:"))
        self.deleteButton.setText(_translate("DatabaseWindow", "Удалить"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DatabaseWindow = QtWidgets.QWidget()
    ui = Ui_DatabaseWindow()
    ui.setupUi(DatabaseWindow)
    DatabaseWindow.show()
    sys.exit(app.exec_())
