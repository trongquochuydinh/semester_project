import pytest

from api.domain import ConflictError, NotFoundError, ValidationError
from api.services.company_service import edit_company
from api.models import Company

def test_edit_company_success(db, superadmin, company):
    response = edit_company(
        db=db,
        current_user=superadmin,
        company_id=company.id,
        name="Updated Company",
        field="New field",
    )

    db.refresh(company)

    assert response.message == "Company was successfully updated."
    assert company.name == "Updated Company"
    assert company.field == "New field"

def test_edit_company_not_found(db, superadmin):
    with pytest.raises(NotFoundError):
        edit_company(
            db=db,
            current_user=superadmin,
            company_id=9999,
            name="X",
            field="Y",
        )

def test_edit_company_duplicate_name(db, superadmin, company):
    other = Company(name="OtherCo", field="X")
    db.add(other)
    db.flush()

    with pytest.raises(ConflictError):
        edit_company(
            db=db,
            current_user=superadmin,
            company_id=company.id,
            name="OtherCo",
            field="X",
        )

def test_edit_company_empty_fields(db, superadmin, company):
    with pytest.raises(ValidationError):
        edit_company(
            db=db,
            current_user=superadmin,
            company_id=company.id,
            name="",
            field="X",
        )
