import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from enum import Enum
import psycopg2
#from typing import Union
#from pydantic import BaseModel

"""conn = psycopg2.connect(
    dbname="cardshop",
    user="postgres",
    password=os.getenv('PHILPW'),
    host="localhost",
    port="1007"
)"""

"""cur = conn.cursor()
cur.execute("
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(20) NOT NULL,
                password VARCHAR(20) NOT NULL,
                email VARCHAR(100) NOT NULL,
                name VARCHAR(100),
                phone TEXT,
                country TEXT,
                address TEXT,
                zipcode TEXT,
                birthday TEXT,
                profile_picture_url TEXT
            ")
            )     """  
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

