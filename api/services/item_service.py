from decimal import Decimal
import re
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.schemas import (
    PaginationResponse, MessageResponse, ItemCreationRequest, ItemGetResponse, ItemEditRequest, ItemEditResponse
)
from api.models.user import User
from api.models.item import Item

from api.db.item_db import (
    insert_item as db_insert_item,
    get_item_data_by_id as db_get_item_data_by_id,
    edit_item as db_edit_item,
    paginate_items as db_paginate_items,
    change_item_is_active as db_change_user_is_active
)

from api.services import (
    assert_company_access
)

from api.utils import validate_item_data

def create_item(data: ItemCreationRequest, db: Session, current_user: User) -> MessageResponse:
    name, price, quantity = validate_item_data(data)

    sku = generate_sku(name)

    item = Item(
        name=name,
        sku=sku,
        price=price,
        quantity=quantity,
        company_id=current_user.company_id,
        is_active=True,
    )

    db_insert_item(db, item)

    return MessageResponse(
        message="Item was successfully added."
    )

def edit_item(item_id: int, data: ItemEditRequest, db: Session, current_user: User) -> ItemEditResponse:
    item = db_get_item_data_by_id(db, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    assert_company_access(
        db,
        is_superadmin=(current_user.role.name == "superadmin"),
        current_user_company_id=current_user.company_id,
        company_id=item.company_id,
    )

    name, price, quantity = validate_item_data(data)

    updates = {
        "name": name,
        "price": price,
        "quantity": quantity,
    }

    updated_item = db_edit_item(
        db=db,
        item_id=item.id,
        updates=updates
    )

    return ItemGetResponse(
        name=updated_item.name,
        price=updated_item.price,
        quantity=updated_item.quantity
    )

def get_item(item_id: int, db: Session, current_user: User):
    item = db_get_item_data_by_id(db, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    assert_company_access(
        db,
        is_superadmin=(current_user.role.name == "superadmin"),
        current_user_company_id=current_user.company_id,
        company_id=item.company_id,
    )

    return ItemGetResponse(
        name=item.name,
        price=item.price,
        quantity=item.quantity
    )

def toggle_item_is_active(item_id: int, db: Session, current_user: User) -> MessageResponse:
    item = db_get_item_data_by_id(db, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    assert_company_access(
        db,
        is_superadmin=(current_user.role.name == "superadmin"),
        current_user_company_id=current_user.company_id,
        company_id=item.company_id,
    )

    is_active = not item.is_active

    db_change_user_is_active(item, is_active)

    return MessageResponse(
        message=f"Item was successfully {'activated' if is_active else 'discontinued'}."
    )

def generate_sku(name: str) -> str:
    base = re.sub(r"[^A-Z0-9]", "", name.upper())
    base = base[:8] if base else "ITEM"
    return f"{base}-{uuid4().hex[:6].upper()}"

def paginate_items(
    db: Session,
    limit: int,
    offset: int,
    filters: dict,
    company_id: int,
):
    
    total, results = db_paginate_items(
        db=db,
        filters=filters,
        company_id=company_id,
        limit=limit,
        offset=offset,
    )

    def serialize(i):
        d = {c.name: getattr(i, c.name) for c in i.__table__.columns}
        d["company_name"] = i.company.name if i.company else None
        d["is_active"] = "Active" if i.is_active else "Discontinued"
        return d

    return PaginationResponse(
        total=total,
        data=[serialize(r) for r in results],
    )
