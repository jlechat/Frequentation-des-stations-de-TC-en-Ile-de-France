import pandas as pd
from pre_process_validations_stations import df_stations, df_validations

def df_jointure_validations_stations():
    validations=df_validations()
    stations=df_stations()
    stations.loc[stations['id_ref_ZdC'] == 72225, 'id_ref_ZdC'] = 72219
    stations.loc[stations['id_ref_ZdC'] == 478926, 'id_ref_ZdC'] = 73792
    stations.loc[stations['id_ref_ZdC'] == 478733, 'id_ref_ZdC'] = 71410
    stations.loc[stations['id_ref_ZdC'] == 478505, 'id_ref_ZdC'] = 62737
    stations.loc[stations['id_ref_ZdC'] == 462934, 'id_ref_ZdC'] = 67747
    stations.loc[stations['id_ref_ZdC'] == 479919, 'id_ref_ZdC'] = 412697
    stations.loc[stations['id_ref_ZdC'] == 478855, 'id_ref_ZdC'] = 59577
    joint_table = pd.merge(validations, stations, left_on='lda', right_on='id_ref_ZdC', how='right')
    return joint_table