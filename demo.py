import pandas as pd
import numpy as np

ventsettings = pd.read_csv('ventsettings.csv')
ICUSTAY = pd.read_csv('OLD/raw_data/ICUSTAYS.csv')

icustay_id = 200001.0
temp = ICUSTAY[ICUSTAY['ICUSTAY_ID'] == icustay_id]


''' Rough algorithm 
For subject_id in SUBJECT_ID 
    FIND 
'''
