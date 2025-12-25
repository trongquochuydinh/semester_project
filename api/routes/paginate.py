from fastapi import APIRouter, Depends, HTTPException, Request, Body
from fastapi.security import HTTPBearer
from api.db.db_engine import get_db
from sqlalchemy.orm import Session
from api.db.db_engine import SessionLocal
from api.models.user import User
from api.models.company import paginate_companies
from api.services import paginate_users

from api.dependencies import get_current_user

security = HTTPBearer()

router = APIRouter(prefix="/api", tags=["pagination"])


# TODO: refactor and use pagination_service.py
@router.post("/paginate")
async def paginate(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    body = await request.json()
    table_name = body.get("table_name")
    limit = int(body.get("limit", 10))
    offset = int(body.get("offset", 0))
    filters = body.get("filters", {})

    role_name = current_user.role.name
    company_id = current_user.company_id

    try:
        handler_map = {
            "users": paginate_users,
            "companies": paginate_companies,
        }
        handler = handler_map.get(table_name, db)
        if not handler:
            raise HTTPException(status_code=400, detail="Invalid table_name")

        return handler(db, limit, offset, filters, role_name, company_id)
    finally:
        db.close()