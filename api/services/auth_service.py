from datetime import datetime
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session, joinedload
from api.db.db_engine import get_db
from api.models.user import User, UserRole
from api.services import verify_user
from api.utils import create_access_token, decode_access_token
from typing import List

security = HTTPBearer()

def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    payload = decode_access_token(token.credentials)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = (
        db.query(User)
        .options(joinedload(User.roles).joinedload(UserRole.role))
        .filter(User.id == user_id)
        .first()
    )
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def require_role(required_roles: List[str]):
    def role_checker(current_user: User = Depends(get_current_user)):
        role_name = (
            current_user.roles[0].role.name
            if current_user.roles and current_user.roles[0].role
            else None
        )

        if role_name not in required_roles:
            raise HTTPException(status_code=403, detail="Access forbidden")

        return current_user  # important: pass user downstream

    return role_checker

def login_user(identifier: str, password: str, db: Session = Depends(get_db)):

    user = verify_user(identifier, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    db_user = db.query(User).filter(User.id == user.id).first()
    if db_user:
        db_user.status = "online"
        db_user.last_login = datetime.now()
        db.commit()

    role_name = user.roles[0].role.name if user.roles and user.roles[0].role else None
    token = create_access_token(user.id, role_name)
    return {
        "access_token": token,
        "token_type": "bearer",
        "id": user.id,
        "username": user.username,
        "role": role_name,
        "company_id": user.company_id
    }

def logout_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.status = "offline"
    db.commit()
    return {"message": "User logged out successfully"}
