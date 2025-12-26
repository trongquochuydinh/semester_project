import os
import secrets
import string
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from werkzeug.security import check_password_hash

from api.config import JWT_SECRET
JWT_ALGORITHM = "HS256"

def create_access_token(user_id: int, role: str, session_id, expires_in: int = 3600) -> str:
    payload = {
        "sub": user_id,
        "role": role,
        "session_ud": session_id,
        "exp": datetime.utcnow() + timedelta(seconds=expires_in),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def generate_password(length=10):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

def verify_password(password: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, password)
