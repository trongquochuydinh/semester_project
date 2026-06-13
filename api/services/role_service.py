from typing import List, Optional

from sqlalchemy.orm import Session

from api.db.role_db import get_all_roles, get_role_by_name
from api.domain.access import RolePolicy
from api.domain.exceptions import ForbiddenError, NotFoundError
from api.models.role import Role
from api.models.user import User


def resolve_assignable_role(
    db: Session,
    *,
    role_name: str,
    current_user: User,
) -> Role:
    role_name = role_name.lower()
    role = get_role_by_name(db, role_name)
    if not role:
        raise NotFoundError("Role not found")

    RolePolicy.can_assign(
        actor_role_name=current_user.role.name,
        actor_rank=current_user.role.rank,
        target_rank=role.rank,
    )
    return role


def get_subroles_for_role(
    db: Session,
    role_name: str,
    excluded_roles: Optional[List[str]] = None,
) -> List[Role]:
    role_name = role_name.lower()
    excluded = {r.lower() for r in excluded_roles or []}

    current_role = get_role_by_name(db, role_name)
    if not current_role:
        raise ForbiddenError("Invalid role")

    all_roles = get_all_roles(db)
    return [
        role
        for role in all_roles
        if role.rank >= current_role.rank and role.name.lower() not in excluded
    ]
