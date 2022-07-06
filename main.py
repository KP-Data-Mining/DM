import sys
import threading

from colorama import init, Fore
from datetime import datetime
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *

from dbWorker import dbWorker
from Models.LSTM.rnnModel import rnnModel

from View.MainWindow import Ui_MainWindow
from View.LoginWindow import Ui_LoginWindow
from View.DatabaseWindow import Ui_DatabaseWindow
from View.DataLoadWindow import Ui_LoadDataWindow
from View.AdministratorWindow import Ui_AdministratorWindow

init(autoreset=True)

#########################################################################################################
import tkinter
from tkinter import messagebox as mb

import pandastable as pt
import pandas as pd

import Models.DBSCAN.Compression as Compression
import Models.TSA.TSAModule as TSAModule

from Models.DBSCAN.Clustering import DataPreparation, Plot

import numpy as np
tsa = TSAModule.TSA()

SelectedParametersNamesTSA = []
SelectedParametersIndexesTSA = []

plot_window = []
#########################################################################################################

app = QtWidgets.QApplication(sys.argv)

mainUI          = Ui_MainWindow()
loginUI         = Ui_LoginWindow()
databaseUI      = Ui_DatabaseWindow()
dataLoadUI      = Ui_LoadDataWindow()
administratorUI = Ui_AdministratorWindow()

LoginWindow         = QtWidgets.QDialog()
DataLoadWindow      = QtWidgets.QDialog()
DatabaseWindow      = QtWidgets.QDialog()
AdministratorWindow = QtWidgets.QDialog()
MainWindow          = QtWidgets.QMainWindow()

mainUI.setupUi(MainWindow)
loginUI.setupUi(LoginWindow)
databaseUI.setupUi(DatabaseWindow)
dataLoadUI.setupUi(DataLoadWindow)
administratorUI.setupUi(AdministratorWindow)

def thread(my_func):
    def wrapper(*args):
        my_thread = threading.Thread(target=my_func, args=args)
        my_thread.start()
    return wrapper

dbw = dbWorker()
rnn = rnnModel()

def openMainWindow():
    initializeActions(mainUI)
    initializeLists(mainUI)
    initializeDates(mainUI)
    initializeUi(mainUI)
    MainWindow.show()
def openLoginWindow():
    initializeActions(loginUI)
    LoginWindow.exec_()
def openDatabaseWindow():
    initializeActions(databaseUI)
    initializeLists(databaseUI)
    DatabaseWindow.show()
def openDataLoadWindow():
    initializeActions(dataLoadUI)
    initializeDates(dataLoadUI)
    initializeUi(dataLoadUI)
    DataLoadWindow.exec_()
def openAdministratorWindow():
    initializeActions(administratorUI)
    initializeLists(administratorUI)
    initializeUi(administratorUI)
    AdministratorWindow.show()

def initializeDates(ui):
    if type(ui) == Ui_LoadDataWindow:
        dataLoadUI.FromDateTimeLOAD.setDateTime(datetime.strptime(dbw.minDate, '%Y-%m-%d %H:%M:%S'))
        dataLoadUI.ToDateTimeLOAD.setDateTime(datetime.strptime(dbw.maxDate, '%Y-%m-%d %H:%M:%S'))
        dataLoadUI.FromDateTimeLOAD.setDisplayFormat('dd.MM.yyyy hh:mm:ss')
        dataLoadUI.ToDateTimeLOAD.setDisplayFormat('dd.MM.yyyy hh:mm:ss')
    if type(ui) == Ui_MainWindow:
        ##TSA
        mainUI.FromDateTimeTSA.setDisplayFormat('dd.MM.yyyy hh:mm:ss')
        mainUI.ToDateTimeTSA.setDisplayFormat('dd.MM.yyyy hh:mm:ss')
        mainUI.FromDateTimeTSA.setMinimumDateTime(datetime.strptime(dbw.minDate, '%Y-%m-%d %H:%M:%S'))
        mainUI.ToDateTimeTSA.setMaximumDateTime(datetime.strptime(dbw.maxDate, '%Y-%m-%d %H:%M:%S'))
        mainUI.FromDateTimeTSA.setDateTime(datetime.strptime(dbw.minDate, '%Y-%m-%d %H:%M:%S'))
        mainUI.ToDateTimeTSA.setDateTime(datetime.strptime(dbw.maxDate, '%Y-%m-%d %H:%M:%S'))
