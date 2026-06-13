from typing import Any, Dict, Optional

from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from api.db.user_db import (
    change_user_is_active as db_change_user_is_active,
    count_users as db_count_users,
    edit_user as db_edit_user,
    get_oauth_providers as db_get_oauth_providers,
    get_user_data_by_id as db_get_user_data_by_id,
    insert_user,
    paginate_users as db_paginate_users,
    user_exists_by_username_or_email as db_user_exists_by_username_or_email,
)
from api.domain import ConflictError, MessageResult, NotFoundError
from api.domain.access import RolePolicy
from api.domain.mappers.user_mapper import (
    create_user_result_to_response,
    current_user_profile_to_dict,
    user_profile_to_edit_response,
    user_profile_to_get_response,
    user_stats_to_response,
)
from api.domain.user import (
    CreateUserResult,
    CurrentUserProfile,
    PaginatedUsers,
    UserDraft,
    UserProfile,
    UserStats,
)
from api.models.user import User
from api.services.company_service import assert_company_access
from api.services.role_service import get_subroles_for_role, resolve_assignable_role
from api.utils import generate_password


def _is_superadmin(user: User) -> bool:
    return user.role.name == "superadmin"


def create_user_account(
    db: Session,
    current_user: User,
    username: str,
    email: str,
    role: str,
    company_id: int,
):
    RolePolicy.require(
        current_user.role.name,
        ["superadmin", "admin", "manager"],
    )

    draft = UserDraft.from_raw(username, email, company_id, role)

    if db_user_exists_by_username_or_email(
        db,
        username=draft.username.value,
        email=draft.email.value,
        exclude_user_id=None,
    ):
        raise ConflictError("Username or email already exists")

    company = assert_company_access(
        db,
        is_superadmin=_is_superadmin(current_user),
        current_user_company_id=current_user.company_id,
        company_id=draft.company_id,
    )

    role_entity = resolve_assignable_role(
        db=db,
        role_name=draft.role_name,
        current_user=current_user,
    )

    initial_password = generate_password()
    user = User(
        username=draft.username.value,
        email=draft.email.value,
        company_id=company.id,
        role_id=role_entity.id,
        password_hash=generate_password_hash(initial_password),
        status="offline",
    )
    insert_user(db, user)

    result = CreateUserResult(
        message="User created successfully",
        initial_password=initial_password,
    )
    return create_user_result_to_response(result)


def edit_user(
    db: Session,
    current_user: User,
    user_id: int,
    username: str,
    email: str,
    role: str,
    company_id: int,
):
    RolePolicy.require(
        current_user.role.name,
        ["superadmin", "admin", "manager"],
    )

    draft = UserDraft.from_raw(username, email, company_id, role)

    if db_user_exists_by_username_or_email(
        db,
        username=draft.username.value,
        email=draft.email.value,
        exclude_user_id=user_id,
    ):
        raise ConflictError("Username or email already exists")

    user = db_get_user_data_by_id(db, user_id)
    if not user:
        raise NotFoundError("User not found")

    is_superadmin = _is_superadmin(current_user)

    assert_company_access(
        db,
        is_superadmin=is_superadmin,
        current_user_company_id=current_user.company_id,
        company_id=draft.company_id,
    )

    role_entity = resolve_assignable_role(
        db=db,
        role_name=draft.role_name,
        current_user=current_user,
    )

    RolePolicy.enforce_self_role_change(
        actor_id=current_user.id,
        target_user_id=user.id,
        is_superadmin=is_superadmin,
        current_role_id=user.role_id,
        new_role_id=role_entity.id,
    )

    updates: Dict[str, Any] = {
        "username": draft.username.value,
        "email": draft.email.value,
    }
    if is_superadmin:
        updates["company_id"] = draft.company_id

    updated_user = db_edit_user(
        db=db,
        user=user,
        updates=updates,
        role_id=role_entity.id,
    )

    profile = UserProfile(
        username=updated_user.username,
        email=updated_user.email,
        company_id=updated_user.company_id,
        role=updated_user.role.name,
    )
    return user_profile_to_edit_response(profile)


def toggle_user_is_active(
    db: Session,
    current_user: User,
    user_id: int,
) -> MessageResult:
    RolePolicy.require(
        current_user.role.name,
        ["superadmin", "admin", "manager"],
    )

    user = db_get_user_data_by_id(db, user_id)
    if not user:
        raise NotFoundError("User not found")

    assert_company_access(
        db,
        is_superadmin=_is_superadmin(current_user),
        current_user_company_id=current_user.company_id,
        company_id=user.company_id,
    )

    resolve_assignable_role(
        db=db,
        role_name=user.role.name,
        current_user=current_user,
    )

    is_active = not user.is_active
    db_change_user_is_active(db, user, is_active)

    return MessageResult(
        message=f"User was successfully {'enabled' if is_active else 'disabled'}."
    )


def get_current_user_info(db: Session, current_user: User):
    user = db_get_user_data_by_id(db, current_user.id)
    if user is None:
        raise NotFoundError("User not found")

    providers = db_get_oauth_providers(db, current_user.id)
    profile = CurrentUserProfile(
        id=user.id,
        username=user.username,
        role=user.role.name,
        company_id=user.company_id,
        oauth_github="github" in providers,
    )
    return current_user_profile_to_dict(profile)


def get_info_of_user(db: Session, current_user: User, user_id: int):
    RolePolicy.require(
        current_user.role.name,
        ["superadmin", "admin", "manager"],
    )

    user = db_get_user_data_by_id(db, user_id)
    if not user:
        raise NotFoundError("User not found")

    assert_company_access(
        db,
        is_superadmin=_is_superadmin(current_user),
        current_user_company_id=current_user.company_id,
        company_id=user.company_id,
    )

    profile = UserProfile(
        username=user.username,
        email=user.email,
        company_id=user.company_id,
        role=user.role.name,
    )
    return user_profile_to_get_response(profile)


def paginate_users(
    db: Session,
    current_user: User,
    limit: int,
    offset: int,
    filters: dict,
) -> PaginatedUsers:
    if "status" in filters:
        allowed_roles = None
    else:
        roles = get_subroles_for_role(
            db,
            current_user.role.name,
            excluded_roles=[current_user.role.name],
        )
        allowed_roles = {role.name for role in roles}

    total, results = db_paginate_users(
        db,
        filters,
        allowed_roles,
        current_user.company_id,
        limit,
        offset,
    )

    data = []
    for user in results:
        row = {c.name: getattr(user, c.name) for c in user.__table__.columns}
        row.pop("password_hash", None)
        row["role_name"] = user.role.name if user.role else None
        row["company_name"] = user.company.name if user.company else None
        data.append(row)

    return PaginatedUsers(total=total, data=data)


def get_user_count(db: Session, current_user: User):
    is_superadmin = _is_superadmin(current_user)
    company_id = None if is_superadmin else current_user.company_id

    stats = UserStats(
        total_users=db_count_users(db, company_id=company_id),
        online_users=db_count_users(db, company_id=company_id, online_only=True),
    )
    return user_stats_to_response(stats)
