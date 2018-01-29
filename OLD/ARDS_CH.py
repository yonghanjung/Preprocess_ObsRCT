import pickle
import pandas as pd
import dateutil
import datetime
import numpy as np
from collections import Counter

def most_frequent(input_list, rule):
    counter_pair = Counter(input_list).most_common()
    value,max_count = counter_pair[0]
    counter_pair = [pair_elem for pair_elem in counter_pair if pair_elem[1] == max_count]
    if len(counter_pair) == 1:
        return value
    else:
        value_lst = [pair_elem[0] for pair_elem in counter_pair]
        if rule == 'max':
            return max(value_lst)
        elif rule == 'min':
            return min(value_lst)
        elif rule == 'mean':
            return np.mean(value_lst)
        elif rule == 'median':
            return np.median(value_lst)

CH_ARDS_reduced = pickle.load(open('CH_ARDS_reduced.pkl','rb'))
ARDS_onset = pickle.load(open('ARDS_onset.pkl','rb'))
ARDS_SUBJECT_ID = pd.read_csv('ARDS_SUBJECT_ID_NEW.csv')['SUBJECT_ID']
D_ITEM = pd.read_csv('raw_data/D_ITEMS.csv')

#D_ITEM[['ITEMID','LABEL']][ (D_ITEM['LABEL'].str.contains("PEEP") == True) ]

VT_ID = [681, 682, 683, 2400, 2534]
PEEP_ID = [505, 506, 220339]
FiO2_ID = [190, 2981]
PP_ID = [543, 224696]
PIP_ID = [535,224695]


# ItemID_MAP = [444]
# ItemID_DP = [2129, 7638]
# ItemID_HP = [218]

for subject_id in ARDS_SUBJECT_ID:
    CH_ARDS_subject = CH_ARDS_reduced[CH_ARDS_reduced['SUBJECT_ID'] == subject_id]
    ARDS_onset_subject = list(ARDS_onset['ARDS_ONSET'][ARDS_onset['SUBJECT_ID'] == subject_id])[0]
    ARDS_onset_subject_end = ARDS_onset_subject + datetime.timedelta(days=1)
    mask_subject = (pd.to_datetime(CH_ARDS_subject['CHARTTIME']) >= ARDS_onset_subject) & \
                   (pd.to_datetime(CH_ARDS_subject['CHARTTIME']) <= ARDS_onset_subject_end) & \
                   (pd.isnull(CH_ARDS_subject['VALUE']) == False)
    CH_ARDS_subject = CH_ARDS_subject.loc[mask_subject]

    CH_PEEP = CH_ARDS_subject[CH_ARDS_subject['ITEMID'].isin(PEEP_ID )]
    CH_PEEP = CH_PEEP.sort_index(by=['CHARTTIME'])
    subject_PEEP = most_frequent(pd.to_numeric(CH_PEEP['VALUE']),rule='min')

    CH_FO2 = CH_ARDS_subject[CH_ARDS_subject['ITEMID'].isin(FiO2_ID)]
    CH_FO2 = CH_FO2.sort_index(by=['CHARTTIME'])
    subject_FO2 = most_frequent(pd.to_numeric(CH_FO2['VALUE']),rule='min')

    mask_VT = CH_ARDS_subject['ITEMID'].isin([683])
    if mask_VT.any() == False:
        mask_VT = CH_ARDS_subject['ITEMID'].isin(VT_ID)
        CH_VT = CH_ARDS_subject.loc[mask_VT]
        mask_CHVT = pd.to_numeric(CH_VT['VALUE']) > 0
        CH_VT = CH_VT.loc[mask_CHVT]
        subject_VT = np.median(pd.to_numeric(CH_VT['VALUE']))
    else:
        CH_VT = CH_ARDS_subject[CH_ARDS_subject['ITEMID'].isin([683])]
        CH_VT = CH_ARDS_subject.loc[mask_VT]
        mask_CHVT = pd.to_numeric(CH_VT['VALUE']) > 0
        CH_VT = CH_VT.loc[mask_CHVT]
        subject_VT = most_frequent(pd.to_numeric(CH_VT['VALUE']), rule='median')

    CH_PP = CH_ARDS_subject[CH_ARDS_subject['ITEMID'].isin(PP_ID)]
    CH_PP = CH_PP.sort_index(by=['CHARTTIME'])
    CH_PP = CH_PP[pd.to_numeric(CH_PP['VALUE'])>0]
    subject_PP = most_frequent(pd.to_numeric(CH_PP['VALUE']),rule='max')

    CH_PIP = CH_ARDS_subject[CH_ARDS_subject['ITEMID'].isin(PIP_ID)]
    CH_PIP = CH_PIP.sort_index(by=['CHARTTIME'])
    mask_PIP = (pd.to_numeric(CH_PIP['VALUE']) >= subject_PP)
    if mask_PIP.any() == False:
        subject_PIP = '-'
    else:
        CH_PIP = CH_PIP.loc[mask_PIP]
        subject_PIP = most_frequent(pd.to_numeric(CH_PIP['VALUE']), rule='max')

    print(subject_id, subject_VT, subject_PP, round(subject_FO2,1), subject_PEEP, subject_PIP, subject_PP - subject_PEEP)