def initializeLists(ui):
    if type(ui) == Ui_AdministratorWindow:
        administratorUI.QualitIndicatorComboBoxRNN.addItems(dbw.getNames(dbw.ruNames, dbw.defects))
        addCheckableItems(administratorUI.RelevantFeaturesRNN, dbw.getNames(dbw.ruNames, dbw.features))
        administratorUI.OptimizerComboBoxRNN.addItems(dbw.optimizers.values())
        administratorUI.BatchComboBoxRNN.addItems(dbw.batches.values())
        administratorUI.EpochsComboBoxRNN.addItems(dbw.epochs.values())
        ##TSA
        administratorUI.TimeshiftSpinboxTSA.setValue(tsa.timeshift)
        administratorUI.FeatureExtractionSettingComboboxTSA.addItems(["Извлечение всех характеристик",
                                                                      "Извлечение минимального набора характеристик",
                                                                      "Извлечение предполагаемых эффективных характеристик"])
        administratorUI.FeatureExtractionSettingComboboxTSA.setCurrentIndex(tsa.settingsIndex)
        ##DBSCAN
        administratorUI.nneighboursUMAP.setValue(tsa.nneighboursUMAP)
        administratorUI.minimaldistanseUMAP.setValue(tsa.minimaldistanseUMAP)
        administratorUI.nneighboursDBSCAN.setValue(tsa.nneighboursDBSCAN)
        administratorUI.minimaldistanseDBSCAN.setValue(tsa.minimaldistanseDBSCAN)
    if type(ui) == Ui_MainWindow:
        mainUI.ModelComboBoxRNN.addItems(dbw.models.values())
        ##TSA
        items = dbw.getNames(dbw.ruNames, dbw.x)
        outputItems = dbw.getNames(dbw.ruNames, dbw.y)
        outputItems = [x for x in outputItems if str(x) != 'nan']
        for item in items:
            newitem = QListWidgetItem()
            newitem.setText(QApplication.translate("Dialog", item, None))
            newitem.setFlags(newitem.flags() | QtCore.Qt.ItemIsUserCheckable)
            newitem.setCheckState(QtCore.Qt.Unchecked)
            mainUI.ParametersTSA.addItem(newitem)
        for item in outputItems:
            newitem = QListWidgetItem()
            newitem.setText(QApplication.translate("Dialog", item, None))
            mainUI.OutputParametersTSA.addItem(newitem)
        mainUI.ParametersTSA.itemChanged.connect(ParametersSelectionTSA)
    if type(ui) == Ui_DatabaseWindow:
        addTableItems()

