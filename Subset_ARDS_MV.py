import pandas as pd
import numpy as np
import scipy as sp
import pickle

class Subset_ARDS_MV(object):
    ''' Rough algorithm
    For each icustay_id in ventsettings,
        If list(ventsettings['mechvent'][ventsettings['icustay_id'] == icustay_id]) includes 1,
            Match icustay_id with SUBJECT_ID
        Else,
            Skip

    '''

    def __init__(self):
        self.ARDS_PT = pickle.load(open('PKL/ARDS_PT.pkl','rb'))
        self.ventsettings = pd.read_csv('ventsettings.csv')
        self.ICUSTAY = pd.read_csv('OLD/raw_data/ICUSTAYS.csv')

    def MV_identifier(self, icustay_id):
        if 1 in list(self.ventsettings['mechvent'][self.ventsettings['icustay_id'] == icustay_id]):
            return True
        else:
            return False

    def Match_ICU_SUBJECT(self, icustay_id):
        return list(self.ICUSTAY['SUBJECT_ID'][self.ICUSTAY['ICUSTAY_ID'] == icustay_id])[0]

    def ARDS_identifier(self, subject_id):
        if int(subject_id) in self.ARDS_PT:
            return True
        else:
            return False

    def Execute(self):
        ICUSTAY_IDs = np.unique(self.ventsettings['icustay_id'])
        ARDS_MV_SUBSET = []
        ARDS_ICUID = []
        for icustay_id in ICUSTAY_IDs:
            if self.MV_identifier(icustay_id):
                subject_id = self.Match_ICU_SUBJECT(icustay_id)
                if self.ARDS_identifier(subject_id):
                    ARDS_MV_SUBSET.append(subject_id)
                    ARDS_ICUID.append(icustay_id)
                else:
                    continue
            else:
                continue
        return ARDS_MV_SUBSET, ARDS_ICUID

##### MAIN #####
if __name__ == '__main__':
    subset = Subset_ARDS_MV()
    ARDS_MV_SUBSET, ARDS_ICUID = subset.Execute()
    pickle.dump(ARDS_ICUID,open('PKL/ARDS_ICUID.pkl','wb'))
    pickle.dump(ARDS_MV_SUBSET,open('PKL/ARDS_MV_SUBSET.pkl','wb'))