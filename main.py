import pandas as pd

from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello goof World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get('/get_max_duration/{anio}/{plataforma}/{dtype}')
def get_max_duration(anio: int, plataforma: str, dtype: str):
    
    df_m_d=pd.read_csv("duracion_max_pelicula.cvs")
    duracion_maxima = df_m_d[(df_m_d["release_year"]==anio) 
       & (df_m_d["plataforma"]==plataforma)
        & (df_m_d["duration_type"]==dtype)]["title"].max()
    
    return {'pelicula': duracion_maxima}
