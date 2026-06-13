import pytest

from api.domain import ForbiddenError
from api.services.company_service import assert_user_company_scope

def test_assert_user_company_scope_superadmin_allows():
    assert_user_company_scope(
        is_superadmin=True,
        current_user_company_id=1,
        target_company_id=2,
    )


def test_assert_user_company_scope_denies_other_company():
    with pytest.raises(ForbiddenError):
        assert_user_company_scope(
            is_superadmin=False,
            current_user_company_id=1,
            target_company_id=2,
        )
