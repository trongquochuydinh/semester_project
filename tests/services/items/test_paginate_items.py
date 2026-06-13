from api.domain.mappers.item_mapper import item_domain_to_row
from api.services.item_service import paginate_items


def test_paginate_items_basic(db, admin, item):
    result = paginate_items(
        db=db,
        current_user=admin,
        limit=1,
        offset=0,
        filters={},
    )

    assert result.total >= 1
    assert len(result.data) == 1

    row = item_domain_to_row(result.data[0])
    assert "company_name" in row
    assert "is_active" in row


def test_paginate_items_other_company_excluded(db, admin, item, company2):
    test_paginate_items_basic(db, admin, item)

    item.company_id = company2.id
    db.flush()

    result = paginate_items(
        db=db,
        current_user=admin,
        limit=10,
        offset=0,
        filters={},
    )

    assert result.total == 0
