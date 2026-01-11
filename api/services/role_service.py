from fastapi import HTTPException
from typing import List, Optional

from api.db.role_db import (
    get_role_by_id,
    get_all_roles,
    get_role_by_name
)

from sqlalchemy.orm import Session
from api.models.user import User
from api.models.role import Role


def resolve_assignable_role(
    db: Session,
    *,
    role_name: str,
    current_user: User,
) -> Role:
    role_name = role_name.lower()
    current_role = current_user.role.name.lower()

    role = get_role_by_name(db, role_name)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if current_role != "superadmin":
        # cannot assign same or higher privilege role
        if role.rank <= current_user.role.rank:
            raise HTTPException(
                status_code=403,
                detail="You are not allowed to assign this role",
            )

    return role

def get_subroles_for_role(
    db: Session,
    role_name: str,
    excluded_roles: Optional[List[str]]
) -> List[Role]:
    role_name = role_name.lower()
    excluded = {r.lower() for r in excluded_roles or []}

    current_role = get_role_by_name(db, role_name)
    if not current_role:
        raise HTTPException(status_code=403, detail="Invalid role")

    all_roles = get_all_roles(db)

    return [
        role
        for role in all_roles
        if role.rank >= current_role.rank
        and role.name.lower() not in excluded
    ]
