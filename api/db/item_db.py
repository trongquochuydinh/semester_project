from sqlalchemy.orm import Session, joinedload
from api.models.item import Item

def insert_item(db: Session, item: Item):
    db.add(item)
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
) -> Item:

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

    # --------------------
    # Apply filters
    # --------------------
    for key, value in filters.items():
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
