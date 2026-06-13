import pytest
from decimal import Decimal

from api.domain import ForbiddenError, NotFoundError
from api.services.item_service import edit_item


def test_edit_item_success(db, admin, item):
    response = edit_item(
        db=db,
        current_user=admin,
        item_id=item.id,
        name="Updated Item",
        price=Decimal("120.00"),
        quantity=5,
    )

    db.refresh(item)

    assert response.name == "Updated Item"
    assert response.price == Decimal("120.00")
    assert response.quantity == 5


def test_edit_item_not_found(db, admin):
    with pytest.raises(NotFoundError):
        edit_item(
            db=db,
            current_user=admin,
            item_id=9999,
            name="X",
            price=Decimal("10.00"),
            quantity=1,
        )


def test_edit_item_other_company_forbidden(db, admin, item, company2):
    edit_item(
        db=db,
        current_user=admin,
        item_id=item.id,
        name="Updated Item",
        price=Decimal("120.00"),
        quantity=5,
    )

    item.company_id = company2.id
    db.flush()

    with pytest.raises(ForbiddenError):
        edit_item(
            db=db,
            current_user=admin,
            item_id=item.id,
            name="X",
            price=Decimal("10.00"),
            quantity=1,
        )
