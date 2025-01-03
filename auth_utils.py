from fastapi import FastAPI, Request, Response, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, Dict
import jwt
import re
from pydantic import BaseModel, validator
import redis
from fastapi.middleware.cors import CORSMiddleware

# Config
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION = 300  # 5 minutes

# Redis setup for rate limiting
redis_client = redis.Redis(host='localhost', port=6379, db=0)

class PasswordValidator:
    @staticmethod
    def validate(password: str) -> bool:
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

class User(BaseModel):
    username: str
    password: str

    @validator('password')
    def password_strength(cls, v):
        if not PasswordValidator.validate(v):
            raise ValueError(
                'Password must be 8+ characters with uppercase, lowercase, number, and special character'
            )
        return v

class TokenBlacklist:
    _blacklist: Dict[str, datetime] = {}

    @classmethod
    def add(cls, token: str):
        cls._blacklist[token] = datetime.utcnow()

    @classmethod
    def is_blacklisted(cls, token: str) -> bool:
        return token in cls._blacklist

class RateLimiter:
    @staticmethod
    def check_rate_limit(username: str) -> bool:
        key = f"login_attempts:{username}"
        attempts = redis_client.get(key)
        
        if attempts and int(attempts) >= MAX_LOGIN_ATTEMPTS:
            return False
        
        redis_client.incr(key)
        redis_client.expire(key, LOCKOUT_DURATION)
        return True

    @staticmethod
    def reset_attempts(username: str):
        key = f"login_attempts:{username}"
        redis_client.delete(key)

class AuthHandler:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    @staticmethod
    def create_token(username: str) -> str:
        expires = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return jwt.encode(
            {"sub": username, "exp": expires},
            SECRET_KEY,
            algorithm=ALGORITHM
        )

    @staticmethod
    def verify_token(token: str) -> Optional[str]:
        if TokenBlacklist.is_blacklisted(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked"
            )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload.get("sub")
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )

# FastAPI dependency
async def get_current_user(token: str = Depends(AuthHandler.oauth2_scheme)) -> str:
    username = AuthHandler.verify_token(token)
    if not username:
        raise HTTPException(status_code=401)
    return username

# Mock database (replace with real database in production)
users_db = {}

# API Routes
app = FastAPI()

@app.post("/register")
async def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = AuthHandler.pwd_context.hash(user.password)
    users_db[user.username] = hashed_password
    return {"message": "User created successfully"}

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not RateLimiter.check_rate_limit(form_data.username):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many login attempts. Try again in {LOCKOUT_DURATION} seconds"
        )

    user = users_db.get(form_data.username)
    if not user or not AuthHandler.pwd_context.verify(form_data.password, user):
        raise HTTPException(status_code=401)
    
    RateLimiter.reset_attempts(form_data.username)
    access_token = AuthHandler.create_token(form_data.username)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/logout")
async def logout(token: str = Depends(AuthHandler.oauth2_scheme)):
    TokenBlacklist.add(token)
    return {"message": "Successfully logged out"}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, token: str = Depends(AuthHandler.oauth2_scheme)):
    try:
        username = get_current_user(token)
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "username": username, "logged_in": True}
        )
    except HTTPException:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "logged_in": False}
        )