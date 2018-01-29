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

        self.key_VT  = [639, 654, 681, 682, 683, 684, 224685, 224684, 224686]
        self.key_FiO2 = [190, 2981]
        self.key_PP = [543]
        self.key_PEEP = [60,437,505,506,686,220339,224700]
        self.key_PaO2 = [779]
        self.key_PIP = [221,1,1211,1655,2000,226873,224738,224419,224750,227187]
        self.Berlin = self.key_FiO2 + self.key_PaO2

        self.key_Ventmode = [223849]
