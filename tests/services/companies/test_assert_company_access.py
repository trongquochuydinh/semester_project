import pytest
from fastapi import HTTPException

from api.services.company_service import assert_company_access

def test_assert_company_access_success(db, admin, company):
    result = assert_company_access(
        db=db,
        is_superadmin=False,
        current_user_company_id=company.id,
        company_id=company.id,
    )

    assert result.id == company.id

def test_assert_company_access_not_found(db, admin):
    with pytest.raises(HTTPException) as exc:
        assert_company_access(
            db=db,
            is_superadmin=False,
            current_user_company_id=1,
            company_id=9999,
        )

    assert exc.value.status_code == 404

def test_assert_company_access_forbidden_other_company(
    db, admin, company, company2
):
    
    assert admin.company_id == company.id

    with pytest.raises(HTTPException) as exc:
        assert_company_access(
            db=db,
            is_superadmin=False,
            current_user_company_id=admin.company_id,
            company_id=company2.id,
        )

    assert exc.value.status_code == 403
