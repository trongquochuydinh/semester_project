import pytest
from fastapi import HTTPException

from api.services.role_service import resolve_assignable_role

def test_admin_can_assign_manager(db, admin, role_manager):
    role = resolve_assignable_role(
        db=db,
        role_name="manager",
        current_user=admin,
    )

    assert role.name == "manager"

def test_admin_can_assign_employee(db, admin, role_employee):
    role = resolve_assignable_role(
        db=db,
        role_name="employee",
        current_user=admin,
    )

    assert role.name == "employee"

def test_admin_cannot_assign_same_role(db, admin, role_admin):
    with pytest.raises(HTTPException) as exc:
        resolve_assignable_role(
            db=db,
            role_name="admin",
            current_user=admin,
        )

    assert exc.value.status_code == 403

def test_admin_cannot_assign_superadmin(db, admin, role_superadmin):
    with pytest.raises(HTTPException) as exc:
        resolve_assignable_role(
            db=db,
            role_name="superadmin",
            current_user=admin,
        )

    assert exc.value.status_code == 403

def test_superadmin_can_assign_admin(db, superadmin, role_admin):
    role = resolve_assignable_role(
        db=db,
        role_name="admin",
        current_user=superadmin,
    )

    assert role.name == "admin"

def test_resolve_assignable_role_invalid_role(db, admin):
    with pytest.raises(HTTPException) as exc:
        resolve_assignable_role(
            db=db,
            role_name="nonexistent",
            current_user=admin,
        )

    assert exc.value.status_code == 404





