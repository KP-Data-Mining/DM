import sqlite3
import math

PATH = 'extcaland.db'

class dbWorker:
    isDataLoaded = False
    
    minDate = ''
    maxDate = ''

    dates = list()       
    
    parameters  = dict() #[id] = [code]              для всех параметров
    features    = dict() #[id] = [code]              для управляющих воздействий
    defects     = dict() #[id] = [code]              для выходных параметров
    ruNames     = dict() #[id] = [ruName]            для всех параметров
    enNames     = dict() #[id] = [enName]            для всех параметров
    
    limits = {}          #limit[id][0(min)/1(max)]   для всех параметров
    
    all = dict()         #[id] = [values]            для всех параметров
    x   = dict()         #[id] = [values]            для управляющих воздействий
    y   = dict()         #[id] = [values]            для выходных параметров

    #RNN
    models          = dict()
    epochs          = dict()
    batches         = dict()
    optimizers      = dict()
    allWithDates    = dict()

    def __init__(self):
        self.getMinMaxDates()    
    def getMinMaxDates(self):
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        cursor.execute( f" SELECT MIN(DateTime)"
                        f" FROM ParameterValues"
                        f" WHERE LENGTH(DateTime) = LENGTH('yyyy-mm-dd hh:mm:ss')" )
        minDate = cursor.fetchall()
        cursor.execute( f" SELECT MAX(DateTime)"
                        f" FROM ParameterValues"
                        f" WHERE LENGTH(DateTime) = LENGTH('yyyy-mm-dd hh:mm:ss')" )
        maxDate = cursor.fetchall()
        self.minDate = str(minDate[0][0])
        self.maxDate = str(maxDate[0][0])        
        cursor.close()
        conn.close()
    
    def loadData(self, startDate, endDate):
        self.minDate = startDate
        self.maxDate = endDate
        self.loadRNNParameters()
        self.loadParameters()
        self.loadRNNModels()
        self.loadValues()
        self.isDataLoaded = True
    def loadRNNParameters(self):
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        cursor.execute( f" SELECT *" 
                        f" FROM NNCoefficients" )
        params_row = cursor.fetchall()
        for row_id in range(len(params_row)):
            if params_row[row_id][2] == 1:
                self.batches[params_row[row_id][0]] = params_row[row_id][1]
            if params_row[row_id][2] == 2:
                self.optimizers[params_row[row_id][0]] = params_row[row_id][1]
            if params_row[row_id][2] == 3:
                self.epochs[params_row[row_id][0]] = params_row[row_id][1]
        cursor.close()
        conn.close()
    def loadParameters(self):
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        cursor.execute( f" SELECT IdParameter, ParameterCode, ParameterNameRu, ParameterNameEng"
                        f" FROM Parameters"
                        f" WHERE IdParameterType == 2"
                        f" OR IdParameterType == 3" )
        params_row = cursor.fetchall()
        cursor.execute( f" SELECT Limits.IdParameter, LowLimitValue, HighLimitValue"
                        f" FROM Limits"
                        f" LEFT JOIN Parameters ON Parameters.IdParameter = Limits.IdParameter"
                        f" WHERE IdParameterType == 2"
                        f" OR IdParameterType == 3" )
        limits_row = cursor.fetchall()
        self.allWithDates['dt'] = list()
        for row_id in range(len(params_row)):
            self.ruNames[params_row[row_id][0]] = params_row[row_id][2]
            self.enNames[params_row[row_id][0]] = params_row[row_id][3]
            max = float('nan') if limits_row[row_id][2] is None else float(limits_row[row_id][2])
            self.limits[limits_row[row_id][0]] = max
            self.parameters[params_row[row_id][0]] = params_row[row_id][1]
            if params_row[row_id][1].split('.')[0] == 'Defects':
                self.defects[params_row[row_id][0]] = params_row[row_id][1]
                self.y[params_row[row_id][0]] = list()
            else:
                self.features[params_row[row_id][0]] = params_row[row_id][1]
                self.x[params_row[row_id][0]] = list()
            self.all[params_row[row_id][0]] = list()
            self.allWithDates[params_row[row_id][0]] = list()
        cursor.close()
        conn.close()
    def loadRNNModels(self):
        self.models.clear()
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        cursor.execute( f" SELECT *" 
                        f" FROM NNModels" )
        params_row = cursor.fetchall()
        for row_id in range(len(params_row)):
            self.models[params_row[row_id][0]] = params_row[row_id][1]
        cursor.close()
        conn.close()
    def loadValues(self):
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        cursor.execute( f" SELECT DateTime, group_concat(ParameterValues.IdParameter || ': ' || Value, ',')"
                        f" FROM ParameterValues"
                        f" LEFT JOIN Parameters ON Parameters.IdParameter = ParameterValues.IdParameter"
                        f" WHERE DateTime BETWEEN '{self.minDate}' AND '{self.maxDate}'"
                        f" AND IdParameterType == 2"
                        f" OR DateTime BETWEEN '{self.minDate}' AND '{self.maxDate}'"
                        f" AND IdParameterType == 3"
                        f" GROUP BY DateTime" )
        while True:
            row = cursor.fetchone()
            if row:
                row_time = row[0]
                row_parameters = row[1].split(',')
                row_values = self.initializeParametersDictionary()
                for parameter in row_parameters:
                    splited_parameter = parameter.split(':')
                    index = int(splited_parameter[0])
                    row_values[index] = round(float(splited_parameter[1]), 4)
                if self.isValidValues(row_values):
                    self.dates.append(row_time)
                    self.allWithDates['dt'].append(row_time)
                    for index in self.parameters:
                        if index in self.defects:
                            self.y[index].append(row_values[index])
                        else:
                            self.x[index].append(row_values[index])
                        self.all[index].append(row_values[index])
                        self.allWithDates[index].append(row_values[index])
            else:
                break
        cursor.close()
        conn.close()

    def initializeParametersDictionary(self):
        param = dict()
        for parameter in self.parameters:
            param[parameter] = float('nan')
        return param
    def isValidValues(self, values):
        for value in values:
            if math.isnan(values[value]):
                return False
        return True
    
    def getNames(self, names, parameters):
        result = list()
        for parameter in parameters:
            if names[parameter] != 'nan' and names[parameter] != "":
                result.append(names[parameter])
        return result
    def getParameterName(self, dict, id):
        return dict[id]
    def getParameterUnit(self, id):
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        cursor.execute( f" SELECT IdUnit"
                        f" FROM Parameters"
                        f" WHERE IdParameter == {id}")
        params_row = cursor.fetchall()
        unitId = str(params_row[0][0])
        cursor.execute( f" SELECT Sign"
                        f" FROM Units"
                        f" WHERE IdUnit == {unitId}")
        params_row = cursor.fetchall()
        return str(params_row[0][0])
    def getDefectThreshold(self, id):
        return self.limits[id]

    def loadModel(self, name):
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        cursor.execute( f" SELECT IdModel, Model" 
                        f" FROM NNModels"
                        f" WHERE Name == '{name}'")
        output_file = open(str(name) + ".h5", "wb")
        params_row = cursor.fetchone()
        output_file.write(params_row[1])
        cursor.close()
        conn.close()
        return params_row[0]
    def getModelPredictableDefect(self, key):
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        cursor.execute( f" SELECT IdParameter"
                        f" FROM NNModelRelevantParameters"
                        f" WHERE IdParameterType == 2"
                        f" AND IdModel == {key}" )
        params_row = cursor.fetchone()
        cursor.close()
        conn.close()
        return self.getParameterName(self.ruNames, params_row[0])
    def getModelRelevantParameters(self, key):
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        cursor.execute( f" SELECT IdParameter"
                        f" FROM NNModelRelevantParameters"
                        f" WHERE IdParameterType == 1"
                        f" AND IdModel == {key}" )
        params_row = cursor.fetchall()
        result = list()
        for row_id in range(len(params_row)):
            result.append(self.getParameterName(self.ruNames, params_row[row_id][0]))
        cursor.close()
        conn.close()
        return result
    def getModelBatch(self, key):
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        cursor.execute( f" SELECT IdCoefficient"
                        f" FROM NNModelCoefficients"
                        f" WHERE IdModel == {key}" )
        params_row = cursor.fetchall()
        for row_id in range(len(params_row)):
            cursor.execute( f" SELECT Value"
                        f" FROM NNCoefficients"
                        f" WHERE IdCoefficientType == 1"
                        f" AND IdCoefficient == {params_row[row_id][0]}" )
            res = cursor.fetchall()
            if len(res) != 0:
                cursor.close()
                conn.close()
                return res[0][0]
    def getModelEpochs(self, key):
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        cursor.execute( f" SELECT IdCoefficient"
                        f" FROM NNModelCoefficients"
                        f" WHERE IdModel == {key}" )
        params_row = cursor.fetchall()
        for row_id in range(len(params_row)):
            cursor.execute( f" SELECT Value"
                        f" FROM NNCoefficients"
                        f" WHERE IdCoefficientType == 3"
                        f" AND IdCoefficient == {params_row[row_id][0]}" )
            res = cursor.fetchall()
            if len(res) != 0:
                cursor.close()
                conn.close()
                return res[0][0]
    def getModelOptimizer(self, key):
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        cursor.execute( f" SELECT IdCoefficient"
                        f" FROM NNModelCoefficients"
                        f" WHERE IdModel == {key}" )
        params_row = cursor.fetchall()
        for row_id in range(len(params_row)):
            cursor.execute( f" SELECT Value"
                        f" FROM NNCoefficients"
                        f" WHERE IdCoefficientType == 2"
                        f" AND IdCoefficient == {params_row[row_id][0]}" )
            res = cursor.fetchall()
            if len(res) != 0:
                cursor.close()
                conn.close()
                return res[0][0]
    def getModelMetrics(self, key):
        MSE     = 0
        RMSE    = 0 
        MAE     = 0
        MAPE    = 0
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        cursor.execute( f" SELECT IdMetric, Value"
                        f" FROM NNModelMetrics"
                        f" WHERE IdModel == {key}" )
        params_row = cursor.fetchall()
        for row_id in range(len(params_row)):
            if int(params_row[row_id][0]) == 1:
                MSE = params_row[row_id][1]
            if int(params_row[row_id][0]) == 2:
                RMSE = params_row[row_id][1]
            if int(params_row[row_id][0]) == 3:
                MAE = params_row[row_id][1]
            if int(params_row[row_id][0]) == 4:
                MAPE = params_row[row_id][1]
        cursor.close()
        conn.close()
        return (MSE, RMSE, MAE, MAPE)
    def saveModel(self, name):
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        query = (   f" INSERT INTO NNModels"
                    f" (Name, FromDateTime, ToDateTime, Model)"
                    f" VALUES (?, ?, ?, ?)" )
        data = (name, self.minDate, self.maxDate, self.convertToBinaryData(name + '.h5'))
        cursor.execute(query, data)
        conn.commit()
        cursor.execute( f" SELECT IdModel, Model" 
                        f" FROM NNModels"
                        f" WHERE Name == '{name}'")
        params_row = cursor.fetchone()
        id = params_row[0]
        cursor.close()
        conn.close()
        return id
    def saveModelMetrics(self, key, MAE, MAPE, MSE, RMSE):
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        query = (   f" INSERT INTO NNModelMetrics"
                    f" (IdModel, IdMetric, Value)"
                    f" VALUES (?, ?, ?)" )
        data = (key, 1, MSE)
        cursor.execute(query, data)
        conn.commit()
        data = (key, 2, RMSE)
        cursor.execute(query, data)
        conn.commit()
        data = (key, 3, MAE)
        cursor.execute(query, data)
        conn.commit()
        data = (key, 4, MAPE)
        cursor.execute(query, data)
        conn.commit()
        cursor.close()
        conn.close()
    def saveModelParameters(self, key, optimizer, batch, epochs):
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        query = (   f" INSERT INTO NNModelCoefficients"
                    f" (IdModel, IdCoefficient)"
                    f" VALUES (?, ?)" )
        data = (key, optimizer)
        cursor.execute(query, data)
        conn.commit()
        data = (key, batch)
        cursor.execute(query, data)
        conn.commit()
        data = (key, epochs)
        cursor.execute(query, data)
        conn.commit()
        cursor.close()
        conn.close()
    def saveModelFeatures(self, key, features):
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        query = (   f" INSERT INTO NNModelRelevantParameters"
                    f" (IdModel, IdParameter, IdParameterType)"
                    f" VALUES (?, ?, ?)" )
        data = (key, features[0], 2)
        cursor.execute(query, data)
        conn.commit()
        features.pop(0)
        for feature in features:
            data = (key, feature, 1)
            cursor.execute(query, data)
            conn.commit()
        cursor.close()
        conn.close()

    def getIdFromDict(self, dict, name):
        for key, value in dict.items():
            if name == value:
                return key

    def convertToBinaryData(self, filename):
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData

    def getFromModelDate(self, key):
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        cursor.execute( f" SELECT FromDateTime" 
                        f" FROM NNModels"
                        f" WHERE IdModel == '{key}'")
        params_row = cursor.fetchone()
        cursor.close()
        conn.close()
        return params_row[0]
    def getToModelDate(self, key):
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        cursor.execute( f" SELECT ToDateTime" 
                        f" FROM NNModels"
                        f" WHERE IdModel == '{key}'")
        params_row = cursor.fetchone()
        cursor.close()
        conn.close()
        return params_row[0]
    
    def getModelsWithParameters(self):
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        cursor.execute( f" SELECT IdModel, Name, FromDateTime, ToDateTime"
                        f" FROM NNModels")
        params_row = cursor.fetchall()
        cursor.close()
        conn.close()
        return params_row
    def deleteModel(self, key):
        conn = sqlite3.connect(PATH)
        cursor = conn.cursor()
        cursor.execute( f"DELETE FROM NNModelCoefficients WHERE IdModel == '{key}'")
        conn.commit()
        cursor.execute( f"DELETE FROM NNModelMetrics WHERE IdModel == '{key}'")
        conn.commit()
        cursor.execute( f"DELETE FROM NNModelRelevantParameters WHERE IdModel == '{key}'")
        conn.commit()
        cursor.execute( f"DELETE FROM NNModels WHERE IdModel == '{key}'")
        conn.commit()
        cursor.close()
        conn.close()
        return True