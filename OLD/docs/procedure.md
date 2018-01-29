**Last update**: 170816 



**Procedure** 

1. Reducing CHARTEVENT size by calling only necessary 
   1. Reduction_CHARTEVENT_Berlin.py - Reducing CHARTEVENT
   2. Reduction_CPTEVENTS_Resp.py - Reducing CHARTEVENT and extract subject candidates 
   3. ARDS_patients_extract.py - Extract ARDS_SUBJECT_ID
   4. CH_ARDS_reduced.py - Using ARDS_SUBJECT_ID, reduce CHARTEVENT 
   5. ARDS_PRESCRIPTION
2. Collect necessary demographic data 
   1. ARDS_onset.py - ARDS onset timing and corresponding Berlin score
   2. Death_detector.py - Mortality 
   3. sex_ARDS.py - Sex
   4. Age.py - Age 
   5. Weight.py - Weight 
   6. Height.py - Height 
3. Collect necessary chartvalue data  ​




---

## All data 

```python
import pickle 
import pandas as pd 

D_ITEM = pd.read_csv('raw_data/D_ITEMS.csv')
CH_ARDS_reduced = pickle.load(open('CH_ARDS_reduced.pkl','rb'))
ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))
ARDS_onset = pickle.load(open('ARDS_onset.pkl','rb'))
ARDS_PRESCRIPTION = pickle.load(open('ARDS_PRESCRIPTION.pkl','rb'))
```







---

## Preprocessing - CHARTEVENT reduction 

As CHARTEVENT table is over 40GB, we have to extract necessary information, instead of fully using CHARTEVENT. 



**Reduction_CHARTEVENT_Berlin.py** 

```python
import pandas as pd
import pickle

CHARTEVENT = pd.read_csv('raw_data/CHARTEVENTS.csv',chunksize=10**6)
ItemID_FiO2 = [190, 2981]
ItemID_PaO2 = [779]
ITEMID_Berlin = ItemID_PaO2 + ItemID_FiO2

REDUCTION_CHARTEVENT = []
idx = 0
for CH in CHARTEVENT:
    idx += 1
    mask = CH['ITEMID'].isin(ITEMID_Berlin)
    if mask.any():
        REDUCTION_CHARTEVENT.append(CH.loc[mask])
        print(idx, 'include')
    else:
        print(idx, 'skip')
        continue

CH_Berlin = pd.concat(REDUCTION_CHARTEVENT)
SUBJECT_cand = list(CH_Berlin.SUBJECT_ID.unique())
pickle.dump(REDUCTION_CHARTEVENT,open('CH_Berlin.pkl','wb'))
```



## ARDS subject candidate detection

* Subjects in REDUCTION_CHARTEVENT 
* Subjects whose billing code is Resp. 


**Reduction_CPTEVENTS_Resp.py**

```python
import pickle
import pandas as pd

CH_Berlin = pickle.load(open('CH_Berlin.pkl','rb'))
SUBJECT_cand = list(CH_Berlin.SUBJECT_ID.unique())

CPTEVENTS = pd.read_csv('raw_data/CPTEVENTS.csv')
CPTEVENTS_reduced = CPTEVENTS[CPTEVENTS['SUBJECT_ID'].isin(SUBJECT_cand)]
CPTEVENTS_reduced = CPTEVENTS_reduced[CPTEVENTS_reduced['COSTCENTER'] == 'Resp']
SUBJECT_cand = list(CPTEVENTS_reduced.SUBJECT_ID.unique())

CH_Berlin = CH_Berlin[CH_Berlin['SUBJECT_ID'].isin(SUBJECT_cand)]
CH_Berlin_reduced = CH_Berlin[['SUBJECT_ID','ITEMID','CHARTTIME','VALUE']]

pickle.dump(SUBJECT_cand,open('SUBJECT_cand.pkl','wb'))
pickle.dump(CH_Berlin, open('CH_Berlin_reduced.pkl','wb'))
```






## ARDS patients detection 

*ARDS onset* is defined as 

* PaO2 / FiO2 <= 200 
* Measurement time interval between PaO2 and Fio2 is within 2 hours. 

*ARDS patients* are defined as those who have *ARDS onset* within 2 days from admission date. 



**ARDS_patients_extract.py**

