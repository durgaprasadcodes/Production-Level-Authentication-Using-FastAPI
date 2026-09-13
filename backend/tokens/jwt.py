from jose import jwt ,JWTError
from config import ACCESS_TOKEN_EXPIRY_TIME,REFRESH_TOKEN_EXPIRY_TIME,ALGORITHM,SECRET_KEY,hash_refresh_token
from datetime import datetime,timedelta,timezone
from uuid import uuid4
import hashlib
import secrets

def create_access_token(user_id,user_email):
    payload = {
        'sub':str(user_id),
        'email':str(user_email),
        "type":"access",
        'exp':datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRY_TIME)
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)

def create_refresh_token():
    token = secrets.token_urlsafe(64)
    token_hash = hash_refresh_token(token)
    return token, token_hash

def decode_access_token(token):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        if not payload.get("sub"):
            raise ValueError("Invalid Access Token")
        if payload.get("type") != "access":
            raise ValueError("Invalid Token Given")
        return payload
    except JWTError:
        raise  ValueError("Invalid Access Token")