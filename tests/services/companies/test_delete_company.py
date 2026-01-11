import pytest
from fastapi import HTTPException

from api.services.company_service import delete_company
from api.db.company_db import get_company_data_by_id as db_get_company_data_by_id
from api.schemas import CompanyCreateRequest, MessageResponse

def test_delete_company_success(db, company):
    response = delete_company(company_id=company.id, db=db)

    assert response.message == "Company was successfully deleted."

    assert db_get_company_data_by_id(db, company.id) is None

def test_delete_company_not_found_raises_404(db):
    with pytest.raises(HTTPException) as exc:
        delete_company(company_id=9999, db=db)

    assert exc.value.status_code == 404
