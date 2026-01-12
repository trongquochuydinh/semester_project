# Import FastAPI and type utilities
from fastapi import HTTPException
from typing import List, Optional

# Import database operations for role management
from api.db.role_db import (
    get_role_by_id,
    get_all_roles,
    get_role_by_name
)

# Import models
from sqlalchemy.orm import Session
from api.models.user import User
from api.models.role import Role


def resolve_assignable_role(
    db: Session,
    *,
    role_name: str,
    current_user: User,
) -> Role:
    """Validate and return role that current user can assign."""
    role_name = role_name.lower()
    current_role = current_user.role.name.lower()

    # Find requested role
    role = get_role_by_name(db, role_name)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Superadmins can assign any role
    if current_role != "superadmin":
        # Regular users cannot assign same or higher privilege roles
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
    """Get roles with lower privileges than specified role."""
    role_name = role_name.lower()
    excluded = {r.lower() for r in excluded_roles or []}

    # Find current role for rank comparison
    current_role = get_role_by_name(db, role_name)
    if not current_role:
        raise HTTPException(status_code=403, detail="Invalid role")

    all_roles = get_all_roles(db)

    # Return roles with higher or equal rank (lower privilege)
    return [
        role
        for role in all_roles
        if role.rank >= current_role.rank
        and role.name.lower() not in excluded
    ]
