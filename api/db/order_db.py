from sqlalchemy.orm import Session, joinedload
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

    for key, value in filters.items():
        if hasattr(Order, key):
            query = query.filter(getattr(Order, key) == value)

    if company_id is not None:
        query = query.filter(Order.company_id == company_id)

    total = query.count()
    results = query.offset(offset).limit(limit).all()

    # ONLY change: add formatted fields, do NOT overwrite columns
    for order in results:
        order.created_at_fmt = (
            order.created_at.strftime("%d.%m.%Y %H:%M")
            if order.created_at else None
        )
        order.completed_at_fmt = (
            order.completed_at.strftime("%d.%m.%Y %H:%M")
            if order.completed_at else None
        )

    return total, results