def initializeActions(ui):
    if type(ui) == Ui_AdministratorWindow:
        administratorUI.RocTrendButtonRNN.clicked.connect(showRoc)
        administratorUI.RelevantFeaturesRNN.clicked.connect(clearUI)
        administratorUI.MetricsButtonRNN.clicked.connect(showHistory)
        administratorUI.SaveModelButtonRNN.clicked.connect(saveModel)
        administratorUI.LearnButtonRNN.clicked.connect(lambda: learnModel())
        administratorUI.BatchComboBoxRNN.currentIndexChanged.connect(clearUI)
        administratorUI.ModelsDbButtonRNN.clicked.connect(openDatabaseWindow)
        administratorUI.EpochsComboBoxRNN.currentIndexChanged.connect(clearUI)
        administratorUI.ResultTrendsButtonRNN.clicked.connect(showResultTrends)
        administratorUI.OptimizerComboBoxRNN.currentIndexChanged.connect(clearUI)
        administratorUI.StartTrendsButtonRNN.clicked.connect(showSourceTrendsLearn)
        administratorUI.QualitIndicatorComboBoxRNN.currentIndexChanged.connect(clearUI)
        ##TSA
        administratorUI.TimeshiftSpinboxTSA.valueChanged.connect(TimeshiftValueTSA)
        administratorUI.FeatureExtractionSettingComboboxTSA.currentIndexChanged.connect(SettingsValueTSA)
        ##DBSCAN
        administratorUI.nneighboursUMAP.valueChanged.connect(SavePropDBSCAN)
        administratorUI.nneighboursDBSCAN.valueChanged.connect(SavePropDBSCAN)
        administratorUI.minimaldistanseUMAP.valueChanged.connect(SavePropDBSCAN)
        administratorUI.minimaldistanseDBSCAN.valueChanged.connect(SavePropDBSCAN)
    if type(ui) == Ui_LoadDataWindow:
        dataLoadUI.loadButton.clicked.connect(lambda: loadData())
    if type(ui) == Ui_LoginWindow:
        loginUI.loginButton.clicked.connect(login)
    if type(ui) == Ui_MainWindow:
        mainUI.RocTrendButtonRNN.clicked.connect(showRoc)
        mainUI.loadModelButtonRNN.clicked.connect(selectModel)
        mainUI.StartButtonRNN.clicked.connect(lambda: forecast())
        mainUI.ModelComboBoxRNN.currentIndexChanged.connect(clearUI)
        mainUI.ResultTrendsButtonRNN.clicked.connect(showResultTrends)
        mainUI.administrator_button.clicked.connect(openLoginWindow)
        mainUI.StartTrendsButtonRNN.clicked.connect(showSourceTrendsForecast)
        ##TSA
        mainUI.ClusterDataButtonRAW.clicked.connect(ViewCompresClustersOfBase)
        mainUI.StartButtonTSA.clicked.connect(PrepareDataTSA)
        mainUI.ClusterDataButtonTSA.clicked.connect(ViewCompresClustersOfTSA)
        mainUI.RawDataButtonTSA.clicked.connect(ShowRawDataTSA)
        mainUI.FeaturesDataButtonTSA.clicked.connect(ShowFeaturesTSA)
    if type(ui) == Ui_DatabaseWindow:
        databaseUI.deleteButton.clicked.connect(deleteModel)
def initializeUi(ui):
    if type(ui) == Ui_AdministratorWindow:
        administratorUI.progressBar.setMinimum(0)
        administratorUI.progressBar.setValue(0)    
    if type(ui) == Ui_LoadDataWindow:
        dataLoadUI.progressBar.setMinimum(0)
        dataLoadUI.progressBar.setValue(0)
    if type(ui) == Ui_MainWindow:
        mainUI.progressBar.setMinimum(0)
        mainUI.progressBar.setValue(0)

#########################################################################################################
def SavePropDBSCAN():
    tsa.nneighboursUMAP = administratorUI.nneighboursUMAP.value()
    tsa.minimaldistanseUMAP = administratorUI.minimaldistanseUMAP.value()
    tsa.nneighboursDBSCAN = administratorUI.nneighboursDBSCAN.value()
    tsa.minimaldistanseDBSCAN = administratorUI.minimaldistanseDBSCAN.value()

def ParametersSelectionTSA():
    SelectedParametersNamesTSA.clear()
    SelectedParametersIndexesTSA.clear()
    for i in range(mainUI.ParametersTSA.count() - 1):
        if (mainUI.ParametersTSA.item(i).checkState() == QtCore.Qt.Checked):
            SelectedParametersNamesTSA.append(mainUI.ParametersTSA.item(i).text())
            SelectedParametersIndexesTSA.append(
                list(dbw.ruNames.keys())[list(dbw.ruNames.values()).index(mainUI.ParametersTSA.item(i).text())])\

