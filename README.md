# Análisis de calidad de datasets

Este repositorio pretende ser un registro del analisis de calidad de los datasets presentes en 
[data.buenosaires.gob.ar](https://data.buenosaires.gob.ar/) 

## Setup

Crear por única vez un [virtualenv](https://virtualenv.pypa.io/en/latest/) usando python 3.6.3
```bash
virtualenv venv
```

Para cada comando en adelante, es necesario previamente activar el virtualenv. 
```bash
. venv/bin/activate
```

Instalar las dependencias listadas en el archivo `requirements.txt`
```bash
pip install -r requirements.txt
```

Para ejecutar las rutinas de descarga y subida es necesario crear un archivo con nombre `ftp_password` que tenga como
contenido solo la contraseña del usuario `datosabiertos` para el ftp de gcba y ubicar el archivo en la carpeta `src`

## Notebooks

El repo contiene notebooks de [jupyter](https://jupyter.org/) en la carpeta `notebooks`

## Ejecutar rutinas

Para ejecutar las tres rutinas (descarga, limpieza, subida), ejecutar el comando 
```bash
python main.py
```
Es posible saltar la ejecución de las diferentes rutinas mediante el uso de parametros al momento de ejecutar el script.
Los distintos parametros que acepta el script son: `--no-download`, `--no-data-cleaner`, `--no-upload` y 
`--download-via-scrapy`.
Para conocer en detalle qué hace cada una de las rutninas y poder ejecutar solo una de ellas, leer a continuación.

## Descarga de datasets

La rutina de descarga obtiene los datasets listados en el archivo `manifest.json`. Hay dos fuentes posibles para
estos datasets: el ftp de buenosaires.gob.ar o el sitio [data.buenosaires.gob.ar](https://data.buenosaires.gob.ar/).

Para solo descargar desde el servidor ftp, correr el siguiente comando
```bash
python main.py --no-data-cleaner --no-upload
```

Para solo descargar una copia de los datasets de [data.buenosaires.gob.ar](https://data.buenosaires.gob.ar/) usando el 
scrapper de scrapy, correr el siguiente comando:
```bash
python main.py --no-data-cleaner --no-upload --download-via-scrapy
```

Ambas formas de descarga recorren los datasets listados en el archivo `manifest.json` y descargan los archivos 
correspondientes a los datasets en él. Los datasets descargados son ubicados en la carpeta `downloaded-datasets`. Si 
para un dataset su carpeta ya existe entonces se saltea su descarga. Para forzar la descarga, eliminar su carpeta y 
volver a correr el script. 

> El tamaño total de la descarga al momento de la elaboración de este script es de aproximadamente 7.45gb

## Scripts de limpieza

La rutina de limpieza aplica las reglas del [data-cleaner](https://github.com/datosgobar/data-cleaner/) ubicadas en
`src/cleaner/rules` a los datasets que se encuentren en la carpeta `downloaded-datasets`. Como resultado se obtienen
copias de los datasets en la carpeta `clean-datasets`

Para solo aplicar las reglas de limpieza a los datasets descargados en la carpeta `downloaded-datasets`, 
correr el comando:
```bash
python main.py --no-download --no-upload
```

## Subida de datasets

La rutina de subida de datasets toma los datasets ubicados en la carpeta `clean-datasets` generada por la rutina de
limpieza y sube los datasets al ftp en una carpeta tambien llamada `clean-datasets`.

Para ejecutar solo la rutina de subida, ejecutar:
```bash
python main.py --no-download --no-data-cleaner
```


## Referencias

El análisis y limpieza de los datasets realizado en este repositorio sigue los lineamientos de la [guia de datos 
abiertos](https://datosgcba.github.io/guia-datos/guia-abiertos/) del Gobierbo de la Ciudad de Buenos Aires, y utiliza
como herramienta el modulo [Data Cleaner](https://github.com/datosgobar/data-cleaner/) desarrollado por la Dirección de
Datos Abiertos del Gobierno Nacional Argentino

