from fastapi import HTTPException
import pytest

from api.services.item_service import get_item

def test_get_item_success(db, admin, item):
    response = get_item(
        item_id=item.id,
        db=db,
        current_user=admin,
    )

    assert response.name == item.name
    assert response.price == item.price
    assert response.quantity == item.quantity

def test_get_item_other_company_forbidden(db, admin, item, company2):

    test_get_item_success(db, admin, item)

    item.company_id = company2.id
    db.flush()

    with pytest.raises(HTTPException) as exc:
        get_item(
            item_id=item.id,
            db=db,
            current_user=admin,
        )

    assert exc.value.status_code == 403

def test_get_item_not_found(db, admin):

    with pytest.raises(HTTPException) as exc:
        get_item(
            item_id=9999,
            db=db,
            current_user=admin,
        )

    assert exc.value.status_code == 404