```python
def ARDS_patients_detector(ADMISSIONS, CH, DIAGNOSIS, subject_id):
	# CH = CH_Berlin_reduced 
    Berlin_within_measure_hour = 4
    ICU_within_days = 2

    # Exclude patients with ICD9 code 4280, because this patients
    ICD9_list = list(DIAGNOSIS['ICD9_CODE'][DIAGNOSIS['SUBJECT_ID']==subject_id])
    if '4280' in ICD9_list:
        return False

    # Extract admission times
    admittimes = list(ADMISSIONS['ADMITTIME'][ADMISSIONS['SUBJECT_ID'] == subject_id])

    # subject's PaO2 and FiO2
    subject_PaO2_FiO2 = CH[CH['SUBJECT_ID'] == subject_id]
    chart_time = pd.to_datetime(subject_PaO2_FiO2['CHARTTIME'])

    # For each admission time.
    ARDS_TF = False
    for admittime in admittimes:
        admittime = dateutil.parser.parse(admittime)
        # If there is no charttime, then return false
        try:
            min_charttime = min(chart_time)
        except:
            return False
        # If admission time and charttime is encoded differently,
        # then match year to 100.
        if abs(min_charttime.year - admittime.year) >= 100:  # replace needed
            if admittime > min(chart_time):
                admittime = admittime.replace(year=admittime.year - 100)
            else:
                admittime = admittime.replace(year=admittime.year + 100)

        # Consider only 2 days within admission
        admittime_end = admittime + datetime.timedelta(days=ICU_within_days)
        mask = (chart_time >= admittime) & (chart_time <= admittime_end)
        subject_PaO2_FiO2_admit = subject_PaO2_FiO2.loc[mask]
        if len(subject_PaO2_FiO2_admit) == 0:
            continue
        df_FiO2 = subject_PaO2_FiO2_admit[subject_PaO2_FiO2_admit['ITEMID'].isin(ItemID_FiO2)]
        df_PaO2 = subject_PaO2_FiO2_admit[subject_PaO2_FiO2_admit['ITEMID'].isin(ItemID_PaO2)]
        Fo2_value = list(map(float, list(df_FiO2['VALUE'])))
        Po2_value = list(map(float, list(df_PaO2['VALUE'])))
        F_time = list(pd.to_datetime(df_FiO2['CHARTTIME']))
        P_time = list(pd.to_datetime(df_PaO2['CHARTTIME']))
        if len(Fo2_value) > 0 and len(Po2_value) > 0:
            # For constraining Berlin score computed withint 2 hours gap.
            Po2_Fo2_combi_idx = list()
            for i in range(len(P_time)):
                for j in range(len(F_time)):
                    if abs(P_time[i].value - F_time[j].value)/(10**9) <= 60*60*Berlin_within_measure_hour:
                        Po2_Fo2_combi_idx.append((i, j))
                    else:
                        continue
            if len(Po2_Fo2_combi_idx) > 0:
                Berlin_possible = [Po2_value[x[0]]/Fo2_value[x[1]] for x in Po2_Fo2_combi_idx]
            else:
                continue

            for berlin in Berlin_possible:
                if berlin < 300:
                    ARDS_TF = True
                    break
            if ARDS_TF == True:
                break
        else:
            continue
    return ARDS_TF
  
''' Main '''
import pandas as pd
import pickle
import methods

ADMISSIONS = pd.read_csv('raw_data/ADMISSIONS.csv')
DIAGNOSIS = pd.read_csv('raw_data/DIAGNOSES_ICD.csv')
CH_Berlin_reduced = pickle.load(open('CH_Berlin_reduced.pkl','rb'))
SUBJECT_cand = pickle.load(open('SUBJECT_cand.pkl','rb'))
SUBJECT_cand.sort()


ARDS_patients = list()
N = len(SUBJECT_cand)
idx = 0
for subject_id in SUBJECT_cand:
    result = methods.ARDS_patients_detector(ADMISSIONS, CH_Berlin_reduced, DIAGNOSIS, subject_id)
    if result:
        ARDS_patients.append(subject_id)
        print(subject_id, round(idx/N,4),result)
    else:
        print(subject_id, round(idx/N,4),result)
    idx += 1
    break

pickle.dump(ARDS_patients, open('ARDS_SUBJECT_ID.pkl','wb'))
```



## CHARTEVENT reduction for ARDS: CH_ARDS construction 

