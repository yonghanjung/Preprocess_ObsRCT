# Document: preprocessing MIMIC database for ARDS analysis  

## Data collection procedure 

### Step 1. Reduce CHARTEVENTS

As the size of CHARTEVENT is massive, we don't want to call _CHARTEVENTS_ everytime for conducting analysis. Motivated by the fact that _FiO2_ and _PaO2_ are two essential variables in defining ARDS / ALI, _CHARTEVENT_ is reduced by containing only rows with _FiO2_ and _PaO2_.

By searching *reduced_CHARTEVENT* (denote *reduced_CH*), we can search patients more efficiently.

#### Action  

1. Run *ReduceCHARTEVENT.py*. Then *reduced_CH.pkl* file will be stored in *PKL* folder. 




### Step 2. Extract patients with ARDS 

Inclusion criteria is following: 

* **Job 1** _PaO2 / FiO2_ < 300, which is a definition of ARDS. 
  * For some time index $t$ and $s$, we compute $PaO2_t / FiO2_s$ where $|t-s | < h$, where $h$ is a predefined width of observing window.
  * Patients with ARDS satisfying this criterion is identified by running *ARDS_Extract.py*. The output, a list of patients, is stored as *ARDS_PT.pkl* in *PKL* folder. 
* **Job 2** Patients with Mechanical ventilated after the ARDS event. 
  * As a prerequisite, run [ventilation-duration.sql](https://github.com/MIT-LCP/mimic-code/blob/master/concepts/durations/ventilation-durations.sql) to obtain patients' ventilation duration information.  Call the output as *ventilation-duration.csv*
  * Identify patients who have been ventilated. 
* **Job 3 = Job 1 $\cap$ Job 2**   By taking intersect set of ARDS event time and *ventilation-duration.csv*, we collect patients such that 
  * ARDS event happened at some moment $t$; and 
  * ventilated around $t$. 
  * Let's denote such data as *ARDS_PT.csv*



#### Action

1. Run *ARDS_Extract.py* to obtain *PKL/ARDS_PT.pkl*.
2. Run *Subset_ARDS_MV.py* to obtain *PKL/ARDS_MV_SUBSET.pkl*.
3. Run ARDS_HADM_extractor.py to obtain *PKL/ARDS_ID.pkl*




### Step 3. Reduce ARDS patients with sufficient features.

Reduce *CHARTEVENT.csv* data by containing only ARDS patients (w.r.t subject id).

#### Action

1. Run *ReduceARDS_CHART.py* file to generate *CH_ARDS_reduced.pkl*




### Step 3-1. Reduce variables with itemID  

* Extract ARDS onset time
* Extract ARDS death time 
* Extract **confounding variables**
  - weight 
  - gender 
  - Age
  - severity score (APACHE, SOFA, etc). See the [Link](https://github.com/MIT-LCP/mimic-code/tree/master/concepts/severityscores)
* Collect all variables' item id 
  * **vent:** { PEEP, PP, Tidal volume, PIP, Respiratory rate, MInute ventilation } 
  * **O2_vital**: { *SpO2*, *FiO2* , *pH* , *PaO2*  }
  * **vital:** { heartrate, bloodpressure, glucose, gcs score, temperature, creatine, lactate, potassium}
  * **drug**: { Cisatracurium, Atorvastatin, Fluvastatin, Lovastatin, Pravastatin, Rosuvastatin, Simvastatin}
* Reduce CH_ARDS database. 


#### Action 

1. Run *ARDS_reducer_ItemID.py* to generate *ARDS_reduced_CH.pkl* 



### Step 4. Collect variables 

* Extract ARDS confounders/ 
* Extract **ventilator variables** around the event time up to the end of the event (weaning and death)
  * { PEEP, PP, Tidal volume, PIP, Respiratory rate, MInute ventilation } 
* Extract **biomarker variable** around the event time up to the end of the event (weaning and death)



This output is called *Reduced_ARDS_PT.csv*



#### Action

1. To extract ARDS onset time, run *ARDS_onset.py*
2. To extract ARDS death time, run *ARDS_death.py* 
3. To extract ARDS confounder data (age, gender, weight, height, APACHE score, etc.,) run *ARDS_counfounders.py* 





#### Step 3. Imputaiton of data

* If any variables are missing, impute the variable by some statistical technique. 
* This procedure is applied to *ARDS_PT.csv* and *Reduced_ARDS_PT.csv*



## Data analysis procedure 

#### Step 1. Structural learning (Using R or Others) 

* Select several algorithms such as PC, FCI, and score based algorithm 
* Put a constaints by medical analysis 

#### Step 2.  

#### Step 3. 

