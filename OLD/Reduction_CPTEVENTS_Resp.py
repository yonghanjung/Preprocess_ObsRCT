import pickle
import pandas as pd

CH_Berlin = pickle.load(open('CH_Berlin.pkl','rb'))
SUBJECT_cand = list(CH_Berlin.SUBJECT_ID.unique())

CPTEVENTS = pd.read_csv('raw_data/CPTEVENTS.csv')
CPTEVENTS_reduced = CPTEVENTS[CPTEVENTS['SUBJECT_ID'].isin(SUBJECT_cand)]
CPTEVENTS_reduced = CPTEVENTS_reduced[CPTEVENTS_reduced['COSTCENTER'] == 'Resp']
SUBJECT_cand = list(CPTEVENTS_reduced.SUBJECT_ID.unique())

CH_Berlin = CH_Berlin[CH_Berlin['SUBJECT_ID'].isin(SUBJECT_cand)]
CH_Berlin_reduced = CH_Berlin[['SUBJECT_ID','ITEMID','CHARTTIME','VALUE']]

pickle.dump(SUBJECT_cand,open('SUBJECT_cand_CPT.pkl','wb'))
pickle.dump(CH_Berlin, open('CH_Berlin_reduced.pkl','wb'))