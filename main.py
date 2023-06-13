from fastapi import FastAPI
import pandas as pd
from datetime import datetime
import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv('database/base_datos.csv')
df_modelo = pd.read_csv("database\modelo.csv")
df_modelo1 = df_modelo[['id', 'vote_average']]

cosine_sim = cosine_similarity(df_modelo1)

#instancia de fastApi
app = FastAPI()


#crear entrada
@app.get('/')
def mensaje():
    return 'Hola, bienvenido '

#Función para obtener la cantidad de filmaciones de un mes escefífico
@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes: str):
    df["release_date"] = pd.to_datetime(df["release_date"])
    meses = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7,
             "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12}
    
    mes_numero = meses.get(mes.lower())
    contador = 0 
    
    for fecha in df["release_date"]:
        if fecha.month == mes_numero:
            contador += 1
            
    return {'mes':mes, 'cantidad':contador} 

#Función para obtener la cantidad de películas lanzadas en un día específico
@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia:str):
    df["release_date"] = pd.to_datetime(df["release_date"])
    dias_semana = {
    'lunes': 0, 
    'martes' : 1,
    'miercoles' : 2,
    'jueves' : 3,
    'viernes' : 4,
    'sabado' : 5,
    'domingo' :6}
    
    dia_numero = dias_semana.get(dia.lower())
    contador = 0 
    
    for fecha in df["release_date"]:
        if fecha.weekday() == dia_numero:
            contador += 1
    return {'dia':dia, 'cantidad':contador}

#Función que devuelve la popularidad de una película en específico
@app.get('/score_titulo/{titulo}')
def score_titulo( titulo: str):
    for index, titulos in enumerate(df["title"]):
        if titulos.lower() == titulo.lower():
            t = str(df.loc[index, "title"])
            a = str(df.loc[index, 'release_year'])
            p = str(df.loc[index, "popularity"])
    return {'titulo': t , 'anio': a , 'popularidad': p}


@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo: str):
    for index, titulos in enumerate(df["title"]):
        if titulos.lower() == titulo.lower():
            t = str(df.loc[index, "title"])
            cant = df.loc[index, 'vote_count']
            a = str(df.loc[index, 'release_year'])
            promedio = str(df.loc[index, "vote_average"])
            if cant < 2000:
                return "La película no posee suficientes valoraciones"
            else:
                cant = str(df.loc[index, 'vote_count'])
                return {'titulo': t, 'anio': a, 'voto_total': cant, 'voto_promedio': promedio}   
 
            
@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor: str):
    retorno = 0
    cant = 0
    for lista_actores, valor_retorno in zip(df["Name_cast"], df["return"]):
        if nombre_actor in lista_actores:
            retorno += valor_retorno
            cant += 1
            promedio = retorno/cant
            
    return {'actor':nombre_actor, 'cantidad_filmaciones':cant, 'retorno_total':retorno, 'retorno_promedio':promedio}

@app.get('/get_director/{nombre_director}')
def get_director(nombre_director: str):
    retorno = 0
    l_titulo = []
    l_fecha = []
    l_retorno = []
    l_costo = []
    l_ganancia = []
    for indice, lista_directores in enumerate(df["Director"]):
        if nombre_director in lista_directores:
            retorno += df.loc[indice, "return"]
            titulo_pelicula = df.loc[indice, "title"]
            fecha = df.loc[indice, "release_date"]
            retorno_individual = df.loc[indice, "return"]
            costo = df.loc[indice, "budget"]
            ganancia_total = df.loc[indice, "revenue"]
            
            # Agregar los datos a la lista
            l_titulo.append(titulo_pelicula)
            l_fecha.append(fecha)
            l_retorno.append(retorno_individual)
            l_costo.append(costo)
            l_ganancia.append(ganancia_total)
           
            
    return {"director": nombre_director, 'retorno_total_director': retorno, "peliculas": l_titulo[:5], 'anio':l_fecha[:5],
            'retorno_pelicula':l_retorno[:5], 'budget_pelicula': l_costo[:5], 'revenue_pelicula': l_ganancia[:5]}
    
    
@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    #Convertir el titulo en el id de la película
    for index, value in df_modelo["title"].iteritems():
        if value == titulo:
            id_pelicula = df_modelo.loc[index, "id"]
    
    # Obtener el índice de la película de interés
    indice_pelicula = df_modelo1[df_modelo1['id'] == id_pelicula].index[0]

    # Obtener los puntajes de similitud para todas las películas
    sim_scores = list(enumerate(cosine_sim[indice_pelicula]))

    # Ordenar las películas por puntaje de similitud en orden descendente
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Obtener los top_n índices de las películas más similares (excluyendo la película de interés)
    top_indices = [item[0] for item in sim_scores[1:6]]

    # Obtener los ID de las películas más recomendadas
    top_recomendaciones = df_modelo1.loc[top_indices, 'id'].tolist()
    
    #Convertir los id recomendados a los titulos de peliculas
    titulos_recomendados = df_modelo.loc[df_modelo["id"].isin(top_recomendaciones), "title"].tolist()
    
    return {'lista recomendada': titulos_recomendados}