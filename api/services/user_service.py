from fastapi import HTTPException
from werkzeug.security import generate_password_hash
from typing import Dict, Any

from api.db.user_db import (
    insert_user,
    paginate_users as db_paginate_users,
    count_users as db_count_users,
    get_user_data_by_id as db_get_user_data_by_id,
    edit_user as db_edit_user,
    change_user_is_active as db_change_user_is_active,
    user_exists_by_username_or_email as db_user_exists_by_username_or_email,
    get_oauth_providers as db_get_oauth_providers
)

from api.schemas.user_schema import LoginResponse, OAuthInfo
from api.services.company_service import assert_company_access
from api.services.role_service import resolve_assignable_role, get_subroles_for_role

from sqlalchemy.orm import Session
from api.models.user import User
from api.utils import generate_password, validate_user_data
from api.schemas import UserCreateResponse, UserCreateRequest, UserCountResponse, UserGetResponse, UserEditResponse, PaginationResponse, MessageResponse, UserEditRequest

def create_user_account(data: UserCreateRequest, db: Session, current_user: User) -> UserCreateResponse:
    """Create new user with validation and authorization checks."""
    # Validate input data format and constraints
    validate_user_data(data)

    # Normalize user input
    username = data.username.strip()
    email = data.email.strip().lower()

    # Check for duplicate username/email
    if db_user_exists_by_username_or_email(
        db,
        username=username,
        email=email,
        exclude_user_id=None
    ):
        raise HTTPException(
            status_code=409,
            detail="Username or email already exists",
        )

    # Validate company access for multi-tenant security
    company = assert_company_access(
        db,
        is_superadmin=(current_user.role.name == "superadmin"),
        current_user_company_id=current_user.company_id,
        company_id=data.company_id,
    )

    # Validate role assignment permissions
    role = resolve_assignable_role(
        db=db,
        role_name=data.role,
        current_user=current_user,
    )

    # Create user with generated password
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
    """Update existing user with authorization and validation."""
    # Validate input data
    validate_user_data(data)

    username = data.username.strip()
    email = data.email.strip().lower()

    # Check for conflicts excluding current user
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

    # Get user to edit
    user = db_get_user_data_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")

    is_superadmin = current_user.role.name == "superadmin"

    # Validate company access
    assert_company_access(
        db,
        is_superadmin=is_superadmin,
        current_user_company_id=current_user.company_id,
        company_id=data.company_id,
    )

    # Validate role assignment
    role = resolve_assignable_role(
        db=db,
        role_name=data.role,
        current_user=current_user,
    )

    # Prevent self role changes (unless superadmin)
    if user.id == current_user.id and not is_superadmin:
        if role.id != user.role_id:
            raise HTTPException(
                status_code=403,
                detail="You cannot change your own role",
            )

    # Build update data
    updates: Dict[str, Any] = {
        "username": username,
        "email": email,
    }

    # Superadmins can change company
    if is_superadmin:
        updates["company_id"] = data.company_id

    updated_user = db_edit_user(
        db=db,
        user=user,
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
    """Enable/disable user account with authorization checks."""
    user = db_get_user_data_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    
    # Validate company access
    assert_company_access(
        db,
        is_superadmin=(current_user.role.name == "superadmin"),
        current_user_company_id=current_user.company_id,
        company_id=user.company_id,
    )

    # Validate role permissions
    role = resolve_assignable_role(
        db=db,
        role_name=user.role.name,
        current_user=current_user,
    )

    is_active = not user.is_active
    db_change_user_is_active(db, user, is_active)

    return MessageResponse(
        message=f"User was successfully {'enabled' if is_active else 'disabled'}."
    )

def get_current_user_info(db: Session, current_user: User):
    """Get current user profile with OAuth provider info."""
    user = db_get_user_data_by_id(db, current_user.id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Get linked OAuth providers
    providers = db_get_oauth_providers(db, current_user.id)

    return {
        "id": user.id,
        "username": user.username,
        "role": user.role.name,
        "company_id": user.company_id,
        "oauth_info": OAuthInfo(
            github="github" in providers
        ),
    }

def get_info_of_user(user_id: int, db: Session, current_user: User) -> UserGetResponse:
    """Get user details with authorization checks."""
    user = db_get_user_data_by_id(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Validate company access
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
    """Get paginated user list with role-based filtering."""
    # Apply role-based access control
    if "status" in filters:
        allowed_roles = None  # Show all roles for status filtering
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
        """Convert user to dict with role and company info."""
        d = {c.name: getattr(u, c.name) for c in u.__table__.columns}
        d.pop("password_hash", None)  # Never expose password hash
        d["role_name"] = u.role.name if u.role else None
        d["company_name"] = u.company.name if u.company else None
        return d

    return PaginationResponse(
        total=total,
        data=[serialize(r) for r in results],
    )

def get_user_count(db: Session, current_user: User) -> UserCountResponse:
    """Get user statistics scoped by permissions."""
    is_superadmin = current_user.role.name == "superadmin"
    company_id = None if is_superadmin else current_user.company_id

    total = db_count_users(db, company_id=company_id)
    online = db_count_users(db, company_id=company_id, online_only=True)

    return UserCountResponse(
        total_users=total,
        online_users=online,
    )

