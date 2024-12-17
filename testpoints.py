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

#class Item (BaseModel):

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    


"""from fastapi import Depends, FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

def get_db():
    conn = psycopg2.connect("dbname=test user=postgres password=secret")
    try:
        yield conn
    finally:
        conn.close()

def get_cursor(conn=Depends(get_db)):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        yield cursor
    finally:
        cursor.close()

@app.post("/users/register", response_class=HTMLResponse)
async def add_user(username: str = Form(...), password: str = Form(...), email: str = Form(...), cur=Depends(get_cursor)):
    try:
        cur.execute('''INSERT INTO users (username, password, email) VALUES (%s, %s, %s)''', (username, password, email))
        cur.connection.commit()
        return RedirectResponse("/", status_code=302)
    except Exception as e:
        cur.connection.rollback()
        raise HTTPException(status_code=400, detail=str(e))"""