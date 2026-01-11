
import pytest
from fastapi import HTTPException

from api.services.user_service import paginate_users
from api.models import User

def test_paginate_users_basic_limit_offset(db, admin, company, role_manager):
    # create extra employees
    users = []
    for i in range(5):
        u = User(
            username=f"user_{i}",
            email=f"user_{i}@example.com",
            password_hash="x",
            company_id=company.id,
            role_id=role_manager.id,  # same role for simplicity
            is_active=True,
            status="offline",
        )
        db.add(u)
        users.append(u)

    db.flush()

    response = paginate_users(
        db=db,
        limit=2,
        offset=0,
        filters={},
        user_role="admin",
        company_id=company.id,
    )

    assert response.total >= 5
    assert len(response.data) == 2

def test_paginate_users_offset_skips_results(db, admin, company):
    response1 = paginate_users(
        db=db,
        limit=2,
        offset=0,
        filters={},
        user_role="admin",
        company_id=company.id,
    )

    response2 = paginate_users(
        db=db,
        limit=2,
        offset=2,
        filters={},
        user_role="admin",
        company_id=company.id,
    )

    ids_page_1 = {u["id"] for u in response1.data}
    ids_page_2 = {u["id"] for u in response2.data}

    assert ids_page_1.isdisjoint(ids_page_2)

def test_paginate_users_respects_role_scope(db, admin, manager, employee, company):
    response = paginate_users(
        db=db,
        limit=10,
        offset=0,
        filters={},
        user_role="manager",
        company_id=company.id,
    )

    roles = {u["role_name"] for u in response.data}

    assert "employee" in roles
    assert "manager" not in roles
    assert "admin" not in roles
