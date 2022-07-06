from tsfresh import extract_relevant_features, extract_features
from sklearn import linear_model
import numpy as np
from tsfresh.feature_extraction import settings
from tsfresh.utilities.dataframe_functions import roll_time_series
import pandas as pd
import tkinter
from tkinter import messagebox as mb


class TSA:
    nneighboursUMAP = 5
    minimaldistanseUMAP = 0.1
    nneighboursDBSCAN = 5
    minimaldistanseDBSCAN = 0.8

    usefilter = True
    settings = settings.ComprehensiveFCParameters() #default settings
    settingsIndex = 0 #default settings index
    timeshift = 50 #default timeshift
    defects = [] #raw defect
    rolleddef =[] #rolled defect
    dfy = [] #target vector y
    timeseries = [] #raw data
    rolledts = [] #rolled time series
    filteredfeatures = [] #features after filtering

    def SetSettings(self, currentSetting):
        self.settingsIndex = currentSetting
        if (currentSetting == 0):
            self.settings = settings.ComprehensiveFCParameters()
        if (currentSetting == 1):
            self.settings = settings.MinimalFCParameters()
        if (currentSetting == 2):
            #self.settings = settings.EfficientFCParameters()
            #"autocorrelation": [{"lag": 2}, {"lag": 4}, {"lag": 6}, {"lag": 8}]
            self.settings = {
                "absolute_maximum": None,
                "absolute_sum_of_changes": None,
                "variance": None,
                "standard_deviation": None,
                "sample_entropy": None,
                "percentage_of_reoccurring_values_to_all_values": None,
                "number_cwt_peaks": [{"n":self.timeshift}],
                "median": None,
                "mean_change": None,
                "kurtosis": None,
                "mean": None
            }


    def TimeSeriesAnalyser(self, parameters, defects, defectlimit):
        self.defects = defects
        self.timeseries = parameters
        if (self.defects.empty or self.timeseries.empty):
            mb.showerror("Ошибка", "Был выбран некорректный временной интервал")
            return False
        self.rolledts = self.RollTimeSeries(parameters)
        self.rolleddef = self.RollTimeSeries(defects)
        self.dfy = self.rolleddef.groupby("id", sort=False)[self.defects.columns.values[0]].max() >= defectlimit
        try:
            if(self.usefilter):
                self.filteredfeatures = self.ExtractRelevantFeatures()
            else:
                self.filteredfeatures = self.ExtractFeatures()
        except AssertionError:
            mb.showerror("Ошибка", "Временной интервал оказался слишком мал")
            return False
        return True

    def RollTimeSeries(self, timeSeries):
        return roll_time_series(timeSeries, column_id="id", column_sort="time", max_timeshift=self.timeshift, min_timeshift=self.timeshift)

    def ExtractRelevantFeatures(self):
        return extract_relevant_features(self.rolledts, self.dfy, column_id='id', column_sort='time', default_fc_parameters=self.settings)

    def ExtractFeatures(self):
        return extract_features(self.rolledts,  column_id='id', column_sort='time',
                                         default_fc_parameters=self.settings)