def PrepareDataTSA():
    try:
        root = tkinter.Tk()
        root.withdraw()
        SelectedOutputParameterIndexTSA = list(dbw.ruNames.keys())[
            list(dbw.ruNames.values()).index(mainUI.OutputParametersTSA.currentItem().text())]
        SelectedOutputParameterNameTSA = mainUI.OutputParametersTSA.currentItem().text()
        defects = pd.DataFrame({str(SelectedOutputParameterNameTSA): pd.Series(dbw.y[SelectedOutputParameterIndexTSA])})
        defects["time"] = pd.Series(dbw.dates)
        timeseries = pd.DataFrame({'time': pd.Series(dbw.dates)})
        indexes = []
        for i in range(timeseries.count()[0]):
            indexes.append("1")
        timeseries["id"] = indexes
        defects["id"] = indexes
        for i in range(len(SelectedParametersIndexesTSA)):
            newparamlist = dbw.x[SelectedParametersIndexesTSA[i]]
            timeseries[SelectedParametersNamesTSA[i]] = newparamlist
        timeseries = timeseries[timeseries['time'].between(str(mainUI.FromDateTimeTSA.dateTime().toPyDateTime()),
                                                           str(mainUI.ToDateTimeTSA.dateTime().toPyDateTime()))]
        defects = defects[defects['time'].between(str(mainUI.FromDateTimeTSA.dateTime().toPyDateTime()),
                                                  str(mainUI.ToDateTimeTSA.dateTime().toPyDateTime()))]
        view_enable = tsa.TimeSeriesAnalyser(timeseries, defects, dbw.limits[SelectedOutputParameterIndexTSA])
        mainUI.ControlPanelTSA.setEnabled(view_enable)
        mainUI.RawDataButtonTSA.setEnabled(view_enable)
        mainUI.RawDataLabelTSA.setEnabled(view_enable)
    except AttributeError:
        mb.showerror("Ошибка", "Вы не выбрали технологический параметр/параметры")
        mainUI.ControlPanelTSA.setEnabled(False)

def TimeshiftValueTSA():
    tsa.timeshift = administratorUI.TimeshiftSpinboxTSA.value()

def SettingsValueTSA():
    tsa.SetSettings(administratorUI.FeatureExtractionSettingComboboxTSA.currentIndex())

def FilterTSA():
    tsa.usefilter = administratorUI.filterTSACheckbox.isChecked()

def ShowRawDataTSA():
    root = tkinter.Tk()
    root.withdraw()
    frame = tkinter.Frame(root)
    frame.pack()
    dTDa1 = tkinter.Toplevel()
    dTDa1.title('Сырые данные')
    ptable = pt.Table(dTDa1, dataframe=tsa.timeseries, showtoolbar=True, showstatusbar=True)
    ptable.show()
    root.mainloop()

def ShowData(_dataframe, name):
    root = tkinter.Tk()
    root.withdraw()
    frame = tkinter.Frame(root)
    frame.pack()
    dTDa1 = tkinter.Toplevel()
    dTDa1.title(name)
    ptable = pt.Table(dTDa1, dataframe=_dataframe, showtoolbar=True, showstatusbar=True)
    ptable.show()
    root.mainloop()

def ShowFeaturesTSA():
    root = tkinter.Tk()
    root.withdraw()
    frame = tkinter.Frame(root)
    frame.pack()
    dTDa1 = tkinter.Toplevel()
    dTDa1.title('Статистические характеристики')
    ptable = pt.Table(dTDa1, dataframe=tsa.filteredfeatures, showtoolbar=True, showstatusbar=True)
    ptable.show()
    root.mainloop()

