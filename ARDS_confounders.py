import numpy as np
import pandas as pd
import pickle
import dateutil
import datetime

class ARDS_confounder(object):
    def __init__(self):
        self.ARDS_ONSET = pickle.load(open('PKL/ARDS_ONSETTIME.pkl', 'rb'))
        self.ARDS_PT = pickle.load(open('PKL/ARDS_MV_SUBSET.pkl', 'rb'))
        PATIENTS = pd.read_csv('OLD/raw_data/PATIENTS.csv')
        self.PATIENTS = PATIENTS[PATIENTS['SUBJECT_ID'].isin(self.ARDS_PT)]
        AGE = pd.read_csv('age.csv')
        mask_age = AGE['subject_id'].isin(self.ARDS_PT)
        self.AGE = AGE[mask_age]
        self.HeightWeight = pd.read_csv('heightweight.csv')
        self.ARDS_ID = pickle.load(open('PKL/ARDS_ID.pkl', 'rb'))
        self.APACHE = pd.read_csv('apsiii.csv')

    def Gender(self):
        ARDS_gender = dict()
        ARDS_gender['SUBJECT_ID'] = []
        ARDS_gender['SEX'] = []

        for subject_id, gender in zip(self.PATIENTS['SUBJECT_ID'], self.PATIENTS['GENDER']):
            ARDS_gender['SUBJECT_ID'].append(subject_id)
            ARDS_gender['SEX'].append(gender)

        return pd.DataFrame(ARDS_gender)

    def Age_compute_if_none(self, subject_id):
        DOB = list(self.PATIENTS['DOB'][self.PATIENTS['SUBJECT_ID'] == subject_id])[0]
        DOB = dateutil.parser.parse(DOB)
        if DOB.year < 1900:
            return 89
        admit_time = list(self.ARDS_ONSET['ADMITTIME'][self.ARDS_ONSET['SUBJECT_ID'] == subject_id])[0]
        if DOB > admit_time:
            admit_time = admit_time.replace(year=admit_time.year + 100)
        year_diff = admit_time.year - DOB.year
        if year_diff > 100:
            year_diff -= 100
        age = year_diff
        return age

    def Age(self):
        ARDS_age = dict()
        ARDS_age['SUBJECT_ID'] = []
        ARDS_age['AGE'] = []

        for subject_id in self.ARDS_PT:
            subject_AGE = self.AGE[self.AGE['subject_id'] == subject_id]
            if len(subject_AGE) == 0:
                age = self.Age_compute_if_none(subject_id)
            elif len(subject_AGE) == 1:
                age = list(subject_AGE['age'])[0]
            else:
                for idx in range(len(subject_AGE)):
                    age_admittime = pd.to_datetime( subject_AGE.iloc[idx]['admittime'] )
                    ards_admittime = list(self.ARDS_ONSET['ADMITTIME'][self.ARDS_ONSET['SUBJECT_ID'] == subject_id])[0]
                    if age_admittime.month == ards_admittime.month and age_admittime.day == ards_admittime.day:
                        age = subject_AGE.iloc[idx]['age']
                        break
            ARDS_age['SUBJECT_ID'].append(subject_id)
            ARDS_age['AGE'].append(age)
        return pd.DataFrame(ARDS_age)

    def Height_Weight_extracter(self):
        ARDS_HW = dict()
        ARDS_HW['SUBJECT_ID'] = []
        ARDS_HW['ICUID'] = []
        ARDS_HW['Height'] = []
        ARDS_HW['Weight'] = []

        for subject_id, icuid in zip(self.ARDS_ID['SUBJECT_ID'], self.ARDS_ID['ICUID'] ):
            subject_HW = self.HeightWeight[ (self.HeightWeight['subject_id'] == subject_id) &
                               (self.HeightWeight['icustay_id'] == icuid)   ]
            if len(subject_HW) > 0:
                subject_height = subject_HW['height_first'].iloc[0]
                subject_weight = subject_HW['weight_first'].iloc[0]

                ARDS_HW['Height'].append(subject_height)
                ARDS_HW['Weight'].append(subject_weight)
                ARDS_HW['SUBJECT_ID'].append(subject_id)
                ARDS_HW['ICUID'].append(icuid)
            else:
                ARDS_HW['Height'].append(99999)
                ARDS_HW['Weight'].append(99999)
                ARDS_HW['SUBJECT_ID'].append(subject_id)
                ARDS_HW['ICUID'].append(icuid)

        return pd.DataFrame(ARDS_HW)

    def APACHE_extracter(self):
        ARDS_APACHE = dict()
        ARDS_APACHE['SUBJECT_ID'] = []
        ARDS_APACHE['ICUID'] = []
        ARDS_APACHE['APACHE'] = []
        ARDS_APACHE['APACHE_PROB'] = []

        for subject_id, icuid in zip(self.ARDS_ID['SUBJECT_ID'], self.ARDS_ID['ICUID']):
            subject_apache = self.APACHE[(self.APACHE['subject_id'] == subject_id) &
                                           (self.APACHE['icustay_id'] == icuid)]
            if len(subject_apache) > 0:
                subject_apachescore = subject_apache['apsiii'].iloc[0]
                subject_apacheprob = subject_apache['apsiii_prob'].iloc[0]

                ARDS_APACHE['SUBJECT_ID'].append(subject_id)
                ARDS_APACHE['ICUID'].append(icuid)
                ARDS_APACHE['APACHE'].append(subject_apachescore)
                ARDS_APACHE['APACHE_PROB'].append(subject_apacheprob)

            else:
                ARDS_APACHE['SUBJECT_ID'].append(subject_id)
                ARDS_APACHE['ICUID'].append(icuid)
                ARDS_APACHE['APACHE'].append(99999)
                ARDS_APACHE['APACHE_PROB'].append(99999)
        return pd.DataFrame(ARDS_APACHE)


    def Execute(self):
        # ARDS_Age = self.Age()
        # ARDS_HeightWeight = self.Height_Weight_extracter()
        ARDS_Gender = self.Gender()
        # ARDS_APACHE = self.APACHE_extracter()

        # pickle.dump(ARDS_Age,open('PKL/ARDS_Age.pkl','wb'))
        # pickle.dump(ARDS_HeightWeight, open('PKL/ARDS_HeightWeight.pkl', 'wb'))
        pickle.dump(ARDS_Gender, open('PKL/ARDS_Gender.pkl', 'wb'))
        # pickle.dump(ARDS_APACHE, open('PKL/ARDS_APACHE.pkl','wb'))

if __name__ == '__main__':
    confounder = ARDS_confounder()
    confounder.Execute()




















