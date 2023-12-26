from IPython.utils import io
from io import BytesIO  

with io.capture_output() as captured: #on évite d'afficher les sorties lors de l'importation
    !pip install pandas fiona shapely pyproj rtree
    !pip install geopandas
    !pip install topojson
    !pip install contextily
    !pip install requests py7zr geopandas openpyxl tqdm s3fs PyYAML xlrd
    !pip install git+https://github.com/inseefrlab/cartiflette@80b8a5a28371feb6df31d55bcc2617948a5f9b1a

import geopandas as gpd
import pandas as pd
import requests
from zipfile import ZipFile
import tempfile
import os
import matplotlib.pyplot as plt
from shapely.geometry import Point
import contextily as ctx
from donnees_INSEE import donnees_INSEE
from donnees_IDFM import donnees_stations_toutes
import cartiflette.s3 as s3

def fond_de_carte_IDF():
    with io.capture_output() as captured: #on évite d'afficher les sorties lors de l'importation
        shp_communes = s3.download_vectorfile_url_all(
            crs = 4326,
            values = ["75", "92", "93", "94", "77", "78", "91", "95"],
            borders="COMMUNE",
            vectorfile_format="topojson",
            filter_by="DEPARTEMENT",
            source="EXPRESS-COG-CARTO-TERRITOIRE",
            year=2022)

    with io.capture_output() as captured:
    arrondissements = s3.download_vectorfile_url_all(
        crs = 4326,
        values = ["75"],
        borders="COMMUNE_ARRONDISSEMENT",
        vectorfile_format="topojson",
        filter_by="DEPARTEMENT",
        source="EXPRESS-COG-CARTO-TERRITOIRE",
        year=2022)

    shp_communes = pd.concat(
  [
    shp_communes.loc[shp_communes['INSEE_DEP'] != "75"].to_crs(2154),
    arrondissements.to_crs(2154)
  ])
    return shp_communes