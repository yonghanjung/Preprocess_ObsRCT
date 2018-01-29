import pickle
import pandas as pd

PATIENTS = pd.read_csv('raw_data/PATIENTS.csv')
ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))

ARDS_PATIENTS = PATIENTS[PATIENTS['SUBJECT_ID'].isin(ARDS_SUBJECT_ID)]
for subject_id, gender in zip(ARDS_PATIENTS['SUBJECT_ID'], ARDS_PATIENTS['GENDER']):
    print(subject_id, gender, sep=',')
