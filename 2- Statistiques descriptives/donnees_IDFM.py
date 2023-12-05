#Ce script contient les fonctions qui permettent de télécharger les données d'Île de France Mobilités (IDFM)
#qui contiennent les validations des pass navigo.
import pandas as pd
import requests
from io import BytesIO, StringIO
from zipfile import ZipFile
import warnings
import geopandas as gpd
from shapely.geometry import Point


def donnees_validation_23() :
    """
    Description : permet de télécharger les données de validation sur l'ensemble du réseau ferré d'Île de France
    du premier semestre 2023.

    Args : ne prend aucun argument.

    Returns : 1 DataFrame
    """
    url = "https://data.iledefrance-mobilites.fr/api/explore/v2.1/catalog/datasets/validations-reseau-ferre-nombre-validations-par-jour-1er-semestre/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
    data_validation_23 = pd.read_csv(url, sep=";")
    return data_validation_23

def donnees_profils_23() :
    """
    Description : permet de télécharger les données de validation par profils horaire sur l'ensemble du réseau 
    ferré d'Île de France du premier semestre 2023.

    Args : ne prend aucun argment

    Returns : 1 DataFrame
    """
    url = "https://data.iledefrance-mobilites.fr/api/explore/v2.1/catalog/datasets/validations-reseau-ferre-profils-horaires-par-jour-type-1er-semestre/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
    data_profils_horaires_23 = pd.read_csv(url, sep=";")
    return data_profils_horaires_23

def donnees_archives() :
    """
    Description : permet de télécharger les données de validation ET les profils horaires sur l'ensemble du réseau 
    ferré d'Île de France entre 2015 et 2022 inclus.

    Args : ne prend aucun argument

    Returns : 2 DataFrame (validation puis profils horaires).
    """
    warnings.filterwarnings('ignore')
    url = "https://data.iledefrance-mobilites.fr/api/explore/v2.1/catalog/datasets/histo-validations-reseau-ferre/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
    data_archives = pd.read_csv(url, sep=";")
    data_archives.rename(columns=dict(zip(data_archives.columns, ["date", "lien"])), inplace=True)
    annees = [annee for annee in range(2015, 2023)]
    table=["NB_S1", "PRO_S1", "NB_S2", "PRO_S2"]
    validations_annees=pd.DataFrame()
    profils_annees=pd.DataFrame()
    for annee in annees:
        print(annee)
        url_zip = data_archives[data_archives['date'] == annee]['lien'].iloc[0]
        response = requests.get(url_zip)
        with ZipFile(BytesIO(response.content)) as zipfile:
            # On récupère la liste des noms de fichier dans le ZIP
            file_names = zipfile.namelist()
            i=0
            for file_name in file_names:
                if file_name.endswith('.zip'): a=1
                else:                
                    name=table[i]
                    i+=1
                    # Lecture du contenu du fichier
                    with zipfile.open(file_name) as file:
                        if file_name.endswith('.csv') :
                            globals()[name] = pd.read_csv(file, sep=";")
                        elif annee==2022:
                            if name=="NB_S2" or name=="PRO_S2": globals()[name] = pd.read_csv(file, sep=";")
                            else: globals()[name] = pd.read_csv(file, sep='\t', header=0)
                        else:
                            globals()[name] = pd.read_csv(file, sep='\t', header=0)
        NB=pd.concat([NB_S1, NB_S2])
        NB['annee']=annee
        PRO=pd.concat([PRO_S1, PRO_S2])
        PRO['annee']=annee
        validations_annees=pd.concat([validations_annees, NB])
        profils_annees=pd.concat([profils_annees, PRO])
    return validations_annees, profils_annees

def donnees_stations_toutes() :
    url="https://data.iledefrance-mobilites.fr/api/explore/v2.1/catalog/datasets/emplacement-des-gares-idf/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
    stations=pd.read_csv(url, sep=";")
    stations = gpd.GeoDataFrame(stations, geometry=[Point(xy) for xy in zip(stations.x, stations.y)])
    stations.crs = "EPSG:2154"
    return stations
    
    

