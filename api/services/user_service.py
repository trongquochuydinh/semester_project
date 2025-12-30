from fastapi import HTTPException
from werkzeug.security import generate_password_hash
from email.utils import parseaddr

from api.db.user_db import (
    insert_user,
    paginate_users as db_paginate_users,
    count_users as db_count_users,
    get_user_data_by_id as db_get_user_data_by_id,
    edit_user as db_edit_user,
    change_user_is_active as db_change_user_is_active,
    user_exists_by_username_or_email as db_user_exists_by_username_or_email
)

from api.services.company_service import assert_company_access
from api.services.role_service import resolve_assignable_role, get_subroles_for_role

from sqlalchemy.orm import Session
from api.models.user import User
from api.utils import generate_password, validate_user_data
from api.schemas import UserWriter, UserCreateResponse, UserCreateRequest, UserCountResponse, UserGetResponse, UserEditResponse, PaginationResponse, MessageResponse, UserEditRequest

def create_user_account(data: UserCreateRequest, db: Session, current_user: User) -> UserCreateResponse:

    validate_user_data(data)

    username = data.username.strip()
    email = data.email.strip().lower()

    if db_user_exists_by_username_or_email(
        db,
        username=username,
        email=email,
    ):
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists",
        )

    company = assert_company_access(
        db,
        is_superadmin=(current_user.role.name == "superadmin"),
        current_user_company_id=current_user.company_id,
        company_id=data.company_id,
    )

    # --------------------
    # Role resolution
    # --------------------
    role = resolve_assignable_role(
        db=db,
        role_name=data.role,
        current_user=current_user,
    )

    # --------------------
    # Create user
    # --------------------
    user_initial_password = generate_password()
    password_hash = generate_password_hash(user_initial_password)

    user = User(
        username=username,
        email=email,
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

def edit_user(
    user_id: int,
    data: UserEditRequest,
    db: Session,
    current_user: User,
):
    
    validate_user_data(data)

    username = data.username.strip()
    email = data.email.strip().lower()

    if db_user_exists_by_username_or_email(
        db,
        username=username,
        email=email,
        exclude_user_id=user_id,
    ):
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists",
        )

    user = db_get_user_data_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    is_superadmin = current_user.role.name == "superadmin"

    assert_company_access(
        db,
        is_superadmin=is_superadmin,
        current_user_company_id=current_user.company_id,
        company_id=user.company_id,
    )

    role = resolve_assignable_role(
        db=db,
        role_name=data.role,
        current_user=current_user,
    )

    if user.id == current_user.id and not is_superadmin:
        if role.id != user.role_id:
            raise HTTPException(
                status_code=403,
                detail="You cannot change your own role",
            )

    updates = {
        "username": username,
        "email": email,
    }

    if is_superadmin:
        updates["company_id"] = data.company_id


    updated_user = db_edit_user(
        db=db,
        user_id=user.id,
        updates=updates,
        role_id=role.id,
    )

    return UserEditResponse(
        username=updated_user.username,
        email=updated_user.email,
        company_id=updated_user.company_id,
        role=updated_user.role.name,
    )

def toggle_user_is_active(user_id: int, db: Session, current_user: User) -> MessageResponse:
    user = db_get_user_data_by_id(db, user_id)

    assert_company_access(
        db,
        is_superadmin=(current_user.role.name == "superadmin"),
        current_user_company_id=current_user.company_id,
        company_id=user.company_id,
    )

    role = resolve_assignable_role(
        db=db,
        role_name=user.role.name,
        current_user=current_user,
    )

    is_active = not user.is_active

    db_change_user_is_active(user, is_active)

    return MessageResponse(
        message=f"User was successfully {'enabled' if is_active else 'disabled'}."
    )

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

def paginate_users(
    db: Session,
    limit: int,
    offset: int,
    filters: dict,
    user_role: str,
    company_id: int,
):
    if "status" in filters:
        allowed_roles = None
    else:
        roles = get_subroles_for_role(
            db,
            user_role,
            excluded_roles=[user_role],
        )
        allowed_roles = {role.name for role in roles}

    total, results = db_paginate_users(
        db,
        filters,
        allowed_roles,
        company_id,
        limit,
        offset,
    )

    def serialize(u: User):
        d = {c.name: getattr(u, c.name) for c in u.__table__.columns}
        d.pop("password_hash", None)
        d["role_name"] = u.role.name if u.role else None
        d["company_name"] = u.company.name if u.company else None
        return d

    return PaginationResponse(
        total=total,
        data=[serialize(r) for r in results],
    )

def get_user_count(db: Session, current_user: User) -> UserCountResponse:
    is_superadmin = current_user.role.name == "superadmin"
    company_id = None if is_superadmin else current_user.company_id

    total = db_count_users(db, company_id=company_id)
    online = db_count_users(db, company_id=company_id, online_only=True)

    return UserCountResponse(
        total_users=total,
        online_users=online,
    )
        
