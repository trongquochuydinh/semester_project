import pytest
from fastapi import HTTPException

from api.services.user_service import get_info_of_user

def test_admin_can_get_user_info(db, admin, employee):
    response = get_info_of_user(
        user_id=employee.id,
        db=db,
        current_user=admin,
    )

    assert response.username == employee.username
    assert response.email == employee.email
    assert response.company_id == employee.company_id
    assert response.role == "employee"

def test_admin_cannot_get_user_info_from_other_company(
    db, admin, employee, company2, company
):
    response = get_info_of_user(
        user_id=employee.id,
        db=db,
        current_user=admin,
    )

    assert response.username == employee.username
    assert response.company_id == company.id

    employee.company_id = company2.id
    db.flush()

    with pytest.raises(HTTPException) as exc:
        get_info_of_user(
            user_id=employee.id,
            db=db,
            current_user=admin,
        )

    assert exc.value.status_code == 403

def test_superadmin_can_get_user_info_from_other_company(
    db, superadmin, employee, company, company2
):
    
    response = get_info_of_user(
        user_id=employee.id,
        db=db,
        current_user=superadmin,
    )

    assert response.username == employee.username
    assert response.company_id == company.id

    employee.company_id = company2.id
    db.flush()

    response = get_info_of_user(
        user_id=employee.id,
        db=db,
        current_user=superadmin,
    )

    assert response.username == employee.username
    assert response.company_id == company2.id

def test_get_user_info_nonexistent_user_raises_404(db, admin):
    with pytest.raises(HTTPException) as exc:
        get_info_of_user(
            user_id=999999,
            db=db,
            current_user=admin,
        )

    assert exc.value.status_code == 404
