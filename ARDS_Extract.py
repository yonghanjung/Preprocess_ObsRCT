import numpy as np
import pandas as pd
import pickle
import dateutil
import datetime

class ARDS_Extract(object):
    def __init__(self):
        ### Predefined variable ###
        ### Window days are days w such that  |s-t| <= w for PaO2_s and SpO2_t
        self.window_days = 1

        ### Necessary Item IDs ###
        self.key_PEEP = [505, 506]

        self.key_VT = [639, 654, 681, 682, 683, 684, 224685, 224684, 224686]
        self.key_FiO2 = [190, 2981]
        self.key_PP = [543]
        self.key_PEEP = [60, 437, 505, 506, 686, 220339, 224700]
        self.key_PaO2 = [779]
        self.key_PIP = [221, 1, 1211, 1655, 2000, 226873, 224738, 224419, 224750, 227187]
        self.Berlin = self.key_FiO2 + self.key_PaO2

        self.key_Ventmode = [223849]

        ### Necessary csv files (reduced and ecoded with pickle) ###
        try:
            self.reduced_CH = pickle.load(open('PKL/reduced_CH.pkl','rb'))
        except:
            print("Run 'ReduceCHARTEVENT.py' first")
            raise Exception(" There is no 'reduced_CH.pkl' file! ")

        self.ADMISSIONS = pd.read_csv('OLD/raw_data/ADMISSIONS.csv')

    def TF_HeartFailure(self, subject_id):
        '''
        Check subject has heart failure or not.
        If heart fail, then NOT ARDS.
        :param subject_id: subject id
        :return: True means no heart failure ==> ARDS
        '''
        subject_CH = self.reduced_CH[self.reduced_CH['SUBJECT_ID'] == subject_id]
        subject_ICD9 = subject_CH['ICD9_CODE']
        if '4280' in list(subject_ICD9):
            return False
        else:
            return True

    def Admittime_extract(self, subject_id):
        '''
        Extract admission time of subject
        :param subject_id:
        :return: sorted array of subject admission times.
        '''
        subject_ADMITTIME= self.ADMISSIONS['ADMITTIME'][self.ADMISSIONS['SUBJECT_ID'] == subject_id]
        return sorted(pd.to_datetime(subject_ADMITTIME))


    def Admittime_correction(self, subject_admittimes, subject_CH):
        '''
        Match years of chartevent and admission time 
        :param admittime: PT's admission time in ADMISSION (sorted and encoded as array)
        :param subject_id: subject id 
        :return: new admissiontime array, matchined with charttime.
        '''
        min_admittime = subject_admittimes[0]
        subject_CH_time = pd.to_datetime(subject_CH['CHARTTIME'])
        try:
            min_charttime = min(subject_CH_time)
        except:
            print(subject_CH_time)
            raise Exception('Error in taking min of subject_CH_time')

        new_admittimes = []
        # If there are 100 yrs differences b/w earlist chart event time and initial admission,
        # which is not making any sense, implying neccesity in correcing year encoding

        while( abs(min_charttime.year - min_admittime.year) >= 100 ):
            # Matching charttime and admission time
            # by replacing admission time to charttime.
            if min_admittime > min_charttime: ##
                for a in subject_admittimes:
                    a = a.replace(year=a.year - 100)
                    new_admittimes.append(a)
            else:
                for a in subject_admittimes:
                    a = a.replace(year=a.year + 100)
                    new_admittimes.append(a)
            min_admittime = min(new_admittimes)

        subject_admittimes = new_admittimes
        return subject_admittimes

    def ARDS_marker_in_Window(self, subject_admittimes, subject_CH):
        '''

        :param subject_admittimes: Admittime with matched years to chartevent
        :return:
        '''

        subject_admittimes_end = np.array(subject_admittimes) + \
                                 datetime.timedelta(days = self.window_days)

        # for a_start, a_end in zip(subject_admittimes, subject_admittimes_end):
        #     mask = (subjec>= admittime) & (chart_time <= admittime_end)









