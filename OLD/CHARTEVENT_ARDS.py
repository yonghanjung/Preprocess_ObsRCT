import pandas as pd
import pickle
import dateutil

SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))
PATIENTS = pd.read_csv('raw_data/PATIENTS.csv')

CH_IT = pd.read_csv('raw_data/CHARTEVENTS.csv',chunksize=10 ** 6)
CH_ARDS = []
idx = 0
for chunk in CH_IT:
    mask = chunk['SUBJECT_ID'].isin(SUBJECT_ID)
    if mask.any():
        chunk = chunk[['SUBJECT_ID','ITEMID','CHARTTIME','VALUE']]
        CH_ARDS.append(chunk.loc[mask])
        print(idx, mask.any())
        idx += 1
    else:
        print(idx, 'skip')
        idx += 1
        continue


CH_ARDS = pd.concat(CH_ARDS)
pickle.dump(CH_ARDS, open('CH_ARDS.pkl','wb'))