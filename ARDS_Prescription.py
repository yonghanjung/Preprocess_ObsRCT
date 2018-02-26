import numpy as np
import scipy as sp
import pandas as pd
import pickle
import datetime

class ARDS_Prescription():
    def __init__(self):
        PRESCRIPTION = pd.read_csv('OLD/raw_data/PRESCRIPTIONS.csv')
        self.ARDS_ID = pickle.load(open('PKL/ARDS_ID.pkl','rb'))
        self.ARDS_PRESCRIPTION = PRESCRIPTION[(PRESCRIPTION['SUBJECT_ID'].isin(self.ARDS_ID['SUBJECT_ID']))
            & (PRESCRIPTION['HADM_ID'].isin(self.ARDS_ID['HADM_ID'])) &
                     (PRESCRIPTION['ICUSTAY_ID'].isin(self.ARDS_ID['ICUSTAY_ID']))
        ]

        self.drug_name = ['Cisatracurium','Atorvastatin','Simvastatin']

    def df_float_convertible(self,df):
        try:
            pd.to_numeric(df)
            return True
        except ValueError:
            return False

    def float_convertible(self,val):
        try:
            float(val)
            return True
        except ValueError:
            return False

    def float_convertible_extractor(self, df):
        list_df = list(df)
        output = []
        for idx in range(len(list_df)):
            x = list_df[idx]
            if self.float_convertible(x) == True:
                output.append(float(x))
            else:
                continue
        return output

    def drug_extractor(self):
        drug_dict = dict()
        drug_dict['SUBJECT_ID'] = list()
        drug_dict['HADM_ID'] = list()
        drug_dict['ICUSTAY_ID'] = list()
        drug_dict['Cisatracurium'] = list()
        drug_dict['Simvastatin'] = list()

        for idx in range(len(self.ARDS_ID)):
            subject_id = self.ARDS_ID['SUBJECT_ID'].iloc[idx]
            subject_hadm = self.ARDS_ID['HADM_ID'].iloc[idx]
            subject_icu = self.ARDS_ID['ICUSTAY_ID'].iloc[idx]
            subject_prescription = self.ARDS_PRESCRIPTION[(self.ARDS_PRESCRIPTION['SUBJECT_ID'] == subject_id) &
                                                          (self.ARDS_PRESCRIPTION['HADM_ID'] == subject_hadm) &
                                                          (self.ARDS_PRESCRIPTION['ICUSTAY_ID'] == subject_icu)
            ]
            subject_Cisa = subject_prescription[subject_prescription['DRUG'].str.contains('Cisatracurium')]
            subject_Statin = subject_prescription[subject_prescription['DRUG'].str.contains('Simvastatin')]

            if len(subject_Cisa) != 0:
                if self.df_float_convertible(subject_Cisa['DOSE_VAL_RX']) == True:
                    drug_dict['Cisatracurium'].append(np.mean(list(pd.to_numeric(subject_Cisa['DOSE_VAL_RX']))))
                else:
                    subject_Cisa_DOSE = self.float_convertible_extractor(subject_Cisa['DOSE_VAL_RX'])
                    # print(subject_Cisa_DOSE)
                    if len(subject_Cisa_DOSE) > 0:
                        drug_dict['Cisatracurium'].append(np.mean(subject_Cisa_DOSE))
                    else:
                        drug_dict['Cisatracurium'].append(0)
            else:
                drug_dict['Cisatracurium'].append(0)

            if len(subject_Statin) != 0:
                if self.df_float_convertible(subject_Statin['DOSE_VAL_RX']) == True:
                    drug_dict['Simvastatin'].append(np.mean(list(pd.to_numeric(subject_Statin['DOSE_VAL_RX']))))
                else:
                    subject_Statin_DOSE = self.float_convertible_extractor(subject_Statin['DOSE_VAL_RX'])
                    if len(subject_Statin_DOSE) > 0:
                        drug_dict['Simvastatin'].append(np.mean(subject_Statin_DOSE))
                    else:
                        drug_dict['Simvastatin'].append(0)
            else:
                drug_dict['Simvastatin'].append(0)

            drug_dict['SUBJECT_ID'].append(subject_id)
            drug_dict['HADM_ID'].append(subject_hadm)
            drug_dict['ICUSTAY_ID'].append(subject_icu)

        return pd.DataFrame(drug_dict)

if __name__ == '__main__':
    drug = ARDS_Prescription()
    DRUG_DICT = drug.drug_extractor()
    pickle.dump(DRUG_DICT, open('PKL/ARDS_drug.pkl', 'wb'))