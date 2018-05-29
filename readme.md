# Data collection procedure 

All source codes can be viewed at the [link](https://github.com/HansJung/Preprocess_ObsRCT).



## Variables to be collected 

* **Patients ID**: {SUBJECT_ID, ICUSTAY_ID, HADM_ID}
* **Demographic information**: {Age, Weight, Height, Gender, Death}
* **Ventilator setting**: {PEEP, PP, VT, PIP} 
  * First 2 days average // First 7 days average. 
* **Admission**: {ARDS onset time, ARDS stop time} // to compute ICU days 
* **Treatment**: {cisatracurium, vecuronium, Atorvastatin, Fluvastatin, Lovastatin, Pravastatin, Rosuvastatin, Simvastatin}
* **Vitals**: {heartrate, systolic blood pressure, diastollic blood pressure, respiratory rate, temperature, SpO2, PaO2, glucose_mean, Mean arterial pressure, pH_arterial, Glasgow coma scale}
* **Labs**: {WBC_min, WBC_max, serum (sodium,Potassium (serum), creatine, Hematocrit}
* **Disease**: {Pneumonia, Sepsis}



## Summary of lists of codes and outputs 

#### Requirements 

Before running, users have to contain raw **MIMIC-III** database on **local**. For my example, all MIMIC database are stored in OLD/raw_data folder. 



#### Dependencies 

* Pandas, Numpy, Scipy
* Python 3.6 >= 



#### List of programs and outputs 

| Programs                                                 | Output                                                       | Comment                                                      |
| -------------------------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| ReduceCHARTEVENT.py                                      | reduced_CH.pkl                                               | Reduced CHARTEVENT with FiO2 and PaO2                        |
| ARDS_Extract.py                                          | ARDS_PT.pkl                                                  | List of ARDS patients s.t. Berlin score less than 300        |
| Subset_ARDS_MV.py, ventilation-duration.sql              | ARDS_ICUID.pkl, ARDS_MV_SUBSET.pkl                           | Match patients whose Berlin score less than 300 and MV equippted |
| ReduceARDS_CHART.py                                      | CH_ARDS_reduced.pkl                                          | Reduced CHARTEVENT containing all ARDS patients              |
| ARDS_confounders.py, ARDS_death.py HeightWeightQuery.sql | ARDS_Gender.pkl, ARDS_Age.pkl, ARDS_HeightWeight.pkl, ARDS_DOD.pkl | Collect {Age, Weight, Height, Gender, Death}.                |
| ARDS_variable_collector.py                               | ARDS_data.pkl                                                | Collect {PEEP, PP, VT, PIP} w.r.t. first 2 days and first 7 days. |
| ARDS_Prescription.py                                     | ARDS_drug.pkl                                                | Collect {cisatracurium, vecuronium, Atorvastatin, Fluvastatin, Lovastatin, Pravastatin, Rosuvastatin, Simvastatin} |
| ARDS_firstday.py                                         | ARDS_firstday.pkl                                            | Collect {heartrate, systolic blood pressure, diastollic blood pressure, respiratory rate, temperature, SpO2, PaO2, glucose_mean, Mean arterial pressure, pH_arterial, Glasgow coma scale} |
| ARDS_diagnoses.py                                        | ARDS_diagnoses.pkl                                           | For Pneumonia, Aspiration, Sepsis, Severe Sepsis, and Septic Shock, the indicator variable was assigned. |



## Procedure - Code 

### 1. Reduce CHARTEVENTS

**Purpose**: As the size of CHARTEVENT is massive, we don't want to call _CHARTEVENTS_ everytime for conducting analysis. Motivated by the fact that _FiO2_ and _PaO2_ are two essential variables in defining ARDS / ALI, _CHARTEVENT_ is reduced by containing only rows with _FiO2_ and _PaO2_.

**Program**: *ReduceCHARTEVENT.py*

**Tasks**: Extract FiO2 and PaO2 from raw CHARTEVENT dataset. 

**Output**: *reduced_CH.pkl*, which contains only FiO2 and PaO2 for all patients in MIMIC III. 



### 2. Extract patients with ARDS

**Purpose**: Identify all patients whose Berlin score < 300 with mechanical ventilated. 

**Tasks** 

1. Extract patients whose Berlin score is less than 300. 
2. Among patients satisfying the condition 1, extract those who are mechanically ventilated. 



#### 2.1. Extract patients whose Berlin score < 300.  

**Procedure** For all patients who are NOT heart failure, identify those whose Berlin score is less than 300. For some time index $t$ and $s$, we compute $PaO2_t / FiO2_s$ where $|t-s | < h$, where $h$ is a predefined width of observing window.

**Program**: *ARDS_Extract.py*

**Output**:  *ARDS_PT.pkl*, a list of patients. 



#### 2.2. Extract patients equipped with mechanical ventilation 

**Purpose**: Obtain mechanical ventilated patients. 

**Program**: *ventilation-duration.sql* **and** *Subset_ARDS_MV.py*

**Procedure**: We are given patients (<300)' SUBJECT_ID and patients (with MV) ICUSTAY_ID. We match patients by identifying whose Berlin score less than 300 and equipped with MV. 

**Output**: 

* *ARDS_ICUID.pkl*, a list of patients' ICUSTAY_ID
* *ARDS_MV_SUBSET.pkl*, a list of patients' SUBJECT_ID  



### 3. Reduce CHARTEVENT with ARDS patients 

**Purpose**: As *CHARTEVENT* and *Reduced_CH* still contain information about non-ARDS patients, we will reduce those dataset to contain only ARDS patients. 

**Program**: *ReduceARDS_CHART.py*

**Procedure**: For all CHARTEVENT, catch those who are in ARDS_PT. 

**Output**: *CH_ARDS_reduced.pkl*



### 4. Collect variables  

####4.1. Demographic information 

**Purpose**: Collect {Age, Weight, Height, Gender, Death}. 

**Program**: *ARDS_confounders.py* **AND** *ARDS_death.py*

**Output**

From *ARDS_confounders.py*

* *ARDS_Gender.pkl*
* *ARDS_Age.pkl*
* *ARDS_HeightWeight.pkl*
* *ARDS_APACHE.pkl*

From *ARDS_death.py*

* *ARDS_DOD.pkl*



#### 4.2. Ventilator setting 

**Purpose**: Collect {PEEP, PP, VT, PIP} w.r.t. first 2 days and first 7 days. 

**Program**: *ARDS_variable_collector.py*

**Output**: *ARDS_data.pkl*



#### 4.3. Admission  

**Purpose**: Collect {ARDS onset time, ARDS stop time} // to compute ICU days

**Program**: *ARDS_death.py*

**Output**: ARDS onset and death, which gives staying duration. 



#### 4.4. Treatment 

**Purpose**: Collect NMBA and Statin drug treatment.

**Treatment**: {cisatracurium, vecuronium, Atorvastatin, Fluvastatin, Lovastatin, Pravastatin, Rosuvastatin, Simvastatin}

**Program**: *ARDS_Prescription.py* 

**Procedure**: Collect Cisatracurium, Atorvastatin, and Simvastatin. 

**Output**: *ARDS_drug.pkl*



#### 4.5 Vitals & Labs (1st day of admission) 

**Purpose**: Collect {heartrate, systolic blood pressure, diastollic blood pressure, respiratory rate, temperature, SpO2, PaO2, glucose_mean, Mean arterial pressure, pH_arterial, Glasgow coma scale}

**Procedure**: Each variable is collected at the first day of the admission. Those data are collected from SQL dataset. 

**Program**: *ARDS_firstday.py*

**Output**: *ARDS_firstday.pkl*



#### 4.6. Disease 

**Purpose**: Collect {Pneumonia, Sepsis}

**Procedure**: For Pneumonia, Aspiration, Sepsis, Severe Sepsis, and Septic Shock, the indicator variable was assigned. 

**ICD9 codes**

* [Pnuemonia](http://www.icd9data.com/2012/Volume1/460-519/480-488/default.htm): 480-486, 507.0 (Aspiraiton Pnuemonia)
* Sepsis: 995.91, 995.92 (severe), 785.52 (septic shock)

**Program**: *ARDS_diagnoses.py*

**Outputs**: *ARDS_diagnoses.pkl*