def ViewCompresClustersOfBase():
    try:
        root = tkinter.Tk()
        root.withdraw()
        SelectedOutputParameterIndexTSA = list(dbw.ruNames.keys())[
            list(dbw.ruNames.values()).index(mainUI.OutputParametersTSA.currentItem().text())]
        SelectedOutputParameterNameTSA = mainUI.OutputParametersTSA.currentItem().text()

        timeseries = pd.DataFrame({'time': pd.Series(dbw.dates)})
        for i in range(len(SelectedParametersIndexesTSA)):
            newparamlist = dbw.x[SelectedParametersIndexesTSA[i]]
            timeseries[SelectedParametersNamesTSA[i]] = newparamlist
        timeseries = timeseries[timeseries['time'].between(str(mainUI.FromDateTimeTSA.dateTime().toPyDateTime()),
                                                           str(mainUI.ToDateTimeTSA.dateTime().toPyDateTime()))]
        defects = [defect[0] for defect in pd.DataFrame({str(SelectedOutputParameterNameTSA): pd.Series(dbw.y[SelectedOutputParameterIndexTSA])}).to_numpy(np.float32)]
        points = np.array(Compression.CompressingData(timeseries.drop(columns=['time']),
                                                      n_neighbors=tsa.nneighboursUMAP,
                                                      min_dist=tsa.minimaldistanseUMAP))
        labels = DataPreparation.GetLabels(points, eps=tsa.minimaldistanseDBSCAN,
                                           min_samples=tsa.nneighboursDBSCAN)
        info = timeseries

        pd.DataFrame(defects, columns=['defects']).to_csv('2.csv', index_label='index')
        timeseries.join(pd.DataFrame(labels, columns=["Кластер"])).to_csv('3.csv', index_label='index')

        Plot.create(points, defects, labels, info, dbw.limits[SelectedOutputParameterIndexTSA])
        plot_window.append(Plot.show())
    except AttributeError:
        mb.showerror("Ошибка", "Вы не выбрали технологический параметр/параметры")

def ViewCompresClustersOfTSA():
    SelectedOutputParameterIndexTSA = list(dbw.ruNames.keys())[
        list(dbw.ruNames.values()).index(mainUI.OutputParametersTSA.currentItem().text())]
    points = np.array(Compression.CompressingData(tsa.filteredfeatures,
                                                  n_neighbors=tsa.nneighboursUMAP,
                                                  min_dist=tsa.minimaldistanseUMAP))
    defects = np.array(np.array(tsa.defects)[len(tsa.defects) - len(points):, 0], dtype=np.float32)

    labels = DataPreparation.GetLabels(points, eps=tsa.minimaldistanseDBSCAN,
                                       min_samples=tsa.nneighboursDBSCAN)
    info = tsa.timeseries.drop(columns=['id'])[len(tsa.defects) - len(points):].reset_index(drop=True)

    pd.DataFrame(defects, columns=['defects']).to_csv('2.csv', index_label='index')
    tsa.timeseries.drop(columns=['id'])[len(tsa.defects) - len(points):].reset_index(drop=True).join(
        tsa.filteredfeatures.reset_index(drop=True)).join(
        pd.DataFrame(labels, columns=["Кластер"])).to_csv('3.csv', index_label='index')

    Plot.create(points, defects, labels, info, dbw.limits[SelectedOutputParameterIndexTSA])
    plot_window.append(Plot.show())
#########################################################################################################

#########################################################################################################
def showResultTrends():
    rnn.showResultDataTrends(dbw)
def showRoc():
    rnn.showRocTrend()
def clearUI():
    global rnn
    rnn = rnnModel()
    administratorUI.ResultTrendsButtonRNN.setEnabled(False)
    administratorUI.ModelNameLineEditRNN.setEnabled(False)
    administratorUI.SaveModelButtonRNN.setEnabled(False)
    administratorUI.RocTrendButtonRNN.setEnabled(False)
    administratorUI.MetricsButtonRNN.setEnabled(False)
    administratorUI.LearnButtonRNN.setEnabled(True)
    administratorUI.PrecisionRNN.setText("")
    administratorUI.RecallRNN.setText("")
    administratorUI.RmseRNN.setText("")
    administratorUI.MapeRNN.setText("")
    administratorUI.AucRNN.setText("")
    administratorUI.MseRNN.setText("")
    administratorUI.MaeRNN.setText("")
    administratorUI.F1RNN.setText("")
    mainUI.ResultTrendsButtonRNN.setEnabled(False)
    mainUI.StartTrendsButtonRNN.setEnabled(False)
    mainUI.RocTrendButtonRNN.setEnabled(False)
    mainUI.StartButtonRNN.setEnabled(False)
    mainUI.ModelDescriptionTextRNN.setText("")
    mainUI.PrecisionRNN.setText("")
    mainUI.RecallRNN.setText("")
    mainUI.RmseRNN.setText("")
    mainUI.MapeRNN.setText("")
    mainUI.AucRNN.setText("")
    mainUI.MseRNN.setText("")
    mainUI.MaeRNN.setText("")
    mainUI.F1RNN.setText("")

