import pytest

from api.domain import ForbiddenError, ValidationError
from api.services.user_service import edit_user


def test_admin_can_edit_employee_basic_fields(db, admin, employee, role_manager):
    response = edit_user(
        db=db,
        current_user=admin,
        user_id=employee.id,
        username="updated_employee",
        email="updated_employee@example.com",
        role="manager",
        company_id=employee.company_id,
    )

    assert response.username == "updated_employee"
    assert response.email == "updated_employee@example.com"
    assert response.company_id == employee.company_id
    assert response.role == "manager"


def test_edit_user_empty_username(db, admin, employee):
    with pytest.raises(ValidationError):
        edit_user(
            db=db,
            current_user=admin,
            user_id=employee.id,
            username="",
            email="valid@example.com",
            role="employee",
            company_id=employee.company_id,
        )


def test_manager_cannot_edit_user_to_higher_role(db, manager, role_admin, employee):
    with pytest.raises(ForbiddenError):
        edit_user(
            db=db,
            current_user=manager,
            user_id=employee.id,
            username="employee_new",
            email="employee_new@example.com",
            role="admin",
            company_id=employee.company_id,
        )


def test_admin_cannot_change_user_company(db, admin, employee, company2):
    with pytest.raises(ForbiddenError):
        edit_user(
            db=db,
            current_user=admin,
            user_id=employee.id,
            username="employee_new",
            email="employee_new@example.com",
            role="employee",
            company_id=company2.id,
        )
