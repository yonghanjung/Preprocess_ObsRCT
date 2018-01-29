import pandas as pd
import pickle

ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))
CHARTEVENT = pd.read_csv('raw_data/CHARTEVENTS.csv',chunksize=10 ** 6)

ItemID_FiO2 = [190, 2981]
ItemID_PaO2 = [779]
ITEMID_Berlin = ItemID_PaO2 + ItemID_FiO2

CH_ARDS = []
idx = 0
for CH in CHARTEVENT:
    idx += 1
    print(idx)
    mask = CH['SUBJECT_ID'].isin(ARDS_SUBJECT_ID)
    if mask.any():
        CH_ARDS.append(CH.loc[mask])
    else:
        continue

CH_ARDS = pd.concat(CH_ARDS)
CH_ARDS_reduced = CH_ARDS[['SUBJECT_ID','ITEMID','CHARTTIME','VALUE']]
CH_ARDS_Berlin = CH_ARDS_reduced[CH_ARDS_reduced['ITEMID'].isin(ITEMID_Berlin)]

pickle.dump(CH_ARDS,open('CH_ARDS.pkl','wb'))
pickle.dump(CH_ARDS_reduced,open('CH_ARDS_reduced.pkl','wb'))
pickle.dump(CH_ARDS_Berlin,open('CH_ARDS_Berlin.pkl','wb'))