#Login
def login():
    if loginUI.passwordText.text() == "1111":
        print(Fore.GREEN + "Вход выполнен")
        LoginWindow.close()
        openAdministratorWindow()
    else:
        print(Fore.RED + "Ошибка входа")

#Administrator
@thread
def learnModel():
    print("Обучение модели...")
    administratorUI.progressBar.setMaximum(0)
    administratorUI.LearnButtonRNN.setEnabled(False)
    administratorUI.BatchComboBoxRNN.setEnabled(False)
    administratorUI.EpochsComboBoxRNN.setEnabled(False)
    administratorUI.ModelsDbButtonRNN.setEnabled(False)
    administratorUI.StartTrendsButtonRNN.setEnabled(False)
    administratorUI.OptimizerComboBoxRNN.setEnabled(False)
    administratorUI.QualitIndicatorComboBoxRNN.setEnabled(False)
    administratorUI.RelevantFeaturesGroupBoxRNN.setEnabled(False)
    
    if validateParameters():
        global rnn
        rnn = rnnModel(name="", dbw=dbw, parameters=getCheckedParameters(administratorUI.RelevantFeaturesRNN),
                                    defect=administratorUI.QualitIndicatorComboBoxRNN.currentText(),
                                    optimizer=administratorUI.OptimizerComboBoxRNN.currentText(),
                                    epochs=administratorUI.EpochsComboBoxRNN.currentText(),
                                    batch=administratorUI.BatchComboBoxRNN.currentText())
        if rnn.learn(dbw):
            if rnn.forecast(dbw, True):
                if rnn.getMetrics(dbw):
                    administratorUI.ResultTrendsButtonRNN.setEnabled(True)
                    administratorUI.ModelNameLineEditRNN.setEnabled(True)
                    administratorUI.SaveModelButtonRNN.setEnabled(True)
                    administratorUI.RocTrendButtonRNN.setEnabled(True)
                    administratorUI.MetricsButtonRNN.setEnabled(True)
                    administratorUI.PrecisionRNN.setText(str(rnn.precision))
                    administratorUI.RecallRNN.setText(str(rnn.recall))
                    administratorUI.RmseRNN.setText(str(rnn.RMSE))
                    administratorUI.MapeRNN.setText(str(rnn.MAPE))
                    administratorUI.AucRNN.setText(str(rnn.AUC))
                    administratorUI.MseRNN.setText(str(rnn.MSE))
                    administratorUI.MaeRNN.setText(str(rnn.MAE))
                    administratorUI.F1RNN.setText(str(rnn.F1))
                    print(Fore.GREEN + "Модель обучена")
                else:
                    print(Fore.RED + "Ошибка расчета метрик")
            else:
                print(Fore.RED + "Ошибка валидации модели")
        else:
            print(Fore.RED + "Ошибка обучения модели")
    administratorUI.progressBar.setMaximum(100)
    administratorUI.BatchComboBoxRNN.setEnabled(True)
    administratorUI.EpochsComboBoxRNN.setEnabled(True)
    administratorUI.ModelsDbButtonRNN.setEnabled(True)
    administratorUI.StartTrendsButtonRNN.setEnabled(True)
    administratorUI.OptimizerComboBoxRNN.setEnabled(True)
    administratorUI.QualitIndicatorComboBoxRNN.setEnabled(True)
    administratorUI.RelevantFeaturesGroupBoxRNN.setEnabled(True)
def validateParameters():
    if administratorUI.OptimizerComboBoxRNN.currentText == "":
        print(Fore.RED + "Сначала нужно выбрать оптимизатор")
        return False
    if administratorUI.BatchComboBoxRNN.currentText == "":
        print(Fore.RED + "Сначала нужно выбрать размер пакета")
        return False
    if administratorUI.EpochsComboBoxRNN.currentText == "":
        print(Fore.RED + "Сначала нужно выбрать максимальное число эпох")
        return False
    if administratorUI.QualitIndicatorComboBoxRNN.currentText == "":
        print(Fore.RED + "Сначала нужно выбрать прогнозируемый показатель качества")
        return False
    if len(getCheckedParameters(administratorUI.RelevantFeaturesRNN)) == 0:
        print(Fore.RED + "Сначала нужно выбрать как минимум один влияющий параметр")
        return False
    return True
