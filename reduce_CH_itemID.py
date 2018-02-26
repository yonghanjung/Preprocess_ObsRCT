import pandas as pd
import numpy as np
import pickle

class reduce_CH_itemID(object):
    def __init__(self):
        self.reduced_CH = pickle.load(open('PKL/CH_ARDS_reduced.pkl','rb'))
        self.key_VT = [639, 654, 681, 682, 683, 684, 224685, 224684, 224686]
        self.key_FiO2 = [190, 2981]
        self.key_PP = [543]
        self.key_PEEP = [60, 437, 505, 506, 686, 220339, 224700]
        # self.key_PIP = [221, 1, 1211, 1655, 2000, 226873, 224738, 224419, 224750, 227187]
        self.key_insTime_pct = [1, 1211]
        self.key_insTime = [1655, 2000, 224738]
        # self.key_insratio = [226873]
        # self.key_PIP = [,224750,227187]
        self.key_MV = [445, 448, 449, 450, 1340, 1486, 1600, 224687]

        self.key_PaO2 = [779]
        self.key_SpO2 = [646]
        self.HeartRate = [211, 220045]
        self.ResRate = [618, 615, 220210, 224690]

        self.MV_items = [self.key_VT, self.key_FiO2, self.key_PP,
                         self.key_PEEP, self.key_insTime, self.key_MV
                         ]
        self.Bio_items = [self.key_PaO2, self.key_SpO2, self.HeartRate, self.ResRate]
        self.MV_items_name = ['VT', 'FiO2', 'PP', 'PEEP', 'PIP', 'MV']
        self.Bio_items_name = ['PaO2', 'SpO2', 'HeartRate', 'ResRate']


