import pickle
import pandas as pd
import numpy as np
import datetime
import methods

ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))
ARDS_HEIGHT = pickle.load(open('ARDS_HEIGHT.pkl','rb'))
ARDS_PATIENTS = pickle.load(open('ARDS_PATIENTS.pkl','rb'))
ARDS_onset = pickle.load(open('ARDS_onset.pkl','rb'))
CH_ARDS_reduced = pickle.load(open('CH_ARDS_reduced.pkl','rb'))
D_ITEM = pd.read_csv('raw_data/D_ITEMS.csv')

# D_ITEM[['ITEMID','LABEL']][ (D_ITEM['LABEL'].str.contains("PEEP") == True) ]

Weight_ID = [580,763,581,224639,226512,226531]
Weight_SubID = [580,763,581]
CH_ARDS_weight = CH_ARDS_reduced[CH_ARDS_reduced['ITEMID'].isin(Weight_ID)]

for subject_id in ARDS_SUBJECT_ID:
    # HEIGHT exists?
    height_subject = list(ARDS_HEIGHT['HEIGHT'][ARDS_HEIGHT['SUBJECT_ID'] == subject_id])[0]
    if pd.isnull(height_subject):
        CH_weight_subject = CH_ARDS_weight[CH_ARDS_weight['SUBJECT_ID'] == subject_id]
        subject_admission = pd.to_datetime(list(ARDS_onset['ADMITTIME'][ARDS_onset['SUBJECT_ID'] == subject_id])[0] )
        subject_onset = pd.to_datetime(list(ARDS_onset['ARDS_ONSET'][ARDS_onset['SUBJECT_ID'] == subject_id])[0] )
        subject_admission_end = subject_onset + datetime.timedelta(days = 3)
        mask_subject = (pd.to_datetime(CH_weight_subject['CHARTTIME']) >= subject_admission) & \
                       (pd.to_datetime(CH_weight_subject['CHARTTIME']) <= subject_admission_end) & \
                       (pd.isnull(pd.to_numeric(CH_weight_subject['VALUE'])) == False )
        if mask_subject.any() == False:
            print(subject_id, '-', sep="|")
            continue
        CH_weight_subject_selected = CH_weight_subject.loc[mask_subject]

        mask_Subselect = CH_weight_subject_selected['ITEMID'].isin(Weight_SubID)
        if mask_Subselect.any() == False:
            print("HOHOHOHO")
        CH_weight_subject_Subselected = CH_weight_subject_selected.loc[mask_Subselect]
        subject_weight = np.mean(pd.to_numeric(CH_weight_subject_Subselected['VALUE']))
        subject_weight = round(subject_weight, 2)
        print(subject_id, subject_weight, sep="|")

    else:
        subject_gender = list(ARDS_PATIENTS['GENDER'][ARDS_PATIENTS['SUBJECT_ID']==subject_id])[0]
        if subject_gender == 'M':
            subject_weight = 50 + 0.91 * (height_subject - 152.4)
            subject_weight = round(subject_weight,2)
        elif subject_gender == 'F':
            subject_weight = 45.5 + 0.91 * (height_subject - 152.4)
            subject_weight = round(subject_weight, 2)

        print(subject_id, subject_weight, sep='|')
