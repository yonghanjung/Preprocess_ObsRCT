import pandas as pd
import numpy as np
import pickle

# Load ARDS_ID
ARDS_ID = pickle.load(open('PKL/ARDS_ID.pkl','rb'))

# Load Demographic information
ARDS_Age = pickle.load(open('PKL/ARDS_Age.pkl','rb'))
ARDS_HeightWeight = pickle.load(open('PKL/ARDS_HeightWeight.pkl','rb'))

ARDS_Gender = pickle.load(open('PKL/ARDS_Gender.pkl','rb'))
ARDS_DOD = pickle.load(open('PKL/ARDS_DOD.pkl','rb'))

# Load Ventilator Setting
ARDS_VENT = pickle.load(open('PKL/ARDS_VENT.pkl','rb'))

# Load drug treatment information
ARDS_DRUG = pickle.load(open('PKL/ARDS_drug.pkl','rb'))

# Load Vital Lab information
ARDS_VITALLAB = pickle.load(open('PKL/ARDS_firstday.pkl','rb'))

# Load Diagnoses information
ARDS_DIAGNOSES = pickle.load(open('PKL/ARDS_diagnoses.pkl','rb'))

# Matching with IDs
merged = pd.merge(ARDS_ID, ARDS_Age, on=['SUBJECT_ID'])
merged = pd.merge(merged, ARDS_HeightWeight, on=['SUBJECT_ID', 'ICUSTAY_ID'])
merged = pd.merge(merged, ARDS_Gender, on=['SUBJECT_ID'])
merged = pd.merge(merged, ARDS_DOD, on=['SUBJECT_ID'])
merged = pd.merge(merged, ARDS_VENT, on=['SUBJECT_ID','HADM_ID','ICUSTAY_ID'])
merged = pd.merge(merged, ARDS_DRUG, on=['SUBJECT_ID','HADM_ID','ICUSTAY_ID'])
merged = pd.merge(merged, ARDS_DIAGNOSES, on=['SUBJECT_ID','HADM_ID'])
merged = pd.merge(merged, ARDS_VITALLAB, on=['SUBJECT_ID','HADM_ID'])

# CSV Export
merged.to_csv('df_to_csv/merged.csv',sep="|",na_rep="-")

# ARDS_ID.to_csv('df_to_csv/ARDS_ID.csv',sep="|",na_rep="-")
# ARDS_Age.to_csv('df_to_csv/ARDS_Age.csv',sep="|",na_rep="-")
# ARDS_HeightWeight.to_csv('df_to_csv/ARDS_HeightWeight.csv',sep="|",na_rep="-")
# ARDS_Gender.to_csv('df_to_csv/ARDS_Gender.csv',sep="|",na_rep="-")
# ARDS_DOD.to_csv('df_to_csv/ARDS_DOD.csv',sep="|",na_rep="-")
# ARDS_VENT.to_csv('df_to_csv/ARDS_VENT.csv',sep="|",na_rep="-")
# ARDS_DRUG.to_csv('df_to_csv/ARDS_DRUG.csv',sep="|",na_rep="-")
# ARDS_VITALLAB.to_csv('df_to_csv/ARDS_VITALLAB.csv',sep="|",na_rep="-")
# ARDS_DIAGNOSES.to_csv('df_to_csv/ARDS_DIAGNOSES.csv',sep="|",na_rep="-")



