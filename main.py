import pandas as pd
import numpy as np
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello goof GOD TAKE MY CHANCES World ver1"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
    
@app.get('/developer/{desarrollador}')
def developer(desarrollador:str):
  df=pd.read_csv("apiFreeDeveloper.csv")
  total_datos = df[(df['developer']==desarrollador)].groupby(["year"]).count()["developer"]
  datos_free = df[(df['developer']==desarrollador)&(df['price']=="Free")].groupby(["year"]).count()["developer"]
  df_1=pd.DataFrame(total_datos)
  df_2=pd.DataFrame(datos_free)
  
  
  df_2.reset_index(inplace=True)
  df_1.reset_index(inplace=True)

  df_t=df_1.merge(df_2, left_on='year', right_on='year')
  mul=df_t["developer_y"]*100
  df_t['Contenido Free']=mul.div(df_t["developer_x"])

  return df_t.to_json(orient="records",lines=True,indent=2)
    
@app.get('/userdata/{User_id}')
def userdata( User_id : str ):
   
  total=pd.read_csv("user_reviews_corto_to.csv",lineterminator='\n')
  gasto=total[total["user_id"]==User_id]["price"].sum()
  conteo_item=total[total["user_id"]==User_id]["user_id"].count()
  sum_true=total[(total["user_id"]==User_id )&(total['recomended']== True)]["recomended"].count()
  pporciento=(sum_true * 100)/conteo_item
  #arr = ([{gasto}, {pporciento} , {conteo_item}])
                 
  return conteo_item


@app.get('/UserForGenre/{genero}')
def UserForGenre(genero:str):
  genre_csv=pd.read_csv('genres_join.csv')
  max_playtime=genre_csv[genre_csv['genres']==genero][["playtime","user_id","year"]].sort_values(by="playtime",ascending=False).head(1)
  u_i=max_playtime["user_id"]
  valor=u_i.to_string().split()[1]
  diccionario_f=genre_csv[genre_csv['user_id']==valor].groupby("year").sum()["playtime"].to_dict()

  return diccionario_f


@app.get('/get_max_duration/{anio}/{plataforma}/{dtype}')
def get_max_duration(anio: int, plataforma: str, dtype: str):
    
    df_m_d=pd.read_csv("duracion_max_pelicula.cvs")
    duracion_maxima = df_m_d[(df_m_d["release_year"]==anio) 
       & (df_m_d["plataforma"]==plataforma)
        & (df_m_d["duration_type"]==dtype)]["title"].max()
    {"Usuario" :"x", "Dinero gastado": gasto , "P de recomendación": pporciento, "cantidad de items": conteo_item}
    return {'pelicula': duracion_maxima}
