# Document: preprocessing MIMIC database for ARDS analysis  

## Module (in order)
#### Step 1. Reduce CHARTEVENTS

As the size of CHARTEVENT is massive, we don't want to call _CHARTEVENTS_ everytime for conducting analysis. Motivated by the fact that _FiO2_ and _PaO2_ are two essential variables in defining ARDS / ALI, _CHARTEVENT_ is reduced by containing only rows with _FiO2_ and _PaO2_.

#### Step 2. 
   

## Procedure 

