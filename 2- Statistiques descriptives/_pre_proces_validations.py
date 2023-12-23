from _importation_donnees import donnees_archives, donnees_validation_23, donnees_profils_23, donnees_stations_toutes
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import plotly.express as px

def df_validations():
    data=donnees_validation_23()
    data.loc[data['LIBELLE_ARRET'].isin(['CHATELET', 'LES HALLES']), 'lda'] = 474151
    data = data[data['LIBELLE_ARRET'] != 'MIRABEAU']
    validations_23_tr = data.groupby(['JOUR', 'lda', 'CATEGORIE_TITRE'])['NB_VALD'].sum().reset_index()
    # transformation des variables en excluant / transformant les valeurs prises (tr pour transformé)
    # CODE_STIF_RES
    # CATEGORIE_TITRE
    validations_23_tr.loc[validations_23_tr['CATEGORIE_TITRE'] == '?', 'CATEGORIE_TITRE'] = 'NON DEFINI'
    validations_23_tr['JOUR'] = pd.to_datetime(validations_23_tr['JOUR'], format='%Y-%m-%d')
    validations_23_tr['Mois'] = validations_23_tr['JOUR'].dt.month
    validations_23_tr['Année'] = validations_23_tr['JOUR'].dt.year
    return validations_23_tr
    

