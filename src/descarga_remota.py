import kaggle
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent #obtener path de src

# Subir de `src/` a `repositry/` y luego añadir `data`.

REPO_ROOT = CURRENT_DIR.parent
DOWNLOAD_DIR = REPO_ROOT / 'data'

# Convertir a string 
DOWNLOAD_PATH = str(DOWNLOAD_DIR)



#####url para descargar el repositorio

KAGGLE_ID = 'ziya07/drugpatient-dataset-for-ckd-prediction'

######




def descargar(DOWNLOAD_PATH, KAGGLE_ID):
    try:
        kaggle.api.dataset_download_files(
            KAGGLE_ID,  #cambie segun el dataset a descargar
                                                              #de la url https://www.kaggle.com/datasets/nombre_usuario/nombre_data_set
                                                              #copie el fragmento nombre_usuario/nombre_data_set
            path=DOWNLOAD_PATH, 
            unzip=True
        )

    except Exception as e:
        print(f'se genero un error: {e}')


if __name__ == "__main__":
    descargar(DOWNLOAD_PATH, KAGGLE_ID)