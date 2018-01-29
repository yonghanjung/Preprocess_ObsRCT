import pandas as pd
import numpy as np
import pickle
import datetime

CH_ARDS = pickle.load(open('CH_ARDS.pkl','rb'))
ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))
ARDS_onset = pickle.load(open('ARDS_onset_time.pkl','rb'))

days_chart = 2
VT_ID = [681, 683, 2043, 2044, 224684, 2400, 2408]
PEEP_ID = [505,506]

for subject_id in ARDS_SUBJECT_ID:
    onset_subject_id = list(ARDS_onset['onset_time'][ARDS_onset['subject_id'] == subject_id])[0]
    onsetend_subject_id = onset_subject_id + datetime.timedelta(days=days_chart)
    CH_subject = CH_ARDS[CH_ARDS['SUBJECT_ID'] == subject_id]
    mask = (pd.to_datetime(CH_subject['CHARTTIME']) > onset_subject_id) & \
           (pd.to_datetime(CH_subject['CHARTTIME']) < onsetend_subject_id)
    CH_subject_days = CH_subject.loc[mask]
    CH_subject_days_VT = CH_subject_days[CH_subject_days['ITEMID'].isin(VT_ID)]
    if len(CH_subject_days_VT) > 0:
        CH_subject_earlist_VT = CH_subject_days_VT.loc[
            pd.to_datetime(CH_subject_days_VT['CHARTTIME']) == min(pd.to_datetime(CH_subject_days_VT['CHARTTIME']))]
        VT = float(list(CH_subject_earlist_VT['VALUE'])[0])
    else:
        print(subject_id,'missing','missing')
        continue

    CH_subject_days_PEEP = CH_subject_days[CH_subject_days['ITEMID'].isin(PEEP_ID)]
    if len(CH_subject_days_PEEP) > 0:
        CH_subject_earlist_PEEP = CH_subject_days_PEEP.loc[
            pd.to_datetime(CH_subject_days_PEEP['CHARTTIME']) == min(pd.to_datetime(CH_subject_days_PEEP['CHARTTIME']))]
        PEEP = float(list(CH_subject_earlist_PEEP['VALUE'])[0])
    else:
        print(subject_id, 'missing', 'missing')
        continue

    print(subject_id,VT,PEEP,sep=',')
