import secrets
import string
from datetime import datetime
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from requests import Session
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash

from api.db.db_engine import SessionLocal, get_db
from api.models.user import User, UserRole, Role, verify_user
from api.utils.auth_utils import create_access_token, decode_access_token

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


def login_user(identifier: str, password: str):
    user = verify_user(identifier, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Update status + timestamp
    session = SessionLocal()
    try:
        db_user = session.query(User).filter(User.id == user.id).first()
        if db_user:
            db_user.status = "online"
            db_user.last_login = datetime.now()
            session.commit()
    finally:
        session.close()

    role_name = user.roles[0].role.name if user.roles and user.roles[0].role else None
    token = create_access_token(user.id, role_name)

    return {
        "access_token": token,
        "token_type": "bearer",
        "id": user.id,
        "username": user.username,
    }


def get_subroles_for_role(creator_role: str):
    session = SessionLocal()
    try:
        roles = session.query(Role).all()
        role_map = {
            "superadmin": {"admin"},
            "admin": {"manager", "employee"},
            "manager": {"employee"},
        }
        allowed = role_map.get(creator_role.lower(), set())
        return [r for r in roles if r.name.lower() in allowed]
    finally:
        session.close()


def create_user_account(data):
    session = SessionLocal()
    try:
        alphabet = string.ascii_letters + string.digits
        initial_password = "".join(secrets.choice(alphabet) for _ in range(10))
        password_hash = generate_password_hash(initial_password)

        user = User(
            username=data.username,
            email=data.email,
            company_id=data.company_id,
            password_hash=password_hash,
            status="offline",
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        role = session.query(Role).filter_by(id=data.role_id).first()
        if not role:
            raise HTTPException(status_code=400, detail="Role not found")

        session.add(UserRole(user_id=user.id, role_id=role.id))
        session.commit()
        return {"message": "User created successfully", "initial_password": initial_password}
    finally:
        session.close()


def logout_user(user_id: int):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        user.status = "offline"
        session.commit()
        return {"message": "User logged out successfully"}
    finally:
        session.close()
