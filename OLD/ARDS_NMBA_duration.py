import pickle
import pandas as pd
import datetime
import numpy as np

ARDS_NMBA_dosage = pd.read_csv('raw_data/ARDS_NMBA_dosage.csv')
ARDS_NMBA_SUBJECT = list(ARDS_NMBA_dosage['SUBJECT_ID'])
ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))
ARDS_PRESCRIPTION = pickle.load(open('ARDS_PRESCRIPTION.pkl','rb'))
ARDS_PRESCRIPTION = ARDS_PRESCRIPTION[['SUBJECT_ID','STARTDATE','ENDDATE','DRUG','DOSE_VAL_RX']]
ARDS_PRESCRIPTION_NMBA = ARDS_PRESCRIPTION[(ARDS_PRESCRIPTION['DRUG'].str.contains('Cisa'))]
ARDS_onset_time = pickle.load(open('ARDS_onset_time.pkl','rb'))

for subject_id in ARDS_NMBA_SUBJECT:
    ARDS_PRESCRIPTION_NMBA_subject = ARDS_PRESCRIPTION_NMBA[ARDS_PRESCRIPTION_NMBA['SUBJECT_ID'] == subject_id]
    ARDS_NMBA_dosage_subject = ARDS_NMBA_dosage[ARDS_NMBA_dosage['SUBJECT_ID'] == subject_id]
    if pd.isnull(list(ARDS_NMBA_dosage_subject['NMBA'])[0]):
        print(subject_id,'',sep=',')
        continue
    else:
        ARDS_onset_subject = list(ARDS_onset_time['onset_time'][ARDS_onset_time['subject_id'] == subject_id])[0]
        ARDS_onset_subject = ARDS_onset_subject.replace(hour=0, minute=0, second=0)
        ARDS_onset_subject_end = ARDS_onset_subject + datetime.timedelta(days=7)
        mask = (pd.to_datetime(ARDS_PRESCRIPTION_NMBA_subject['STARTDATE']) >= ARDS_onset_subject) & \
               (pd.to_datetime(ARDS_PRESCRIPTION_NMBA_subject['ENDDATE']) <= ARDS_onset_subject_end)
        ARDS_PRESCRIPTION_NMBA_subject = ARDS_PRESCRIPTION_NMBA_subject.loc[mask]
        subject_dosage = list(ARDS_NMBA_dosage['NMBA'][ARDS_NMBA_dosage['SUBJECT_ID'] == subject_id])[0]
        ARDS_PRESCRIPTION_NMBA_subject = \
            ARDS_PRESCRIPTION_NMBA_subject[ARDS_PRESCRIPTION_NMBA_subject['DOSE_VAL_RX'] == str(int(subject_dosage))]
        dosage_startdate = min(pd.to_datetime(ARDS_PRESCRIPTION_NMBA_subject['STARTDATE']))
        dosage_enddate = max(pd.to_datetime(ARDS_PRESCRIPTION_NMBA_subject['ENDDATE']))
        timediff = dosage_enddate.value - dosage_startdate.value
        timediff /= 10 ** 9
        timediff /= 86400
        print(subject_id, timediff, sep=',')
