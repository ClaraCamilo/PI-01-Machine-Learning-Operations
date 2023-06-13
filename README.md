# Machine Learning Operations (MLOps)


## Index 
- [Machine Learning Operations (MLOps)](#machine-learning-operations-mlops)
  - [Index](#index)
  - [Introducción](#introducción)
  - [Objetivos](#objetivos)
  - [ETL](#etl)
  - [EDA](#eda)
  - [Sistema de Recomendación](#sistema-de-recomendación)
  - [Funciones de la API](#funciones-de-la-api)
  - [Video](#video)
  
## Introducción

Este es mi proyecto de MLOps de la carrera de Data Science de Henry. Este proyecto utiliza los datos de dos Datasets con información sobre diferentes películas, que incluye información como títulos de películas, géneros, fechas de lanzamiento, popularidad, tanto crew como cast de las mismas y más. Utilicé diferentes técnicas en ETL (Extract, Transform, Load), análisis exploratorio de datos (EDA) y desarrollo de API para ofrecer un sistema de recomendación de películas 

## Objetivos
- Transformación y limpieza de datos: Aplicar técnicas de Extracción, Transformación y Carga (ETL) para preprocesar y limpiar el conjunto de datos de películas.
- Desarrollo de API: Diseñar e implementar un conjunto de funciones y una API que se integre sin problemas con el sistema de recomendación basado en el contenido.
- Análisis Exploratorio de Datos (EDA): Realizar un análisis exhaustivo de los datos para obtener información sobre las relaciones entre las variables, la detección de outliers y la búsqueda de patrones.
- Sistema de Recomendaciones: Desarrollar un modelo de aprendizaje automático que encuentre la similitud de puntuación entre esa película y el resto para recomendar nuevas películas a los usuarios.
- Implementación de la API: Desplegar la API del sistema de recomendación en un entorno de producción, asegurando que esté disponible y accesible para los usuarios.
  
  
## ETL
El proceso ETL lo realicé con los dos Dataset proporcionados para prepararlo para el análisis y la consulta, siguiendo los siguientes pasos:
- Se realizó un merge de ambos dataset en la columna id
-	Se eliminaron los duplicados en la columna “id” para garantizar la integridad de los datos
-	Los campos anidados como “belongs_to_collection”, “genres”, “production_companies”, “production_countries”, “spoken_languages”, “cast” y “crew” se desanidaron para facilitar la manipulación de datos". Se agregaron solamente al data frame las columnas que se creyeron necesarias para un futuro análisis. También se creó un diccionario de géneros 
-	Los valores nulos en los campos "revenue" y "budget" se reemplazaron por 0, asegurando consistencia en los cálculos. Se eliminaron los valores nulos en el campo "release date" y de “title” para garantizar la integridad de los datos. 
-	Se estandarizó el formato la columna “realease_date” a YYYY-mm-dd
-	Se crearon tres columnas nuevas “realese_year”, “realese_month” extrayendo el año y el mes de estreno de la película respectivamente y otra, “return” generando el retorno de inversión, a partir de la división entre las columnas “revenue” y “Budget” 
-	Para simplificar el conjunto de datos y centrarme en la información relevante, se eliminaron las columnas innecesarias, incluyendo “video”, “imdb_id”, “adult”, “original_title”, “poster_path”, “tagline”, “status”, “overview” y “homepage”. Además de eliminar también las columnas originales que fueron desanidadas 

## EDA
Los datos resultantes del proceso de ETL se utilizaron para realizar el Análisis Exploratorio de Datos (EDA). Todas las columnas se analizaron con la ayuda de la herramienta ProfileReport de la biblioteca ydata_profiling. 
[Pandas-profiling](profiling.html)

Se miraron las correlaciones entre las variables, la cantidad de ceros por columna y, al encontrarse con la variable “Budget” que tiene su mayoría de valores en cero, se realizó una segunda matiz de correlación sin estos valores para comprender mejor las relaciones entre las mismas. 

Se realizaron gráficos para entender la distribución de las variables numéricas, las conclusiones más relevantes incluyen la detección de algún tipo de error de carga en la variable “popularity”, la identificación de películas con una duración mayor a 5 horas, en algunos casos representando errores de carga y en otros siendo los títulos series en vez de películas.

Se generaron nubes de palabras con los actores, directores, géneros e idiomas con mayor frecuencia entre las películas. En este análisis detectamos que la actriz con mayor frecuencia no es la actriz más famosa, sino una extra conocida por aparecen en más de 200 películas por lo que, a futuro, encontramos interesante el análisis de esta variable agregando algún tipo de peso sobre la popularidad de los mismos. 

En este punto del EDA, es importante mencionar que se crearon variables binarias utilizando la técnica de "one-hot encoding" para las columnas "genres", "Name_cast" y "Director" con el propósito de utilizarlas en el modelo. Sin embargo, se decidió solo las columnas relacionadas al  género debido a problemas de rendimiento al ejecutar el modelo en el equipo.

## Sistema de Recomendación 
El sistema de recomendación fue desarrollado con la herramienta cosine similarity, utilizada para calcular la similitud entre las diferentes películas, en función de algunas de sus  características definidas en el EDA. Basado en las puntuaciones de similitud proporcionadas por la matriz, el algoritmo recomienda las 5 películas más similares a la proporcionada por el usuario como entrada. Este modelo también se hizo disponible como un punto final en la API, aunque con algunas dificultades que serán explicadas en el apartado en relación al desarrollo de la API

## Funciones de la API
Se desarrollaron los endpoints solicitados como funciones de Python en un archivo de Jupyter Notebook para asegurar su funcionamiento. Se creó un entorno virtual y, después de instalar FastAPI y uvicorn, se creó el archivo main.py con la estructura necesaria para implementar los endopints. 
Los primeros seis fueron deployados sin problema alguno pero a la hora de cargar la matriz de similaridad empezaron los problemas de memoria y procesamiento, ya que intentando exportarla se generaba un archivo de 15 GB, luego de probar por horas diferentes ideas desde dividir en partes para generar la matriz, exportarla y luego volver a unirla en el main.py hasta intentar generar la matriz en sí en el mismo main.py, que sé que está mal pero necesitaba que funcione para lograr el MVP. Decidí finalmente realizar nuevamente la matriz pero solo con 1000 registros para poder generar el deployment y su uso. 

En el siguiente link podrán utilizarla [link API](https://movies-api-1ru0.onrender.com/docs)


## Video
En este [enlace](https://www.youtube.com/watch?v=NAUJhIQb500) esta el video de presentación del proyecto 