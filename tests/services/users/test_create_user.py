import pytest
from fastapi import HTTPException

from api.services.user_service import create_user_account
from api.schemas import UserCreateRequest
from api.models.user import User


def test_admin_can_create_user(db, company, role_employee, admin):
    request = UserCreateRequest(
        username="new_user",
        email="new_user@example.com",
        role="employee",
        company_id=company.id,
    )

    # Act
    response = create_user_account(
        data=request,
        db=db,
        current_user=admin,  # admin fixture
    )

    # Assert response
    assert response.message == "User created successfully"
    assert response.initial_password is not None

    # Assert DB state
    created_user = (
        db.query(User)
        .filter(User.username == "new_user")
        .one()
    )

    assert created_user.email == "new_user@example.com"
    assert created_user.company_id == company.id
    assert created_user.role.name == "employee"
    assert created_user.is_active is True

def test_superadmin_can_create_admin(db, company, role_admin, superadmin):
    request = UserCreateRequest(
        username="new_user",
        email="new_user@example.com",
        role="admin",
        company_id=company.id,
    )

    # Act
    response = create_user_account(
        data=request,
        db=db,
        current_user=superadmin,  # admin fixture
    )

    # Assert response
    assert response.message == "User created successfully"
    assert response.initial_password is not None

    # Assert DB state
    created_user = (
        db.query(User)
        .filter(User.username == "new_user")
        .one()
    )

    assert created_user.email == "new_user@example.com"
    assert created_user.company_id == company.id
    assert created_user.role.name == "admin"
    assert created_user.is_active is True

def test_create_user_duplicate_username(db, company, admin):
    # Arrange
    request = UserCreateRequest(
        username=admin.username,  # duplicate
        email="another@example.com",
        role="employee",
        company_id=admin.company_id,
    )

    # Act + Assert
    with pytest.raises(HTTPException) as exc:
        create_user_account(
            data=request,
            db=db,
            current_user=admin,
        )

    assert exc.value.status_code == 409
    assert "exists" in exc.value.detail.lower()

def test_create_user_duplicate_email(db, company, admin):
    request = UserCreateRequest(
        username="another_user",
        email=admin.email,  # duplicate
        role="employee",
        company_id=company.id,
    )

    with pytest.raises(HTTPException) as exc:
        create_user_account(
            data=request,
            db=db,
            current_user=admin,
        )

    assert exc.value.status_code == 409

def test_manager_cannot_create_admin(db, company, manager, role_admin):
    request = UserCreateRequest(
        username="illegal_admin",
        email="illegal_admin@example.com",
        role="admin",
        company_id=company.id,
    )

    with pytest.raises(HTTPException) as exc:
        create_user_account(
            data=request,
            db=db,
            current_user=manager,
        )

    assert exc.value.status_code == 403

def test_admin_cannot_create_user_in_other_company(db, company, company2, admin):
    request = UserCreateRequest(
        username="foreign_user",          
        email="foreign@example.com",      
        role="employee",
        company_id=company2.id,          
    )

    with pytest.raises(HTTPException) as exc:
        create_user_account(
            data=request,
            db=db,
            current_user=admin,
        )

    assert exc.value.status_code == 403
