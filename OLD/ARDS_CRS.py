import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dateutil
import datetime

CH_ARDS_reduced = pickle.load(open('CH_ARDS_reduced.pkl','rb'))
ARDS_onset = pickle.load(open('ARDS_onset.pkl','rb'))
ARDS_SUBJECT_ID = pd.read_csv('ARDS_SUBJECT_ID_NEW.csv')['SUBJECT_ID']
D_ITEM = pd.read_csv('raw_data/D_ITEMS.csv')

# D_ITEM[['ITEMID','LABEL']][ (D_ITEM['LABEL'].str.contains("PEEP") == True) ]

VT_ID = [681,682,683,2400,2534]

PEEP_ID = [505, 506, 220339]
PP_ID = [543, 224696]

DP_ID = [2129, 7638]


for subject_id in ARDS_SUBJECT_ID:
    CH_ARDS_subject = CH_ARDS_reduced[CH_ARDS_reduced['SUBJECT_ID'] == subject_id]
    ARDS_onset_subject = list(ARDS_onset['ARDS_ONSET'][ARDS_onset['SUBJECT_ID'] == subject_id])[0]
    ARDS_admit_subject = list(ARDS_onset['ADMITTIME'][ARDS_onset['SUBJECT_ID'] == subject_id])[0]
    ARDS_admit_subject_end = ARDS_admit_subject + datetime.timedelta(days=2)
    ARDS_onset_subject_end = ARDS_onset_subject+ datetime.timedelta(days=1)


    mask_subject_admit = (pd.to_datetime(CH_ARDS_subject['CHARTTIME']) >= ARDS_admit_subject) & \
                      (pd.to_datetime(CH_ARDS_subject['CHARTTIME']) <= ARDS_admit_subject_end ) & \
                      (pd.isnull(CH_ARDS_subject['VALUE']) == False)
    mask_subject_onset = (pd.to_datetime(CH_ARDS_subject['CHARTTIME']) >= ARDS_admit_subject) & \
                      (pd.to_datetime(CH_ARDS_subject['CHARTTIME']) <= ARDS_onset_subject_end ) & \
                      (pd.isnull(CH_ARDS_subject['VALUE']) == False)

    CH_subject_admit = CH_ARDS_subject.loc[mask_subject_admit]
    CH_subject_onset = CH_ARDS_subject.loc[mask_subject_onset]

    mask_VT_admit = CH_subject_admit['ITEMID'].isin(VT_ID)
    mask_PP_admit = CH_subject_admit['ITEMID'].isin(PP_ID)
    mask_PEEP_admit = CH_subject_admit['ITEMID'].isin(PEEP_ID)
    mask_DP_admit = CH_subject_admit['ITEMID'].isin(DP_ID)

    mask_VT_onset = CH_subject_onset['ITEMID'].isin(VT_ID)
    mask_PP_onset = CH_subject_onset['ITEMID'].isin(PP_ID)
    mask_PEEP_onset = CH_subject_onset['ITEMID'].isin(PEEP_ID)
    mask_DP_onset = CH_subject_onset['ITEMID'].isin(DP_ID)

    if mask_VT_admit.any() == False:
        CH_subject_VT = CH_subject_onset.loc[mask_VT_onset]
    else:
        CH_subject_VT = CH_subject_admit.loc[mask_VT_admit]

    mask_VT = CH_subject_VT['ITEMID'] == 683
    if mask_VT .any() == False:
        mask_VT = CH_subject_VT['ITEMID'] == 682
    CH_subject_VT = CH_subject_VT.loc[mask_VT]

    mintime_VT = min(pd.to_datetime(CH_subject_VT['CHARTTIME']))
    mintime_VT_end = mintime_VT + datetime.timedelta(hours=12)
    mask_mintime_VT = (pd.to_datetime(CH_subject_VT['CHARTTIME']) >= mintime_VT ) & \
                      (pd.to_datetime(CH_subject_VT['CHARTTIME']) <= mintime_VT_end) & \
                      (pd.isnull(pd.to_numeric(CH_subject_VT['VALUE'])) == False)
    CH_subject_VT = CH_subject_VT.loc[mask_mintime_VT]
    subject_VT = np.mean(list(pd.to_numeric(CH_subject_VT['VALUE'])))


    if mask_PP_admit.any() == False:
        CH_subject_PP = CH_subject_onset.loc[mask_PP_onset]
    else:
        CH_subject_PP = CH_subject_admit.loc[mask_PP_admit]
    mintime_PP = min(pd.to_datetime(CH_subject_PP['CHARTTIME']))
    mintime_PP_end = mintime_PP + datetime.timedelta(hours=12)
    mask_mintime_PP = (pd.to_datetime(CH_subject_PP['CHARTTIME']) >= mintime_PP) & \
                      (pd.to_datetime(CH_subject_PP['CHARTTIME']) <= mintime_PP_end) & \
                       (pd.isnull(pd.to_numeric(CH_subject_PP['VALUE'])) == False)
    CH_subject_PP = CH_subject_PP.loc[mask_mintime_PP]
    subject_PP = np.mean(list(pd.to_numeric(CH_subject_PP['VALUE'])))

    if mask_PEEP_admit.any() == False:
        CH_subject_PEEP = CH_subject_onset.loc[mask_PEEP_onset]
    else:
        CH_subject_PEEP = CH_subject_admit.loc[mask_PEEP_admit]
    mintime_PEEP = min(pd.to_datetime(CH_subject_PEEP['CHARTTIME']))
    mintime_PEEP_end = mintime_PEEP + datetime.timedelta(hours=12)
    mask_mintime_PEEP = (pd.to_datetime(CH_subject_PEEP['CHARTTIME']) >= mintime_PEEP) & \
                      (pd.to_datetime(CH_subject_PEEP['CHARTTIME']) <= mintime_PEEP_end) & \
                        (pd.isnull(pd.to_numeric(CH_subject_PEEP['VALUE'])) == False)
    CH_subject_PEEP = CH_subject_PEEP.loc[mask_mintime_PEEP]
    subject_PEEP = np.mean(list(pd.to_numeric(CH_subject_PEEP['VALUE'])))

    subject_CRS = subject_VT / (subject_PP - subject_PEEP)
    if pd.isnull(subject_CRS):
        print(subject_id, subject_VT, subject_PP, subject_PEEP)
    else:
        print(subject_id, subject_CRS)