# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TSAC/Administrator_Eng.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AdministratorWindow_Eng(object):
    def setupUi(self, AdministratorWindow_Eng):
        AdministratorWindow_Eng.setObjectName("AdministratorWindow_Eng")
        AdministratorWindow_Eng.setEnabled(True)
        AdministratorWindow_Eng.resize(500, 530)
        AdministratorWindow_Eng.setMinimumSize(QtCore.QSize(500, 530))
        AdministratorWindow_Eng.setMaximumSize(QtCore.QSize(500, 530))
        self.tabWidget_2 = QtWidgets.QTabWidget(AdministratorWindow_Eng)
        self.tabWidget_2.setGeometry(QtCore.QRect(0, 0, 500, 531))
        self.tabWidget_2.setMinimumSize(QtCore.QSize(0, 0))
        self.tabWidget_2.setMaximumSize(QtCore.QSize(500, 880))
        self.tabWidget_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.TSA_tab = QtWidgets.QWidget()
        self.TSA_tab.setObjectName("TSA_tab")
        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.TSA_tab)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 491, 501))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.SettingsGroupboxTSA = QtWidgets.QGroupBox(self.gridLayoutWidget_3)
        self.SettingsGroupboxTSA.setTitle("")
        self.SettingsGroupboxTSA.setObjectName("SettingsGroupboxTSA")
        self.groupBox_7 = QtWidgets.QGroupBox(self.SettingsGroupboxTSA)
        self.groupBox_7.setGeometry(QtCore.QRect(10, 20, 471, 211))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_7.setFont(font)
        self.groupBox_7.setObjectName("groupBox_7")
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox_7)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 40, 451, 71))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName("groupBox_4")
        self.FeatureExtractionSettingComboboxTSA = QtWidgets.QComboBox(self.groupBox_4)
        self.FeatureExtractionSettingComboboxTSA.setGeometry(QtCore.QRect(10, 20, 431, 31))
        self.FeatureExtractionSettingComboboxTSA.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.FeatureExtractionSettingComboboxTSA.setObjectName("FeatureExtractionSettingComboboxTSA")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_7)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 130, 451, 71))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName("groupBox_3")
        self.TimeshiftSpinboxTSA = QtWidgets.QSpinBox(self.groupBox_3)
        self.TimeshiftSpinboxTSA.setGeometry(QtCore.QRect(10, 30, 431, 22))
        self.TimeshiftSpinboxTSA.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.TimeshiftSpinboxTSA.setMinimum(5)
        self.TimeshiftSpinboxTSA.setMaximum(100)
        self.TimeshiftSpinboxTSA.setProperty("value", 50)
        self.TimeshiftSpinboxTSA.setObjectName("TimeshiftSpinboxTSA")
        self.groupBox_8 = QtWidgets.QGroupBox(self.SettingsGroupboxTSA)
        self.groupBox_8.setGeometry(QtCore.QRect(10, 240, 471, 121))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_8.setFont(font)
        self.groupBox_8.setObjectName("groupBox_8")
        self.groupBox_6 = QtWidgets.QGroupBox(self.groupBox_8)
        self.groupBox_6.setGeometry(QtCore.QRect(10, 30, 221, 71))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_6.setFont(font)
        self.groupBox_6.setObjectName("groupBox_6")
        self.nneighboursUMAP = QtWidgets.QSpinBox(self.groupBox_6)
        self.nneighboursUMAP.setGeometry(QtCore.QRect(10, 30, 191, 22))
        self.nneighboursUMAP.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.nneighboursUMAP.setMinimum(1)
        self.nneighboursUMAP.setMaximum(1000)
        self.nneighboursUMAP.setProperty("value", 5)
        self.nneighboursUMAP.setObjectName("nneighboursUMAP")
        self.groupBox_9 = QtWidgets.QGroupBox(self.groupBox_8)
        self.groupBox_9.setGeometry(QtCore.QRect(250, 30, 211, 71))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_9.setFont(font)
        self.groupBox_9.setObjectName("groupBox_9")
        self.minimaldistanseUMAP = QtWidgets.QDoubleSpinBox(self.groupBox_9)
        self.minimaldistanseUMAP.setGeometry(QtCore.QRect(10, 30, 191, 22))
        self.minimaldistanseUMAP.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.minimaldistanseUMAP.setDecimals(2)
        self.minimaldistanseUMAP.setMinimum(0.01)
        self.minimaldistanseUMAP.setMaximum(100.0)
        self.minimaldistanseUMAP.setSingleStep(0.01)
        self.minimaldistanseUMAP.setProperty("value", 0.1)
        self.minimaldistanseUMAP.setObjectName("minimaldistanseUMAP")
        self.groupBox_10 = QtWidgets.QGroupBox(self.SettingsGroupboxTSA)
        self.groupBox_10.setGeometry(QtCore.QRect(10, 370, 471, 121))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_10.setFont(font)
        self.groupBox_10.setObjectName("groupBox_10")
        self.groupBox_11 = QtWidgets.QGroupBox(self.groupBox_10)
        self.groupBox_11.setGeometry(QtCore.QRect(10, 30, 221, 71))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_11.setFont(font)
        self.groupBox_11.setObjectName("groupBox_11")
        self.nneighboursDBSCAN = QtWidgets.QSpinBox(self.groupBox_11)
        self.nneighboursDBSCAN.setGeometry(QtCore.QRect(10, 30, 191, 22))
        self.nneighboursDBSCAN.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.nneighboursDBSCAN.setMinimum(1)
        self.nneighboursDBSCAN.setMaximum(1000)
        self.nneighboursDBSCAN.setProperty("value", 5)
        self.nneighboursDBSCAN.setObjectName("nneighboursDBSCAN")
        self.groupBox_12 = QtWidgets.QGroupBox(self.groupBox_10)
        self.groupBox_12.setGeometry(QtCore.QRect(250, 30, 211, 71))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_12.setFont(font)
        self.groupBox_12.setObjectName("groupBox_12")
        self.minimaldistanseDBSCAN = QtWidgets.QDoubleSpinBox(self.groupBox_12)
        self.minimaldistanseDBSCAN.setGeometry(QtCore.QRect(10, 30, 191, 22))
        self.minimaldistanseDBSCAN.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.minimaldistanseDBSCAN.setDecimals(2)
        self.minimaldistanseDBSCAN.setMinimum(0.8)
        self.minimaldistanseDBSCAN.setMaximum(100.0)
        self.minimaldistanseDBSCAN.setSingleStep(0.01)
        self.minimaldistanseDBSCAN.setProperty("value", 0.8)
        self.minimaldistanseDBSCAN.setObjectName("minimaldistanseDBSCAN")
        self.gridLayout_3.addWidget(self.SettingsGroupboxTSA, 0, 0, 1, 1)
        self.tabWidget_2.addTab(self.TSA_tab, "")

        self.retranslateUi(AdministratorWindow_Eng)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(AdministratorWindow_Eng)

    def retranslateUi(self, AdministratorWindow_Eng):
        _translate = QtCore.QCoreApplication.translate
        AdministratorWindow_Eng.setWindowTitle(_translate("AdministratorWindow_Eng", "AdministratorWindow"))
        self.groupBox_7.setTitle(_translate("AdministratorWindow_Eng", "Time series analysis"))
        self.groupBox_4.setTitle(_translate("AdministratorWindow_Eng", "Set of statistical characteristics"))
        self.groupBox_3.setTitle(_translate("AdministratorWindow_Eng", "Window size"))
        self.groupBox_8.setTitle(_translate("AdministratorWindow_Eng", "Data compression"))
        self.groupBox_6.setTitle(_translate("AdministratorWindow_Eng", "Number of neighbors"))
        self.groupBox_9.setTitle(_translate("AdministratorWindow_Eng", "Distance to neighbors"))
        self.groupBox_10.setTitle(_translate("AdministratorWindow_Eng", "Clustering"))
        self.groupBox_11.setTitle(_translate("AdministratorWindow_Eng", "Number of neighbors"))
        self.groupBox_12.setTitle(_translate("AdministratorWindow_Eng", "Distance to neighbors"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.TSA_tab), _translate("AdministratorWindow_Eng", "Settings"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AdministratorWindow_Eng = QtWidgets.QWidget()
    ui = Ui_AdministratorWindow_Eng()
    ui.setupUi(AdministratorWindow_Eng)
    AdministratorWindow_Eng.show()
    sys.exit(app.exec_())
