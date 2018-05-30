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