Now we have ARDS patients out of whole population. We can extract CHARTEVENTS with ARDS patients list as follow: 



**CH_ARDS.py**

```python
import pandas as pd
import pickle

ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))
CHARTEVENT = pd.read_csv('raw_data/CHARTEVENTS.csv',chunksize=10 ** 6)

ItemID_FiO2 = [190, 2981]
ItemID_PaO2 = [779]
ITEMID_Berlin = ItemID_PaO2 + ItemID_FiO2

CH_ARDS = []
idx = 0
for CH in CHARTEVENT:
    idx += 1
    print(idx)
    mask = CH['SUBJECT_ID'].isin(ARDS_SUBJECT_ID)
    if mask.any():
        CH_ARDS.append(CH.loc[mask])
    else:
        continue

CH_ARDS = pd.concat(CH_ARDS)
CH_ARDS_reduced = CH_ARDS[['SUBJECT_ID','ITEMID','CHARTTIME','VALUE']]
CH_ARDS_Berlin = CH_ARDS_reduced[CH_ARDS_reduced['ITEMID'].isin(ITEMID_Berlin)]

pickle.dump(CH_ARDS,open('CH_ARDS.pkl','wb'))
pickle.dump(CH_ARDS_reduced,open('CH_ARDS_reduced.pkl','wb'))
pickle.dump(CH_ARDS_Berlin,open('CH_ARDS_Berlin.pkl','wb'))
```



---



## ARDS onset detection 

*ARDS onset* is defined as 

- PaO2 / FiO2 <= 200 
- Measurement time interval between PaO2 and Fio2 is within 2 hours. 

*ARDS patients* are defined as those who have *ARDS onset* within 2 days from admission date. 



**ARDS_onset.py**

```python
import pandas as pd 
import pickle 

def ARDS_onset(ADMISSIONS, CH_ARDS_Berlin, subject_id):
    '''
    :param ADMISSIONS:
    :param CH:
    :param subject_id:
    :return: ARDS onset and Admission time
    '''
    ItemID_FiO2 = [190, 2981]
    ItemID_PaO2 = [779]
    ICU_within_days = 2
    Berlin_within_measure_hour = 2

    admittimes = list(ADMISSIONS['ADMITTIME'][ADMISSIONS['SUBJECT_ID'] == subject_id])
    for admittime in admittimes:
        admittime = dateutil.parser.parse(admittime)
        subject_PaO2_FiO2 = CH_ARDS_Berlin[CH_ARDS_Berlin['SUBJECT_ID'] == subject_id]
        chart_time = pd.to_datetime(subject_PaO2_FiO2['CHARTTIME'])
        min_charttime = min(chart_time)
        if abs(min_charttime.year - admittime.year) >= 100:  # replace needed
            if admittime > min(chart_time):
                admittime = admittime.replace(year=admittime.year - 100)
            else:
                admittime = admittime.replace(year=admittime.year + 100)
        # Consider only 2 days within admission
        admittime_end = admittime + datetime.timedelta(days=ICU_within_days)
        mask = (chart_time >= admittime) & (chart_time <= admittime_end)
        subject_PaO2_FiO2_admit = subject_PaO2_FiO2.loc[mask]
        df_FiO2 = subject_PaO2_FiO2_admit[subject_PaO2_FiO2_admit['ITEMID'].isin(ItemID_FiO2)]
        df_PaO2 = subject_PaO2_FiO2_admit[subject_PaO2_FiO2_admit['ITEMID'].isin(ItemID_PaO2)]
        Fo2_value = list(map(float, list(df_FiO2['VALUE'])))
        Po2_value = list(map(float, list(df_PaO2['VALUE'])))
        F_time = list(pd.to_datetime(df_FiO2['CHARTTIME']))
        P_time = list(pd.to_datetime(df_PaO2['CHARTTIME']))
        Po2_Fo2_combi_idx = list()
        for i in range(len(P_time)):
            for j in range(len(F_time)):
                if abs(P_time[i].value - F_time[j].value) / (10 ** 9) <= 60 * 60 * Berlin_within_measure_hour:
                    Po2_Fo2_combi_idx.append((i, j))
                else:
                    continue
        Berlin_possible = [Po2_value[x[0]] / Fo2_value[x[1]] for x in Po2_Fo2_combi_idx]
        ARDS_TF = False
        for idx in range(len(Berlin_possible)):
            Berlin = Berlin_possible[idx]
            PaO2_time_idx = Po2_Fo2_combi_idx[idx][0]
            FiO2_time_idx = Po2_Fo2_combi_idx[idx][1]
            if Berlin < 300:
                ARDS_TF = True
                onset = min(P_time[PaO2_time_idx], F_time[FiO2_time_idx])
                break
        if ARDS_TF:
            return {'admit': admittime, 'onset': onset,'Berlin_min':min(Berlin_possible), 'Berlin_max':max(Berlin_possible),'Berlin_med':np.median(Berlin_possible)}

''' Main '''
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
```



