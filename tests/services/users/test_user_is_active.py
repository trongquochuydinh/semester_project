
import pytest
from fastapi import HTTPException

from api.services.user_service import toggle_user_is_active

def test_admin_can_toggle_employee_is_active(db, admin, employee):
    assert employee.is_active is True

    response = toggle_user_is_active(
        user_id=employee.id,
        db=db,
        current_user=admin,
    )

    assert employee.is_active is False
    assert "disabled" in response.message.lower()

def test_toggle_user_is_active_twice_restores_state(db, admin, employee):
    assert employee.is_active is True

    toggle_user_is_active(employee.id, db, admin)
    toggle_user_is_active(employee.id, db, admin)

    assert employee.is_active is True

def test_admin_cannot_toggle_user_in_other_company(db, admin, employee, company2):
    employee.company_id = company2.id
    db.flush()

    with pytest.raises(HTTPException) as exc:
        toggle_user_is_active(
            user_id=employee.id,
            db=db,
            current_user=admin,
        )

    assert exc.value.status_code == 403

def test_manager_cannot_toggle_admin(db, manager, admin):
    with pytest.raises(HTTPException) as exc:
        toggle_user_is_active(
            user_id=admin.id,
            db=db,
            current_user=manager,
        )

    assert exc.value.status_code == 403
