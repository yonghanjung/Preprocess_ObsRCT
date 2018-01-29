import pandas as pd
import pickle
import methods

ADMISSIONS = pd.read_csv('raw_data/ADMISSIONS.csv')
DIAGNOSIS = pd.read_csv('raw_data/DIAGNOSES_ICD.csv')
CH_Berlin_reduced = pickle.load(open('CH_Berlin_reduced.pkl','rb'))
SUBJECT_cand = pickle.load(open('SUBJECT_cand_CPT.pkl','rb'))
SUBJECT_cand.sort()


ARDS_patients = list()
N = len(SUBJECT_cand)
idx = 0
for subject_id in SUBJECT_cand:
    result = methods.ARDS_patients_detector(ADMISSIONS, CH_Berlin_reduced, DIAGNOSIS, subject_id)
    if result:
        ARDS_patients.append(subject_id)
        print(subject_id, round(idx/N,4),result)
    else:
        print(subject_id, round(idx/N,4),result)
    idx += 1
    break

pickle.dump(ARDS_patients, open('ARDS_SUBJECT_ID.pkl','wb'))
