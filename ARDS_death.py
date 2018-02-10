import numpy as np
import pandas as pd
import pickle
import dateutil
import datetime

class ARDS_death(object):
    def __init__(self):
        self.ARDS_ONSET = pickle.load(open('PKL/ARDS_ONSETTIME.pkl','rb'))
        self.ARDS_PT = pickle.load(open('PKL/ARDS_MV_SUBSET.pkl','rb'))
        PATIENTS = pd.read_csv('OLD/raw_data/PATIENTS.csv')
        self.PATIENTS = PATIENTS[PATIENTS['SUBJECT_ID'].isin(self.ARDS_PT)]

    def DOD_extracter(self, subject_id):
        DOD = list(self.PATIENTS['DOD'][self.PATIENTS['SUBJECT_ID'] == subject_id])[0]
        if pd.isnull(DOD) == False:
            DOD = pd.to_datetime(DOD)
        return DOD

    def Onset_extracter(self, subject_id):
        return list(self.ARDS_ONSET['ARDS_ONSETTIME'][self.ARDS_ONSET['SUBJECT_ID'] == subject_id])[0]

    def DOD_onsettime_year_match(self, DOD, onsettime):

        while (abs(DOD.year - onsettime.year) >= 100):
            # Matching DOD to onsettime

            # onset.year is 100 years greater than DOD
            # then increase DOD year
            if onsettime > DOD:  ##
                DOD = DOD.replace(year=DOD.year + 100)

            # DOD.year is 100 years greater than onset.year

            else:
                # At first, decrease 100 years
                DOD_cand_1 = DOD.replace(year = DOD.year - 100)

                # If decreased DOD is eariler than onsettime,
                # this means than DOD and onsettime has same year.
                # then choose DOD as onsettime + day2 .
                if DOD_cand_1 < onsettime and DOD.year - onsettime.year == 100:
                    DOD_cand_2 = onsettime.replace(day = onsettime.day + 2)
                    DOD = DOD_cand_2
                else:
                    DOD = DOD_cand_1

        return DOD

    def hour_difference(self,time_obj1, time_obj2):
        return abs(time_obj1.value - time_obj2.value)/(10**9 * 60 * 60)

    def days_difference(self,time_obj1, time_obj2):
        return round(abs(time_obj1.value - time_obj2.value) / (10 ** 9 * 86400),2)

    def Mortality_duration(self, matched_DOD, onsettime):
        return self.days_difference(matched_DOD, onsettime)

    def Execute(self):
        ARDS_survival = dict()
        ARDS_survival['SUBJECT_ID'] = list()
        ARDS_survival['Mortality days duration'] = list()
        ARDS_survival['28-SURVIVAL'] = list()
        ARDS_survival['60-SURVIVAL'] = list()
        ARDS_survival['90-SURVIVAL'] = list()
        ARDS_survival['DOD'] = list()

        for subject_id in self.ARDS_PT:
            ARDS_survival['SUBJECT_ID'].append(subject_id)
            DOD = self.DOD_extracter(subject_id)
            if pd.isnull(DOD) == True:
                ARDS_survival['28-SURVIVAL'].append(1)  # 1 means survival
                ARDS_survival['60-SURVIVAL'].append(1)
                ARDS_survival['90-SURVIVAL'].append(1)
                ARDS_survival['Mortality days duration'].append(99999)
                ARDS_survival['DOD'].append(999999)
            else:
                onsettime = self.Onset_extracter(subject_id)
                matched_DOD = self.DOD_onsettime_year_match(DOD,onsettime)
                durations = self.Mortality_duration(matched_DOD,onsettime)
                ARDS_survival['Mortality days duration'].append(durations)
                ARDS_survival['DOD'].append(matched_DOD)

                if durations < 28:
                    ARDS_survival['28-SURVIVAL'].append(0)
                    ARDS_survival['60-SURVIVAL'].append(0)
                    ARDS_survival['90-SURVIVAL'].append(0)
                elif durations >= 28 and durations < 60:
                    ARDS_survival['28-SURVIVAL'].append(1)
                    ARDS_survival['60-SURVIVAL'].append(0)
                    ARDS_survival['90-SURVIVAL'].append(0)
                elif durations >= 60 and durations < 90:
                    ARDS_survival['28-SURVIVAL'].append(1)
                    ARDS_survival['60-SURVIVAL'].append(1)
                    ARDS_survival['90-SURVIVAL'].append(0)
                elif durations >= 90:
                    ARDS_survival['28-SURVIVAL'].append(1)
                    ARDS_survival['60-SURVIVAL'].append(1)
                    ARDS_survival['90-SURVIVAL'].append(1)
        ARDS_survival = pd.DataFrame(ARDS_survival)
        return ARDS_survival


if __name__ == '__main__':
    death = ARDS_death()
    ARDS_DOD = death.Execute()
    pickle.dump(ARDS_DOD, open('PKL/ARDS_DOD.pkl', 'wb'))











