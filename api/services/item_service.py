from sqlalchemy.orm import Session

from api.schemas import PaginationResponse

from api.db.item_db import paginate_items as db_paginate_items

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
        return d

    return PaginationResponse(
        total=total,
        data=[serialize(r) for r in results],
    )
