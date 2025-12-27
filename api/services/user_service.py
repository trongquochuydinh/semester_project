from fastapi import HTTPException
from werkzeug.security import generate_password_hash
from typing import List

from api.db.user_db import (
    insert_user,
    get_id_by_role,
    paginate_users as db_paginate_users,
    count_users as db_count_users,
    get_user_data_by_id as db_get_user_data_by_id
)
from api.services.company_service import assert_company_access

from sqlalchemy.orm import Session
from api.models.user import User
from api.utils.auth_utils import generate_password
from api.schemas import UserWriter, UserCreateResponse, UserCountResponse, UserGetResponse, PaginationResponse

def create_user_account(data: UserWriter, db: Session, current_user: User) -> UserCreateResponse:

    # 1. Check for company existence and scope
    company = assert_company_access(
        db,
        is_superadmin=(current_user.role.name == "superadmin"),
        current_user_company_id=current_user.company_id,
        company_id=data.company_id,
    )

    # 2. Resolve role from DB FIRST
    role = get_id_by_role(db, data.role)
    if not role:
        raise HTTPException(status_code=400, detail="Role not found")

    # 3. Role permission check
    available_roles = get_subroles_for_role(
        current_user.role.name,
        excluded_roles=[current_user.role.name],
    )

    if role.name not in available_roles:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to assign this role",
        )

    # 4. Create user
    user_initial_password = generate_password()
    password_hash = generate_password_hash(user_initial_password)

    user = User(
        username=data.username,
        email=data.email,
        company_id=company.id,
        role_id=role.id,
        password_hash=password_hash,
        status="offline",
    )

    insert_user(db, user)

    return UserCreateResponse(
        message="User created successfully",
        initial_password=user_initial_password,
    )

def edit_user(data: UserWriter, db: Session, current_user: User):

    company = assert_company_access(
        db,
        is_superadmin=(current_user.role.name == "superadmin"),
        current_user_company_id=current_user.company_id,
        company_id=data.company_id,
    )
    return None

def disable_user(data: UserWarning, db: Session, current_user: User):
    return None

def get_info_of_user(user_id: int, db: Session, current_user: User) -> UserGetResponse:
    user = db_get_user_data_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    assert_company_access(
        db,
        is_superadmin=(current_user.role.name == "superadmin"),
        current_user_company_id=current_user.company_id,
        company_id=user.company_id,
    )

    return UserGetResponse(
        username=user.username,
        email=user.email,
        company_id=user.company_id,
        role=user.role.name,
    )

def get_subroles_for_role(role_name: str, excluded_roles: List[str]=None):
    role_map = {
        "superadmin": {"superadmin", "admin", "manager", "employee"},
        "admin": {"admin", "manager", "employee"},
        "manager": {"manager", "employee"},
        "employee": {"employee"}
    }

    allowed_roles = role_map.get(role_name.lower(), set())

    if excluded_roles:
        excluded = {r.lower() for r in excluded_roles}
        allowed_roles = allowed_roles - excluded
    return allowed_roles

# TODO: Make this more coherent 
def paginate_users(db: Session, limit: int, offset: int, filters: dict, user_role: str, company_id: int):
    if "status" in filters:
        allowed_roles = None
    else:
        allowed_roles = get_subroles_for_role(user_role, excluded_roles=[user_role])
    total, results = db_paginate_users(db, filters, allowed_roles, company_id, limit, offset)

    def serialize(u: User):
        d = {c.name: getattr(u, c.name) for c in u.__table__.columns}
        d.pop("password_hash", None)
        d["role_name"] = u.role.name if u.role else None
        d["company_name"] = u.company.name if u.company else None
        return d

    res = PaginationResponse(
        total=total,
        data=[serialize(r) for r in results]
    )

    return res

def get_user_count(db: Session, current_user: User) -> UserCountResponse:
    is_superadmin = current_user.role.name == "superadmin"
    company_id = None if is_superadmin else current_user.company_id

    total = db_count_users(db, company_id=company_id)
    online = db_count_users(db, company_id=company_id, online_only=True)

    return UserCountResponse(
        total_users=total,
        online_users=online,
    )
        
