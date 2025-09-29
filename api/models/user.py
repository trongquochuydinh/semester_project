from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from api.db.db_engine import Base, SessionLocal
from werkzeug.security import check_password_hash, generate_password_hash
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from typing import Optional

router = APIRouter()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=True)
    # Use only the first role for single-role logic
    def get_role(self):
        return self.roles[0] if self.roles else None
    roles = relationship('UserRole', back_populates='user')
    company = relationship('Company', backref='users')
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    users = relationship('UserRole', back_populates='role')

class UserRole(Base):
    __tablename__ = 'user_roles'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', back_populates='roles')
    role = relationship('Role', back_populates='users')

def get_user_by_username_or_email(identifier):
    session = SessionLocal()
    try:
        return session.query(User).options(
            joinedload(User.roles).joinedload(UserRole.role)
        ).filter((User.username == identifier) | (User.email == identifier)).first()
    finally:
        session.close()

def verify_user(identifier, password):
    user = get_user_by_username_or_email(identifier)
    if user and user.verify_password(password):
        return user
    return None

def paginate_users(db, limit, offset, filters):
    # Role hierarchy
    hierarchy = {
        'superadmin': ['admin'],
        'admin': ['manager', 'employee'],
        'manager': ['employee'],
        'employee': []
    }
    requesting_role = filters.pop('user_role', None)
    company_id = filters.pop('company_id', None)
    allowed_roles = hierarchy.get(requesting_role, None)
    query = db.query(User).options(
        joinedload(User.roles).joinedload(UserRole.role),
        joinedload(User.company)
    )
    for key, value in filters.items():
        if hasattr(User, key):
            query = query.filter(getattr(User, key) == value)
    # Apply role-based filtering
    if allowed_roles is not None and allowed_roles:
        query = query.join(UserRole).join(Role).filter(Role.name.in_(allowed_roles))
    elif allowed_roles == []:
        query = query.filter(False)
    # Apply company filtering if company_id is set
    if company_id is not None:
        query = query.filter(User.company_id == company_id)
    total = query.count()
    results = query.offset(offset).limit(limit).all()
    def to_dict(obj):
        d = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
        d.pop("password_hash", None)
        # Get role name (assume one role per user)
        if obj.roles:
            user_role = obj.roles[0]
            d["role_name"] = user_role.role.name if user_role.role else None
        else:
            d["role_name"] = None
        # Get company name
        d["company_name"] = obj.company.name if hasattr(obj, "company") and obj.company else None
        return d
    data = [to_dict(r) for r in results]
    return {"total": total, "data": data}

class LoginRequest(BaseModel):
    identifier: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    company_id: Optional[int] = None
    role: str

@router.post("/login", response_model=UserResponse)
def login(data: LoginRequest):
    user = verify_user(data.identifier, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Get the single role name (assume one role per user)
    role = user.roles[0].role.name if user.roles and user.roles[0].role else None
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        company_id=user.company_id,
        role=role
    )
