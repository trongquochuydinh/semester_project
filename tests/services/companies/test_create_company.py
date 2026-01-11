import pytest
from fastapi import HTTPException

from api.services.company_service import create_company
from api.schemas import CompanyCreateRequest, MessageResponse

def test_create_company_success(db):
    data = CompanyCreateRequest(
        name="NewCo",
        field="IT"
    )

    result: MessageResponse = create_company(data=data, db=db)

    assert result.message == "Company created successfully."

def test_create_company_duplicate_name(db, company):
    data = CompanyCreateRequest(
        name=company.name,
        field="IT"
    )

    with pytest.raises(HTTPException) as exc:
        create_company(data=data, db=db)

    assert exc.value.status_code == 409

def test_create_company_empty_fields(db):
    data = CompanyCreateRequest(
        name="",
        field="IT"
    )

    with pytest.raises(HTTPException) as exc:
        create_company(data=data, db=db)

    assert exc.value.status_code == 422

