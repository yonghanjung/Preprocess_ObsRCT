import numpy as np
import scipy as sp
import pandas as pd
import pickle
import datetime

class ARDS_variable_collector():
    def __init__(self):
        self.CH_ARDS = pickle.load(open('PKL/ARDS_reduced_CH.pkl', 'rb'))
        self.ARDS_ID = pickle.load(open('PKL/ARDS_ID_unique.pkl', 'rb'))
        self.VENT = pd.read_csv('ventsettings.csv')

        self.ARDS_ONSET = pickle.load(open('PKL/ARDS_ONSETTIME.pkl', 'rb'))

        self.key_VT = [639, 654, 681, 682, 683, 684, 224685, 224684, 224686]
        self.key_FiO2 = [190, 2981]
        self.key_PP = [543]
        self.key_PEEP = [60, 437, 505, 506, 686, 220339, 224700]
        self.key_MV = [445, 448, 449, 450, 1340, 1486, 1600, 224687]

        self.CH_vals = [self.key_PEEP, self.key_FiO2, self.key_PP, self.key_VT, self.key_MV]
        self.CH_names = ['PEEP', 'FiO2', 'PP', 'VT', 'MV']

    def PT_ARDS_onset(self, subject_id):
        return self.ARDS_ONSET['ARDS_ONSETTIME'][self.ARDS_ONSET['SUBJECT_ID']==subject_id].iloc[0]


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

    def Chart_var_collector(self, itemid, subject_id, date_mode):

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

        icuid = self.ARDS_ID['ICUSTAY_ID'][self.ARDS_ID['SUBJECT_ID'] == subject_id].iloc[0]

        if date_mode== '48hr':
            startdate = self.PT_ARDS_onset(subject_id) # SUBJECT_ARDS_Onset
            enddate = 2 # 48 hours
            subject_ARDS_MV_end = startdate + datetime.timedelta(days = enddate)
        elif date_mode == '7days':
            startdate = self.PT_ARDS_onset(subject_id)  # SUBJECT_ARDS_Onset
            subject_MV_duration = self.MV_duration(icuid)
            enddate = subject_MV_duration + 1
            subject_ARDS_MV_end = startdate + datetime.timedelta(days=enddate)

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

    def MV_duration(self, icuid):
        icuid_duration = pd.to_datetime(self.VENT['charttime'][self.VENT['icustay_id'] == icuid])
        if len(icuid_duration) >= 2:
            return self.days_difference(max(icuid_duration),min(icuid_duration))
        elif len(icuid_duration) == 1:
            return 0
        else:
            return np.nan


    def Indiv_preparation(self, subject_id, icuid, subject_hadm):
        subject_dict = dict()
        # Collect subject_basic id
        subject_dict['SUBJECT_ID'] = subject_id
        subject_dict['ICUSTAY_ID'] = icuid
        subject_dict['HADM_ID'] = subject_hadm

        for idx_CH in range(len(self.CH_vals)):
            items = self.CH_vals[idx_CH]
            items_name = self.CH_names[idx_CH]
            subject_CH_48hr = self.Chart_var_collector(items,subject_id,date_mode='48hr')
            subject_CH_7days = self.Chart_var_collector(items, subject_id, date_mode='7days')

            subject_CH_list = [subject_CH_48hr, subject_CH_7days]
            subject_CH_names = ['48hr','7days']

            for idx_subject_CH in range(len(subject_CH_list)):
                subject_CH = subject_CH_list[idx_subject_CH]
                if self.df_float_convertible( subject_CH['VALUE'] ) == True:
                    item_val = np.mean(pd.to_numeric( subject_CH['VALUE']) )
                    subject_dict[items_name + str(' ') + subject_CH_names[idx_subject_CH]] = item_val
                else:
                    subject_CH_list = self.float_convertible_extractor(subject_CH['VALUE'])
                    if len(subject_CH_list) > 0:
                        item_val = np.mean(subject_CH_list)
                        subject_dict[items_name + str(' ') + subject_CH_names[idx_subject_CH]] = item_val
                    else:
                        subject_dict[items_name + str(' ') + subject_CH_names[idx_subject_CH]] = np.nan

        return pd.DataFrame(subject_dict, index=[0])

    def Preparation(self):
        idx = 0
        N = len(self.ARDS_ID)
        for subject_id, icuid, hadm_id in zip(self.ARDS_ID['SUBJECT_ID'],self.ARDS_ID['ICUSTAY_ID'], self.ARDS_ID['HADM_ID']):
            print(subject_id, round((idx / N)*100,4))
            if idx == 0:
                ARDS_data = self.Indiv_preparation(subject_id,icuid,hadm_id)
            else:
                try:
                    ARDS_data = ARDS_data.append(self.Indiv_preparation(subject_id,icuid,hadm_id), ignore_index=True)
                except:
                    print(subject_id, 'occur errors')

            idx += 1
        return ARDS_data

if __name__ == '__main__':
    collector = ARDS_variable_collector()
    ARDS_data = collector.Preparation()
    pickle.dump(ARDS_data, open('PKL/ARDS_VENT.pkl', 'wb'))




