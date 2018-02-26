import numpy as np
import scipy as sp
import pandas as pd
import pickle
import datetime

class ARDS_variable_collector():
    def __init__(self):
        self.CH_ARDS = pickle.load(open('PKL/ARDS_reduced_CH.pkl', 'rb'))
        self.ARDS_ID = pickle.load(open('PKL/ARDS_ID.pkl', 'rb'))
        self.ARDS_ONSET = pickle.load(open('PKL/ARDS_ONSETTIME.pkl', 'rb'))
        self.ARDS_DOD = pickle.load(open('PKL/ARDS_DOD.pkl', 'rb'))
        self.VENT = pd.read_csv('ventsettings.csv')
        self.ARDS_AGE = pickle.load(open('PKL/ARDS_Age.pkl','rb'))
        self.ARDS_DRUG = pickle.load(open('PKL/ARDS_drug.pkl','rb'))
        self.ARDS_Gender = pickle.load(open('PKL/ARDS_Gender.pkl','rb'))
        self.ARDS_APACHE = pickle.load(open('PKL/ARDS_APACHE.pkl','rb'))
        self.ARDS_HeightWeight = pickle.load(open('PKL/ARDS_HeightWeight.pkl','rb'))
        self.ARDS_DIAGNOSES = pickle.load(open('PKL/ARDS_diagnoses.pkl','rb'))

        self.key_VT = [639, 654, 681, 682, 683, 684, 224685, 224684, 224686]
        self.key_FiO2 = [190, 2981]
        self.key_PP = [543]
        self.key_PEEP = [60, 437, 505, 506, 686, 220339, 224700]
        self.key_MV = [445, 448, 449, 450, 1340, 1486, 1600, 224687]

        self.key_PaO2 = [779]
        self.key_SpO2 = [646]
        self.HeartRate = [211, 220045]
        self.ResRate = [618, 615, 220210, 224690]
        self.pH = [780, 1126]

        self.key_Vent = [self.key_PEEP, self.key_FiO2, self.key_PP, self.key_VT, self.key_MV]
        self.O2_vital = [self.key_PaO2, self.key_SpO2, self.HeartRate, self.ResRate, self.pH]
        self.vent_name = ['PEEP', 'FiO2', 'PP', 'VT', 'MV']
        self.O2_vital_name = ['PaO2', 'SpO2', 'HeartRate', 'ResRate', 'pH']

    def hour_difference(self,time_obj1, time_obj2):
        return abs(time_obj1.value - time_obj2.value)/(10**9 * 60 * 60)

    def days_difference(self,time_obj1, time_obj2):
        return round(abs(time_obj1.value - time_obj2.value) / (10 ** 9 * 86400),2)

    def MV_duration(self, icuid):
        icuid_duration = pd.to_datetime(self.VENT['charttime'][self.VENT['icustay_id'] == icuid])
        if len(icuid_duration) >= 2:
            return self.days_difference(max(icuid_duration),min(icuid_duration))
        elif len(icuid_duration) == 1:
            return 0
        else:
            return np.nan

    def PT_ARDS_onset(self, subject_id):
        return self.ARDS_ONSET['ARDS_ONSETTIME'][self.ARDS_ONSET['SUBJECT_ID']==subject_id].iloc[0]

    def Check_Mortality(self, subject_id):
        subject_DOD = list(self.ARDS_DOD[['28-SURVIVAL', '60-SURVIVAL', '90-SURVIVAL']][self.ARDS_DOD['SUBJECT_ID'] == subject_id].iloc[0])
        if subject_DOD == [1,1,1]:
            return 1
        else:
            return 0

    def Chart_var_collector(self, itemid, subject_id, startdate, deadline):

        # Possible start and end date
        ## ARDS initial setting (48hr)
            # startdate = subject_ARDS_onset = self.PT_ARDS_onset(subject_id)
            # enddate = 2
            # then startdate + datetime.timedelta(days = enddate)
        ## ARDS initial setting (all MV end)
            # startdate = subject_ARDS_onset
            # enddate = subject_MV_duration+1
            # subject_MV_duration = self.MV_duration(icuid)
        ## From MV duration to 28 days
        # startdate = subject_ARDS_onset + datetimes
        # enddate = subject_MV_duration+1
        # subject_MV_duration = self.MV_duration(icuid)

        icuid = self.ARDS_ID['ICUID'][self.ARDS_ID['SUBJECT_ID'] == subject_id].iloc[0]

        if deadline== '48hr':
            startdate = self.PT_ARDS_onset(subject_id) # SUBJECT_ARDS_Onset
            enddate = 2 # 48 hours
            subject_ARDS_MV_end = startdate + datetime.timedelta(days = enddate)
        elif deadline == '7days':
            startdate = self.PT_ARDS_onset(subject_id)  # SUBJECT_ARDS_Onset
            subject_MV_duration = self.MV_duration(icuid)
            enddate = subject_MV_duration + 1
            subject_ARDS_MV_end = startdate + datetime.timedelta(days=enddate)
        elif deadline == '28':
            subject_MV_duration = self.MV_duration(icuid)
            startdate = self.PT_ARDS_onset(subject_id) + datetime.timedelta(days=subject_MV_duration+1)
            subject_ARDS_MV_end = startdate + datetime.timedelta(days=28-subject_MV_duration)
        elif deadline == '90':
            startdate = self.PT_ARDS_onset(subject_id) + datetime.timedelta(days=28)
            subject_ARDS_MV_end = startdate + datetime.timedelta(days=90 - 28)

        mask1 = ((self.CH_ARDS['SUBJECT_ID'] == subject_id) &
                (self.CH_ARDS['ICUSTAY_ID'] == icuid) &
                (self.CH_ARDS['ITEMID'].isin(itemid)) &
                 (pd.isnull(self.CH_ARDS['VALUE']) == False)
                 )

        subject_CH = self.CH_ARDS[mask1]
        mask2 = (
                 (pd.to_datetime(subject_CH['CHARTTIME']) >=  startdate) &
                 (pd.to_datetime(subject_CH['CHARTTIME']) <= subject_ARDS_MV_end)
                )

        subject_CH = subject_CH[mask2]
        return subject_CH

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

    def disease_history(self, subject_id):
        icuid = self.ARDS_ID['ICUID'][self.ARDS_ID['SUBJECT_ID'] == subject_id].iloc[0]


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

        for idx in range(len(self.key_Vent)):
            items = self.key_Vent[idx]
            items_name = self.vent_name[idx]
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

        for idx in range(len(self.O2_vital)):
            items = self.O2_vital[idx]
            items_name = self.O2_vital_name[idx]
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

if __name__ == '__main__':
    collector = ARDS_variable_collector()
    ARDS_data = collector.Preparation()
    pickle.dump(ARDS_data, open('PKL/ARDS_data.pkl', 'wb'))




