from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from api.models.user import verify_user, User, UserRole, Role
from api.db.db_engine import SessionLocal
from werkzeug.security import generate_password_hash
import secrets
import string

router = APIRouter(prefix="/api/users", tags=["users"])

class LoginRequest(BaseModel):
    identifier: str  # username or email
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    company_id: Optional[int] = None
    role: str

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

@router.post("/login", response_model=UserResponse)
def login(data: LoginRequest):
    user = verify_user(data.identifier, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Get the single role name (assume one role per user)
    role_name = user.roles[0].role.name if user.roles and user.roles[0].role else None
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        company_id=user.company_id,
        role=role_name
    )

@router.get("/roles", response_model=RolesResponse)
def get_roles(creator_role: str = Query(...)):
    session = SessionLocal()
    try:
        roles = session.query(Role).all()

        # Filter depending on who is creating
        if creator_role == "superadmin":
            allowed = {"admin"}
        elif creator_role == "admin":
            allowed = {"manager", "employee"}
        else:
            allowed = set()  # no creation rights

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
        # Generate random initial password
        alphabet = string.ascii_letters + string.digits
        initial_password = ''.join(secrets.choice(alphabet) for _ in range(10))
        password_hash = generate_password_hash(initial_password)
        # Create the user
        user = User(
            username=data.username,
            email=data.email,
            company_id=data.company_id,
            password_hash=password_hash
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        # Assign role
        role = session.query(Role).filter_by(id=data.role_id).first()
        if not role:
            raise HTTPException(status_code=400, detail="Role not found")
        user_role = UserRole(user_id=user.id, role_id=role.id)
        session.add(user_role)
        session.commit()

        return {"message": "User created successfully", "initial_password": initial_password}
    finally:
        session.close()