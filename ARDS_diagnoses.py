import numpy as np
import scipy as sp
import pandas as pd
import pickle
import datetime

class ARDS_diagnoses():
    def __init__(self):
        self.DIAGNOSES = pd.read_csv('OLD/raw_data/DIAGNOSES_ICD.csv')
        self.ARDS_ID = pickle.load(open('PKL/ARDS_ID.pkl','rb'))
        self.Pneumonia_ICD9 = 486
        self.Sepsis_ICD9 = 99591
        self.Aspiration_ICD9 = 5070

    def Execute(self):
        diag_dict = dict()
        diag_dict['SUBJECT_ID'] = list()
        diag_dict['HADM_ID'] = list()
        diag_dict['Pneumonia'] = list()
        diag_dict['SEPSIS'] = list()
        diag_dict['Aspiration'] = list()

        for idx in range(len(self.ARDS_ID)):
            subject_id = self.ARDS_ID['SUBJECT_ID'].iloc[idx]
            subject_hadm = self.ARDS_ID['HADM_ID'].iloc[idx]
            subject_DIAGNOSES = self.DIAGNOSES[(self.DIAGNOSES['SUBJECT_ID'] == subject_id) & (self.DIAGNOSES['HADM_ID'] == subject_hadm)]

            if str(486) in list(subject_DIAGNOSES['ICD9_CODE']):
                subject_Pneumonia = 1
            else:
                subject_Pneumonia = 0

            if str(5070) in list(subject_DIAGNOSES['ICD9_CODE']):
                subject_Aspiration = 1
            else:
                subject_Aspiration = 0

            if str(99591) in list(subject_DIAGNOSES['ICD9_CODE']) or str(99592) in list(subject_DIAGNOSES['ICD9_CODE']):
                subject_Sepsis = 1
            else:
                subject_Sepsis = 0

            diag_dict['SUBJECT_ID'].append(subject_id)
            diag_dict['HADM_ID'].append(subject_hadm)
            diag_dict['SEPSIS'].append(subject_Sepsis)
            diag_dict['Pneumonia'].append(subject_Pneumonia)
            diag_dict['Aspiration'].append(subject_Aspiration)
        return pd.DataFrame(diag_dict)

if __name__ == '__main__':
    diagnoses = ARDS_diagnoses()
    DIAG_DICT = diagnoses.Execute()
    pickle.dump(DIAG_DICT, open('PKL/ARDS_diagnoses.pkl', 'wb'))


