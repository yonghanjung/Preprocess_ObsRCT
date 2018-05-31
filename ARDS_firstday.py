import numpy as np
import scipy as sp
import pandas as pd
import pickle

class ARDS_firstday():
    def __init__(self):
        self.ARDS_ID = pickle.load(open('PKL/ARDS_ID.pkl','rb'))
        self.bloodgas = pd.read_csv('Firstday/bloodgasfirstdayarterial.csv')
        self.gcs = pd.read_csv('Firstday/gcsfirstday.csv')
        self.uo = pd.read_csv('Firstday/uofirstday.csv')
        self.vitals = pd.read_csv('Firstday/vitalfirstday.csv')
        labs = pd.read_csv('Firstday/labsfirstday.csv')
        self.labs_crea = labs[['subject_id', 'hadm_id', 'icustay_id', 'creatinine_min','creatinine_max']]

    def bloodgas_average(self):
        list_keys = ['so2', 'spo2', 'po2', 'pco2', 'pao2fio2', 'ph', 'totalco2', 'hematocrit', 'hemoglobin', 'carboxyhemoglobin', 'methemoglobin', 'chloride', 'calcium', 'temperature', 'potassium', 'sodium', 'lactate', 'glucose', 'intubated', 'tidalvolume', 'ventilationrate', 'ventilator', 'peep', 'o2flow', 'requiredo2']
        dict_bloodgas = dict()
        dict_bloodgas['subject_id'] = []
        dict_bloodgas['hadm_id'] = []
        dict_bloodgas['icustay_id'] = []
        for key_elem in list_keys:
            dict_bloodgas[key_elem] = []

        for idx in range(len(self.ARDS_ID)):
            print(idx/len(self.ARDS_ID), idx)
            subject_id = int(self.ARDS_ID.iloc[idx]['SUBJECT_ID'])
            icustay_id = int(self.ARDS_ID.iloc[idx]['ICUSTAY_ID'])
            hadm_id = int(self.ARDS_ID.iloc[idx]['HADM_ID'])

            dict_bloodgas['subject_id'].append(subject_id)
            dict_bloodgas['icustay_id'].append(icustay_id)
            dict_bloodgas['hadm_id'].append(hadm_id)

            subject_bloodgas_mask = (self.bloodgas['subject_id'] == subject_id) & \
                            (self.bloodgas['icustay_id'] == icustay_id) & \
                            (self.bloodgas['hadm_id'] == hadm_id)

            subject_bloodgas = self.bloodgas[subject_bloodgas_mask][list_keys]
            for key_elem in list_keys:
                list_elem = list(subject_bloodgas[pd.notnull(subject_bloodgas[key_elem])][key_elem])
                dict_bloodgas[key_elem].append(np.mean(list_elem))

        df_bloodgas = pd.DataFrame(dict_bloodgas)
        return df_bloodgas

    def firstday_merge(self):
        bloodgas = self.bloodgas_average()

        print("bloodgas", len(bloodgas))
        print("gcs", len(self.gcs))
        print("uo", len(self.uo))
        print("vitals", len(self.vitals))
        print("labs_crea", len(self.labs_crea))


        merged = pd.merge(bloodgas, self.gcs, on=['subject_id', 'hadm_id', 'icustay_id'])
        merged = pd.merge(merged, self.uo, on=['subject_id', 'hadm_id', 'icustay_id'])
        merged = pd.merge(merged, self.vitals, on=['subject_id', 'hadm_id', 'icustay_id'])
        merged = pd.merge(merged, self.labs_crea, on=['subject_id', 'hadm_id', 'icustay_id'])

        merged.columns = ['calcium', 'carboxyhemoglobin', 'chloride', 'glucose', 'HADM_ID',
                          'hematocrit', 'hemoglobin', 'ICUSTAY_ID', 'intubated', 'lactate',
                          'methemoglobin', 'o2flow', 'pao2fio2', 'pco2', 'peep', 'ph', 'po2',
                          'potassium', 'requiredo2', 'so2', 'sodium', 'spo2', 'SUBJECT_ID',
                          'temperature', 'tidalvolume', 'totalco2', 'ventilationrate',
                          'ventilator', 'mingcs', 'gcsmotor', 'gcsverbal', 'gcseyes',
                          'endotrachflag', 'urineoutput', 'heartrate_min', 'heartrate_max',
                          'heartrate_mean', 'sysbp_min', 'sysbp_max', 'sysbp_mean', 'diasbp_min',
                          'diasbp_max', 'diasbp_mean', 'meanbp_min', 'meanbp_max', 'meanbp_mean',
                          'resprate_min', 'resprate_max', 'resprate_mean', 'tempc_min',
                          'tempc_max', 'tempc_mean', 'spo2_min', 'spo2_max', 'spo2_mean',
                          'glucose_min', 'glucose_max', 'glucose_mean', 'creatinine_min',
                          'creatinine_max']

        return merged

if __name__ == '__main__':
    firstday = ARDS_firstday()
    merged = firstday.firstday_merge()
    pickle.dump(merged, open('PKL/ARDS_firstday.pkl', 'wb'))






