from sqlalchemy.orm import Session

from api.domain import Item as DomainItem, MessageResult, NotFoundError, PaginatedItems
from api.domain.access import RolePolicy
from api.domain.mappers.item_mapper import (
    item_domain_to_edit_response,
    item_domain_to_entity,
    item_domain_to_get_response,
    item_entity_to_domain,
)
from api.models.user import User
from api.db import (
    insert_item as db_insert_item,
    get_item_data_by_id as db_get_item_data_by_id,
    edit_item as db_edit_item,
    paginate_items as db_paginate_items,
    change_item_is_active as db_change_item_is_active,
)
from api.services.company_service import assert_company_access


def create_item(
    db: Session,
    current_user: User,
    name: str,
    price,
    quantity: int,
) -> MessageResult:
    RolePolicy.require(current_user.role.name, ["admin", "manager"])

    item = DomainItem.draft(
        name=name,
        price=price,
        quantity=quantity,
        company_id=current_user.company_id,
    )

    db_insert_item(db, item_domain_to_entity(item))

    return MessageResult(message="Item was successfully added.")


def edit_item(
    db: Session,
    current_user: User,
    item_id: int,
    name: str,
    price,
    quantity: int,
):
    RolePolicy.require(current_user.role.name, ["admin", "manager"])

    entity = db_get_item_data_by_id(db, item_id)
    if not entity:
        raise NotFoundError("Item not found")

    assert_company_access(
        db,
        is_superadmin=(current_user.role.name == "superadmin"),
        current_user_company_id=current_user.company_id,
        company_id=entity.company_id,
    )

    item = item_entity_to_domain(entity).update(name, price, quantity)

    updated_entity = db_edit_item(
        db=db,
        item_id=entity.id,
        updates={
            "name": item.name.value,
            "price": item.price.value,
            "quantity": item.quantity.value,
        },
    )

    if not updated_entity:
        raise NotFoundError("Failed to update the item.")

    return item_domain_to_edit_response(item_entity_to_domain(updated_entity))


def get_item(db: Session, current_user: User, item_id: int):
    RolePolicy.require(current_user.role.name, ["admin", "manager"])

    entity = db_get_item_data_by_id(db, item_id)
    if not entity:
        raise NotFoundError("Item not found")

    assert_company_access(
        db,
        is_superadmin=(current_user.role.name == "superadmin"),
        current_user_company_id=current_user.company_id,
        company_id=entity.company_id,
    )

    return item_domain_to_get_response(item_entity_to_domain(entity))


def toggle_item_is_active(
    db: Session,
    current_user: User,
    item_id: int,
) -> MessageResult:
    RolePolicy.require(current_user.role.name, ["admin", "manager"])

    entity = db_get_item_data_by_id(db, item_id)
    if not entity:
        raise NotFoundError("Item not found")

    assert_company_access(
        db,
        is_superadmin=(current_user.role.name == "superadmin"),
        current_user_company_id=current_user.company_id,
        company_id=entity.company_id,
    )

    item = item_entity_to_domain(entity).toggle_active()
    db_change_item_is_active(entity, item.is_active)

    status = "activated" if item.is_active else "discontinued"
    return MessageResult(message=f"Item was successfully {status}.")


def paginate_items(
    db: Session,
    current_user: User,
    limit: int,
    offset: int,
    filters: dict,
) -> PaginatedItems:
    total, results = db_paginate_items(
        db=db,
        filters=filters,
        company_id=current_user.company_id,
        limit=limit,
        offset=offset,
    )

    return PaginatedItems(
        total=total,
        data=[item_entity_to_domain(item) for item in results],
    )
