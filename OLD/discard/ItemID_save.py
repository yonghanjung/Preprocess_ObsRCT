import pandas as pd
import numpy as np
import pickle
import methods
import datetime
import dateutil

ADMISSIONS = pd.read_csv('raw_data/ADMISSIONS.csv')
PATIENTS = pd.read_csv('raw_data/PATIENTS.csv')
PRESCRIPTIONS = pd.read_csv('raw_data/PRESCRIPTIONS.csv')
DIAGNOSIS = pd.read_csv('raw_data/DIAGNOSES_ICD.csv')
D_ITEM = pd.read_csv('raw_data/D_ITEMS.csv')
CH = pd.read_csv('raw_data/CHARTEVENTS.csv',usecols=['SUBJECT_ID','ITEMID','CHARTTIME','VALUE'])
CH_it = pd.read_csv('raw_data/CHARTEVENTS.csv',iterator=True)
CH_chunk = pd.read_csv('raw_data/CHARTEVENTS.csv',chunksize=10 ** 6)

ItemID_FiO2 = [190, 2981]
ItemID_PaO2 = [779]

''' Useful phrase '''
# Search ITEMID and Label
# D_ITEM[['ITEMID','LABEL']][ (D_ITEM['LABEL'].str.contains("PEEP") == True) ]

ItemID = [505, 506, # PEEP, PEEP Set
          681, 683, 2043, 2044, 224684, 2400, 2408, # Tidal Volume, Tidal Volume (Set), Tidal Vol (P High), Tidal Vol (P low), Tidal Volume (set)
          190, 2981, # FiO2 Set, FiO2
          543, 224696, # Plateau Pressure, Plateau Pressure,
          444, # Mean Airway Pressure,
          218, # High Insp. Pressure
          436, # Low Insp. Pressure
          535, # Peak Insp. Pressure
          2129, 7638, # Driving Pressure
          3068, # High Pressure Limit
          224697, # Mean Airway Pressure
          618, # Respiratory Rate
          619, # Respiratory Rate Set
          220210, # Respiratory Rate
          223990, # Respiratory Effort
          224688,  # Respiratory Rate (Set)
        1577,     # high minute vent
        1683,    # Low minute volume
        1687,     #  high minute vol
        1990,    # High minute vent.
        2046,      #   hi minute vol
        2090,     #    HI/minute/Vol
        2103,    #High minute volume
        2105,      # hi minute volume
        3190,      # high  minute vol
        3254,     # High minute Vent.
        6065,    # High minute Volume
        445,       # Mech. Minute Volume
        448,        # Minute Volume
        449,         #Minute Volume (Set)
        1486,        #  High Minute Volume
        1498,       #  High Minute Vo;ume
        1562,     #  High Minute Ventil.
        1737,     #       HI/Minute/vol
        1578,     #      HI/Minute/Vol
        1580,     #  HI/Minute/Volume
        1604,   # HI/Minute/Vol/
        3101,   # High Minute volume
        3161,      #   Hi Minute Volume
        3200,    # High Minute Volume m
        5558,    # HI/Minute/VOl
        5782,    # High Minute Ventilan
        2000, # Inspiratory Time
        224738, # Inspiratory Time
        226873, # Inspiratory Ratio
        779, # PaO2
        778, # PaCO2
        780, # pH
        1126, # Art. pH
        4753, # pH (Art)
        646, # SpO2
        226743, # APACHE II
        226745, # APACHE II Predicted Death Rate
        226991, # APACHE III
        227428, # SOFA
        ]


'''ARDS Onset'''
ItemID_FiO2 = [190, 2981]
ItemID_PaO2 = [779]


for chunk in CH_chunk:
    chunk
