import pandas as pd
import numpy as np
import scipy as sp
import pickle

class ARDS_CH_reducer(object):
    def __init__(self):
        self.CH_ARDS = pickle.load(open('PKL/CH_ARDS_reduced.pkl', 'rb' ))
        self.ARDS_ID = pickle.load(open('PKL/ARDS_ID.pkl', 'rb'))
        self.ARDS_ONSET = pickle.load(open('PKL/ARDS_ONSETTIME.pkl', 'rb'))
        self.ARDS_DOD = pickle.load(open('PKL/ARDS_DOD.pkl', 'rb'))
        # self.VENT = pd.read_csv('ventsettings.csv')

        self.key_VT = [639, 654, 681, 682, 683, 684, 224685, 224684, 224686]
        self.key_FiO2 = [190, 2981]
        self.key_PP = [543]
        self.key_PEEP = [60, 437, 505, 506, 686, 220339, 224700]
        # self.key_PIP = [221, 1, 1211, 1655, 2000, 226873, 224738, 224419, 224750, 227187]
        # self.key_insTime_pct = [1, 1211]
        # self.key_insTime = [1655, 2000, 224738]
        # self.key_insratio = [226873]
        # self.key_PIP = [,224750,227187]
        self.key_MV = [445, 448, 449, 450, 1340, 1486, 1600, 224687]

        self.key_PaO2 = [779]
        self.key_SpO2 = [646]
        self.HeartRate = [211, 220045]
        self.ResRate = [618, 615, 220210, 224690]
        self.pH = [780, 1126]

        self.key_Vent = [self.key_PEEP, self.key_FiO2, self.key_PP, self.key_VT, self.key_MV]
        self.O2_vital = [self.key_PaO2, self.key_SpO2, self.HeartRate, self.ResRate, self.pH]
        self.vent_name = ['PEEP', 'FiO2', 'PP', 'VT', 'MV']
        self.O2_vital_name = ['PaO2', 'SpO2', 'HeartRate', 'ResRate', 'pH']

    def reduce_CH_by_ItemID(self):
        ItemID_list = []
        for l in self.key_Vent:
            ItemID_list += l
        for l in self.O2_vital:
            ItemID_list += l

        reduced_CH = self.CH_ARDS[self.CH_ARDS['ITEMID'].isin(ItemID_list)]
        return reduced_CH

    def Execute(self):
        reduced_CH = self.reduce_CH_by_ItemID()
        pickle.dump(reduced_CH, open('PKL/ARDS_reduced_CH.pkl','wb'))
        print("Job completed")


if __name__ == '__main__':
    CH_reducer = ARDS_CH_reducer()
    CH_reducer.Execute()