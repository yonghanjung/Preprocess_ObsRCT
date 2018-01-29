import pickle
import pandas as pd
import methods

ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))
ADMISSIONS = pd.read_csv('raw_data/ADMISSIONS.csv')
CH_ARDS_Berlin = pickle.load(open('CH_ARDS_Berlin.pkl','rb'))

N = len(ARDS_SUBJECT_ID)
idx = 0

ARDS_ID = list()
admit_list = list()
onset_list = list()
Berlin_max_list = list()
Berlin_min_list = list()
Berlin_med_list = list()
for subject_id in ARDS_SUBJECT_ID:
    onset_dict = methods.ARDS_onset(ADMISSIONS,CH_ARDS_Berlin,subject_id)
    admittime = onset_dict['admit']
    onsettime = onset_dict['onset']
    Berlin_min = onset_dict['Berlin_min']
    Berlin_max = onset_dict['Berlin_max']
    Berlin_med = onset_dict['Berlin_med']

    Berlin_max_list.append(Berlin_max)
    Berlin_min_list.append(Berlin_min)
    Berlin_med_list.append(Berlin_med)

    ARDS_ID.append(subject_id)
    admit_list.append(admittime)
    onset_list.append(onsettime)

    print(subject_id,Berlin_min,Berlin_max,Berlin_med, round(idx/N,3), sep=',')
    idx += 1

ARDS_patients_time = pd.DataFrame({'SUBJECT_ID':ARDS_ID, 'ADMITTIME':admit_list, 'ARDS_ONSET':onset_list,'Berlin_min':Berlin_min_list, 'Berlin_med':Berlin_med_list, 'Berlin_max':Berlin_max_list})
pickle.dump(ARDS_patients_time, open('ARDS_onset.pkl','wb'))