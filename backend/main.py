#Server_Project

#AUTHOR:    MUMINUL ISLAM

#Handle:    _MUMINUL_ISLAM___

#Git:
########################################################

#CODE
from  database import *

from pydantic import BaseModel
from typing import List

from fastapi import FastAPI, Depends 
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session

import cache

app=FastAPI()

#Adding Middleware
origin_url=[
    "http://127.0.0.1:3000",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'], #origin_url, #modify it if using redis.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#Middleware closed

#Get Dependency
def get_db():
    db=create_session()
    try:
        yield db
    finally:
        db.close()

class info_model(BaseModel):
    customerID: int
    orderID: int
    orderPrice: int

    class Config:
        orm_mode=True
#Dependency Closed

#routing

@app.get("/search",response_model=info_model)
def search(search_term:int,db: Session=Depends(get_db),):

    #table_row=db.query(info).filter(info.customerID==search_term).first()

    cache.rateLimit(search_term) #use it if you use radis rate limit

    table_row=cache.GetCache(search_term,db) #use it if you use redis cache
    
    return table_row

@app.get("/",response_model=List[info_model])
def read(db: Session=Depends(get_db)):
    table_row=db.query(info).all()
    return table_row

#routing closed
