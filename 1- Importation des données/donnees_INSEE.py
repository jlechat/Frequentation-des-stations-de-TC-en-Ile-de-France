import geopandas as gpd
import requests
from IPython.utils import io
from io import BytesIO 
from zipfile import ZipFile
import tempfile
import os

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
    


    
    

    
    


    
    
    
    

