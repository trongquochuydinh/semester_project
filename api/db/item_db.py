from typing import Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import asc
from api.models.item import Item

LOW_STOCK_THRESHOLD = 20

def insert_item(db: Session, item: Item):
    db.add(item)
    db.flush()

def apply_stock_change(db: Session, item: Item, delta: int):
    item.quantity += delta
    db.flush()

def get_item_data_by_id(db: Session, item_id: int):
    return (
        db.query(Item)
        .options(
            joinedload(Item.company),
        )
        .filter(Item.id == item_id)
        .first()
    )

def edit_item(
    db: Session,
    item_id: int,
    updates: dict,
) -> Optional[Item]:

    EDITABLE_FIELDS = {
        "name",
        "price",
        "quantity"
    }

    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        return None

    for key, value in updates.items():
        if key in EDITABLE_FIELDS:
            setattr(item, key, value)

    db.flush()
    return item

def change_item_is_active(item: Item, is_active: bool):
    item.is_active = is_active

def paginate_items(
    db: Session,
    filters: dict,
    company_id: int,
    limit: int,
    offset: int,
):
    query = (
        db.query(Item)
        .options(
            joinedload(Item.company),
        )
    )


    if filters.get("low_stock"):
        query = (
            query
            .filter(
                Item.quantity <= LOW_STOCK_THRESHOLD,
                Item.is_active == True
            )
            .order_by(asc(Item.quantity))
        )

    # --------------------
    # Apply filters
    # --------------------
    for key, value in filters.items():
        if key in {"low_stock"}:
            continue

        if hasattr(Item, key):
            query = query.filter(getattr(Item, key) == value)

    # --------------------
    # Company restriction
    # --------------------
    if company_id is not None:
        query = query.filter(Item.company_id == company_id)

    # --------------------
    # Pagination
    # --------------------
    total = query.count()
    results = query.offset(offset).limit(limit).all()

    return total, results