In spreadsheet form. 

```python
for subject_id, admittime, onset, berlin_max, berlin_med, berlin_min in zip(ARDS_onset['SUBJECT_ID'],ARDS_onset['ADMITTIME'],ARDS_onset['ARDS_ONSET'],ARDS_onset['Berlin_max'],ARDS_onset['Berlin_med'],ARDS_onset['Berlin_min']):
    timediff = onset.value - admittime.value
    timediff = timediff / (10**9)
    timediff /= 86400
    timediff = round(timediff,1)
    print(subject_id, timediff)

```





## ARDS patients mortality

**Death_detector.py**

```python
import numpy as np
import pandas as pd
import pickle
import datetime
import dateutil

ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))
ARDS_time = pickle.load(open('ARDS_onset.pkl','rb'))
ADMISSIONS = pd.read_csv('raw_data/ADMISSIONS.csv')
PATIENTS = pd.read_csv('raw_data/PATIENTS.csv')
ARDS_PATIENTS = PATIENTS[PATIENTS['SUBJECT_ID'].isin(ARDS_SUBJECT_ID)]

idx = 0
ARDS_survival = dict()
ARDS_survival['SUBJECT_ID'] = list()
ARDS_survival['Mortality days duration'] = list()
ARDS_survival['28-SURVIVAL'] = list()
ARDS_survival['60-SURVIVAL'] = list()
ARDS_survival['90-SURVIVAL'] = list()
ARDS_survival['DOD'] = list()
for subject_id in ARDS_SUBJECT_ID:
    idx += 1
    ARDS_survival['SUBJECT_ID'].append(subject_id)
    DOD = list(ARDS_PATIENTS['DOD'][ARDS_PATIENTS['SUBJECT_ID'] == subject_id ])[0]
    if pd.isnull(DOD):
        ARDS_survival['28-SURVIVAL'].append(1) # 1 means survival
        ARDS_survival['60-SURVIVAL'].append(1)
        ARDS_survival['90-SURVIVAL'].append(1)
        ARDS_survival['Mortality days duration'].append(99999)
        ARDS_survival['DOD'].append(999999)

    else:
        DOD = dateutil.parser.parse(DOD)
        ARDS_survival['DOD'].append(DOD)
        onset_time = list(ARDS_time['ARDS_ONSET'][ARDS_time['SUBJECT_ID'] == subject_id])[0]
        onset_time = onset_time.replace(hour=0,minute=0,second=0)
        if onset_time> DOD: # years are not matching
            DOD = DOD.replace(DOD.year+100)
            diff = DOD - onset_time
            if onset_time > DOD:
                if abs(diff.value / (10 ** 9))/86400 <= 10:
                    ARDS_survival['Mortality days duration'].append(abs(diff.value / (10 ** 9))/86400)
                    ARDS_survival['28-SURVIVAL'].append(0)
                    ARDS_survival['60-SURVIVAL'].append(0)
                    ARDS_survival['90-SURVIVAL'].append(0)
                    continue
                else:
                    DOD = DOD.replace(DOD.year + 100)
        diff = DOD - onset_time
        diff_seconds = diff.value / (10**9)
        diff_days = round(diff_seconds / 86400,2)
        ARDS_survival['Mortality days duration'].append(diff_days)
        if diff_days < 28:
            ARDS_survival['28-SURVIVAL'].append(0)
            ARDS_survival['60-SURVIVAL'].append(0)
            ARDS_survival['90-SURVIVAL'].append(0)
        elif diff_days >= 28 and diff_days < 60:
            ARDS_survival['28-SURVIVAL'].append(1)
            ARDS_survival['60-SURVIVAL'].append(0)
            ARDS_survival['90-SURVIVAL'].append(0)
        elif diff_days >= 60 and diff_days < 90:
            ARDS_survival['28-SURVIVAL'].append(1)
            ARDS_survival['60-SURVIVAL'].append(1)
            ARDS_survival['90-SURVIVAL'].append(0)
        elif diff_days >= 90:
            ARDS_survival['28-SURVIVAL'].append(1)
            ARDS_survival['60-SURVIVAL'].append(1)
            ARDS_survival['90-SURVIVAL'].append(1)


ARDS_survival = pd.DataFrame(ARDS_survival)
pickle.dump(ARDS_survival, open('ARDS_survival.pkl','wb'))
```



