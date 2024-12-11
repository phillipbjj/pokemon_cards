from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from enum import Enum
#from typing import Union
#from pydantic import BaseModel
"""from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
import asyncpg
import bcrypt
from datetime import datetime"""
#Enum for static user roles
class UserRoles(str, Enum):
    admin = 'admin'
    user = 'user'
    shop_owner = 'shop_owner'
    guest = 'guest'

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str
    full_name: Optional[str] = None

    @validator('username')
    def username_must_be_valid(cls, v):
        if len(v) < 3 or len(v) > 20:
            raise ValueError('Username must be between 3 and 20 characters')
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        return v.lower()

    @validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain an uppercase letter')
        if not any(char.islower() for char in v):
            raise ValueError('Password must contain a lowercase letter')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain a number')
        return v

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v

# Database connection function
async def get_db_pool():
    return await asyncpg.create_pool(
        user='your_username',
        password='your_password',
        database='your_database',
        host='localhost'
    )
        
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

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate):
    try:
        # Get database connection from pool
        pool = await get_db_pool()
        async with pool.acquire() as conn:
            # Check if username already exists
            existing_username = await conn.fetchval(
                'SELECT username FROM users WHERE username = $1',
                user.username
            )
            if existing_username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already registered"
                )

            # Check if email already exists
            existing_email = await conn.fetchval(
                'SELECT email FROM users WHERE email = $1',
                user.email
            )
            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

            # Hash password
            hashed_password = bcrypt.hashpw(
                user.password.encode('utf-8'),
                bcrypt.gensalt()
            )

            # Insert new user
            await conn.execute('''
                INSERT INTO users (username, email, password_hash, full_name, created_at)
                VALUES ($1, $2, $3, $4, $5)
            ''',
            user.username,
            user.email,
            hashed_password.decode('utf-8'),
            user.full_name,
            datetime.utcnow()
            )

        return {
            "message": "User registered successfully",
            "username": user.username
        }

    except asyncpg.UniqueViolationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    finally:
        # Close the connection pool
        if 'pool' in locals():
            await pool.close()
