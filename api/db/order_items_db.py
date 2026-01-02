from sqlalchemy.orm import Session, joinedload
from sqlalchemy import asc

from api.models.order_item import OrderItem
from api.models.item import Item


def paginate_order_items(
    db: Session,
    order_id: int,
    company_id: int,
    limit: int,
    offset: int,
):
    query = (
        db.query(
            Item,
            OrderItem.quantity.label("ordered_quantity"),
            OrderItem.unit_price.label("unit_price"),
        )
        .join(OrderItem, OrderItem.item_id == Item.id)
        .options(joinedload(Item.company))
        .filter(OrderItem.order_id == order_id)
    )

    if company_id is not None:
        query = query.filter(Item.company_id == company_id)

    total = query.count()
    results = query.offset(offset).limit(limit).all()

    return total, results
