import pytest

from api.domain import ForbiddenError
from api.services.company_service import create_company, delete_company, edit_company


def test_create_company_forbidden_for_admin(db, admin):
    with pytest.raises(ForbiddenError):
        create_company(db=db, current_user=admin, name="NewCo", field="IT")


def test_edit_company_forbidden_for_admin(db, admin, company):
    with pytest.raises(ForbiddenError):
        edit_company(
            db=db,
            current_user=admin,
            company_id=company.id,
            name="X",
            field="Y",
        )


def test_delete_company_forbidden_for_admin(db, admin, company):
    with pytest.raises(ForbiddenError):
        delete_company(db=db, current_user=admin, company_id=company.id)
