#Ce script contient les fonctions qui permettent de télécharger les données d'Île de France Mobilités (IDFM)
#qui contiennent les validations des pass navigo.
import pandas as pd
import requests
from IPython.utils import io
from io import BytesIO, StringIO
from zipfile import ZipFile
import warnings
import geopandas as gpd
from shapely.geometry import Point
import tempfile
import os
from bs4 import BeautifulSoup

#1- DONNEES INSEE :
def donnees_INSEE():
    with io.capture_output() as captured:
        url_zip="https://drive.google.com/uc?export=download&id=1U9HT438foGzW06JdtVC3_ByA17Qipyrd"
        response = requests.get(url_zip)
        # Créer un répertoire temporaire pour stocker les fichiers
        with tempfile.TemporaryDirectory() as tmpdirname:
            with ZipFile(BytesIO(response.content)) as zipfile:
                # Extraire tous les fichiers dans le répertoire temporaire
                zipfile.extractall(tmpdirname)
        
                # Rechercher le fichier .shp dans le répertoire temporaire
                for file_name in os.listdir(tmpdirname):
                    if file_name.endswith('.shp'):
                        shp_path = os.path.join(tmpdirname, file_name)
                        data = gpd.read_file(shp_path)  
    return data
    

#2- DONNEES IDFM :
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
    """
    Description : permet de télécharger les données des stations du réseau IDFM.

    Args : ne prend aucun argument

    Returns : 1 DataFrame.
    """
    url="https://data.iledefrance-mobilites.fr/api/explore/v2.1/catalog/datasets/emplacement-des-gares-idf/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
    stations=pd.read_csv(url, sep=";")
    stations = gpd.GeoDataFrame(stations, geometry=[Point(xy) for xy in zip(stations.x, stations.y)])
    stations.crs = "EPSG:2154"
    return stations

def donnees_stations_toutes_sauvegarde() :
    """
    Description : permet de télécharger les données des stations du réseau IDFM, à partir d'une sauvegarde si jamais
    les données étaient modifiées entre temps.

    Args : ne prend aucun argument

    Returns : 1 DataFrame.
    """
    url="https://drive.google.com/uc?export=download&id=1meJK1440KCLhubkyL9iZ6sXfuUaWRYJJ"
    stations=pd.read_csv(url, sep=";")
    stations = gpd.GeoDataFrame(stations, geometry=[Point(xy) for xy in zip(stations.x, stations.y)])
    stations.crs = "EPSG:2154"
    return stations

#3 - Scrapping

def scrapping():
    url = 'https://fr.wikipedia.org/wiki/Liste_des_gares_du_RER_d%27%C3%8Ele-de-France'
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    def clean_text(text):
        return text.replace('\xa0', ' ').strip() 


    lignes = []
    gares = []  
    
    for row in soup.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 1:

            station_link = cells[0].find('a')
            if station_link:
                station_name = clean_text(station_link.get_text())
                gares.append(station_name)
                lignes.append([clean_text(link['title'].replace("Ligne", "")) for cell in cells[1:] for link in cell.find_all('a', title=True) if 'Ligne' in link['title']])
        

    tableau_gares = soup.find("table", class_=["wikitable sortable center"])
    tableau_gares_non_desservies = soup.find("table", class_=["wikitable sortable"])

    url_gares=[]

    for row in tableau_gares.find_all("tr")[1:]:  
            cellules = row.find_all("td")
            lien = cellules[0].find("a")
            url_gare = "https://fr.wikipedia.org" + lien.get("href")
            url_gares.append(url_gare)

    for row in tableau_gares_non_desservies.find_all("tr")[1:]:  
            cellules = row.find_all("td")
            lien = cellules[0].find("a")
            url_gare = "https://fr.wikipedia.org" + lien.get("href")
            url_gares.append(url_gare)
                
    bus=[]
    bus_jour = []
    noctilien = []

    for url in url_gares :
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        bandeau = soup.find("table", {'class' : 'infobox_v2 noarchive'})
        td_tags = bandeau.find_all("td")
        numeros_lignes_bus = []

        for td_tag in td_tags : 

            balises_b = td_tag.find_all("b")

            for balise_b in balises_b:
                numero_ligne = balise_b.get_text()
                numeros_lignes_bus.append(clean_text(numero_ligne))

        bus_clean = [num for num in numeros_lignes_bus if (any(i.isdigit() for i in num) or len(num)<3)]
        nocti = [i for i in bus_clean if i.startswith('N') and i[1].isdigit()]
        bus_j = [x for x in bus_clean if not (x.startswith('N') and x[1].isdigit())]
        concat = [bus_jour,noctilien]
        bus.append(concat)
        bus_jour.append(bus_j)
        noctilien.append(nocti)


    for i in range(len(gares)):
        gares[i] = gares[i].upper()
    
    concat = { 
        'arret' : gares,
        'lignes' : lignes,
        'bus_jour' : bus_jour,
        'noctilien' : noctilien,
    }

    data_bus = pd.DataFrame(concat)

    quanti_bus = data_bus.copy()
    quanti_bus['lignes'] = quanti_bus['lignes'].apply(lambda x: len(x))
    quanti_bus['bus_jour'] = quanti_bus['bus_jour'].apply(lambda x: len(x))
    quanti_bus['noctilien'] = quanti_bus['noctilien'].apply(lambda x: len(x))
    return quanti_bus















    
