import pytest

from api.domain import ConflictError, ForbiddenError, ValidationError
from api.domain.access import RolePolicy
from api.domain.user import UserDraft


def test_user_draft_requires_company():
    with pytest.raises(ValidationError):
        UserDraft.from_raw("user", "a@b.com", None, "employee")


def test_user_draft_validates_email():
    with pytest.raises(ValidationError):
        UserDraft.from_raw("user", "invalid", 1, "employee")


def test_role_policy_can_assign_superadmin():
    RolePolicy.can_assign(
        actor_role_name="superadmin",
        actor_rank=1,
        target_rank=1,
    )


def test_role_policy_denies_higher_role():
    with pytest.raises(ForbiddenError):
        RolePolicy.can_assign(
            actor_role_name="manager",
            actor_rank=3,
            target_rank=2,
        )


def test_role_policy_blocks_self_role_change():
    with pytest.raises(ForbiddenError):
        RolePolicy.enforce_self_role_change(
            actor_id=1,
            target_user_id=1,
            is_superadmin=False,
            current_role_id=2,
            new_role_id=3,
        )
