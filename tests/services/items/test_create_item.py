from decimal import Decimal

import pytest

from api.domain import NotFoundError, ValidationError
from api.services.item_service import create_item, edit_item, get_item


def test_create_item_success(db, admin):
    result = create_item(
        db=db,
        current_user=admin,
        name="Test Item",
        price=Decimal("99.99"),
        quantity=10,
    )

    assert result.message == "Item was successfully added."


def test_create_item_empty_name(db, admin):
    with pytest.raises(ValidationError):
        create_item(
            db=db,
            current_user=admin,
            name="",
            price=Decimal("0"),
            quantity=0,
        )


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


def test_get_item_success(db, admin, item):
    response = get_item(item_id=item.id, db=db, current_user=admin)

    assert response.name == item.name
    assert response.price == item.price
    assert response.quantity == item.quantity
