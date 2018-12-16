# Análisis de calidad de datasets

Este repositorio pretende ser un registro del analisis de calidad de los datasets presentes en 
[data.buenosaires.gob.ar](https://data.buenosaires.gob.ar/) 

## Setup

Crear por única vez un [virtualenv](https://virtualenv.pypa.io/en/latest/) usando python 3.
```bash
virtualenv -p python3 venv
```

Para cada comando en adelante, es necesario previamente activar el virtualenv. 
```bash
. venv/bin/activate
```

Instalar las dependencias listadas en el archivo `requirements.txt`
```bash
pip install -r requirements.txt
```

## Notebooks

El repo contiene notebooks de [jupyter](https://jupyter.org/) en la carpeta `notebooks`

## Datasets

Para descargar una copia de los datasets listados en el archivo `datasets/manifest.json`, correr el 
scrapper de scrapy via:
```bash
scrapy runspider datasets/download.py
```
Este script recorre los datasets listados en `datasets/manifest.json`, descarga cada archivo comprimido correspondiente
desde [data.buenosaires.gob.ar](https://data.buenosaires.gob.ar/) y los descomprime en carpetas correspondientes dentro
de `datasets`. Si para un dataset su carpeta ya existe entonces se saltea su descarga. Para forzar la descarga, 
eliminar su carpeta y volver a correr el script. 
> El tamaño total de la descarga al momento de la elaboración de este script es de aproximadamente 2.5gb