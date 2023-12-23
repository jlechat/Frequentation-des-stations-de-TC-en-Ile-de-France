#Ce script contient la fonction qui permet de télécharger et de mettre en forme les données de l'Insee
#après leur jointure avec les stations de RER.
#Les explications sont accessibles depuis le Note Book "pre_process_INSEE_IDFM.ipynb" du dossier 
#"1- Importation des données".

from IPython.utils import io
from io import BytesIO 
import geopandas as gpd
import pandas as pd
import requests
import os
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily as ctx
from donnees_INSEE import donnees_INSEE
from donnees_IDFM import donnees_stations_toutes

def data_INSEE_stations():
    with io.capture_output() as captured:
        data = donnees_INSEE()
        stations=donnees_stations_toutes()
        stations_socio = gpd.sjoin(stations, data, how='inner', predicate='intersects')
        stations_RER=stations.loc[stations['mode_']=="RER"]
        stations_socio_RER=stations_socio.loc[stations_socio['mode_']=='RER']
        fusion = pd.merge(stations_RER, stations_socio_RER, on='Geo Point', how='outer', indicator=True)
        elements_uniques = fusion[fusion['_merge'] == 'left_only']
        elements_ajout=elements_uniques.drop(columns=['Geo Shape_y', 'gares_id_y',
       'nom_long_y', 'nom_so_gar_y', 'nom_su_gar_y', 'id_ref_ZdC_y',
       'nom_ZdC_y', 'id_ref_ZdA_y', 'nom_ZdA_y', 'idrefliga_y', 'idrefligc_y',
       'res_com_y', 'indice_lig_y', 'mode__y', 'tertrain_y', 'terrer_y',
       'termetro_y', 'tertram_y', 'terval_y', 'exploitant_y', 'idf_y',
       'principal_y', 'x_y', 'y_y', 'picto ligne_y', 'nom_iv_y', 'geometry_y', '_merge'])
        nouveaux_noms = {col: col.rstrip('_x') if col.endswith('_x') else col for col in elements_ajout.columns}
        elements_ajout.rename(columns=nouveaux_noms, inplace=True)
        elements_ajout.rename(columns={"mode" : "mode_"}, inplace=True)
        colonnes_a_modifier = ['ind', 'men', 'men_pauv', 'men_1ind', 'men_5ind', 'men_prop', 'men_fmp', 'ind_snv',
                       'men_surf', 'men_coll', 'men_mais', 'log_av45', 'log_45_70', 'log_70_90', 'log_ap90',
                       'log_inc', 'log_soc', 'ind_0_3', 'ind_4_5', 'ind_6_10', 'ind_11_17', 'ind_18_24',
                       'ind_25_39', 'ind_40_54', 'ind_55_64', 'ind_65_79', 'ind_80p']
        for colonne in colonnes_a_modifier:
            elements_ajout[colonne] = 0
        stations_socio_RER = gpd.GeoDataFrame(pd.concat([stations_socio_RER, elements_ajout], ignore_index=True))
        #On retire les stations en trop pour la suite de l'analyse
        stations_socio_RER = stations_socio_RER[stations_socio_RER['nom_long'] != 'Creil']
        stations_socio_RER = stations_socio_RER[stations_socio_RER['nom_long'] != 'Chantilly-Gouvieux']
        stations_socio_RER = stations_socio_RER[stations_socio_RER['nom_long'] != 'Orry-la-Ville-Coye-la-Forêt']
        stations_socio_RER = stations_socio_RER[stations_socio_RER['nom_long'] != 'La Borne Blanche']
        stations_socio_RER = stations_socio_RER[stations_socio_RER['nom_long'] != 'Malesherbes']
        stations_socio_RER = stations_socio_RER[stations_socio_RER['nom_long'] != 'Igny']
        stations_socio_RER = stations_socio_RER[stations_socio_RER['nom_long'] != 'Bièvres']
        stations_socio_RER = stations_socio_RER[stations_socio_RER['nom_long'] != 'Vauboyen']
        stations_socio_RER = stations_socio_RER[stations_socio_RER['nom_long'] != 'Jouy-en-Josas']
        stations_socio_RER = stations_socio_RER[stations_socio_RER['nom_long'] != 'Petit-Jouy-les-Loges']
        
    return stations_socio_RER
