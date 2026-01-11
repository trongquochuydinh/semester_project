import pytest
from fastapi import HTTPException

from api.services.user_service import get_user_count
from api.models import User

def test_admin_get_user_count_only_own_company(
    db, admin, employee, company, company2
):
    # create user in another company
    other_user = User(
        username="other",
        email="other@example.com",
        password_hash="x",
        company_id=company2.id,
        role_id=employee.role_id,
        is_active=True,
        status="offline",
    )
    db.add(other_user)
    db.flush()

    response = get_user_count(db=db, current_user=admin)

    # admin + employee belong to same company
    assert response.total_users == 2
    assert response.online_users == 0

def test_admin_get_user_count_online_only(db, admin, employee):
    employee.status = "online"
    db.flush()

    response = get_user_count(db=db, current_user=admin)

    assert response.total_users == 2 # (admin and employee)
    assert response.online_users == 1 # (only employee)


def test_superadmin_get_user_count_all_companies(
    db, superadmin, admin, employee, company2
):
    other_user = User(
        username="other",
        email="other@example.com",
        password_hash="x",
        company_id=company2.id,
        role_id=employee.role_id,
        is_active=True,
        status="online",
    )
    db.add(other_user)
    db.flush()

    response = get_user_count(db=db, current_user=superadmin)

    assert response.total_users == 4 # (superadmin + admin + employee + other_user)
    assert response.online_users == 1 # (other_user)

def test_superadmin_online_user_count_across_companies(
    db, superadmin, admin, employee
):
    admin.status = "online"
    employee.status = "online"
    db.flush()

    response = get_user_count(db=db, current_user=superadmin)

    assert response.online_users == 2