```python
for subject_id, day28, day60, day90, dod, duration in zip(ARDS_survival['SUBJECT_ID'],ARDS_survival['28-SURVIVAL'],ARDS_survival['60-SURVIVAL'],ARDS_survival['90-SURVIVAL'],ARDS_survival['DOD'],ARDS_survival['Mortality days duration']):
    print(subject_id, day28, day60, day90, dod, duration, sep='|')

```





## Demographic variable detection 

## Sex

**sex_ARDS.py**

```python
import pickle
import pandas as pd

PATIENTS = pd.read_csv('raw_data/PATIENTS.csv')
ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))

ARDS_PATIENTS = PATIENTS[PATIENTS['SUBJECT_ID'].isin(ARDS_SUBJECT_ID)]
for subject_id, gender in zip(ARDS_PATIENTS['SUBJECT_ID'], ARDS_PATIENTS['GENDER']):
    print(subject_id, gender, sep=',')
```



### Age

Age is defined as a time difference between DOB and admission date. 

**Age.py**

```python
import pandas as pd
import pickle
import methods

def Age_compute(PATIENTS, ARDS_time, subject_id):
    DOB = list(PATIENTS['DOB'][PATIENTS['SUBJECT_ID'] == subject_id])[0]
    DOB = dateutil.parser.parse(DOB)
    if DOB.year < 1900:
        return 89
    admit_time = list(ARDS_time['ADMITTIME'][ARDS_time['SUBJECT_ID'] == subject_id])[0]
    if DOB > admit_time:
        admit_time = admit_time.replace(year = admit_time.year+100)
    year_diff = admit_time.year - DOB.year
    if year_diff > 100:
        year_diff -= 100
    age = year_diff
    return age

ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))
ADMISSIONS = pd.read_csv('raw_data/ADMISSIONS.csv')
PATIENTS = pd.read_csv('raw_data/PATIENTS.csv')
ARDS_onset = pickle.load(open('ARDS_onset.pkl','rb'))

ARDS_age = dict()
ARDS_age['SUBJECT_ID'] = list()
ARDS_age['AGE'] = list()

for subject_id in ARDS_SUBJECT_ID:
    age = methods.Age_compute(PATIENTS,ARDS_onset, subject_id)
    ARDS_age['SUBJECT_ID'].append(subject_id)
    ARDS_age['AGE'].append(age)
ARDS_age = pd.DataFrame(ARDS_age)

pickle.dump(ARDS_age,open('ARDS_age.pkl','wb'))
```

```python
ARDS_age = pickle.load(open('ARDS_age.pkl','rb'))
for subject_id, age in zip(ARDS_age['SUBJECT_ID'],ARDS_age['AGE']):
    print(subject_id,age,sep=',')
```



### Weight 

**Weight.py**

```python
import pickle
import pandas as pd
import numpy as np
import methods

ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))
CH_ARDS = pickle.load(open('CH_ARDS.pkl','rb'))

Weight_ID = [226512, 224639, 763] # 763: Daily weight
CH_ARDS_weight = CH_ARDS[CH_ARDS['ITEMID'].isin(Weight_ID)]

for subject_id in ARDS_SUBJECT_ID:
    weight_list = list(CH_ARDS_weight['VALUE'][CH_ARDS_weight['SUBJECT_ID']==subject_id])
    weight_list = list(map(float,weight_list))
    weight = np.median(weight_list)
    if pd.isnull(weight) and len(weight_list) > 0:
        weight = max(weight_list)
        if pd.isnull(weight):
            weight = weight_list[0]
    print(subject_id, weight, sep='|')
```



### Height 

**Height.py**

