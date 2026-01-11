import pytest
from fastapi import HTTPException

from decimal import Decimal

from api.schemas.item_schema import ItemEditRequest
from api.services.item_service import edit_item

def test_edit_item_success(db, admin, item):
    data = ItemEditRequest(
        name="Updated Item",
        price=Decimal("120.00"),
        quantity=5,
    )

    response = edit_item(
        item_id=item.id,
        data=data,
        db=db,
        current_user=admin,
    )

    db.refresh(item)

    assert response.name == "Updated Item"
    assert response.price == Decimal("120.00")
    assert response.quantity == 5


def test_edit_item_not_found(db, admin):
    data = ItemEditRequest(
        name="X",
        price=Decimal("10.00"),
        quantity=1,
    )

    with pytest.raises(HTTPException) as exc:
        edit_item(
            item_id=9999,
            data=data,
            db=db,
            current_user=admin,
        )

    assert exc.value.status_code == 404

def test_edit_item_other_company_forbidden(db, admin, item, company2):
    data = ItemEditRequest(
        name="Updated Item",
        price=Decimal("120.00"),
        quantity=5,
    )

    response = edit_item(
        item_id=item.id,
        data=data,
        db=db,
        current_user=admin,
    )

    db.refresh(item)

    assert response.name == "Updated Item"
    assert response.price == Decimal("120.00")
    assert response.quantity == 5


    item.company_id = company2.id
    db.flush()

    data = ItemEditRequest(
        name="X",
        price=Decimal("10.00"),
        quantity=1,
    )

    with pytest.raises(HTTPException) as exc:
        edit_item(
            item_id=item.id,
            data=data,
            db=db,
            current_user=admin,
        )

    assert exc.value.status_code == 403
