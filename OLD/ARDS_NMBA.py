import pickle
import pandas as pd
import datetime
import numpy as np

ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))
ARDS_PRESCRIPTION = pickle.load(open('ARDS_PRESCRIPTION.pkl','rb'))
ARDS_PRESCRIPTION = ARDS_PRESCRIPTION[['SUBJECT_ID','STARTDATE','ENDDATE','DRUG','DOSE_VAL_RX']]
ARDS_PRESCRIPTION_NMBA = ARDS_PRESCRIPTION[(ARDS_PRESCRIPTION['DRUG'].str.contains('Cisa'))]
ARDS_SUBJECT_ID_NMBA = pickle.load(open('ARDS_SUBJECT_ID_NMBA.pkl','rb'))
ARDS_onset_time = pickle.load(open('ARDS_onset_time.pkl','rb'))
idx = 0
ARDS_SUBJECT_ID_NMBA_TRUE = list()
for subject_id in ARDS_SUBJECT_ID:
    if subject_id in ARDS_SUBJECT_ID_NMBA:
        ARDS_PRESCRIPTION_NMBA_subject = ARDS_PRESCRIPTION_NMBA[ARDS_PRESCRIPTION_NMBA['SUBJECT_ID'] == subject_id]
        ARDS_onset_subject = list(ARDS_onset_time['onset_time'][ARDS_onset_time['subject_id'] == subject_id])[0]
        ARDS_onset_subject = ARDS_onset_subject.replace(hour=0, minute=0, second=0)
        ARDS_onset_subject_end = ARDS_onset_subject + datetime.timedelta(days=7)
        mask = (pd.to_datetime(ARDS_PRESCRIPTION_NMBA_subject['STARTDATE']) >= ARDS_onset_subject) & \
               (pd.to_datetime(ARDS_PRESCRIPTION_NMBA_subject['ENDDATE']) <= ARDS_onset_subject_end )
        if mask.any():
            ARDS_PRESCRIPTION_NMBA_subject = ARDS_PRESCRIPTION_NMBA_subject.loc[mask]
            try:
                ARDS_PRESCRIPTION_NMBA_subject = ARDS_PRESCRIPTION_NMBA_subject[pd.to_datetime(ARDS_PRESCRIPTION_NMBA_subject['STARTDATE']) == min(pd.to_datetime(ARDS_PRESCRIPTION_NMBA_subject['STARTDATE']))]
                NMBA_dosage = list(ARDS_PRESCRIPTION_NMBA_subject['DOSE_VAL_RX'])[0]
                NMBA_dosage = float(NMBA_dosage)
                print(subject_id,NMBA_dosage,sep=',')
                ARDS_SUBJECT_ID_NMBA_TRUE.append(subject_id)
            except:
                NMBA_dosage = list(ARDS_PRESCRIPTION_NMBA_subject['DOSE_VAL_RX'])[1]
                NMBA_dosage = float(NMBA_dosage)
                print(subject_id, NMBA_dosage,sep=',')
                ARDS_SUBJECT_ID_NMBA_TRUE.append(subject_id)
        else:
            print(subject_id, np.nan , sep=",")
    else:
        print(subject_id,np.nan,sep=",")

print(ARDS_SUBJECT_ID_NMBA_TRUE)