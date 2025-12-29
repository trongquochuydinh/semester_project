from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List

from requests import Session
from api.db.db_engine import SessionLocal, get_db
from api.dependencies import get_current_user
from api.models.company import Company
from api.models.user import User
from api.schemas import(
    CompanyCreate,
    PaginationRequest
)

from api.services import paginate_items

router = APIRouter(prefix="/api/items", tags=["items"])

@router.post("/paginate")
def paginate_companies_endpoint(
    request: PaginationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return paginate_items(
        db=db,
        limit=request.limit,
        offset=request.offset,
        filters=request.filters,
        company_id=current_user.company_id,
    )