```python
import numpy as np
import pandas as pd
import pickle

CH_ARDS_reduced = pickle.load(open('CH_ARDS_reduced.pkl','rb'))
ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))

HEIGHT_ID = [920, 1394, 4187, 3486, 3485, 4188]
CH_ARDS_height = CH_ARDS_reduced[CH_ARDS_reduced['ITEMID'].isin(HEIGHT_ID)]

for subject_id in ARDS_SUBJECT_ID:
    subject_height = CH_ARDS_height[['ITEMID', 'VALUE']][CH_ARDS_height['SUBJECT_ID'] == subject_id]
    height_find = False
    for height_id in HEIGHT_ID:
        height_id_list = list(subject_height['VALUE'][subject_height['ITEMID'] == height_id])
        if len(height_id_list) > 0:
            height_id_list = list(map(float, height_id_list))
            height = max(height_id_list)
            if pd.isnull(height):
                continue
            if height_id in [920,1394,3486,4187]:
                height *= 2.54
            print(subject_id, height, sep='|')
            height_find = True
            break
        else:
            continue
    if height_find == False:
        print(subject_id, '', sep='|')
```



## Prescription 

### Cisatracurium (NMBA) 

```python
import pandas as pd 
import pickle

PRESCRIPTION = pd.read_csv('raw_data/PRESCRIPTIONS.csv')
ARDS_PRESCRIPTION = PRESCRIPTION[PRESCRIPTION['SUBJECT_ID'].isin(ARDS_SUBJECT_ID)]

pickle.dump(ARDS_PRESCRIPTION,open('ARDS_PRESCRIPTION.pkl','wb'))
```

### Extract patients with NMBA 



```python
import pandas as pd 
import pickle 
import datetime 

ARDS_PRESCRIPTION = pickle.load(open('ARDS_PRESCRIPTION.pkl','rb'))
ARDS_onset = pickle.load(open('ARDS_onset.pkl','rb'))
Cisa_Patients = ARDS_PRESCRIPTION['SUBJECT_ID'][ARDS_PRESCRIPTION['DRUG'].str.contains('Cisa') == True].unique()

mask = ARDS_PRESCRIPTION['SUBJECT_ID'].isin(Cisa_Patients) & ARDS_PRESCRIPTION['DRUG'].str.contains('Cisa')

ARDS_NMBA = ARDS_PRESCRIPTION[['SUBJECT_ID','DRUG','STARTDATE','ENDDATE','DOSE_VAL_RX','DOSE_UNIT_RX']].loc[mask]

ARDS_NMBA_dose = dict()
ARDS_NMBA_dose['SUBJECT_ID'] = []
ARDS_NMBA_dose['NMBA'] = []

for subject_id in Cisa_Patients:
  ARDS_NMBA_subject = ARDS_NMBA[ARDS_NMBA['SUBJECT_ID'] == subject_id]
  ARDS_admittime = list(ARDS_onset['ADMITTIME'][ARDS_onset['SUBJECT_ID'] == subject_id])[0]
  ARDS_admittime = ARDS_admittime.replace(hour=0,minute=0,second=0)
  ARDS_onset_subject = list(ARDS_onset['ARDS_ONSET'][ARDS_onset['SUBJECT_ID'] == subject_id])[0]
  ARDS_onset_subject = ARDS_onset_subject.replace(hour=0,minute=0,second=0)
  ARDS_onset_subject_end = ARDS_onset_subject + datetime.timedelta(days=2)
  mask_subject = ((pd.to_datetime(ARDS_NMBA_subject['STARTDATE']) >= ARDS_admittime) | (pd.to_datetime(ARDS_NMBA_subject['STARTDATE']) >= ARDS_onset_subject)) & (pd.to_datetime(ARDS_NMBA_subject['STARTDATE']) <= ARDS_onset_subject_end) 
  if mask_subject.any() == False:
  	print(subject_id, 0)  
    continue
  ARDS_NMBA_subject = ARDS_NMBA_subject.loc[mask_subject] # Filtering done 
  
  ARDS_NMBA_subject_start = min(pd.to_datetime(ARDS_NMBA_subject['STARTDATE']))
  ARDS_NMBA_subject_end = max(pd.to_datetime(ARDS_NMBA_subject['ENDDATE']))
  timediff = ARDS_NMBA_subject_end.value - ARDS_NMBA_subject_start.value
  timediff /= 10**9
  timediff /= -86400
  ARDS_NMBA_subject_dose = list(ARDS_NMBA_subject['DOSE_VAL_RX'][pd.to_datetime(ARDS_NMBA_subject['STARTDATE']) == ARDS_NMBA_subject_start])
  list_mask = [str(x).isdigit() for x in ARDS_NMBA_subject_dose]
  ARDS_NMBA_subject_dose = [ item for item, flag in zip( ARDS_NMBA_subject_dose, mask_list ) if flag == True ]
  ARDS_NMBA_subject_dose.sort()
  if (divmod(len(ARDS_NMBA_subject_dose),2)[1] == 0 and len(ARDS_NMBA_subject_dose) > 1):
    ARDS_NMBA_subject_dose = ARDS_NMBA_subject_dose[int(len(ARDS_NMBA_subject_dose)/2+1)-1]
  elif (divmod(len(ARDS_NMBA_subject_dose),2)[1] == 1 and len(ARDS_NMBA_subject_dose) > 1):
    ARDS_NMBA_subject_dose = np.median(ARDS_NMBA_subject_dose)
  elif len(ARDS_NMBA_subject_dose) == 1:
    ARDS_NMBA_subject_dose = ARDS_NMBA_subject_dose[0]
  else:
    continue
  print(subject_id, ARDS_NMBA_subject_dose, timediff)
  ARDS_Cisa_Patients.append(subject_id)
```





