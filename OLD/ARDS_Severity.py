import pandas as pd
import numpy as np
import pickle
import datetime
import dateutil

ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))
ARDS_onset = pickle.load(open('ARDS_onset.pkl','rb'))
ARDS_APACHE = pd.read_csv('Preprocessed_result/Jenna/apacheiii_ards.csv')
ARDS_SAPS = pd.read_csv('Preprocessed_result/Jenna/sapsii_ards.csv')
ARDS_SOFA = pd.read_csv('Preprocessed_result/Jenna/sofa_ards.csv')
ADMISSION = pd.read_csv('raw_data/ADMISSIONS.csv')
ARDS_ADMISSION = ADMISSION[ADMISSION['SUBJECT_ID'].isin(ARDS_SUBJECT_ID)]

# iteration
for subject_id in ARDS_SUBJECT_ID:
    ARDS_onset_subject = ARDS_onset[ARDS_onset['SUBJECT_ID'] == subject_id]
    ARDS_ADMISSION_subject = ARDS_ADMISSION[ARDS_ADMISSION['SUBJECT_ID'] == subject_id ]
    ARDS_APACHE_subject = ARDS_APACHE[ARDS_APACHE['subject_id'] == subject_id]
    ARDS_SAPS_subject = ARDS_SAPS[ARDS_SAPS['subject_id'] == subject_id]
    ARDS_SOFA_subject = ARDS_SOFA[ARDS_SOFA['subject_id'] == subject_id]
    # APACHE
    if len(ARDS_APACHE_subject) == 1:
        subject_APACHE = list(ARDS_APACHE_subject['apsiii'])[0]
        subject_hadm_id = list(ARDS_ADMISSION_subject['HADM_ID'])[0]
        subject_APACHE_prob = list(ARDS_APACHE_subject['apsiii_prob'])[0]
    else:
        subject_onset = list(pd.to_datetime(ARDS_onset_subject['ADMITTIME']))[0] # onset's admit
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

    # SOFA
    if len(ARDS_SOFA_subject) == 1:
        subject_SOFA = list(ARDS_SOFA_subject['sofa'])[0]
        subject_hadm_id = list(ARDS_ADMISSION_subject['HADM_ID'])[0]
    else:
        subject_onset = list(pd.to_datetime(ARDS_onset_subject['ADMITTIME']))[0]
        subject_onset = subject_onset.replace(year=subject_onset.year - 100)
        subject_ADMISSION = ARDS_ADMISSION_subject[pd.to_datetime(ARDS_ADMISSION_subject['ADMITTIME']) == subject_onset]
        subject_hadm_id = list(subject_ADMISSION['HADM_ID'])[0]
        subject_SOFA_df = ARDS_SOFA_subject[ARDS_SOFA_subject['hadm_id'] == subject_hadm_id]
        if len(subject_SOFA_df) > 0:
            subject_SOFA = list(subject_SOFA_df['sofa'])[0]
        else:
            subject_SOFA = np.nan

    # SAPS
    if len(ARDS_SAPS_subject) == 1:
        subject_SAPS = list(ARDS_SAPS_subject['sapsii'])[0]
        subject_hadm_id = list(ARDS_ADMISSION_subject['HADM_ID'])[0]
        subject_SAPS_prob = list(ARDS_SAPS_subject['sapsii_prob'])[0]
    else:
        subject_onset = list(pd.to_datetime(ARDS_onset_subject['ADMITTIME']))[0]
        subject_onset = subject_onset.replace(year=subject_onset.year - 100)
        subject_ADMISSION = ARDS_ADMISSION_subject[
            pd.to_datetime(ARDS_ADMISSION_subject['ADMITTIME']) == subject_onset]
        subject_hadm_id = list(subject_ADMISSION['HADM_ID'])[0]
        subject_SAPS_df = ARDS_SAPS_subject[ARDS_SAPS_subject['hadm_id'] == subject_hadm_id]
        if len(subject_SAPS_df) > 0:
            subject_SAPS = list(subject_SAPS_df['sapsii'])[0]
            subject_SAPS_prob = list(ARDS_SAPS_subject['sapsii_prob'])[0]
        else:
            subject_SOFA = np.nan
            subject_SAPS_prob = np.nan


    print(subject_id, subject_hadm_id, subject_APACHE,subject_APACHE_prob, subject_SOFA, subject_SAPS, subject_SAPS_prob, sep=',')