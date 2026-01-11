import pytest
from fastapi import HTTPException

from api.services.company_service import edit_company
from api.models import Company
from api.schemas import CompanyEditRequest

def test_edit_company_success(db, company):

    data = CompanyEditRequest(
        name="Updated Company",
        field="New field"
    )

    response = edit_company(
        company_id=company.id,
        db=db,
        data=data,
    )

    db.refresh(company)

    assert response.message == "Company was successfully updated."
    assert company.name == "Updated Company"
    assert company.field == "New field"

def test_edit_company_not_found(db):
    with pytest.raises(HTTPException) as exc:
        edit_company(
            company_id=9999,
            db=db,
            data = CompanyEditRequest(
                name="X",
                field="Y"
            )
        )

    assert exc.value.status_code == 404

def test_edit_company_duplicate_name(db, company):
    other = Company(name="OtherCo", field="X")
    db.add(other)
    db.flush()

    with pytest.raises(HTTPException) as exc:
        edit_company(
            company_id=company.id,
            db=db,
            data = CompanyEditRequest(
                name="OtherCo",
                field="X"
            )
        )

    assert exc.value.status_code == 409

def test_edit_company_empty_fields(db, company):
    data = CompanyEditRequest(
            name="",
            field="X"
        )

    with pytest.raises(HTTPException) as exc:
        edit_company(company_id=company.id, data=data, db=db)

    assert exc.value.status_code == 422