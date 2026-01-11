import pytest
from fastapi import HTTPException

from api.services.user_service import edit_user
from api.schemas import UserEditRequest
from api.models.user import User

def test_admin_can_edit_employee_basic_fields(db, admin, employee, role_manager):

    request = UserEditRequest(
        username="updated_employee",
        email="updated_employee@example.com",
        role="manager",
        company_id=employee.company_id,
    )

    response = edit_user(
        user_id=employee.id,
        data=request,
        db=db,
        current_user=admin,
    )

    assert response.username == "updated_employee"
    assert response.email == "updated_employee@example.com"
    assert response.company_id == employee.company_id
    assert response.role == "manager"

def test_edit_user_empty_username(db, admin, employee):
    request = UserEditRequest(
        username="",
        email="valid@example.com",
        role="employee",
        company_id=employee.company_id,
    )

    with pytest.raises(HTTPException) as exc:
        edit_user(
            user_id=employee.id,
            data=request,
            db=db,
            current_user=admin,
        )

    assert exc.value.status_code == 422

def test_manager_cannot_edit_user_to_higher_role(db, manager, role_admin, employee):
    request = UserEditRequest(
        username="employee_new",
        email="employee_new@example.com",
        role="admin",  # higher than manager
        company_id=employee.company_id,
    )

    with pytest.raises(HTTPException) as exc:
        edit_user(
            user_id=employee.id,
            data=request,
            db=db,
            current_user=manager,
        )

    assert exc.value.status_code == 403

def test_admin_cannot_change_user_company(db, admin, employee, company2):
    request = UserEditRequest(
        username="employee_new",
        email="employee_new@example.com",
        role="employee",
        company_id=company2.id,  # different company
    )

    with pytest.raises(HTTPException) as exc:
        edit_user(
            user_id=employee.id,
            data=request,
            db=db,
            current_user=admin,
        )

    assert exc.value.status_code == 403
