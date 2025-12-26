from typing import List
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session, joinedload

from api.db.db_engine import get_db
from api.models.user import User
from api.utils.auth_utils import decode_access_token
from api.db.user_db import get_user_data_by_id

security = HTTPBearer()

def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    payload = decode_access_token(token.credentials)

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = get_user_data_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def require_role(required_roles: List[str]):
    def role_checker(current_user: User = Depends(get_current_user)):
        role_name = current_user.role.name

        if role_name not in required_roles:
            raise HTTPException(status_code=403, detail="Access forbidden")

        return current_user

    return role_checker