def showHistory():
    rnn.showHistoryTrends()
def showSourceTrendsLearn():
    tmpRnn = rnnModel(name="", dbw=dbw, parameters=getCheckedParameters(administratorUI.RelevantFeaturesRNN),
                                    defect=administratorUI.QualitIndicatorComboBoxRNN.currentText(),
                                    optimizer=administratorUI.OptimizerComboBoxRNN.currentText(),
                                    epochs=administratorUI.EpochsComboBoxRNN.currentText(),
                                    batch=administratorUI.BatchComboBoxRNN.currentText())
    tmpRnn.showSourceDataTrends(dbw)
def saveModel():
    if (administratorUI.ModelNameLineEditRNN.text() != ""):
        print("Сохранение модели...")
        if rnn.save(dbw, administratorUI.ModelNameLineEditRNN.text()):
            print(Fore.GREEN + "Модель успешно сохранена")   
            administratorUI.ModelNameLineEditRNN.setText("")
            dbw.loadRNNModels()
            addTableItems()
        else:
            print(Fore.RED + "Ошибка при сохранении модели")    
    else:
        print(Fore.RED + "Сначала нужно ввести название модели")
    return

#Database
def checkModels(key):
    for model in dbw.models:
        if key == model:
            return True
    return False
def deleteModel():
    key = databaseUI.spinBox.value()
    if checkModels(key):
        if dbw.deleteModel(key):
            print(Fore.GREEN + "Модель удалена")
            dbw.loadRNNModels()
            addTableItems()
        else:
            print(Fore.RED + "Ошибка удаления модели")
    else:
        print(Fore.RED + "Такой модели нет в базе данных")
    return
def addTableItems():
    tmp = dbw.getModelsWithParameters()
    databaseUI.modelsTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
    databaseUI.modelsTable.clear()
    row = 0
    for i in tmp:
        databaseUI.modelsTable.setRowCount(row+1)
        databaseUI.modelsTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i[0])))
        databaseUI.modelsTable.setItem(row, 1, QtWidgets.QTableWidgetItem(i[1]))
        databaseUI.modelsTable.setItem(row, 2, QtWidgets.QTableWidgetItem(i[2]))
        databaseUI.modelsTable.setItem(row, 3, QtWidgets.QTableWidgetItem(i[3]))
        row+=1
#DataLoad
@thread
def loadData():
    if validateDates(dataLoadUI.FromDateTimeLOAD, dataLoadUI.ToDateTimeLOAD):
        print("Начало загрузки данных...")
        dataLoadUI.progressBar.setMaximum(0)
        dataLoadUI.loadButton.setEnabled(False)
        dataLoadUI.ToDateTimeLOAD.setEnabled(False)
        dataLoadUI.FromDateTimeLOAD.setEnabled(False)
        dbw.loadData(str(dataLoadUI.FromDateTimeLOAD.dateTime().toPyDateTime()), str(dataLoadUI.ToDateTimeLOAD.dateTime().toPyDateTime()))
        dataLoadUI.progressBar.setMaximum(100)
        dataLoadUI.loadButton.setEnabled(True)
        dataLoadUI.ToDateTimeLOAD.setEnabled(True)
        dataLoadUI.FromDateTimeLOAD.setEnabled(True)
        print(Fore.GREEN + "Данные успешно загружены")
        DataLoadWindow.close()
def validateDates(fromDT, toDT):
    enabledMin = datetime.strptime(dbw.minDate, '%Y-%m-%d %H:%M:%S')
    enabledMax = datetime.strptime(dbw.maxDate, '%Y-%m-%d %H:%M:%S')
    min = fromDT.dateTime().toPyDateTime()
    max = toDT.dateTime().toPyDateTime()
    if min < enabledMin:
        min = enabledMin
    if min > enabledMax:
        min = enabledMax
    if max < enabledMin:
        max = enabledMin
    if max > enabledMax:
        max = enabledMax
    if min == max:
        print(Fore.RED + "Некорректный выбор диапазона. Начальная дата не может быть равна конечной! Выберите другой диапазон и попробуйте снова")
        return False
    if min > max:
        tmp = min
        min = max
        max = tmp
        fromDT.setDateTime(datetime.strptime(str(min), '%Y-%m-%d %H:%M:%S'))
        toDT.setDateTime(datetime.strptime(str(max), '%Y-%m-%d %H:%M:%S'))
    return True

