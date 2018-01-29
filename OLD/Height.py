import numpy as np
import pandas as pd
import pickle

CH_ARDS_reduced = pickle.load(open('CH_ARDS_reduced.pkl','rb'))
ARDS_SUBJECT_ID = pickle.load(open('ARDS_SUBJECT_ID.pkl','rb'))

HEIGHT_ID = [920, 1394, 4187, 3486, 3485, 4188]
CH_ARDS_height = CH_ARDS_reduced[CH_ARDS_reduced['ITEMID'].isin(HEIGHT_ID)]

ARDS_HEIGHT = dict()
ARDS_HEIGHT['SUBJECT_ID'] = list()
ARDS_HEIGHT['HEIGHT'] = list()

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
            ARDS_HEIGHT['HEIGHT'].append(height)
            ARDS_HEIGHT['SUBJECT_ID'].append(subject_id)
            height_find = True
            break
        else:
            continue
    if height_find == False:
        print(subject_id, '', sep='|')
        ARDS_HEIGHT['HEIGHT'].append(np.nan)
        ARDS_HEIGHT['SUBJECT_ID'].append(subject_id)

ARDS_HEIGHT = pd.DataFrame(ARDS_HEIGHT)