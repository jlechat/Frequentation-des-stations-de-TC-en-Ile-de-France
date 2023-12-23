import pandas as pd
from _pre_proces_validations import df_validations
from _pre_proces_stations import df_stations

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
    joint_table.loc[joint_table['CATEGORIE_TITRE'] == '?', 'CATEGORIE_TITRE'] = 'NON DEFINI'
    joint_table['JOUR'] = pd.to_datetime(joint_table['JOUR'], format='%Y-%m-%d')
    joint_table['Mois'] = joint_table['JOUR'].dt.month
    joint_table['Année'] = joint_table['JOUR'].dt.year
    return joint_table