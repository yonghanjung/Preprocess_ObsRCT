import pandas as pd
import numpy as np
import scipy as sp

class ItemIDSearch(object):
    def __init__(self):
        pd.read_csv('OLD/raw_data/CHARTEVENTS.csv', chunksize=10 ** 6)
        self.D_ITEM = pd.read_csv('OLD/raw_data/D_ITEMS.csv')

    def FindItemID(self, item_name):
        return self.D_ITEM[['ITEMID', 'LABEL']][(self.D_ITEM['LABEL'].str.contains("PEEP") == True)]

    def ItemKey(self):
        self.key_PEEP = [505, 506]
        self.key_VT  = [681,683,2043,2044,224684,2400, 2408]
        self.key_FiO2 = [190, 2981]
        self.key_PP = [543, 224696]
        self.key_PaO2 = [779]
        self.Berlin = self.key_FiO2 + self.key_PaO2



# def D_item_str_search(D_ITEM, myStr):
#     '''
#     Extract ITEMID and Label, which label includes myStr.
#     :param D_ITEM:
#     :param myStr:
#     :return: rows that contain myStr in Label
#     '''
#     return D_ITEM[['ITEMID', 'LABEL']][(D_ITEM['LABEL'].str.contains("PEEP") == True)]
