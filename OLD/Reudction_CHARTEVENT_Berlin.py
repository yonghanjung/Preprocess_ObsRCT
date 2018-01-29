import pandas as pd
import pickle

CHARTEVENT = pd.read_csv('raw_data/CHARTEVENTS.csv',chunksize=10**6)
ItemID_FiO2 = [190, 2981]
ItemID_PaO2 = [779]
ITEMID_Berlin = ItemID_PaO2 + ItemID_FiO2

REDUCTION_CHARTEVENT = []
idx = 0
for CH in CHARTEVENT:
    idx += 1
    mask = CH['ITEMID'].isin(ITEMID_Berlin)
    if mask.any():
        REDUCTION_CHARTEVENT.append(CH.loc[mask])
        print(idx, 'include')
    else:
        print(idx, 'skip')
        continue

REDUCTION_CHARTEVENT = pd.concat(REDUCTION_CHARTEVENT)
pickle.dump(REDUCTION_CHARTEVENT,open('CH_Berlin.pkl','wb'))
