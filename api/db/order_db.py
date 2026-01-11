from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from api.models import Order, User

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

def insert_order(db: Session, order: Order):
    db.add(order)
    db.flush()

def get_order_by_id(db: Session, order_id: int) -> Optional[Order]:
    return (
        db.query(Order)
        .options(
            joinedload(Order.company),
        )
        .filter(Order.id == order_id)
        .first()
    )

def change_order_status(order: Order, status: str):
    order.status = status

def count_orders(
    db: Session,
    company_id: int,
    filters: dict,
) -> int:
    query = db.query(func.count(Order.id))

    # Company scope (mandatory in your system)
    query = query.filter(Order.company_id == company_id)

    # Status filter
    status = filters.get("status")
    if status is not None:
        query = query.filter(Order.status == status)

    # Time range filters
    from_ts = filters.get("from_ts")
    to_ts = filters.get("to_ts")

    if from_ts is not None:
        query = query.filter(Order.created_at >= from_ts)

    if to_ts is not None:
        query = query.filter(Order.created_at <= to_ts)

    return query.scalar()

def count_orders_grouped_by_status(
    db: Session,
    company_id: int,
    is_superadmin: bool,
    filters: dict,
):
    query = db.query(
        Order.status,
        func.count(Order.id).label("count")
    )

    if not is_superadmin:
        query = query.filter(Order.company_id == company_id)

    if "from_ts" in filters:
        query = query.filter(Order.created_at >= filters["from_ts"])

    if "to_ts" in filters:
        query = query.filter(Order.created_at <= filters["to_ts"])

    if "order_type" in filters:
        query = query.filter(Order.order_type == filters["order_type"])

    return query.group_by(Order.status).all()