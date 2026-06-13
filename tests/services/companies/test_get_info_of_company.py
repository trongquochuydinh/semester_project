import pytest

from api.domain import NotFoundError
from api.services.company_service import get_info_of_company


def test_get_info_of_company_success(db, superadmin, company):
    result = get_info_of_company(db=db, current_user=superadmin, company_id=company.id)

    assert result.id == company.id
    assert result.name.value == company.name
    assert result.field.value == company.field

def test_get_info_of_company_not_found(db, superadmin):
    with pytest.raises(NotFoundError):
        get_info_of_company(db=db, current_user=superadmin, company_id=9999)
