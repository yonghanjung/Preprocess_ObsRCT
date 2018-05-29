import numpy as np
import scipy as sp
import pandas as pd
import pickle

class ARDS_firstday():
    def __init__(self):
        self.bloodgas = pd.read_csv('Firstday/bloodgasfirstdayarterial.csv')
        self.gcs = pd.read_csv('Firstday/gcsfirstday.csv')
        self.uo = pd.read_csv('Firstday/uofirstday.csv')
        self.vitals = pd.read_csv('Firstday/vitalfirstday.csv')
        labs = pd.read_csv('Firstday/labsfirstday.csv')
        self.labs_crea = labs[['subject_id', 'hadm_id', 'icustay_id', 'creatinine_min','creatinine_max']]

    def firstday_merge(self):
        merged = pd.merge(self.bloodgas, self.gcs, on=['subject_id', 'hadm_id', 'icustay_id'])
        merged = pd.merge(merged, self.uo, on=['subject_id', 'hadm_id', 'icustay_id'])
        merged = pd.merge(merged, self.vitals, on=['subject_id', 'hadm_id', 'icustay_id'])
        merged = pd.merge(merged, self.labs_crea, on=['subject_id', 'hadm_id', 'icustay_id'])
        return merged

if __name__ == '__main__':
    firstday = ARDS_firstday()
    merged = firstday.firstday_merge()
    pickle.dump(merged, open('PKL/ARDS_firstday.pkl', 'wb'))






