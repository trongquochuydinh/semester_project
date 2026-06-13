import pytest

from api.domain import ConflictError, ValidationError
from api.services.company_service import create_company

def test_create_company_success(db, superadmin):
    result = create_company(
        db=db,
        current_user=superadmin,
        name="NewCo",
        field="IT",
    )

    assert result.message == "Company created successfully."

def test_create_company_duplicate_name(db, superadmin, company):
    with pytest.raises(ConflictError):
        create_company(
            db=db,
            current_user=superadmin,
            name=company.name,
            field="IT",
        )

def test_create_company_empty_fields(db, superadmin):
    with pytest.raises(ValidationError):
        create_company(
            db=db,
            current_user=superadmin,
            name="",
            field="IT",
        )
