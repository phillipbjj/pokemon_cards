from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

#class Item (BaseModel):
    
    
@app.get("/")
async def read_root():
    return "Home page"
