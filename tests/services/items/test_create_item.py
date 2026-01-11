from decimal import Decimal

from fastapi import HTTPException
import pytest

from api.services.item_service import create_item
from api.models import Item
from api.schemas import ItemCreationRequest

def test_create_item_success(db, admin):
    data = ItemCreationRequest(
        name="Test Item",
        price=Decimal("99.99"),
        quantity=10,
    )

    response = create_item(
        data=data,
        db=db,
        current_user=admin,
    )

    assert response.message == "Item was successfully added."

    item = db.query(Item).first()
    assert item.name == "Test Item"
    assert item.company_id == admin.company_id
    assert item.is_active is True
    assert item.sku is not None

def test_create_item_empty_fields(db, admin):
    data = ItemCreationRequest(
        name="",
        price=Decimal("0"),
        quantity=0,
    )

    with pytest.raises(HTTPException) as exc:
        create_item(
            data=data,
            db=db,
            current_user=admin,
        )

    assert exc.value.status_code == 422
