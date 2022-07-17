import sys
import json
import threading

from colorama import init, Fore
from datetime import datetime
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *

from DbWorker import DbWorker
from MODELS.RNN.RnnModel import RnnModel

from VIEWS.RNN.MainWindow_Ru import Ui_MainWindow_Ru
from VIEWS.RNN.DatabaseWindow_Ru import Ui_DatabaseWindow_Ru
from VIEWS.RNN.AdministratorWindow_Ru import Ui_AdministratorWindow_Ru

from VIEWS.RNN.MainWindow_Eng import Ui_MainWindow_Eng
from VIEWS.RNN.DatabaseWindow_Eng import Ui_DatabaseWindow_Eng
from VIEWS.RNN.AdministratorWindow_Eng import Ui_AdministratorWindow_Eng

init(autoreset=True)

app = QtWidgets.QApplication(sys.argv)

file = open('settings.json')
settings = json.load(file)

if settings['Language'] == 'Ru':
    mainUI          = Ui_MainWindow_Ru()
    databaseUI      = Ui_DatabaseWindow_Ru()
    administratorUI = Ui_AdministratorWindow_Ru()
else:
    mainUI          = Ui_MainWindow_Eng()
    databaseUI      = Ui_DatabaseWindow_Eng()
    administratorUI = Ui_AdministratorWindow_Eng()

DatabaseWindow      = QtWidgets.QDialog()
AdministratorWindow = QtWidgets.QDialog()
MainWindow          = QtWidgets.QMainWindow()

mainUI.setupUi(MainWindow)
databaseUI.setupUi(DatabaseWindow)
administratorUI.setupUi(AdministratorWindow)

def thread(my_func):
    def wrapper(*args):
        my_thread = threading.Thread(target=my_func, args=args)
        my_thread.start()
    return wrapper

dbw = DbWorker()
rnn = RnnModel(language=settings['Language'])

def openMainWindow():
    initializeActions(mainUI)
    initializeLists(mainUI)
    initializeUi(mainUI)
    MainWindow.show()
def openDatabaseWindow():
    initializeActions(databaseUI)
    initializeLists(databaseUI)
    DatabaseWindow.show()
def openAdministratorWindow():
    initializeActions(administratorUI)
    initializeLists(administratorUI)
    initializeUi(administratorUI)
    AdministratorWindow.show()

def initializeLists(ui):
    if type(ui) == Ui_AdministratorWindow_Ru or type(ui) == Ui_AdministratorWindow_Eng:
        administratorUI.QualitIndicatorComboBoxRNN.addItems(dbw.getNames(dbw.names, dbw.defects))
        addCheckableItems(administratorUI.RelevantFeaturesRNN, dbw.getNames(dbw.names, dbw.features))
        administratorUI.OptimizerComboBoxRNN.addItems(dbw.optimizers.values())
        administratorUI.BatchComboBoxRNN.addItems(dbw.batches.values())
        administratorUI.EpochsComboBoxRNN.addItems(dbw.epochs.values())
    if type(ui) == Ui_MainWindow_Ru or type(ui) == Ui_MainWindow_Eng:
        mainUI.ModelComboBoxRNN.addItems(dbw.models.values())
    if type(ui) == Ui_DatabaseWindow_Ru or type(ui) == Ui_DatabaseWindow_Eng:
        addTableItems()

def initializeActions(ui):
    if type(ui) == Ui_AdministratorWindow_Ru or type(ui) == Ui_AdministratorWindow_Eng:
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
    if type(ui) == Ui_MainWindow_Ru or type(ui) == Ui_MainWindow_Eng:
        mainUI.RocTrendButtonRNN.clicked.connect(showRoc)
        mainUI.loadModelButtonRNN.clicked.connect(selectModel)
        mainUI.StartButtonRNN.clicked.connect(lambda: forecast())
        mainUI.ModelComboBoxRNN.currentIndexChanged.connect(clearUI)
        mainUI.ResultTrendsButtonRNN.clicked.connect(showResultTrends)
        mainUI.administrator_button.clicked.connect(openAdministratorWindow)
        mainUI.StartTrendsButtonRNN.clicked.connect(showSourceTrendsForecast)
    if type(ui) == Ui_DatabaseWindow_Ru or type(ui) == Ui_DatabaseWindow_Eng:
        databaseUI.deleteButton.clicked.connect(deleteModel)
def initializeUi(ui):
    if type(ui) == Ui_AdministratorWindow_Ru or type(ui) == Ui_AdministratorWindow_Eng:
        administratorUI.progressBar.setMinimum(0)
        administratorUI.progressBar.setValue(0)
    if type(ui) == Ui_MainWindow_Ru or type(ui) == Ui_MainWindow_Eng:
        mainUI.progressBar.setMinimum(0)
        mainUI.progressBar.setValue(0)

#########################################################################################################
def showResultTrends():
    rnn.showResultDataTrends(dbw)
def showRoc():
    rnn.showRocTrend()
def clearUI():
    global rnn
    rnn = RnnModel(language=settings['Language'])
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
        rnn = RnnModel(language=settings['Language'], name="", dbw=dbw, parameters=getCheckedParameters(administratorUI.RelevantFeaturesRNN),
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
                    administratorUI.PrecisionRNN.setText(str(round(float(rnn.precision), 4)))
                    administratorUI.RecallRNN.setText(str(round(float(rnn.recall), 4)))
                    administratorUI.RmseRNN.setText(str(round(float(rnn.RMSE), 4)))
                    administratorUI.MapeRNN.setText(str(round(float(rnn.MAPE), 4)))
                    administratorUI.AucRNN.setText(str(round(float(rnn.AUC), 4)))
                    administratorUI.MseRNN.setText(str(round(float(rnn.MSE), 4)))
                    administratorUI.MaeRNN.setText(str(round(float(rnn.MAE), 4)))
                    administratorUI.F1RNN.setText(str(round(float(rnn.F1), 4)))
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
    tmpRnn = RnnModel(language=settings['Language'], name="", dbw=dbw, parameters=getCheckedParameters(administratorUI.RelevantFeaturesRNN),
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
def loadData():
    print("Начало загрузки данных...")
    dbw.loadData(settings['Language'], str(settings['FromDateTime']), str(settings['ToDateTime']))
    print(Fore.GREEN + "Данные успешно загружены")

#Main
def selectModel():
    print("Загрузка модели...")
    if mainUI.ModelComboBoxRNN.currentText != "":
        clearUI()
        global rnn
        selectedModel = mainUI.ModelComboBoxRNN.currentText()
        rnn = RnnModel(language=settings['Language'], dbw=dbw, name=selectedModel)
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
            mainUI.PrecisionRNN.setText(str(round(float(rnn.precision), 4)))
            mainUI.RecallRNN.setText(str(round(float(rnn.recall), 4)))
            mainUI.RmseRNN.setText(str(round(float(rnn.RMSE), 4)))
            mainUI.MapeRNN.setText(str(round(float(rnn.MAPE), 4)))
            mainUI.AucRNN.setText(str(round(float(rnn.AUC), 4)))
            mainUI.MseRNN.setText(str(round(float(rnn.MSE), 4)))
            mainUI.MaeRNN.setText(str(round(float(rnn.MAE), 4)))
            mainUI.F1RNN.setText(str(round(float(rnn.F1), 4)))
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
    loadData()
    if dbw.isDataLoaded:
        openMainWindow()
        sys.exit(app.exec_())
    else:
        sys.exit()