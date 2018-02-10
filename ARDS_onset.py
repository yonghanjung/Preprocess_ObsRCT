import numpy as np
import pandas as pd
import pickle
import dateutil
import datetime

from ARDS_Extract import ARDS_Extract_Berlin

class ARDS_onsettime(ARDS_Extract_Berlin):
    def __init__(self):
        super().__init__()
        self.ARDS_PT = pickle.load(open('PKL/ARDS_MV_SUBSET.pkl','rb'))

    def ARDS_onsettime_detector(self, subject_admittimes, subject_CH):
        '''
        :param subject_admittimes: Admittime with matched years to chartevent
        :return: Whether or NOT a patient is in ARDS.
        '''

        subject_admittimes_end = np.array(subject_admittimes) + \
                                 datetime.timedelta(days=self.window_days)
        chart_time = pd.to_datetime(subject_CH['CHARTTIME'])

        for a_start, a_end in zip(subject_admittimes, subject_admittimes_end):
            # This mask is covering all the chartevent of subject
            # happened within the interval (a_start, a_end)
            mask = (chart_time >= a_start) & (chart_time <= a_end)
            subject_CH_a = subject_CH.loc[mask]
            subject_CH_a = subject_CH_a.sort_index(by=['CHARTTIME'])

            subject_Berlin = []

            # If there is no chartevents within the interval,
            # move on to the next interval
            if len(subject_CH_a) == 0:
                continue

            # Otherwise
            else:
                # Pick FiO2 and PaO2
                subject_CH_a_FiO2 = subject_CH_a[subject_CH_a['ITEMID'].isin(self.key_FiO2)]
                subject_CH_a_PaO2 = subject_CH_a[subject_CH_a['ITEMID'].isin(self.key_PaO2)]

                # If patients have no info about FiO2 or PaO2, skip the patients
                if len(subject_CH_a_PaO2) == 0 or len(subject_CH_a_PaO2) == 0:
                    continue

                # Otherwise
                else:
                    # List of FiO2 and PaO2 value
                    subject_FiO2 = list(pd.to_numeric(subject_CH_a_FiO2['VALUE']))
                    subject_PaO2 = list(pd.to_numeric(subject_CH_a_PaO2['VALUE']))

                    # List of FiO2 and PaO2 timing
                    subject_Ftime = list(pd.to_datetime(subject_CH_a_FiO2['CHARTTIME']))
                    subject_Ptime = list(pd.to_datetime(subject_CH_a_PaO2['CHARTTIME']))

                    # For each FiO2 measured time
                    for f in range(len(subject_Ftime)):
                        ftime = subject_Ftime[f]

                        # For each PaO2 measured time
                        for p in range(len(subject_Ptime)):
                            ptime = subject_Ptime[p]

                            # Takes two measurements within window_hour (2hour)
                            if self.hour_difference(ftime, ptime) > self.window_hour_p_f:
                                continue
                            else:

                                # Among PaO2 value and FiO2 value within two hours,
                                fio2 = subject_FiO2[f]
                                pao2 = subject_PaO2[p]

                                # If Berlin score less than 300, then TRUE!
                                berlin = pao2 / (fio2 + 1e-6)
                                if berlin > 300:
                                    continue
                                else:
                                    subject_ARDS_TF = True
                                    # ARDS_onsettime_detecting
                                    # This is ONLY DIFFERENCE!
                                    ards_onsettime = min(ftime, ptime)
                                    return a_start, ards_onsettime, berlin
        return False

    def onset_Execute(self):
        ARDS_onset_dict = dict()
        ARDS_onset_dict['SUBJECT_ID'] = []
        ARDS_onset_dict['ARDS_ONSETTIME'] = []
        ARDS_onset_dict['BERLIN'] = []
        ARDS_onset_dict['ADMITTIME'] = []

        print("ARDS_onset_running")
        idx = 1
        for subject_id in self.ARDS_PT:
            print(round(idx / len(self.ARDS_PT), 3), subject_id)
            idx += 1
            subject_CH = self.reduced_CH[self.reduced_CH['SUBJECT_ID'] == subject_id]

            subject_admittimes = self.Admittime_extract(subject_id)
            subject_admittimes = self.Admittime_correction(subject_admittimes,subject_CH)

            subject_admittimes, ards_onsettime, berlin = self.ARDS_onsettime_detector(subject_admittimes,subject_CH)
            ARDS_onset_dict['SUBJECT_ID'].append(subject_id)
            ARDS_onset_dict['ARDS_ONSETTIME'].append(ards_onsettime)
            ARDS_onset_dict['ADMITTIME'].append(subject_admittimes)
            ARDS_onset_dict['BERLIN'].append(berlin)

        return pd.DataFrame(ARDS_onset_dict)

if __name__ == '__main__':
    onset = ARDS_onsettime()
    ARDS_onset_dict = onset.onset_Execute()
    pickle.dump(ARDS_onset_dict, open('PKL/ARDS_ONSETTIME.pkl', 'wb'))



