import numpy as np
import pandas as pd
import pickle

def compare_two_elem(x1,x0):
    result = pd.DataFrame(np.isin(x0,x1))*1
    result = list(result[0])
    return result



DIAGNOSIS = pd.read_csv('raw_data/DIAGNOSES_ICD.csv')

# ICD9_risk = ['486', '99591', '5070', '95901', '7907', '78552']
ICD9_risk = ['5185','51882']
ICD9_risk_num = [int(x) for x in ICD9_risk]
ICD9_risk_num.sort()

ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))
ARDS_DIAGNOSIS = DIAGNOSIS[DIAGNOSIS['SUBJECT_ID'].isin(ARDS_SUBJECT_ID)]
ARDS_DIAGNOSIS_risk = ARDS_DIAGNOSIS[ARDS_DIAGNOSIS['ICD9_CODE'].isin(ICD9_risk)]

ARDS_ICD9 = dict()
ARDS_ICD9['SUBJECT_ID'] = list()
ARDS_ICD9['ICD9_CODE'] = list()
ARDS_ICD9['ARDS_RISK'] = list()

# iteration
idx = 0
for subject_id in ARDS_SUBJECT_ID:
    mask = ARDS_DIAGNOSIS_risk['SUBJECT_ID'] == subject_id
    if mask.any():
        ARDS_DIAGNOSIS_subject = ARDS_DIAGNOSIS_risk.loc[mask]
        ICD9_subject = list(ARDS_DIAGNOSIS_subject['ICD9_CODE'].unique())
        ICD9_subject = [int(x) for x in ICD9_subject]
        ICD9_subject.sort()
        ARDS_ICD9['SUBJECT_ID'].append(subject_id)
        ARDS_ICD9['ICD9_CODE'].append(ICD9_subject)
        ARDS_ICD9['ARDS_RISK'].append(compare_two_elem(ICD9_subject, ICD9_risk_num))
    else:
        ARDS_ICD9['SUBJECT_ID'].append(subject_id)
        ARDS_ICD9['ICD9_CODE'].append(np.nan)
        ARDS_ICD9['ARDS_RISK'].append(np.nan)

ARDS_ICD9 = pd.DataFrame(ARDS_ICD9)
ARDS_SUBJECT_ID = list(ARDS_ICD9['SUBJECT_ID'])
ARDS_RISK = list(ARDS_ICD9['ARDS_RISK'])

for subject_id, ICD9_risk_subject in zip(ARDS_SUBJECT_ID,ARDS_RISK):
    try:
        n = len(ICD9_risk_subject)
        ICD9_risk_subject = [str(x) for x in ICD9_risk_subject]
        print(subject_id,",".join(ICD9_risk_subject),sep=",")
        idx += 1
    except:
        ICD9_risk_subject = [str(x) for x in [0]*6]
        print(subject_id, ",".join(ICD9_risk_subject), sep=",")

print(idx)