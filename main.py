from fastapi import FastAPI
import pandas as pd
from datetime import datetime

#instancia de fastApi
app = FastAPI()
df = pd.read_csv('database/base_datos.csv')

#crear entrada
@app.get('/')
def mensaje():
    return 'Hola, bienvenido '

#Función para obtener la cantidad de filmaciones de un mes escefífico
@app.get('/mes/{Mes}')
def cantidad_filmaciones_mes(Mes: str):
    df["release_date"] = pd.to_datetime(df["release_date"])
    meses = {"enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7,
             "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12}
    
    mes_numero = meses.get(Mes.lower())
    contador = 0 
    
    for fecha in df["release_date"]:
        if fecha.month == mes_numero:
            contador += 1
            
    return f'{contador} cantidad de películas que fueron estrenadas en el mes de {Mes}' 

#Función para obtener la cantidad de películas lanzadas en un día específico
@app.get('/dia/{Dia}')
def cantidad_filmaciones_dia(Dia:str):
    df["release_date"] = pd.to_datetime(df["release_date"])
    dias_semana = {
    'lunes': 0, 
    'martes' : 1,
    'miercoles' : 2,
    'jueves' : 3,
    'viernes' : 4,
    'sabado' : 5,
    'domingo' :6}
    
    dia_numero = dias_semana.get(Dia.lower())
    contador = 0 
    
    for fecha in df["release_date"]:
        if fecha.weekday() == dia_numero:
            contador += 1
    return f'{contador} cantidad de películas fueron estrenadas en los días {Dia}'

#Función que devuelve la popularidad de una película en específico
@app.get('/score_titulo/')
def score_titulo(titulo_de_la_filmación: str):
    for index, titulo in enumerate(df["title"]):
        if titulo.lower() == titulo_de_la_filmación.lower():
            t = df.loc[index, "title"]
            a = df.loc[index, 'release_year']
            p = df.loc[index, "popularity"]
    return f'La película {t} fue estrenada en el año {a} con un score/popularidad de {p}'


@app.get('/votos_titulo/')
def votos_titulo(titulo_de_la_filmación: str):
    for index, titulo in enumerate(df["title"]):
        if titulo.lower() == titulo_de_la_filmación.lower():
            t = df.loc[index, "title"]
            cant = df.loc[index, 'vote_count']
            a = df.loc[index, 'release_year']
            promedio = df.loc[index, "vote_average"]
            if cant < 2000:
                return "La película no posee suficientes valoraciones"
            else:
                return f'La película {t} fue estrenada en el año {a}. La misma cuenta con un total de {cant} valoraciones, con un promedio de {promedio}'    
 
            
@app.get('/get_actor/')
def get_actor(nombre_actor: str):
    retorno = 0
    cant = 0
    for lista_actores, valor_retorno in zip(df["Name_cast"], df["return"]):
        if nombre_actor in lista_actores:
            retorno += valor_retorno
            cant += 1
            promedio = retorno/cant
            
    return f"El actor {nombre_actor} ha participado de {cant} filmaciones, el mismo ha conseguido un retorno de {retorno} con un promedio de {promedio} por filmación"


@app.get('/get_director/')
def get_director(nombre_director):
    retorno = 0
    lista = []
    for indice, lista_directores in enumerate(df["Director"]):
        if nombre_director in lista_directores:
            retorno += df.loc[indice, "return"]
            titulo_pelicula = df.loc[indice, "title"]
            retorno_individual = df.loc[indice, "return"]
            costo = df.loc[indice, "budget"]
            ganancia_total = df.loc[indice, "revenue"]
            
            # Agregar los datos a la lista
            lista.append((titulo_pelicula +
                " con un retorno individual de " + str(retorno_individual) +
                ", tuvo un costo de " +  str(costo) +
                " y una ganancia total de " +  str(ganancia_total)))
            
    return {
        "El director": nombre_director,
        "tiene un retorno total de ": retorno,
        "y las películas que dirigió fueron": lista
    }