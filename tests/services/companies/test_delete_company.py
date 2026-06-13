import pytest

from api.domain import NotFoundError
from api.services.company_service import delete_company
from api.db.company_db import get_company_data_by_id as db_get_company_data_by_id

def test_delete_company_success(db, superadmin, company):
    response = delete_company(db=db, current_user=superadmin, company_id=company.id)

    assert response.message == "Company was successfully deleted."

    assert db_get_company_data_by_id(db, company.id) is None

def test_delete_company_not_found_raises_404(db, superadmin):
    with pytest.raises(NotFoundError):
        delete_company(db=db, current_user=superadmin, company_id=9999)
