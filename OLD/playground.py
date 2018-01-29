import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import dateutil
import datetime

CH_ARDS_reduced = pickle.load(open('CH_ARDS_reduced.pkl','rb'))
ARDS_onset = pickle.load(open('ARDS_onset.pkl','rb'))
ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))
D_ITEM = pd.read_csv('raw_data/D_ITEMS.csv')

# D_ITEM[['ITEMID','LABEL']][ (D_ITEM['LABEL'].str.contains("PEEP") == True) ]

PEEP_ID = [505, 506, 220339]
PP_ID = [543, 224696]

ItemID_FiO2 = [190, 2981]

ItemID_MAP = [444]
ItemID_DP = [2129, 7638]
ItemID_HP = [218]

# VT_ID = [681, 682, 683, 2043, 2044, 224684, 224685, 2400, 2408, 2534]
VT_ID = [681,682,683,2400,2534]

for subject_id in ARDS_SUBJECT_ID:
    CH_ARDS_subject = CH_ARDS_reduced[CH_ARDS_reduced['SUBJECT_ID'] == subject_id]
    ARDS_onset_subject = list(ARDS_onset['ARDS_ONSET'][ARDS_onset['SUBJECT_ID'] == subject_id])[0]
    ARDS_onset_subject_end = ARDS_onset_subject + datetime.timedelta(days=7)

    mask_subject = (pd.to_datetime(CH_ARDS_subject['CHARTTIME']) >= ARDS_onset_subject) & \
                      (pd.to_datetime(CH_ARDS_subject['CHARTTIME']) <= ARDS_onset_subject_end ) & \
                      (pd.isnull(CH_ARDS_subject['VALUE']) == False)

    # Filter 1 -- Common
    if mask_subject.any() == False:
        print(subject_id, '-', sep=',')
        continue

    CH_ARDS_subject = CH_ARDS_subject.loc[mask_subject]

    # Filter 2 -- No VT?
    mask_VTID = CH_ARDS_subject['ITEMID'].isin(VT_ID)
    if mask_VTID.any() == False:
        print(subject_id, '-', sep=',')
        continue
    CH_ARDS_subject_VT = CH_ARDS_subject.loc[mask_VTID]

    # Filter 3 -- 1Day
    ARDS_onset_subject_VTend = ARDS_onset_subject + datetime.timedelta(days=1)
    mask_subject_VT = (pd.to_datetime(CH_ARDS_subject_VT['CHARTTIME']) >= ARDS_onset_subject) & \
                      (pd.to_datetime(CH_ARDS_subject_VT['CHARTTIME']) <= ARDS_onset_subject_VTend) & \
                      (pd.isnull(CH_ARDS_subject_VT['VALUE']) == False)

    if mask_subject_VT.any() == False:
        print(subject_id, '-', sep=',')
        continue
    CH_ARDS_subject_VT = CH_ARDS_subject_VT.loc[mask_subject_VT]

    # Filter 4 -- VT_set
    mask_subject_VT_set = (CH_ARDS_subject_VT['ITEMID'] == 683)
    if mask_subject_VT_set.any():
        CH_ARDS_subject_VTSet = CH_ARDS_subject_VT.loc[mask_subject_VT_set]
        subject_VT_val = np.mean(pd.to_numeric(CH_ARDS_subject_VTSet['VALUE']))
        subject_VT_val = round(subject_VT_val,1)
    else:
        CH_ARDS_subject_VT = CH_ARDS_subject_VT.loc[mask_subject_VT]
        subject_VT_val = np.mean(pd.to_numeric(CH_ARDS_subject_VT['VALUE']))
        subject_VT_val = round(subject_VT_val, 1)

    # ##### PEEP #####
    # # Filter 2 -- No PEEP?
    # mask_subject_PEEP = (CH_ARDS_subject['ITEMID'].isin(PEEP_ID))
    # if mask_subject_PEEP.any() == False:
    #     print(subject_id, '-', sep=',')
    #     continue
    #
    # CH_ARDS_subject_PEEP = CH_ARDS_subject.loc[mask_subject_PEEP]
    #
    # # Filter 3 -- Day 1
    # ARDS_onset_subject_PEEPend = ARDS_onset_subject + datetime.timedelta(days=1)
    # mask_subject_PEEP = (pd.to_datetime(CH_ARDS_subject_PEEP['CHARTTIME']) >= ARDS_onset_subject) & \
    #                   (pd.to_datetime(CH_ARDS_subject_PEEP['CHARTTIME']) <= ARDS_onset_subject_PEEPend) & \
    #                   (pd.isnull(CH_ARDS_subject_PEEP['VALUE']) == False)
    # if mask_subject_PEEP.any() == False:
    #     print(subject_id, '-', sep=',')
    #     continue
    # CH_ARDS_subject_PEEP = CH_ARDS_subject_PEEP.loc[mask_subject_PEEP]
    #
    # # Filter 4 -- PEEP Set?
    # mask_subject_PEEP_set = (CH_ARDS_subject_PEEP['ITEMID'].isin([506,220339]))
    # if mask_subject_PEEP_set.any():
    #     CH_ARDS_subject_PEEPSet = CH_ARDS_subject_PEEP.loc[mask_subject_PEEP_set]
    #     subject_PEEP_val = np.mean(pd.to_numeric(CH_ARDS_subject_PEEPSet['VALUE']))
    #     subject_PEEP_val = round(subject_PEEP_val,1)
    # else:
    #     CH_ARDS_subject_PEEPSet = CH_ARDS_subject_PEEP.loc[mask_subject_PEEP]
    #     subject_PEEP_val = np.mean(pd.to_numeric(CH_ARDS_subject_PEEPSet['VALUE']))
    #     subject_PEEP_val = round(subject_PEEP_val, 1)
    #
    # #### PP
    # # Filter 2 -- No PP?
    # mask_subject_PP = CH_ARDS_subject['ITEMID'].isin(PP_ID)
    # if mask_subject_PP.any() == False:
    #     print(subject_id, '-', sep=',')
    #     continue
    # CH_ARDS_subject_PP = CH_ARDS_subject[CH_ARDS_subject['ITEMID'].isin(PP_ID)]
    #
    # # Filter 3 - PP > PEEP
    # ARDS_onset_subject_PPend = ARDS_onset_subject + datetime.timedelta(days=1)
    # mask_subject_PP = (pd.to_datetime(CH_ARDS_subject_PP['CHARTTIME']) >= ARDS_onset_subject) & \
    #                     (pd.to_datetime(CH_ARDS_subject_PP['CHARTTIME']) <= ARDS_onset_subject_PPend) & \
    #                     (pd.isnull(CH_ARDS_subject_PP['VALUE']) == False) & \
    #                     (pd.to_numeric(CH_ARDS_subject_PP['VALUE']) > subject_PEEP_val)
    # if mask_subject_PP.any() == False:
    #     print(subject_id, '-', sep=',')
    #     continue
    # CH_ARDS_subject_PP = CH_ARDS_subject_PP.loc[mask_subject_PP]
    # subject_PP_val = np.mean(pd.to_numeric(CH_ARDS_subject_PP['VALUE']))
    # subject_PP_val = round(subject_PP_val,1)
    #
    # print(subject_id, subject_VT_val, subject_PEEP_val, subject_PP_val,sep=',')