#Main
def selectModel():
    print("Загрузка модели...")
    if mainUI.ModelComboBoxRNN.currentText != "":
        clearUI()
        global rnn
        selectedModel = mainUI.ModelComboBoxRNN.currentText()
        rnn = rnnModel(dbw=dbw, name=selectedModel)
        mainUI.ModelDescriptionTextRNN.setText(rnn.getDescription(dbw))
        mainUI.ResultTrendsButtonRNN.setEnabled(False)
        mainUI.StartTrendsButtonRNN.setEnabled(True)
        mainUI.RocTrendButtonRNN.setEnabled(False)
        mainUI.StartButtonRNN.setEnabled(True)
        print(Fore.GREEN + "Модель успешно загружена")
    else:
        print(Fore.RED + "Сначала нужно выбрать модель")
@thread
def forecast():
    print("Прогнозирование...")
    mainUI.progressBar.setMaximum(0)
    mainUI.StartButtonRNN.setEnabled(False)
    mainUI.ModelComboBoxRNN.setEnabled(False)
    mainUI.loadModelButtonRNN.setEnabled(False)
    mainUI.StartTrendsButtonRNN.setEnabled(False)
    mainUI.administrator_button.setEnabled(False)
    if rnn.forecast(dbw, False):
        if rnn.getMetrics(dbw):
            mainUI.StartButtonRNN.setEnabled(False)
            mainUI.ModelComboBoxRNN.setEnabled(True)
            mainUI.RocTrendButtonRNN.setEnabled(True)
            mainUI.loadModelButtonRNN.setEnabled(True)
            mainUI.StartTrendsButtonRNN.setEnabled(True)
            mainUI.ResultTrendsButtonRNN.setEnabled(True)
            mainUI.PrecisionRNN.setText(str(rnn.precision))
            mainUI.RecallRNN.setText(str(rnn.recall))
            mainUI.RmseRNN.setText(str(rnn.RMSE))
            mainUI.MapeRNN.setText(str(rnn.MAPE))
            mainUI.AucRNN.setText(str(rnn.AUC))
            mainUI.MseRNN.setText(str(rnn.MSE))
            mainUI.MaeRNN.setText(str(rnn.MAE))
            mainUI.F1RNN.setText(str(rnn.F1))
            print(Fore.GREEN + "Прогноз успешно построен")
        else:
            print(Fore.RED + "Ошибка рассчета метрик")
    else:
        print(Fore.RED + "Ошибка построения прогноза")
    mainUI.progressBar.setMaximum(100)
    mainUI.ModelComboBoxRNN.setEnabled(True)
    mainUI.loadModelButtonRNN.setEnabled(True)
    mainUI.StartTrendsButtonRNN.setEnabled(True)
    mainUI.administrator_button.setEnabled(True)
def showSourceTrendsForecast():
    rnn.showSourceDataTrends(dbw)
#########################################################################################################

def addCheckableItems(ui, items):
    for item in items:
        newItem = QListWidgetItem()
        newItem.setText(item)
        newItem.setFlags(newItem.flags() | QtCore.Qt.ItemIsUserCheckable)
        newItem.setCheckState(QtCore.Qt.Unchecked)
        ui.addItem(newItem)
def getCheckedParameters(ui):
    result = list()
    for i in range(ui.count() - 1):
        if (ui.item(i).checkState() == QtCore.Qt.Checked):
            result.append(ui.item(i).text())
    return result

if __name__ == "__main__":
    openDataLoadWindow()
    if dbw.isDataLoaded:
        openMainWindow()
        sys.exit(app.exec_())
    else:
        sys.exit()