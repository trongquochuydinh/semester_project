from api.services.item_service import paginate_items

def test_paginate_items_basic(db, admin, item):
    response = paginate_items(
        db=db,
        limit=1,
        offset=0,
        filters={},
        company_id=admin.company_id,
    )

    assert response.total >= 1
    assert len(response.data) == 1

    row = response.data[0]
    assert "company_name" in row
    assert "is_active" in row

def test_paginate_items_other_company_excluded(db, admin, item, company2):

    test_paginate_items_basic(db, admin, item)

    item.company_id = company2.id
    db.flush()

    response = paginate_items(
        db=db,
        limit=10,
        offset=0,
        filters={},
        company_id=admin.company_id,
    )

    assert response.total == 0
