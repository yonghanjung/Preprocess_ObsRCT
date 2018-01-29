# Document: preprocessing MIMIC database for ARDS analysis  

## Data collection procedure 

### Step 1. Reduce CHARTEVENTS

As the size of CHARTEVENT is massive, we don't want to call _CHARTEVENTS_ everytime for conducting analysis. Motivated by the fact that _FiO2_ and _PaO2_ are two essential variables in defining ARDS / ALI, _CHARTEVENT_ is reduced by containing only rows with _FiO2_ and _PaO2_.

#### Action  

1. Run *ReduceCHARTEVENT.py*. Then *reduced_CH.pkl* file will be stored in *PKL* folder. 



### Step 2. Extract patients with ARDS 

Inclusion criteria is following: 

* _PaO2 / FiO2_ < 300, which is a definition of ARDS. 
  * For some time index $t$ and $s$, we compute $PaO2_t / FiO2_s$ where $|t-s | < h$, where $h$ is a predefined width of observing window.
* Patients with Mechanical ventilated after the ARDS event. 
  * Refer the [Link](https://github.com/MIT-LCP/mimic-code/blob/master/concepts/durations/ventilation-durations.sql) for rough logic to extract Mechanical ventilated patients in MIMIC.
  * Ask Jenna's help to run the code at [Link](https://github.com/MIT-LCP/mimic-code/blob/master/concepts/durations/ventilation-durations.sql). Let *Ventilated.csv* as such data. 
* By taking intersect set of ARDS event time and *Ventilated.csv*, we collect patients such that 
  * ARDS event happened at some moment $t$; and 
  * ventilated around $t$. 
* Let's denote such data as *ARDS_PT.csv*



#### Action 







#### Step 3. Reduce ARDS patients with sufficient features.  

* Extract **ventilator variables** around the event time up to the end of the event (weaning and death)
  * PEEP 
  * PP 
  * Tidal volume 
  * PIP 
  * Respiratory rate 
  * MInute ventilation 
* Extract **biomarker variable** around the event time 
  * *SpO2*
  * *FiO2* 
  * *pH* 
  * *PaO2*
* Extract **confounding variables**
  * weight 
  * gender 
  * Age
  * severity score (APACHE, SOFA, etc). See the [Link](https://github.com/MIT-LCP/mimic-code/tree/master/concepts/severityscores)



This output is called *Reduced_ARDS_PT.csv*

#### Step 3. Imputaiton of data

* If any variables are missing, impute the variable by some statistical technique. 
* This procedure is applied to *ARDS_PT.csv* and *Reduced_ARDS_PT.csv*



## Data analysis procedure 

#### Step 1. Structural learning (Using R or Others) 

* Select several algorithms such as PC, FCI, and score based algorithm 
* Put a constaints by medical analysis 

#### Step 2.  

#### Step 3. 

