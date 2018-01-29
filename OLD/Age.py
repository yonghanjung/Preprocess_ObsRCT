import pandas as pd
import pickle
import methods

ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))
ADMISSIONS = pd.read_csv('raw_data/ADMISSIONS.csv')
PATIENTS = pd.read_csv('raw_data/PATIENTS.csv')
ARDS_onset = pickle.load(open('ARDS_onset.pkl','rb'))

ARDS_age = dict()
ARDS_age['SUBJECT_ID'] = list()
ARDS_age['AGE'] = list()

for subject_id in ARDS_SUBJECT_ID:
    age = methods.Age_compute(PATIENTS,ARDS_onset, subject_id)
    ARDS_age['SUBJECT_ID'].append(subject_id)
    ARDS_age['AGE'].append(age)
ARDS_age = pd.DataFrame(ARDS_age)

pickle.dump(ARDS_age,open('ARDS_age.pkl','wb'))