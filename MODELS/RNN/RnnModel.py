import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import pandas
pandas.options.mode.chained_assignment = None

import numpy
import matplotlib
import tensorflow
import keras.backend

from datetime import datetime
from matplotlib import pyplot

class RnnModel:
    key             = 0
    name            = ""

    defect          = 0
    features        = []
    parameters      = []
    
    batch           = 32
    epochs          = 20
    optimizer       = tensorflow.optimizers.Nadam()
    lstm_model      = tensorflow.keras.models.Sequential()

    dataframe       = 0
    rawDataframe    = 0

    resultReal      = 0
    resultForecast  = 0

    testReal        = 0
    testForecast    = 0
    
    val_df          = 0
    test_df         = 0
    full_df         = 0
    train_df        = 0

    history         = 0

    MSE             = 0
    MAE             = 0
    RMSE            = 0
    MAPE            = 0

    TPR             = []
    FPR             = []

    F1              = 0
    AUC             = 0
    recall          = 0
    precision       = 0

    language = ''

    optimizers = {
        'SGD'       : tensorflow.optimizers.SGD(),
        'Adam'      : tensorflow.optimizers.Adam(),
        'Nadam'     : tensorflow.optimizers.Nadam(),
        'Adamax'    : tensorflow.optimizers.Adamax(),
        'RMSprop'   : tensorflow.optimizers.RMSprop(),
        'Adagrad'   : tensorflow.optimizers.Adagrad(),
        'Adadelta'  : tensorflow.optimizers.Adadelta()
    }

    def __init__(self, **kwargs):
        self.language = kwargs['language']
        if(len(kwargs) > 1):
            self.name = kwargs['name']
            self.initializeModel(kwargs)                
            self.initializeDataframes(kwargs['dbw'])
    def initializeModel(self, kwargs):
        self.lstmModel  = self.lstm_model = tensorflow.keras.models.Sequential([
                tensorflow.keras.layers.BatchNormalization(),
                tensorflow.keras.layers.LSTM(128, activation='tanh', return_sequences=True),
                tensorflow.keras.layers.Dropout(0.4),
                tensorflow.keras.layers.Dense(units=1)
            ])
        if self.name != "":
            self.key        = int(kwargs['dbw'].loadModel(self.name))
            self.batch      = int(kwargs['dbw'].getModelBatch(self.key))
            self.epochs     = int(kwargs['dbw'].getModelEpochs(self.key))
            self.defect     = kwargs['dbw'].getModelPredictableDefect(self.key)
            self.parameters = kwargs['dbw'].getModelRelevantParameters(self.key)
            self.optimizer  = self.optimizers[kwargs['dbw'].getModelOptimizer(self.key)]
            self.lstm_model.build(input_shape=(None, 128, len(self.parameters) + 1))
            self.lstmModel.load_weights(self.name + '.h5')
            os.remove(self.name + '.h5')
        else:
            self.defect     = kwargs['defect']
            self.parameters = kwargs['parameters']
            self.batch      = int(kwargs['batch'])
            self.epochs     = int(kwargs['epochs'])
            self.optimizer  = self.optimizers[kwargs['optimizer']]        
        self.features = []
        self.features.append(kwargs['dbw'].getIdFromDict(kwargs['dbw'].names, self.defect))
        for parameter in self.parameters:
            self.features.append(kwargs['dbw'].getIdFromDict(kwargs['dbw'].names, parameter))
    def initializeDataframes(self, dbw):
        df = pandas.DataFrame.from_dict(dbw.allWithDates)
        self.dataframe = df[self.features]
        self.dataframe.index = pandas.to_datetime(df['dt'])
        self.rawDataframe = self.dataframe.copy(deep=True)
        for feat in self.features:
            self.dataframe[[feat]] = self.scale(self.dataframe[[feat]], self.rawDataframe[[feat]].max(), self.rawDataframe[[feat]].min(), 1, -1)
        self.val_df     = self.dataframe[int(len(self.dataframe)*0.7):int(len(self.dataframe)*0.9)]
        self.train_df   = self.dataframe[:int(len(self.dataframe)*0.7)]
        self.test_df    = self.dataframe[int(len(self.dataframe)*0.9):]
        self.full_df    = self.dataframe
    
    def getMetrics(self, dbw):
        if self.name != "":
            self.MSE, self.RMSE, self.MAE, self.MAPE = dbw.getModelMetrics(self.key)
        else:
            self.MSE    = self.history.history['mean_squared_error'][len(self.history.history['mean_squared_error'])-1]
            self.MAE    = self.history.history['mean_absolute_error'][len(self.history.history['mean_absolute_error'])-1]
            self.RMSE   = self.history.history['root_mean_squared_error'][len(self.history.history['root_mean_squared_error'])-1]
            self.MAPE   = self.history.history['mean_absolute_percentage_error'][len(self.history.history['mean_absolute_percentage_error'])-1]
        
        TP, FP, TN, FN  = self.getClassifiers(dbw, dbw.getDefectThreshold(dbw.getIdFromDict(dbw.names, self.defect)))
        if (TP + FP) == 0:
            self.precision  = 1
        else:
            self.precision  = TP / (TP + FP)
        if (TP + FN) == 0:
            self.recall     = 1
        else:    
            self.recall     = TP / (TP + FN)
        if (self.precision + self.recall) == 0:
            self.F1         = 1
        else:
            self.F1         = 2 * ((self.precision * self.recall) / (self.precision + self.recall))
        self.getRocAuc(dbw)
        return True
    def getDescription(self, dbw):
        if self.language == 'Ru':
            return (f"Модель: {self.name}.\n\n"
                f"Модель обучена для прогнозирования:\n  ['{self.defect}'].\n\nC учетом влияния следующих параметров:\n  {self.parameters}.\n\n" 
                f"Модель обучена на данных от {dbw.getFromModelDate(self.key)} до {dbw.getToModelDate(self.key)}\n\n"
                f"Параметры модели: \n"
                f"  Оптимизатор: {dbw.getIdFromDict(self.optimizers, self.optimizer)};\n"
                f"  Размер пакета: {self.batch};\n"
                f"  Число эпох: {self.epochs}.")
        else:
            return (f"Model: {self.name}.\n\n"
                f"Model trained for prediction:\n  ['{self.defect}'].\n\nC учетом влияния следующих параметров:\n  {self.parameters}.\n\n" 
                f"Model trained on dataset from {dbw.getFromModelDate(self.key)} to {dbw.getToModelDate(self.key)}\n\n"
                f"Model parameters: \n"
                f"  Optimizer: {dbw.getIdFromDict(self.optimizers, self.optimizer)};\n"
                f"  Batch size: {self.batch};\n"
                f"  Epochs: {self.epochs}.")

    def learn(self, dbw):
        window = WindowGenerator(128, 128, 1, self.train_df, self.val_df, self.test_df, self.batch, [dbw.getIdFromDict(dbw.names, self.defect)], False)
        self.lstm_model.compile(loss=tensorflow.losses.MeanSquaredError(), optimizer=self.optimizer,
                                metrics=[tensorflow.metrics.MeanSquaredError(), tensorflow.metrics.RootMeanSquaredError(),
                                        tensorflow.metrics.MeanAbsoluteError(), tensorflow.metrics.MeanAbsolutePercentageError()])
        self.history = self.lstm_model.fit(window.train, epochs=self.epochs, validation_data=window.val)
        return True
    def forecast(self, dbw, state):
        wide_window = WindowGenerator(len(self.dataframe), len(self.dataframe), 0, self.full_df, self.val_df, self.test_df, self.batch, [dbw.getIdFromDict(dbw.names, self.defect)], False)
        inputs = wide_window.example
        predictions = self.lstm_model.predict(inputs)
        real = list()
        for element in keras.backend.batch_get_value(inputs[0][:][0]):
            real.append(element[0])
        result = predictions[0, :, 0]
        self.resultReal = self.dataframe.copy(deep=True)
        self.resultForecast = self.dataframe.copy(deep=True)
        self.resultReal[dbw.getIdFromDict(dbw.names, self.defect)] = real
        self.resultForecast[dbw.getIdFromDict(dbw.names, self.defect)] = result
        for feat in self.features:
            self.resultReal[[feat]] = self.unscale(self.resultReal[[feat]], self.rawDataframe[[feat]].max(), self.rawDataframe[[feat]].min(), 1, -1)
            self.resultForecast[[feat]] = self.unscale(self.resultForecast[[feat]], self.rawDataframe[[feat]].max(), self.rawDataframe[[feat]].min(), 1, -1) 
        for i in range(len(self.resultForecast[dbw.getIdFromDict(dbw.names, self.defect)])):
            if self.resultForecast[dbw.getIdFromDict(dbw.names, self.defect)][i] < 0:
                self.resultForecast[dbw.getIdFromDict(dbw.names, self.defect)][i] = 0
        self.testReal = self.resultReal.copy(deep=True)
        self.testReal = self.testReal[int(len(self.testReal)*0.9):]
        self.testForecast = self.resultForecast.copy(deep=True)
        self.testForecast = self.testForecast[int(len(self.testForecast)*0.9):]
        return True
    def save(self, dbw, name):
        name = name + '_' + datetime.now().strftime("%m.%d.%Y_%H-%M-%S")
        self.lstm_model.save_weights(name + '.h5')
        key = dbw.saveModel(name)
        os.remove(name + '.h5')
        dbw.saveModelMetrics(key, self.MAE, self.MAPE, self.MSE, self.RMSE)
        dbw.saveModelParameters(key, dbw.getIdFromDict(dbw.optimizers, dbw.getIdFromDict(self.optimizers, self.optimizer)), dbw.getIdFromDict(dbw.batches, str(self.batch)), dbw.getIdFromDict(dbw.epochs, str(self.epochs)))
        dbw.saveModelFeatures(key, self.features)
        return True

    def scale(self, values, values_max, values_min, max, min):
        return (((values - values_min) * (max - min)) / (values_max - values_min)) + min
    def unscale(self, values, values_max, values_min, max, min):
        return (((values - min) * (values_max - values_min)) / (max - min)) + values_min

    def showRocTrend(self):
        matplotlib.rcParams['figure.figsize'] = (5, 5)
        matplotlib.rcParams['axes.grid'] = True
        pyplot.plot(self.FPR, self.TPR, label='ROC curve')
        pyplot.plot([0, 1], [0, 1])
        pyplot.xlim([-0.1, 1.1])
        pyplot.ylim([-0.1, 1.1])
        if self.language == 'Ru':
            pyplot.xlabel('Доля ложных положительных классификаций')
            pyplot.ylabel('Доля верных положительных классификаций')
            pyplot.title('ROC кривая')
        else:
            pyplot.xlabel('False Positive Rate')
            pyplot.ylabel('True Positive Rate')
            pyplot.title('ROC-curve')
        pyplot.show()
    def showSourceDataTrends(self, dbw):
        fig = pyplot.figure(figsize=(10, len(self.features) * 2))
        gs = fig.add_gridspec(len(self.features), 1)
        for i in range(len(self.features)):
            ax = fig.add_subplot(gs[i, 0])
            pyplot.plot(self.rawDataframe.index.values, self.rawDataframe[self.features[i]])
            ax.set_title(dbw.getParameterName(dbw.names, self.features[i]))
            ax.set_ylabel(dbw.getParameterUnit(self.features[i]))
            if self.language == 'Ru':
                ax.set_xlabel("Время")
            else:
                ax.set_xlabel("Time")
        fig.tight_layout()
        pyplot.show()
    def showResultDataTrends(self, dbw):
        matplotlib.rcParams['figure.figsize'] = (10, 5)
        matplotlib.rcParams['axes.grid'] = True
        if self.language == 'Ru':
            pyplot.plot(self.resultReal.index.values, self.resultReal[dbw.getIdFromDict(dbw.names, self.defect)], label='Реальное значение дефекта')
            pyplot.plot(self.resultForecast.index.values, self.resultForecast[dbw.getIdFromDict(dbw.names, self.defect)], label='Предсказанное значение дефекта')
            pyplot.axhline(dbw.getDefectThreshold(dbw.getIdFromDict(dbw.names, self.defect)), label='Регламентное ограничение')
        else:
            pyplot.plot(self.resultReal.index.values, self.resultReal[dbw.getIdFromDict(dbw.names, self.defect)], label='Real values')
            pyplot.plot(self.resultForecast.index.values, self.resultForecast[dbw.getIdFromDict(dbw.names, self.defect)], label='Predicted values')
            pyplot.axhline(dbw.getDefectThreshold(dbw.getIdFromDict(dbw.names, self.defect)), label='Regulatory restriction')
        pyplot.ylabel(dbw.getParameterUnit(dbw.getIdFromDict(dbw.names, self.defect)))
        if self.language == 'Ru':
            pyplot.xlabel("Время")
        else:
            pyplot.xlabel("Time")
        pyplot.title(self.defect)
        pyplot.gca().legend(loc='upper left')
        pyplot.show()
    def showHistoryTrends(self):
        epochs = list()
        for i in range(len(self.history.history['mean_squared_error'])):
            epochs.append(i+1)
        fig = pyplot.figure(figsize=(10, 10))
        gs = fig.add_gridspec(2, 2)
        ax = fig.add_subplot(gs[0, 0])
        if self.language == 'Ru':
            pyplot.plot(epochs, self.history.history['mean_absolute_error'], label='обучение')
            pyplot.plot(epochs, self.history.history['val_mean_absolute_error'], label='валидация')
        else:
            pyplot.plot(epochs, self.history.history['mean_absolute_error'], label='learning')
            pyplot.plot(epochs, self.history.history['val_mean_absolute_error'], label='validation')
        ax.set_title("MAE")
        if self.language == 'Ru':
            ax.set_xlabel("Эпоза")
        else:
            ax.set_xlabel("Epoch")
        ax.legend(loc='upper left')
        ax = fig.add_subplot(gs[0, 1])
        if self.language == 'Ru':
            pyplot.plot(epochs, self.history.history['mean_absolute_percentage_error'], label='обучение')
            pyplot.plot(epochs, self.history.history['val_mean_absolute_percentage_error'], label='валидация')
        else:
            pyplot.plot(epochs, self.history.history['mean_absolute_percentage_error'], label='learning')
            pyplot.plot(epochs, self.history.history['val_mean_absolute_percentage_error'], label='validation')
        ax.set_title("MAPE")
        if self.language == 'Ru':
            ax.set_xlabel("Эпоза")
        else:
            ax.set_xlabel("Epoch")
        ax.legend(loc='upper left')
        ax = fig.add_subplot(gs[1, 0])
        if self.language == 'Ru':
            pyplot.plot(epochs, self.history.history['mean_squared_error'], label='обучение')
            pyplot.plot(epochs, self.history.history['val_mean_squared_error'], label='валидация')
        else:
            pyplot.plot(epochs, self.history.history['mean_squared_error'], label='learning')
            pyplot.plot(epochs, self.history.history['val_mean_squared_error'], label='validation')
        ax.set_title("MSE")
        if self.language == 'Ru':
            ax.set_xlabel("Эпоза")
        else:
            ax.set_xlabel("Epoch")
        ax.legend(loc='upper left')
        ax = fig.add_subplot(gs[1, 1])
        if self.language == 'Ru':
            pyplot.plot(epochs, self.history.history['root_mean_squared_error'], label='обучение')
            pyplot.plot(epochs, self.history.history['val_root_mean_squared_error'], label='валидация')
        else:
            pyplot.plot(epochs, self.history.history['root_mean_squared_error'], label='learning')
            pyplot.plot(epochs, self.history.history['val_root_mean_squared_error'], label='validation')
        ax.set_title("RMSE")
        if self.language == 'Ru':
            ax.set_xlabel("Эпоза")
        else:
            ax.set_xlabel("Epoch")
        ax.legend(loc='upper left')
        fig.tight_layout()
        pyplot.show()   

    def getRocAuc(self, dbw):
        thresholds = numpy.linspace(0, dbw.getDefectThreshold(dbw.getIdFromDict(dbw.names, self.defect)))
        for i in thresholds:            
            TP, FP, TN, FN = self.getClassifiers(dbw, i)
            if (TP + FN) != 0:
                t = TP / (TP + FN)
                self.TPR.append(t)
            else:
                self.TPR.append(1)
            if (FP + TN) != 0:
                t = FP / (FP + TN)
                self.FPR.append(t)
            else:
                self.FPR.append(1)
        self.TPR.sort()
        self.FPR.sort()
        for i in range(len(thresholds) - 1):
            self.AUC = self.AUC + (((self.TPR[i] + self.TPR[i + 1]) / 2) * (self.FPR[i + 1] - self.FPR[i]))
    def getClassifiers(self, dbw, threshold, tollerance=0):
        TP = 0
        FP = 0
        TN = 0
        FN = 0
        for i in range(len(self.testForecast)):
            if self.testForecast[dbw.getIdFromDict(dbw.names, self.defect)][i] >= threshold:
                if self.testReal[dbw.getIdFromDict(dbw.names, self.defect)][i] >= threshold:
                    TN = TN + 1
                else:
                    FN = FN + 1
            else:
                if self.testReal[dbw.getIdFromDict(dbw.names, self.defect)][i] < threshold:
                    TP = TP + 1
                else:
                    FP = FP + 1
        return (TP, FP, TN, FN)

