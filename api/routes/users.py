from fastapi import APIRouter, HTTPException, Query, Depends, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from typing import List, Optional
from api.models.user import verify_user, User, UserRole, Role
from api.db.db_engine import SessionLocal
from werkzeug.security import generate_password_hash
import secrets
import string
from datetime import datetime, timedelta
import jwt
import os

router = APIRouter(prefix="/api/users", tags=["users"])

# ============================================================
# CONFIG
# ============================================================
JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret-key")
JWT_ALGORITHM = "HS256"
security = HTTPBearer()

# ============================================================
# SCHEMAS
# ============================================================
class LoginRequest(BaseModel):
    identifier: str  # username or email
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    email: str
    company_id: Optional[int] = None
    role_id: int

class RoleOut(BaseModel):
    id: int
    name: str

class RolesResponse(BaseModel):
    roles: List[RoleOut]

class LogoutRequest(BaseModel):
    user_id: int

# ============================================================
# HELPERS
# ============================================================
def create_access_token(user_id: int, role: str, expires_in: int = 3600):
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(token=Depends(security)):
    payload = decode_access_token(token.credentials)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# ============================================================
# ROUTES
# ============================================================

@router.post("/login", response_model=UserResponse)
def login(data: LoginRequest):
    user = verify_user(data.identifier, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Update user status and timestamp
    session = SessionLocal()
    try:
        db_user = session.query(User).filter(User.id == user.id).first()
        if db_user:
            db_user.status = 'online'
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
        "username": user.username
    }

@router.get("/get_subroles", response_model=RolesResponse)
def get_roles(creator_role: str = Query(...)):
    session = SessionLocal()
    try:
        roles = session.query(Role).all()

        if creator_role == "superadmin":
            allowed = {"admin"}
        elif creator_role == "admin":
            allowed = {"manager", "employee"}
        elif creator_role == "manager":
            allowed = {"employee"}
        else:
            allowed = set()

        role_objs = [
            RoleOut(id=role.id, name=role.name)
            for role in roles if role.name.lower() in allowed
        ]
        return RolesResponse(roles=role_objs)
    finally:
        session.close()

@router.post("/create")
def create_user_endpoint(data: UserCreate):
    session = SessionLocal()
    try:
        alphabet = string.ascii_letters + string.digits
        initial_password = ''.join(secrets.choice(alphabet) for _ in range(10))
        password_hash = generate_password_hash(initial_password)

        user = User(
            username=data.username,
            email=data.email,
            company_id=data.company_id,
            password_hash=password_hash,
            status='offline'
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        role = session.query(Role).filter_by(id=data.role_id).first()
        if not role:
            raise HTTPException(status_code=400, detail="Role not found")
        user_role = UserRole(user_id=user.id, role_id=role.id)
        session.add(user_role)
        session.commit()

        return {"message": "User created successfully", "initial_password": initial_password}
    finally:
        session.close()

@router.post("/logout")
def logout(data: LogoutRequest):
    session = SessionLocal()
    try:
        user = session.query(User).filter(User.id == data.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.status = 'offline'
        session.commit()

        return {"message": "User logged out successfully"}
    finally:
        session.close()

# ============================================================
# PROTECTED ROUTE EXAMPLE
# ============================================================
@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    """Return info for authenticated user"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.roles[0].role.name if current_user.roles else None
    }

@router.get("/get_my_role")
def get_my_role(current_user=Depends(get_current_user)):
    """Return role for authenticated user"""
    return {
        "role": current_user.roles[0].role.name if current_user.roles else None
    }