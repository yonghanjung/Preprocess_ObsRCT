import numpy as np
import pandas as pd
import pickle
import datetime
import dateutil

ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))
ARDS_time = pickle.load(open('ARDS_onset.pkl','rb'))
ADMISSIONS = pd.read_csv('raw_data/ADMISSIONS.csv')
PATIENTS = pd.read_csv('raw_data/PATIENTS.csv')
ARDS_PATIENTS = PATIENTS[PATIENTS['SUBJECT_ID'].isin(ARDS_SUBJECT_ID)]

idx = 0
ARDS_survival = dict()
ARDS_survival['SUBJECT_ID'] = list()
ARDS_survival['Mortality days duration'] = list()
ARDS_survival['28-SURVIVAL'] = list()
ARDS_survival['60-SURVIVAL'] = list()
ARDS_survival['90-SURVIVAL'] = list()
ARDS_survival['DOD'] = list()
for subject_id in ARDS_SUBJECT_ID:
    idx += 1
    ARDS_survival['SUBJECT_ID'].append(subject_id)
    DOD = list(ARDS_PATIENTS['DOD'][ARDS_PATIENTS['SUBJECT_ID'] == subject_id ])[0]
    if pd.isnull(DOD):
        ARDS_survival['28-SURVIVAL'].append(1) # 1 means survival
        ARDS_survival['60-SURVIVAL'].append(1)
        ARDS_survival['90-SURVIVAL'].append(1)
        ARDS_survival['Mortality days duration'].append(np.nan)
        ARDS_survival['DOD'].append(np.nan)

    else:
        DOD = dateutil.parser.parse(DOD)
        ARDS_survival['DOD'].append(DOD)
        onset_time = list(ARDS_time['ARDS_ONSET'][ARDS_time['SUBJECT_ID'] == subject_id])[0]
        onset_time = onset_time.replace(hour=0,minute=0,second=0)
        if onset_time> DOD: # years are not matching
            DOD = DOD.replace(DOD.year+100)
            diff = DOD - onset_time
            if onset_time > DOD:
                if abs(diff.value / (10 ** 9))/86400 <= 10:
                    print(subject_id)
                    ARDS_survival['Mortality days duration'].append(abs(diff.value / (10 ** 9))/86400)
                    ARDS_survival['28-SURVIVAL'].append(0)
                    ARDS_survival['60-SURVIVAL'].append(0)
                    ARDS_survival['90-SURVIVAL'].append(0)
                    continue
                else:
                    DOD = DOD.replace(DOD.year + 100)
        diff = DOD - onset_time
        if diff.value < 0:
            print(subject_id,'ho')
        diff_seconds = diff.value / (10**9)
        diff_days = round(diff_seconds / 86400,2)
        ARDS_survival['Mortality days duration'].append(diff_days)
        if diff_days < 28:
            ARDS_survival['28-SURVIVAL'].append(0)
            ARDS_survival['60-SURVIVAL'].append(0)
            ARDS_survival['90-SURVIVAL'].append(0)
        elif diff_days >= 28 and diff_days < 60:
            ARDS_survival['28-SURVIVAL'].append(1)
            ARDS_survival['60-SURVIVAL'].append(0)
            ARDS_survival['90-SURVIVAL'].append(0)
        elif diff_days >= 60 and diff_days < 90:
            ARDS_survival['28-SURVIVAL'].append(1)
            ARDS_survival['60-SURVIVAL'].append(1)
            ARDS_survival['90-SURVIVAL'].append(0)
        elif diff_days >= 90:
            ARDS_survival['28-SURVIVAL'].append(1)
            ARDS_survival['60-SURVIVAL'].append(1)
            ARDS_survival['90-SURVIVAL'].append(1)


ARDS_survival = pd.DataFrame(ARDS_survival)
# pickle.dump(ARDS_survival, open('ARDS_survival.pkl','wb'))