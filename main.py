import pandas as pd

from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello goof GOD TAKE MY CHANCES World"}

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
  pporciento=(sum_true*100)/conteo_item
  return {"Usuario" : User_id, "Dinero gastado":gasto , "% de recomendación": pporciento , "cantidad de items": conteo_item}

@app.get('/get_max_duration/{anio}/{plataforma}/{dtype}')
def get_max_duration(anio: int, plataforma: str, dtype: str):
    
    df_m_d=pd.read_csv("duracion_max_pelicula.cvs")
    duracion_maxima = df_m_d[(df_m_d["release_year"]==anio) 
       & (df_m_d["plataforma"]==plataforma)
        & (df_m_d["duration_type"]==dtype)]["title"].max()
    
    return {'pelicula': duracion_maxima}
