import pytest

from api.domain import ConflictError, ForbiddenError
from api.services.user_service import create_user_account


def test_admin_can_create_user(db, company, role_employee, admin):
    response = create_user_account(
        db=db,
        current_user=admin,
        username="new_user",
        email="new_user@example.com",
        role="employee",
        company_id=company.id,
    )

    assert response.message == "User created successfully"
    assert response.initial_password is not None


def test_superadmin_can_create_admin(db, company, role_admin, superadmin):
    response = create_user_account(
        db=db,
        current_user=superadmin,
        username="new_user",
        email="new_user@example.com",
        role="admin",
        company_id=company.id,
    )

    assert response.message == "User created successfully"
    assert response.initial_password is not None


def test_create_user_duplicate_username(db, company, admin):
    with pytest.raises(ConflictError):
        create_user_account(
            db=db,
            current_user=admin,
            username=admin.username,
            email="another@example.com",
            role="employee",
            company_id=admin.company_id,
        )


def test_create_user_duplicate_email(db, company, admin):
    with pytest.raises(ConflictError):
        create_user_account(
            db=db,
            current_user=admin,
            username="another_user",
            email=admin.email,
            role="employee",
            company_id=company.id,
        )


def test_manager_cannot_create_admin(db, company, manager, role_admin):
    with pytest.raises(ForbiddenError):
        create_user_account(
            db=db,
            current_user=manager,
            username="illegal_admin",
            email="illegal_admin@example.com",
            role="admin",
            company_id=company.id,
        )


def test_admin_cannot_create_user_in_other_company(db, company, company2, admin):
    with pytest.raises(ForbiddenError):
        create_user_account(
            db=db,
            current_user=admin,
            username="foreign_user",
            email="foreign@example.com",
            role="employee",
            company_id=company2.id,
        )
