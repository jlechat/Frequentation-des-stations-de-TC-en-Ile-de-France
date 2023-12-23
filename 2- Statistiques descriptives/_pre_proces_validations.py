from _importation_donnees import donnees_archives, donnees_validation_23, donnees_profils_23, donnees_stations_toutes
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import plotly.express as px

def process_validations():
    validations_23=donnees_validation_23()
    # transformation des variables en excluant / transformant les valeurs prises (tr pour transformé)
    # CODE_STIF_RES
    validations_23_tr = validations_23[validations_23['CODE_STIF_RES'] != 'ND']
    # CATEGORIE_TITRE
    validations_23_tr.loc[validations_23_tr['CATEGORIE_TITRE'] == '?', 'CATEGORIE_TITRE'] = 'NON DEFINI'
    validations_23_tr['JOUR'] = pd.to_datetime(validations_23_tr['JOUR'], format='%Y-%m-%d')
    validations_23_tr['CODE_STIF_RES'] = validations_23_tr['CODE_STIF_RES'].astype(int)
    validations_23_tr['CODE_STIF_ARRET'] = validations_23_tr['CODE_STIF_ARRET'].astype(int)
    validations_23_tr['LIBELLE_ARRET'] = validations_23_tr['LIBELLE_ARRET'].astype(str)
    validations_23_tr['Mois'] = validations_23_tr['JOUR'].dt.month
    validations_23_tr['Année'] = validations_23_tr['JOUR'].dt.year
    return validations_23_tr
    