class WindowGenerator():
    def __init__(self, input_width, label_width, shift, train_df, val_df, test_df, batch, label_columns, shuffle):
        self.shuffle = shuffle
        self.batch = batch
        self.train_df = train_df
        self.val_df = val_df
        self.test_df = test_df
        self.label_columns = label_columns
        if label_columns is not None:
            self.label_columns_indices = {name: i for i, name in enumerate(label_columns)}
        self.column_indices = {name: i for i, name in enumerate(train_df.columns)}
        self.input_width = input_width
        self.label_width = label_width
        self.shift = shift
        self.total_window_size = input_width + shift
        self.input_slice = slice(0, input_width)
        self.input_indices = numpy.arange(self.total_window_size)[self.input_slice]
        self.label_start = self.total_window_size - self.label_width
        self.labels_slice = slice(self.label_start, None)
        self.label_indices = numpy.arange(self.total_window_size)[self.labels_slice]
    def split_window(self, features):
        inputs = features[:, self.input_slice, :]
        labels = features[:, self.labels_slice, :]
        if self.label_columns is not None:
            labels = tensorflow.stack(
                [labels[:, :, self.column_indices[name]] for name in self.label_columns],
                axis=-1)
        inputs.set_shape([None, self.input_width, None])
        labels.set_shape([None, self.label_width, None])
        return inputs, labels
    def __repr__(self):
        return '\n'.join([
            f'Total window size: {self.total_window_size}',
            f'Input indices: {self.input_indices}',
            f'Label indices: {self.label_indices}',
            f'Label column name(s): {self.label_columns}'])
    def make_dataset(self, data):
        data = numpy.array(data, dtype=numpy.float32)
        ds = tensorflow.keras.utils.timeseries_dataset_from_array(
            data=data,
            targets=None,
            sequence_length=self.total_window_size,
            sequence_stride=1,
            shuffle=self.shuffle,
            batch_size=self.batch)
        ds = ds.map(self.split_window)
        return ds
    @property
    def train(self):
        return self.make_dataset(self.train_df)
    @property
    def val(self):
        return self.make_dataset(self.val_df)
    @property
    def test(self):
        return self.make_dataset(self.test_df)
    @property
    def example(self):
        result = getattr(self, '_example', None)
        if result is None:
            result = next(iter(self.train))
            self._example = result
        return result