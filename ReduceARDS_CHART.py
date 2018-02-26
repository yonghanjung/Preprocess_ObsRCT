import numpy as np
import scipy as sp
import pandas as pd
import pickle

'''
Reduce CHARTEVENTS.csv by containing all chart event of ARDS PT    
'''

class ReduceARDS_CHART(object):
    def __init__(self):
        self.ARDS_PT = pickle.load(open('PKL/ARDS_PT.pkl','rb'))
        self.CHARTEVENT = pd.read_csv('OLD/raw_data/CHARTEVENTS.csv', chunksize=10 ** 6)

    def Reduce_ARDS_PT(self):
        CH_ARDS = []
        idx = 0
        for CH in self.CHARTEVENT:
            idx += 1
            print(idx)
            mask = CH['SUBJECT_ID'].isin(self.ARDS_PT)
            if mask.any():
                CH_ARDS.append(CH.loc[mask])
            else:
                continue

        CH_ARDS_raw = pd.concat(CH_ARDS)
        self.CH_ARDS_reduced = CH_ARDS_raw[['SUBJECT_ID','ICUSTAY_ID', 'ITEMID', 'CHARTTIME', 'VALUE']]

    def Dump_Pickle(self, X, X_name):
        pickle.dump(X, open(X_name, 'wb'))

    def Execute(self):
        self.Reduce_ARDS_PT()
        # self.Dump_Pickle(self.CH_ARDS_raw, 'PKL/CH_ARDS_raw.pkl')
        self.Dump_Pickle(self.CH_ARDS_reduced, 'PKL/CH_ARDS_reduced.pkl')

''' Main '''
if __name__ == '__main__':
    reduceCH = ReduceARDS_CHART()
    reduceCH.Execute()
