import pandas as pd
import numpy as np
import pickle
import methods
import dateutil

SUBJECT_ID = pickle.load(open('ARDS_patients.pkl','rb'))
ADMISSIONS = pd.read_csv('raw_data/ADMISSIONS.csv')
PATIENTS = pd.read_csv('raw_data/PATIENTS.csv')
ARDS_time = pickle.load(open('ARDS_patients_time.pkl','rb'))

ARDS_patients_demo = PATIENTS[['SUBJECT_ID','DOB','DOD']][PATIENTS['SUBJECT_ID'].isin(SUBJECT_ID)]
ARDS_time