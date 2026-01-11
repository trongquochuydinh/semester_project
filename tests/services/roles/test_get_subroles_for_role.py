import pytest
from fastapi import HTTPException

from api.services.role_service import get_subroles_for_role

def test_get_subroles_for_admin(db, role_admin, role_manager, role_employee):
    roles = get_subroles_for_role(db, "admin", None)

    names = {r.name for r in roles}

    assert names == {"admin", "manager", "employee"}

def test_get_subroles_for_manager(db, role_manager, role_employee):
    roles = get_subroles_for_role(db, "manager", None)

    names = {r.name for r in roles}

    assert names == {"manager", "employee"}

def test_get_subroles_excludes_roles(db, role_admin, role_manager, role_employee):
    roles = get_subroles_for_role(
        db,
        "admin",
        excluded_roles=["admin", "manager"],
    )

    names = {r.name for r in roles}

    assert names == {"employee"}

def test_get_subroles_invalid_role_raises_403(db):
    with pytest.raises(HTTPException) as exc:
        get_subroles_for_role(db, "nonexistent", None)

    assert exc.value.status_code == 403
