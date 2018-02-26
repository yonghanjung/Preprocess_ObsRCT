import numpy as np
import scipy as sp
import pandas as pd
import pickle
import datetime
from ARDS_vent import ARDS_vent

class Data_Preparation(ARDS_vent):
    def __init__(self):
        super(Data_Preparation, self).__init__()
        self.ARDS_AGE = pickle.load(open('PKL/ARDS_Age.pkl','rb'))
        self.ARDS_Gender = pickle.load(open('PKL/ARDS_Gender.pkl', 'rb'))
        self.ARDS_APACHE = pickle.load(open('PKL/ARDS_APACHE.pkl','rb'))
        self.ARDS_HeightWeight = pickle.load(open('PKL/ARDS_HeightWeight.pkl','rb'))

    def PBW(self, height, sex):
        if sex == 1: # MALE
            height = height * 0.3937
            PBW = 50 + 2.3 * (height - 60)
        else:
            height = height * 0.3937
            PBW = 45.5 + 2.3 * (height - 60)
        return PBW

    def df_float_convertible(self,df):
        try:
            pd.to_numeric(df)
            return True
        except ValueError:
            return False

    def float_convertible(self,val):
        try:
            float(val)
            return True
        except ValueError:
            return False


    def float_convertible_extractor(self, df):
        list_df = list(df)
        output = []
        for idx in range(len(list_df)):
            x = list_df[idx]
            if self.float_convertible(x) == True:
                output.append(x)
            else:
                continue
        return output

    def Indiv_preparation(self, subject_id, init_TF):
        subject_dict = dict()
        subject_dict['SUBJECT_ID'] = subject_id

        icuid = self.ARDS_ID['ICUID'][self.ARDS_ID['SUBJECT_ID']==subject_id].iloc[0]
        subject_dict['ICUID'] = icuid

        subject_age = self.ARDS_AGE['AGE'][self.ARDS_AGE['SUBJECT_ID']==subject_id].iloc[0]
        subject_dict['AGE'] = subject_age

        subject_SEX = self.ARDS_Gender['SEX'][self.ARDS_Gender['SUBJECT_ID']==subject_id].iloc[0]

        if subject_SEX == 'M':
            subject_SEX = 1
        else:
            subject_SEX = 0

        subject_dict['SEX'] = subject_SEX

        subject_apache = pd.to_numeric( self.ARDS_APACHE['APACHE'][(self.ARDS_APACHE['SUBJECT_ID']==subject_id) &
                                                 (self.ARDS_APACHE['ICUID']==icuid)].iloc[0] )
        subject_dict['APACHE'] = subject_apache

        subject_height = pd.to_numeric( self.ARDS_HeightWeight['Height'][(self.ARDS_HeightWeight['SUBJECT_ID']==subject_id) &
                                                 (self.ARDS_HeightWeight['ICUID']==icuid)].iloc[0] )
        if pd.isnull(subject_height) == True:
            subject_weight = self.ARDS_HeightWeight['Weight'][(self.ARDS_HeightWeight['SUBJECT_ID']==subject_id) &
                                                 (self.ARDS_HeightWeight['ICUID']==icuid)].iloc[0]
        else:
            subject_weight = pd.to_numeric( self.PBW(subject_height, subject_SEX) )
        subject_dict['WEIGHT'] = subject_weight

        subject_MV_duration = pd.to_numeric( self.MV_duration(icuid) )
        subject_dict['MV_DURATION'] = subject_MV_duration

        subject_DOD = list(self.ARDS_DOD[['28-SURVIVAL', '60-SURVIVAL', '90-SURVIVAL']][
                 self.ARDS_DOD['SUBJECT_ID'] == subject_id].iloc[0])
        subject_dict['28-SURVIVAL'] = subject_DOD[0]
        subject_dict['60-SURVIVAL'] = subject_DOD[1]
        subject_dict['90-SURVIVAL'] = subject_DOD[2]

        for idx in range(len(self.MV_items)):
            items = self.MV_items[idx]
            items_name = self.MV_items_name[idx]
            subject_CH = self.Chart_var_collector(items,subject_id,init_TF)
            if self.df_float_convertible( subject_CH['VALUE'] ) == True:
                item_val = np.mean(pd.to_numeric( subject_CH['VALUE']) )
                subject_dict[items_name] = item_val
            else:
                subject_CH_list = self.float_convertible_extractor(subject_CH['VALUE'])
                if len(subject_CH_list) > 0:
                    item_val = np.mean(subject_CH_list)
                    subject_dict[items_name] = item_val
                else:
                    subject_dict[items_name] = np.nan

        for idx in range(len(self.Bio_items)):
            items = self.Bio_items[idx]
            items_name = self.Bio_items_name[idx]
            subject_CH = self.Chart_var_collector(items,subject_id,init_TF)
            if self.df_float_convertible( subject_CH['VALUE'] ) == True:
                item_val = np.mean(pd.to_numeric( subject_CH['VALUE']) )
                subject_dict[items_name] = item_val
            else:
                subject_CH_list = self.float_convertible_extractor(subject_CH['VALUE'])
                if len(subject_CH_list) > 0:
                    item_val = np.mean(subject_CH_list)
                    subject_dict[items_name] = item_val
                else:
                    subject_dict[items_name] = np.nan
        return pd.DataFrame(subject_dict, index=[0])

    def Preparation(self):
        idx = 0
        for subject_id, icuid in zip(self.ARDS_ID['SUBJECT_ID'],self.ARDS_ID['ICUID']):
            print(subject_id)
            if idx == 0:
                ARDS_data = self.Indiv_preparation(subject_id,True)
            else:
                try:
                    ARDS_data = ARDS_data.append(self.Indiv_preparation(subject_id,True), ignore_index=True)
                except:
                    print(subject_id, 'occur errors')
                    raise TypeError
            idx += 1
        return ARDS_data



    def Print_Preparation(self):
        idx = 0
        for subject_id, icuid in zip(self.ARDS_ID['SUBJECT_ID'], self.ARDS_ID['ICUID']):
            if idx == 0:
                ARDS_data = self.Indiv_preparation(subject_id, True)
            else:
                try:
                    ARDS_data = ARDS_data.append(self.Indiv_preparation(subject_id, True), ignore_index=True)
                except:
                    print(subject_id, 'occur errors')
                    raise TypeError
            idx += 1




if __name__ == '__main__':
    preparation = Data_Preparation()
    ARDS_data = preparation.Preparation()
    pickle.dump(ARDS_data,open('PKL/ARDS_data.pkl','wb'))
    # subject_id = 1616
    # subject_info = preparation.Indiv_preparation(subject_id,False)