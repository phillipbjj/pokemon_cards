from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
#from typing import Union
#from pydantic import BaseModel

#Create FastAPI application
app = FastAPI(title='CardShop')
#Mount the static directory to serve static files. Used for sub-apps or static files.
app.mount('/static', StaticFiles(directory='static'), name='static')
# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

#class Item (BaseModel):

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    
"""@app.get("/")
async def read_root():
    return FileResponse('static/index.html')"""
