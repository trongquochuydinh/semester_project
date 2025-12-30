from decimal import Decimal
import re
from uuid import uuid4
from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.schemas import (
    PaginationResponse, MessageResponse, ItemCreationRequest, ItemGetResponse, ItemEditRequest
)
from api.models.user import User
from api.models.item import Item

from api.db.item_db import (
    insert_item as db_insert_item,
    get_item_data_by_id as db_get_item_data_by_id,
    edit_item as db_edit_item,
    paginate_items as db_paginate_items
)

from api.services import (
    assert_company_access
)

def create_item(data: ItemCreationRequest, db: Session, current_user: User) -> MessageResponse:
    # --------------------
    # Required fields
    # --------------------
    name = data.get("name")
    if not name:
        raise HTTPException(400, "Item name is required")

    # --------------------
    # Validate numbers
    # --------------------
    price, quantity = validate_item_numbers(data)

    # --------------------
    # Generate SKU
    # --------------------
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

def edit_item(item_id: int, data: ItemEditRequest, db: Session, current_user: User):
    item = db_get_item_data_by_id(db, item_id)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    assert_company_access(
        db,
        is_superadmin=(current_user.role.name == "superadmin"),
        current_user_company_id=current_user.company_id,
        company_id=item.company_id,
    )

    updates = {
        "name": data.name.strip(),
        "price": data.price,
        "quantity": data.quantity
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

def get_info_of_item(item_id: int, db: Session, current_user: User):
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

def validate_item_numbers(data: dict):
    try:
        price = Decimal(data.get("price"))
    except Exception:
        raise HTTPException(400, "Invalid price")

    try:
        quantity = int(data.get("quantity"))
    except Exception:
        raise HTTPException(400, "Invalid quantity")

    if price < 0:
        raise HTTPException(400, "Price must be >= 0")

    if quantity < 0:
        raise HTTPException(400, "Quantity must be >= 0")

    return price, quantity

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
