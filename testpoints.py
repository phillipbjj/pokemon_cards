from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


#Create FastAPI application
app = FastAPI(title='CARDSHOP.IO')
#Mount the static directory to serve static files. Used for sub-apps or static files.
app.mount('/static', StaticFiles(directory='static'), name='static')
# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    
@app.get("/users/login", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users_template.html", {"request": request}) 

@app.get("/users/register", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("register_template.html", {"request": request})

@app.get("/users/account", response_class=HTMLResponse)
async def get_users(request: Request):
    return templates.TemplateResponse("users_template.html", {"request": request}) 

@app.get("/cards", response_class=HTMLResponse)
async def get_cards(request: Request):
    return templates.TemplateResponse("cards_template.html", {"request": request}) 

