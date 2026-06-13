from typing import List

from api.domain.exceptions import ForbiddenError


class TenantScope:
    @staticmethod
    def enforce(
        *,
        is_superadmin: bool,
        current_user_company_id: int,
        target_company_id: int,
    ) -> None:
        if is_superadmin:
            return

        if current_user_company_id != target_company_id:
            raise ForbiddenError("Operation not allowed outside your company")


class RolePolicy:
    @staticmethod
    def require(actor_role: str, allowed_roles: List[str]) -> None:
        if actor_role not in allowed_roles:
            raise ForbiddenError("Access forbidden")

    @staticmethod
    def can_assign(
        *,
        actor_role_name: str,
        actor_rank: int,
        target_rank: int,
    ) -> None:
        if actor_role_name.lower() == "superadmin":
            return
        if target_rank <= actor_rank:
            raise ForbiddenError("You are not allowed to assign this role")

    @staticmethod
    def enforce_self_role_change(
        *,
        actor_id: int,
        target_user_id: int,
        is_superadmin: bool,
        current_role_id: int,
        new_role_id: int,
    ) -> None:
        if (
            target_user_id == actor_id
            and not is_superadmin
            and new_role_id != current_role_id
        ):
            raise ForbiddenError("You cannot change your own role")
