from typing import List
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from api.db.db_engine import get_db
from api.models.user import User
from api.utils import decode_access_token, decode_token_ignore_exp, InvalidTokenError, TokenExpiredError
from api.db.user_db import get_user_data_by_id, clear_login_session_by_user_id

security = HTTPBearer()

def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:

    try:
        payload = decode_access_token(token.credentials)

    except TokenExpiredError:
        stale_payload = decode_token_ignore_exp(token.credentials)

        if stale_payload:
            user_id = stale_payload.get("sub")
            if user_id:
                clear_login_session_by_user_id(db, user_id)

        raise HTTPException(
            status_code=401,
            detail="Session expired. Please log in again."
        )

    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401)

    user = get_user_data_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401)

    return user

def require_role(required_roles: List[str]):
    def role_checker(current_user: User = Depends(get_current_user)):
        role_name = current_user.role.name

        if role_name not in required_roles:
            raise HTTPException(status_code=403, detail="Access forbidden")

        return current_user

    return role_checker