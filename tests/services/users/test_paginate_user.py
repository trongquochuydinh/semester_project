from api.models import User
from api.services.user_service import paginate_users


def test_paginate_users_basic_limit_offset(db, admin, company, role_manager):
    for i in range(5):
        db.add(
            User(
                username=f"user_{i}",
                email=f"user_{i}@example.com",
                password_hash="x",
                company_id=company.id,
                role_id=role_manager.id,
                is_active=True,
                status="offline",
            )
        )

    db.flush()

    response = paginate_users(
        db=db,
        current_user=admin,
        limit=2,
        offset=0,
        filters={},
    )

    assert response.total >= 5
    assert len(response.data) == 2


def test_paginate_users_offset_skips_results(db, admin, company):
    response1 = paginate_users(
        db=db,
        current_user=admin,
        limit=2,
        offset=0,
        filters={},
    )

    response2 = paginate_users(
        db=db,
        current_user=admin,
        limit=2,
        offset=2,
        filters={},
    )

    ids_page_1 = {u["id"] for u in response1.data}
    ids_page_2 = {u["id"] for u in response2.data}

    assert ids_page_1.isdisjoint(ids_page_2)


def test_paginate_users_respects_role_scope(db, admin, manager, employee, company):
    response = paginate_users(
        db=db,
        current_user=manager,
        limit=10,
        offset=0,
        filters={},
    )

    roles = {u["role_name"] for u in response.data}

    assert "employee" in roles
    assert "manager" not in roles
    assert "admin" not in roles
