from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, get_db
from api.domain.mappers.company_mapper import (
    company_domain_to_detail_response,
    company_domain_to_row,
    company_list_to_response,
)
from api.models.user import User
from api.schemas import (
    CompaniesResponse,
    CompanyCreateRequest,
    CompanyDetailResponse,
    CompanyEditRequest,
    MessageResponse,
    PaginationRequest,
    PaginationResponse,
)
from api.services import (
    create_company,
    delete_company,
    edit_company,
    get_info_of_company,
    list_companies,
    paginate_companies,
)

router = APIRouter(prefix="/api/companies", tags=["companies"])


@router.get("", response_model=CompaniesResponse)
def list_companies_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = list_companies(db=db, current_user=current_user)
    return company_list_to_response(result.companies)


@router.post("/search", response_model=PaginationResponse)
def paginate_companies_endpoint(
    data: PaginationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = paginate_companies(
        db=db,
        current_user=current_user,
        limit=data.limit,
        offset=data.offset,
        filters=data.filters,
    )
    return PaginationResponse(
        total=result.total,
        data=[company_domain_to_row(company) for company in result.data],
    )


@router.get("/{company_id}", response_model=CompanyDetailResponse)
def get_company_endpoint(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    company = get_info_of_company(
        db=db,
        current_user=current_user,
        company_id=company_id,
    )
    return company_domain_to_detail_response(company)


@router.post("", response_model=MessageResponse)
def create_company_endpoint(
    data: CompanyCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = create_company(
        db=db,
        current_user=current_user,
        name=data.name,
        field=data.field,
    )
    return MessageResponse(message=result.message)


@router.put("/{company_id}", response_model=MessageResponse)
def edit_company_endpoint(
    company_id: int,
    data: CompanyEditRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = edit_company(
        db=db,
        current_user=current_user,
        company_id=company_id,
        name=data.name,
        field=data.field,
    )
    return MessageResponse(message=result.message)


@router.delete("/{company_id}", response_model=MessageResponse)
def delete_company_endpoint(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = delete_company(
        db=db,
        current_user=current_user,
        company_id=company_id,
    )
    return MessageResponse(message=result.message)
