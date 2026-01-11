import pytest
from fastapi import HTTPException

from api.services.company_service import get_info_of_company


def test_get_info_of_company_success(db, company):
    result = get_info_of_company(company.id, db)

    assert result["id"] == company.id
    assert result["company_name"] == company.name
    assert result["field"] == company.field

def test_get_info_of_company_not_found(db):
    with pytest.raises(HTTPException) as exc:
        get_info_of_company(9999, db)

    assert exc.value.status_code == 404
