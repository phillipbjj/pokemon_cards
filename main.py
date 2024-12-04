from typing import Union
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
#from pydantic import BaseModel

app = FastAPI()

#class Item (BaseModel):
#Mount the static directory to serve static files
app.mount('/static', StaticFiles(directory='static'), name='static')
    
@app.get("/")
async def read_root():
    return FileResponse('static/index.html')
