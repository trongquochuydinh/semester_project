import secrets
import string
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError as JWTInvalidTokenError
from datetime import datetime, timedelta, timezone
from werkzeug.security import check_password_hash

from api.config import JWT_SECRET
from api.utils.exception_utils import TokenExpiredError, InvalidTokenError
JWT_ALGORITHM = "HS256"

def create_access_token(user_id: int, role: str, session_id, expires_in: int = 3600) -> str:
    payload = {
        "sub": user_id,
        "role": role,
        "session_id": session_id,
        "exp": datetime.now(timezone.utc) + timedelta(seconds=expires_in),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            options={"verify_exp": True},
            leeway=0,
        )
    except ExpiredSignatureError:
        raise TokenExpiredError()
    except JWTInvalidTokenError:
        raise InvalidTokenError()

def decode_token_ignore_exp(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
            options={"verify_exp": False},
        )
    except JWTInvalidTokenError:
        return None

def generate_password(length=10):
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))

def verify_password(password: str, password_hash: str) -> bool:
    return check_password_hash(password_hash, password)
