from typing import List, Optional

from api.domain.item import Item as DomainItem
from api.models.item import Item as ItemEntity
from api.schemas import ItemEditResponse, ItemGetResponse


def item_entity_to_domain(
    item: ItemEntity,
    *,
    company_name: Optional[str] = None,
) -> DomainItem:
    return DomainItem.from_persistence(
        id=item.id,
        name=item.name,
        sku=item.sku,
        price=item.price,
        quantity=item.quantity,
        company_id=item.company_id,
        is_active=item.is_active,
        company_name=company_name or (item.company.name if item.company else None),
    )


def item_domain_to_entity(item: DomainItem) -> ItemEntity:
    return ItemEntity(
        id=item.id,
        name=item.name.value,
        sku=item.sku,
        price=item.price.value,
        quantity=item.quantity.value,
        company_id=item.company_id,
        is_active=item.is_active,
    )


def item_domain_to_get_response(item: DomainItem) -> ItemGetResponse:
    return ItemGetResponse(
        name=item.name.value,
        price=item.price.value,
        quantity=item.quantity.value,
    )


def item_domain_to_edit_response(item: DomainItem) -> ItemEditResponse:
    return ItemEditResponse(
        name=item.name.value,
        price=item.price.value,
        quantity=item.quantity.value,
    )


def item_domain_to_row(item: DomainItem) -> dict:
    return {
        "id": item.id,
        "name": item.name.value,
        "sku": item.sku,
        "price": item.price.value,
        "quantity": item.quantity.value,
        "company_id": item.company_id,
        "is_active": "Active" if item.is_active else "Discontinued",
        "company_name": item.company_name,
    }


def item_list_to_rows(items: List[DomainItem]) -> List[dict]:
    return [item_domain_to_row(item) for item in items]
