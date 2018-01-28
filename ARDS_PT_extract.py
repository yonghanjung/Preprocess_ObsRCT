import numpy as np
import scipy as sp
import pandas as pd
import pickle
from ItemID import ItemIDSearch 

class ReduceCHARTEVENT(ItemIDSearch):
     def __init__(self):
         super().__init__()
         self.ItemKey()
         self.CHARTEVENT = pd.read_csv('OLD/raw_data/CHARTEVENTS.csv', chunksize=10**6)

     def Reduce_CH_by_Berlin(self):
         reduced_CH = []
         idx = 0
         for CH in self.CHARTEVENT:
             idx += 1
             mask = CH['ITEMID'].isin(self.Berlin)
             if mask.any():
                 reduced_CH.append(CH.loc[mask])
                 print(idx, 'include')
             else:
                 print(idx, 'skip')
                 continue

         self.reduced_CH = pd.concat(reduced_CH)

     def Dump_Pickle(self, X, X_name):
         pickle.dump(X, open(X_name, 'wb'))

     def Execute(self):
         self.Reduce_CH_by_Berlin()
         self.Dump_Pickle(self.reduced_CH,'PKL/reduced_CH.pkl')



''' Main '''
reduceCH = ReduceCHARTEVENT()
reduceCH.Execute()



