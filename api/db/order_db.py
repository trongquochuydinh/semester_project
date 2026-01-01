from sqlalchemy.orm import Session, joinedload
from sqlalchemy import asc
from api.models.order import Order

def paginate_order(
    db: Session,
    filters: dict,
    company_id: int,
    limit: int,
    offset: int,
):
    query = (
        db.query(Order)
        .options(
            joinedload(Order.company),
        )
    )

    # --------------------
    # Apply filters
    # --------------------
    for key, value in filters.items():
        if hasattr(Order, key):
            query = query.filter(getattr(Order, key) == value)

    # --------------------
    # Company restriction
    # --------------------
    if company_id is not None:
        query = query.filter(Order.company_id == company_id)

    # --------------------
    # Pagination
    # --------------------
    total = query.count()
    results = query.offset(offset).limit(limit).all()

    return total, results