import numpy as np
import scipy as sp
import pandas as pd
import pickle
import datetime

class ARDS_vent():
    def __init__(self):
        self.CH_ARDS = pickle.load(open('PKL/CH_ARDS_reduced.pkl','rb'))
        self.ARDS_ID = pickle.load(open('PKL/ARDS_ID.pkl','rb'))
        self.ARDS_ONSET = pickle.load(open('PKL/ARDS_ONSETTIME.pkl', 'rb'))
        self.ARDS_DOD = pickle.load(open('PKL/ARDS_DOD.pkl','rb'))
        self.VENT = pd.read_csv('ventsettings.csv')

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
        self.HeartRate = [211,220045]
        self.ResRate = [618,615,220210,224690]
        self.pH = [780, 1126]

        self.key_Vent = [self.key_PEEP, self.key_FiO2, self.key_PP, self.key_VT, self.key_MV]
        self.O2_vital = [self.key_PaO2, self.key_SpO2, self.HeartRate, self.ResRate, self.pH]
        self.vent_name= ['PEEP', 'FiO2', 'PP', 'VT', 'MV']
        self.O2_vital_name = ['PaO2','SpO2','HeartRate','ResRate','pH']

    def hour_difference(self,time_obj1, time_obj2):
        return abs(time_obj1.value - time_obj2.value)/(10**9 * 60 * 60)

    def days_difference(self,time_obj1, time_obj2):
        return round(abs(time_obj1.value - time_obj2.value) / (10 ** 9 * 86400),2)

    def MV_duration(self, icuid):
        icuid_duration = pd.to_datetime(self.VENT['charttime'][self.VENT['icustay_id'] == icuid])
        if len(icuid_duration) >= 2:
            return self.days_difference(max(icuid_duration),min(icuid_duration))
        elif len(icuid_duration) == 1:
            return 0
        else:
            return np.nan

    def PT_ARDS_onset(self, subject_id):
        return self.ARDS_ONSET['ARDS_ONSETTIME'][self.ARDS_ONSET['SUBJECT_ID']==subject_id].iloc[0]

    def Check_Mortality(self, subject_id):
        subject_DOD = list(self.ARDS_DOD[['28-SURVIVAL', '60-SURVIVAL', '90-SURVIVAL']][self.ARDS_DOD['SUBJECT_ID'] == subject_id].iloc[0])
        if subject_DOD == [1,1,1]:
            return 1
        else:
            return 0

    def Chart_var_collector(self, itemid, subject_id, init_TF):
        subject_ARDS_onset = self.PT_ARDS_onset(subject_id)
        icuid = self.ARDS_ID['ICUID'][self.ARDS_ID['SUBJECT_ID'] == subject_id].iloc[0]
        subject_MV_duration = self.MV_duration(icuid)
        if init_TF == True:
            subject_ARDS_MV_end = subject_ARDS_onset + datetime.timedelta(days = 2)
        else:
            subject_ARDS_MV_end = subject_ARDS_onset + datetime.timedelta(days = subject_MV_duration+1)

        mask1 = ((self.CH_ARDS['SUBJECT_ID'] == subject_id) &
                (self.CH_ARDS['ICUSTAY_ID'] == icuid) &
                (self.CH_ARDS['ITEMID'].isin(itemid)) &
                 (pd.isnull(self.CH_ARDS['VALUE']) == False)
                 )

        subject_CH = self.CH_ARDS[mask1]
        mask2 = (
                 (pd.to_datetime(subject_CH['CHARTTIME']) >=  subject_ARDS_onset) &
                 (pd.to_datetime(subject_CH['CHARTTIME'])  <= subject_ARDS_MV_end)
                )

        subject_CH = subject_CH[mask2]
        return subject_CH

if __name__ == '__main__':
    vent = ARDS_vent()





