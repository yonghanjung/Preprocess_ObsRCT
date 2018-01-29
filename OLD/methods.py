import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy as sp
import dateutil
import datetime
import itertools

def pd_row(df,rowidx):
    '''
    select an individual row from dataframe,
    and encode as list format
    :param df: dataframe in Pandas
    :param rowidx: row index
    :return: list
    '''
    return(list(df.iloc[[rowidx]].values[0]))

def D_item_str_search(D_ITEM, myStr):
    '''
    Extract ITEMID and Label, which label includes myStr.
    :param D_ITEM:
    :param myStr:
    :return: rows that contain myStr in Label
    '''
    return D_ITEM[['ITEMID', 'LABEL']][(D_ITEM['LABEL'].str.contains("PEEP") == True)]


def Admittime(ADMISSIONS, subject_id):
    return list(ADMISSIONS['ADMITTIME'][ADMISSIONS['SUBJECT_ID'] == subject_id])

def ARDS_patients_detector(ADMISSIONS, CH, DIAGNOSIS, subject_id, Berlin_within_measure_hour):
    ItemID_FiO2 = [190, 2981]
    ItemID_PaO2 = [779]
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

def Extract_DOB(PATIENTS,SUBJECT_ID, subject_id):
    ARDS_patients_demo = PATIENTS[['SUBJECT_ID', 'DOB', 'DOD']][PATIENTS['SUBJECT_ID'].isin(SUBJECT_ID)]
    DOB = list(ARDS_patients_demo['DOB'][ARDS_patients_demo['SUBJECT_ID'] == subject_id])[0]
    return dateutil.parser.parse(DOB)

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