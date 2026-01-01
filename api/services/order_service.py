from sqlalchemy.orm import Session

from api.schemas import (
    PaginationResponse
)

from api.db.order_db import (
    paginate_order as db_paginate_orders,
)

def paginate_orders(
    db: Session,
    limit: int,
    offset: int,
    filters: dict,
    company_id: int,
):
    
    total, results = db_paginate_orders(
        db=db,
        filters=filters,
        company_id=company_id,
        limit=limit,
        offset=offset,
    )

    def serialize(i):
        d = {c.name: getattr(i, c.name) for c in i.__table__.columns}
        return d

    return PaginationResponse(
        total=total,
        data=[serialize(r) for r in results],
    )
