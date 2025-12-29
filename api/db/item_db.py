from sqlalchemy.orm import Session, joinedload
from api.models.item import Item

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
