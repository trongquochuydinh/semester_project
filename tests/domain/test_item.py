import pytest
from decimal import Decimal

from api.domain import ConflictError, ForbiddenError, ValidationError
from api.domain.item import Item, SkuGenerator
from api.domain.value_objects import ItemName, Money, Quantity


def test_item_name_rejects_empty():
    with pytest.raises(ValidationError):
        ItemName.from_raw("")


def test_money_rejects_negative():
    with pytest.raises(ValidationError):
        Money.from_raw("-1")


def test_quantity_rejects_negative():
    with pytest.raises(ValidationError):
        Quantity.from_raw(-1)


def test_item_draft_generates_sku():
    item = Item.draft("Test Item", "10.00", 5, company_id=1)
    assert item.sku is not None
    assert "-" in item.sku
    assert item.name.value == "Test Item"


def test_sku_generator_format():
    sku = SkuGenerator.generate("Test Item 123")
    assert "-" in sku
    assert len(sku.split("-")[1]) == 6


def test_item_toggle_active():
    item = Item.draft("Widget", "5", 1, company_id=1)
    toggled = item.toggle_active()
    assert toggled.is_active is False


def test_item_can_fulfill_sale_with_stock():
    item = Item.draft("Widget", "5", 10, company_id=1)
    item.can_fulfill(5, "sale")


def test_item_can_fulfill_rejects_inactive():
    item = Item.draft("Widget", "5", 10, company_id=1).toggle_active()
    with pytest.raises(ConflictError):
        item.can_fulfill(1, "sale")


def test_item_can_fulfill_rejects_insufficient_stock():
    item = Item.draft("Widget", "5", 2, company_id=1)
    with pytest.raises(ForbiddenError):
        item.can_fulfill(5, "sale")
