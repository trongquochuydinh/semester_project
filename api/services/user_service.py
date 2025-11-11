import secrets
import string
from typing import Dict
from fastapi import Depends, HTTPException
from requests import Session
from sqlalchemy.orm import Session, joinedload
from werkzeug.security import generate_password_hash

from api.db.db_engine import SessionLocal, get_db
from api.models.user import User, UserRole, Role

def get_subroles_for_role(creator_role: str, db: Session = Depends(get_db)):
    try:
        roles = db.query(Role).all()
        role_map = {
            "superadmin": {"admin"},
            "admin": {"manager", "employee"},
            "manager": {"employee"},
        }
        allowed = role_map.get(creator_role.lower(), set())
        return [r for r in roles if r.name.lower() in allowed]
    finally:
        db.close()


def create_user_account(data, db: Session = Depends(get_db)):
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
        db.add(user)
        db.commit()
        db.refresh(user)

        role = db.query(Role).filter_by(id=data.role_id).first()
        if not role:
            raise HTTPException(status_code=400, detail="Role not found")

        db.add(UserRole(user_id=user.id, role_id=role.id))
        db.commit()
        return {"message": "User created successfully", "initial_password": initial_password}
    finally:
        db.close()

def get_user_by_username_or_email(identifier: str, db: Session):
    return (
        db.query(User)
        .options(joinedload(User.roles).joinedload(UserRole.role))
        .filter((User.username == identifier) | (User.email == identifier))
        .first()
    )

def verify_user(identifier: str, password: str, db: Session):
    user = get_user_by_username_or_email(identifier, db)
    if user and user.verify_password(password):
        return user
    return None

def create_user_account(data, db: Session):
    """
    Creates a new user account and assigns a role.
    A random initial password is generated automatically.
    """

    # Generate a secure random initial password
    alphabet = string.ascii_letters + string.digits
    initial_password = "".join(secrets.choice(alphabet) for _ in range(10))
    password_hash = generate_password_hash(initial_password)

    # Create new user
    user = User(
        username=data.username,
        email=data.email,
        company_id=data.company_id,
        password_hash=password_hash,
        status="offline",
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Validate and assign role
    role = db.query(Role).filter_by(id=data.role_id).first()
    if not role:
        raise HTTPException(status_code=400, detail="Role not found")

    db.add(UserRole(user_id=user.id, role_id=role.id))
    db.commit()

    return {
        "message": "User created successfully",
        "initial_password": initial_password,
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
    }

def paginate_users(
    db: Session,
    limit: int,
    offset: int,
    filters: Dict,
    user_role: str,
    company_id: int
):
    hierarchy = {
        "superadmin": ["admin"],
        "admin": ["manager", "employee"],
        "manager": ["employee"],
        "employee": []
    }
    allowed_roles = hierarchy.get(user_role, None)

    query = (
        db.query(User)
        .options(joinedload(User.roles).joinedload(UserRole.role), joinedload(User.company))
    )

    # Apply filters
    for key, value in filters.items():
        if hasattr(User, key):
            query = query.filter(getattr(User, key) == value)

    # Role-based filtering
    if allowed_roles:
        query = query.join(UserRole).join(Role).filter(Role.name.in_(allowed_roles))
    elif allowed_roles == []:
        query = query.filter(False)

    # Company restriction
    if company_id is not None:
        query = query.filter(User.company_id == company_id)

    total = query.count()
    results = query.offset(offset).limit(limit).all()

    def to_dict(obj):
        d = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
        d.pop("password_hash", None)
        d["role_name"] = obj.roles[0].role.name if obj.roles and obj.roles[0].role else None
        d["company_name"] = obj.company.name if hasattr(obj, "company") and obj.company else None
        return d

    return {"total": total, "data": [to_dict(r) for r in results]}

def get_user_count(db: Session, company_id: int = None, online_only: bool = False):
    """
    Returns a user count.
    If company_id is given, filters only that company.
    If online_only=True, filters only users with status='online'.
    """
    query = db.query(User)

    if company_id is not None:
        query = query.filter(User.company_id == company_id)

    if online_only:
        query = query.filter(User.status == "online")

    return query.count()