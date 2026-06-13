import pytest

from api.domain import ForbiddenError
from api.services.user_service import toggle_user_is_active


def test_admin_can_toggle_employee_is_active(db, admin, employee):
    assert employee.is_active is True

    response = toggle_user_is_active(
        db=db,
        current_user=admin,
        user_id=employee.id,
    )

    assert employee.is_active is False
    assert "disabled" in response.message.lower()


def test_toggle_user_is_active_twice_restores_state(db, admin, employee):
    assert employee.is_active is True

    toggle_user_is_active(db=db, current_user=admin, user_id=employee.id)
    toggle_user_is_active(db=db, current_user=admin, user_id=employee.id)

    assert employee.is_active is True


def test_admin_cannot_toggle_user_in_other_company(db, admin, employee, company2):
    employee.company_id = company2.id
    db.flush()

    with pytest.raises(ForbiddenError):
        toggle_user_is_active(db=db, current_user=admin, user_id=employee.id)


def test_manager_cannot_toggle_admin(db, manager, admin):
    with pytest.raises(ForbiddenError):
        toggle_user_is_active(db=db, current_user=manager, user_id=admin.id)
