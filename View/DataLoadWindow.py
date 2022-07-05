# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DataLoad.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoadDataWindow(object):
    def setupUi(self, LoadDataWindow):
        LoadDataWindow.setObjectName("LoadDataWindow")
        LoadDataWindow.resize(500, 160)
        LoadDataWindow.setMinimumSize(QtCore.QSize(500, 160))
        LoadDataWindow.setMaximumSize(QtCore.QSize(500, 160))
        self.verticalLayoutWidget = QtWidgets.QWidget(LoadDataWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 502, 158))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.TimeDiapazonLOAD = QtWidgets.QGroupBox(self.verticalLayoutWidget)
        self.TimeDiapazonLOAD.setMinimumSize(QtCore.QSize(490, 100))
        self.TimeDiapazonLOAD.setMaximumSize(QtCore.QSize(490, 100))
        self.TimeDiapazonLOAD.setObjectName("TimeDiapazonLOAD")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.TimeDiapazonLOAD)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(10, 20, 471, 71))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.TimeDiapazonGridLayoutLOAD = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.TimeDiapazonGridLayoutLOAD.setContentsMargins(0, 0, 0, 0)
        self.TimeDiapazonGridLayoutLOAD.setObjectName("TimeDiapazonGridLayoutLOAD")
        self.EndDateLabelLOAD = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.EndDateLabelLOAD.setMaximumSize(QtCore.QSize(230, 20))
        self.EndDateLabelLOAD.setObjectName("EndDateLabelLOAD")
        self.TimeDiapazonGridLayoutLOAD.addWidget(self.EndDateLabelLOAD, 0, 1, 1, 1)
        self.ToDateTimeLOAD = QtWidgets.QDateTimeEdit(self.gridLayoutWidget_3)
        self.ToDateTimeLOAD.setMaximumSize(QtCore.QSize(230, 20))
        self.ToDateTimeLOAD.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.ToDateTimeLOAD.setObjectName("ToDateTimeLOAD")
        self.TimeDiapazonGridLayoutLOAD.addWidget(self.ToDateTimeLOAD, 1, 1, 1, 1)
        self.FromDateTimeLOAD = QtWidgets.QDateTimeEdit(self.gridLayoutWidget_3)
        self.FromDateTimeLOAD.setMaximumSize(QtCore.QSize(230, 20))
        self.FromDateTimeLOAD.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.FromDateTimeLOAD.setObjectName("FromDateTimeLOAD")
        self.TimeDiapazonGridLayoutLOAD.addWidget(self.FromDateTimeLOAD, 1, 0, 1, 1)
        self.StartDateLabelLOAD = QtWidgets.QLabel(self.gridLayoutWidget_3)
        self.StartDateLabelLOAD.setMaximumSize(QtCore.QSize(230, 20))
        self.StartDateLabelLOAD.setObjectName("StartDateLabelLOAD")
        self.TimeDiapazonGridLayoutLOAD.addWidget(self.StartDateLabelLOAD, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.TimeDiapazonLOAD)
        self.loadButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.loadButton.setMinimumSize(QtCore.QSize(490, 20))
        self.loadButton.setMaximumSize(QtCore.QSize(490, 20))
        self.loadButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.loadButton.setObjectName("loadButton")
        self.verticalLayout.addWidget(self.loadButton)
        self.progressBar = QtWidgets.QProgressBar(self.verticalLayoutWidget)
        self.progressBar.setMinimumSize(QtCore.QSize(500, 20))
        self.progressBar.setMaximumSize(QtCore.QSize(500, 20))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)

        self.retranslateUi(LoadDataWindow)
        QtCore.QMetaObject.connectSlotsByName(LoadDataWindow)

    def retranslateUi(self, LoadDataWindow):
        _translate = QtCore.QCoreApplication.translate
        LoadDataWindow.setWindowTitle(_translate("LoadDataWindow", "LoadDataWindow"))
        self.TimeDiapazonLOAD.setTitle(_translate("LoadDataWindow", "Выбор временного диапазона"))
        self.EndDateLabelLOAD.setText(_translate("LoadDataWindow", "Конечная дата"))
        self.StartDateLabelLOAD.setText(_translate("LoadDataWindow", "Начальная дата"))
        self.loadButton.setText(_translate("LoadDataWindow", "Загрузить данные"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LoadDataWindow = QtWidgets.QWidget()
    ui = Ui_LoadDataWindow()
    ui.setupUi(LoadDataWindow)
    LoadDataWindow.show()
    sys.exit(app.exec_())