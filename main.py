from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from enum import Enum
#from typing import Union
#from pydantic import BaseModel

#Enum for static user roles
class UserRoles(str, Enum):
    admin = 'admin'
    user = 'user'
    shop_owner = 'shop_owner'
    guest = 'guest'
    
#Create FastAPI application
app = FastAPI(title='CARDSHOP.IO')
#Mount the static directory to serve static files. Used for sub-apps or static files.
app.mount('/static', StaticFiles(directory='static'), name='static')
# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

#class Item (BaseModel):

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    
@app.get("/users/register", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users_template.html", {"request": request})

@app.get("/users/login", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users_template.html", {"request": request}) 

@app.get("/users/account", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users_template.html", {"request": request}) 

@app.get("/cards", response_class=HTMLResponse)
async def get_cards(request: Request):
    return templates.TemplateResponse("cards_template.html", {"request": request}) 

"""@app.get("/users/forgot-password", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users_template.html", {"request": request})

@app.get("/users/forgot-password", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users_template.html", {"request": request})"""
