import numpy as np
import scipy as sp
import pandas as pd
import pickle
import datetime

class ARDS_diagnoses():
    def __init__(self):
        self.DIAGNOSES = pd.read_csv('OLD/raw_data/DIAGNOSES_ICD.csv')
        self.ARDS_ID = pickle.load(open('PKL/ARDS_ID.pkl','rb'))
        # ICD9 codes for Pneumonia (starting character)
        self.Pneumonia_ICD9 = ['480','481','482','483','484','485','486','487','488']

        # From there all ICD9 are exact
        self.Aspiration_ICD9 = ['5070']  # Aspiration Pneumonia, exact
        # ICD9 codes for Pneumonia (starting character)
        self.Sepsis_ICD9 = ['99591']
        self.Severe_Sepsis_ICD9 = ['99592']
        self.Septic_Shock = ['78552']


    def Execute(self):
        diag_dict = dict()
        diag_dict['SUBJECT_ID'] = list()
        diag_dict['HADM_ID'] = list()
        diag_dict['Pneumonia'] = list()
        diag_dict['Sepsis'] = list()
        diag_dict['Severe Sepsis'] = list()
        diag_dict['Septic Shock'] = list()
        diag_dict['Aspiration'] = list()

        for idx in range(len(self.ARDS_ID)):
            subject_id = self.ARDS_ID['SUBJECT_ID'].iloc[idx]
            subject_hadm = self.ARDS_ID['HADM_ID'].iloc[idx]
            subject_DIAGNOSES = self.DIAGNOSES[(self.DIAGNOSES['SUBJECT_ID'] == subject_id) & (self.DIAGNOSES['HADM_ID'] == subject_hadm)]
            subject_DIAGNOSES_ICD9 = list(subject_DIAGNOSES['ICD9_CODE'])
            for idx in range(len(subject_DIAGNOSES_ICD9)):
                elem_icd9 = subject_DIAGNOSES_ICD9[idx]
                try:
                    # Identify Pnuemonia
                    if elem_icd9[:3] in self.Pneumonia_ICD9:
                        subject_Pneumonia = 1
                    else:
                        subject_Pneumonia = 0

                    # Identify Aspiration_ICD9
                    if elem_icd9 in self.Aspiration_ICD9:
                        subject_Aspiration = 1
                    else:
                        subject_Aspiration = 0

                    # Identify Sepsis
                    if elem_icd9 in self.Sepsis_ICD9:
                        subject_Sepsis= 1
                    else:
                        subject_Sepsis = 0

                    # Identify Severe Sepsis
                    if elem_icd9 in self.Severe_Sepsis_ICD9:
                        subject_Severe_Sepsis = 1
                    else:
                        subject_Severe_Sepsis = 0

                    # Identify Septic Shock
                    if elem_icd9 in self.Septic_Shock:
                        subject_Septic_shock = 1
                    else:
                        subject_Septic_shock = 0


                except:
                    continue

            diag_dict['SUBJECT_ID'].append(subject_id)
            diag_dict['HADM_ID'].append(subject_hadm)
            diag_dict['Pneumonia'].append(subject_Pneumonia)
            diag_dict['Aspiration'].append(subject_Aspiration)
            diag_dict['Sepsis'].append(subject_Sepsis)
            diag_dict['Severe Sepsis'].append(subject_Severe_Sepsis)
            diag_dict['Septic Shock'].append(subject_Septic_shock)

        return pd.DataFrame(diag_dict)

if __name__ == '__main__':
    diagnoses = ARDS_diagnoses()
    DIAG_DICT = diagnoses.Execute()
    pickle.dump(DIAG_DICT, open('PKL/ARDS_diagnoses.pkl', 'wb'))


