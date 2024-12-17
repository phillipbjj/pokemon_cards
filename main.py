import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import psycopg2
#from typing import Union
#from pydantic import BaseModel

load_dotenv()
try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password=os.getenv('PHILPW'),
        host="localhost",
        port="1007",
        )
    print("Database connection successful")



    cur = conn.cursor()

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
        return templates.TemplateResponse("register_template.html", {"request": request})
   
    @app.post("/users/register", response_class=HTMLResponse)
    async def add_user(username: str = Form(...), password: str = Form(...), email: str = Form(...)):
        try:
            cur.execute('''INSERT INTO users (username, password, email) VALUES (%s, %s, %s)''', (username, password, email))
            conn.commit()
            return RedirectResponse("/", status_code=302)
        except Exception as e:
            conn.rollback()
            return {'error': str(e)}







    @app.get("/users/login", response_class=HTMLResponse)
    async def get_users(request: Request):
        return templates.TemplateResponse("users_template.html", {"request": request}) 

    @app.get("/users/account", response_class=HTMLResponse)
    async def get_users(request: Request):
        return templates.TemplateResponse("users_template.html", {"request": request}) 

    @app.get("/cards", response_class=HTMLResponse)
    async def get_cards(request: Request):
        return templates.TemplateResponse("cards_template.html", {"request": request}) 

except Exception as e:
    print(f"An error occurred: {e}")
    print("F homie")