from fastapi import HTTPException
from werkzeug.security import generate_password_hash

from api.db.user_db import (
    insert_user,
    get_role_by_id,
    assign_role,
    get_user_by_identifier as db_get_user,
    paginate_users as db_paginate_users,
    count_users as db_count_users,
    get_user_data_by_id as db_get_user_data_by_id
)
from api.models.user import User
from api.utils.auth_utils import generate_password

def create_user_account(data, db):
    initial_password = generate_password()
    password_hash = generate_password_hash(initial_password)

    user = User(
        username=data.username,
        email=data.email,
        company_id=data.company_id,
        password_hash=password_hash,
        status="offline",
    )

    user = insert_user(db, user)

    role = get_role_by_id(db, data.role_id)
    if not role:
        raise HTTPException(400, "Role not found")

    assign_role(db, user.id, role.id)

    return {
        "message": "User created successfully",
        "initial_password": initial_password,
        "user_id": user.id,
        "username": user.username,
        "email": user.email,
    }

def verify_user(identifier: str, password: str, db):
    user = db_get_user(db, identifier)
    if user and user.verify_password(password):
        return user
    return None

def get_info_of_user(user_id: int, db):
    user = db_get_user_data_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    
    # Transform the user object to include the IDs needed for form population
    user_dict = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "company_id": user.company_id,
        
        # Extract role_id from the relationship
        "role": get_role_by_id(db, user.roles[0].role_id).name if user.roles else None,
    }
    
    return user_dict

def get_subroles_for_role(role_name: str):
    role_map = {
        "superadmin": {"admin"},
        "admin": {"manager", "employee"},
        "manager": {"employee"},
    }
    return role_map.get(role_name.lower(), set())


def paginate_users(db, limit, offset, filters, user_role, company_id):
    allowed_roles = get_subroles_for_role(user_role)
    total, results = db_paginate_users(db, filters, allowed_roles, company_id, limit, offset)

    def serialize(u: User):
        d = {c.name: getattr(u, c.name) for c in u.__table__.columns}
        d.pop("password_hash", None)
        d["role_name"] = u.roles[0].role.name if u.roles else None
        d["company_name"] = u.company.name if u.company else None
        return d

    return {"total": total, "data": [serialize(r) for r in results]}


def get_user_count(db, company_id=None, online_only=False):
    return db_count_users(db, company_id, online_only)
