from fastapi import FastAPI,Request,Depends
from database.database import get_db
from sqlalchemy.orm import Session
from auth.auth import router
from models.model import User,RefreshToken
from tokens.dependency import get_current_user
from config import FRONTEND_URL,GOOGLE_SESSION_SECRET,GOOGLE_REDIRECT_URI
from auth.google_auth import oauth,SessionMiddleware,CORSMiddleware

app = FastAPI(title="Production Authentication API")


app.add_middleware(
    SessionMiddleware,
    secret_key=GOOGLE_SESSION_SECRET,
    https_only=False,   # True only in production (HTTPS)
    same_site="lax",    
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],   # wildcard + credentials is invalid in CORS spec
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"]
)

app.include_router(router=router)

@app.get("/")
def root():
    return {
        "message": "Authentication API is running"
    }

@app.get("/me")   # must be on app, not router — router prefix is /auth
async def get_me(current_user:User=Depends(get_current_user)):
    return {
        "id":current_user.id,
        "name":current_user.name,
        "email":current_user.email
    }