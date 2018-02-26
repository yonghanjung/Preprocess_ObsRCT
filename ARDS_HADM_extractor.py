import numpy as np
import pickle
import pandas as pd

class ARDS_HADM_extractor():
    def __init__(self):
        ADMISSION = pd.read_csv('OLD/raw_data/ADMISSIONS.csv')
        self.ARDS_ID = pickle.load(open('PKL/ARDS_ID.pkl','rb'))
        self.ARDS_ONSET = pickle.load(open('PKL/ARDS_ONSETTIME.pkl','rb'))
        self.ARDS_ADMISSION = ADMISSION[ADMISSION['SUBJECT_ID'].isin(self.ARDS_ID['SUBJECT_ID'])]

    def ARDS_HADM_match(self):
        ARDS_SUBJECT_ID = self.ARDS_ID['SUBJECT_ID']
        subject_id_list = []
        subject_hadm_list = []
        subject_icustay_list = []

        for subject_id in ARDS_SUBJECT_ID :
            ARDS_ADMISSION_subject = self.ARDS_ADMISSION[self.ARDS_ADMISSION['SUBJECT_ID'] == subject_id]
            ARDS_ONSET_subject = self.ARDS_ONSET[self.ARDS_ONSET['SUBJECT_ID'] == subject_id]
            ARDS_ONSET_ADMITTIME = ARDS_ONSET_subject.iloc[0]['ADMITTIME']
            for idx in range(len(ARDS_ADMISSION_subject)):
                each_adm = pd.to_datetime(ARDS_ADMISSION_subject.iloc[idx]['ADMITTIME'])
                if each_adm.day == ARDS_ONSET_ADMITTIME.day and each_adm.month == ARDS_ONSET_ADMITTIME.month:
                    subject_HADM_ID = ARDS_ADMISSION_subject.iloc[idx]['HADM_ID']

            icuid = self.ARDS_ID['ICUID'][self.ARDS_ID['SUBJECT_ID'] == subject_id].iloc[0]
            subject_id_list.append(subject_id)
            subject_hadm_list.append(subject_HADM_ID)
            subject_icustay_list.append(icuid)
        return subject_id_list, subject_icustay_list, subject_hadm_list

    def Execute(self):
        SUBJECT_ID, ICUSTAY_ID, HADM_ID = self.ARDS_HADM_match()
        ARDS_ID = pd.DataFrame({'SUBJECT_ID':SUBJECT_ID, 'ICUSTAY_ID':ICUSTAY_ID,'HADM_ID':HADM_ID})
        return ARDS_ID


if __name__ == '__main__':
    HADM = ARDS_HADM_extractor()
    ARDS_ID = HADM.Execute()
    pickle.dump(ARDS_ID, open('PKL/ARDS_ID.pkl', 'wb'))