## Chart-value extractor 

### VT, PEEP, FiO2, PP, MAP, HP, RR  

We are focusing on initial setting of VT. 

```python
import pickle
import pandas as pd
import dateutil
import datetime

CH_ARDS_reduced = pickle.load(open('CH_ARDS_reduced.pkl','rb'))
ARDS_onset = pickle.load(open('ARDS_onset.pkl','rb'))


ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))


VT_ID = [681, 682, 683, 2043, 2044, 224684, 224685, 2400, 2408, 2534]
PEEP_ID = [505, 506]
ItemID_FiO2 = [190, 2981]
ItemID_PP = [543, 224696]
ItemID_MAP = [444]
ItemID_DP = [2129, 7638]
ItemID_HP = [218]

VT_ID = [681, 682, 683, 2043, 2044, 224684, 224685, 2400, 2408, 2534]
for subject_id in ARDS_SUBJECT_ID:
    CH_ARDS_subject = CH_ARDS_reduced[CH_ARDS_reduced['SUBJECT_ID'] == subject_id]
    CH_ARDS_subject = CH_ARDS_subject[CH_ARDS_subject['ITEMID'].isin(VT_ID )]

    ARDS_onset_subject = list(ARDS_onset['ARDS_ONSET'][ARDS_onset['SUBJECT_ID'] == subject_id])[0]
    ARDS_onset_subject_end = ARDS_onset_subject + datetime.timedelta(days=7)

    mask_subject = (pd.to_datetime(CH_ARDS_subject['CHARTTIME']) >= ARDS_onset_subject) & \
                      (pd.to_datetime(CH_ARDS_subject['CHARTTIME']) <= ARDS_onset_subject_end ) & \
                      (pd.isnull(CH_ARDS_subject['VALUE']) == False)

    if mask_subject.any():
        CH_ARDS_subject = CH_ARDS_subject.loc[mask_subject]
        Val = list(CH_ARDS_subject['VALUE'][CH_ARDS_subject['CHARTTIME'] == min(CH_ARDS_subject['CHARTTIME'])])[0]
        Val = float(Val)
        print(subject_id,Val,sep=",")
    else:
        print(subject_id,'-',sep=',')
```



### ARDS - Select Berlin scores 

```python
# Sev control
for subject_id in SUBJECT_ID:
    df_berlin_subject = df[['Berlin_min', 'Berlin_med', 'Berlin_max']][df['SUBJECT_ID'] == subject_id]
    if pd.isnull(df_berlin_subject['Berlin_med']).any() == False:
        Berlin = list(df_berlin_subject['Berlin_med'])[0]
    else:
        if pd.isnull(df_berlin_subject['Berlin_min']).any() == False:
            Berlin = list(df_berlin_subject['Berlin_min'])[0]
        else:
            Berlin = list(df_berlin_subject['Berlin_max'])[0]
    print(subject_id,Berlin,sep=',')
```

