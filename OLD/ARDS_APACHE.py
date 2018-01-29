import pandas as pd
import numpy as np
import pickle
import datetime
import dateutil

ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))
ARDS_onset = pickle.load(open('ARDS_onset.pkl','rb'))
ARDS_APACHE = pd.read_csv('apacheiii_ards.csv')
ADMISSION = pd.read_csv('raw_data/ADMISSIONS.csv')
ARDS_ADMISSION = ADMISSION[ADMISSION['SUBJECT_ID'].isin(ARDS_SUBJECT_ID)]

# iteration
for subject_id in ARDS_SUBJECT_ID:
    ARDS_onset_subject = ARDS_onset[ARDS_onset['SUBJECT_ID'] == subject_id]
    ARDS_ADMISSION_subject = ARDS_ADMISSION[ARDS_ADMISSION['SUBJECT_ID'] == subject_id ]
    ARDS_APACHE_subject = ARDS_APACHE[ARDS_APACHE['subject_id'] == subject_id]
    # If there is only 1 admission, then no problem!
    if len(ARDS_APACHE_subject) == 1:
        subject_APACHE = list(ARDS_APACHE_subject['apsiii'])[0]
        subject_hadm_id = list(ARDS_ADMISSION_subject['HADM_ID'])[0]
        subject_APACHE_prob = list(ARDS_APACHE_subject['apsiii_prob'])[0]
    else:
        subject_onset = list(pd.to_datetime(ARDS_onset_subject['ADMITTIME']))[0]
        subject_onset = subject_onset.replace(year=subject_onset.year - 100)
        subject_ADMISSION = ARDS_ADMISSION_subject[pd.to_datetime(ARDS_ADMISSION_subject['ADMITTIME']) == subject_onset]
        subject_hadm_id = list(subject_ADMISSION['HADM_ID'])[0]
        subject_APACHE_df = ARDS_APACHE_subject[ARDS_APACHE_subject['hadm_id'] == subject_hadm_id]
        if len(subject_APACHE_df) > 0:
            subject_APACHE = list(subject_APACHE_df['apsiii'])[0]
            subject_APACHE_prob = list(subject_APACHE_df['apsiii_prob'])[0]
        else:
            subject_APACHE = np.nan
            subject_APACHE_prob = np.nan
    print(subject_id, subject_hadm_id, subject_APACHE,subject_APACHE_prob,sep=',')