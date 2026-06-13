import pytest

from api.domain import ConflictError, ForbiddenError, ValidationError
from api.domain.access import RolePolicy, TenantScope
from api.domain.company import Company
from api.domain.value_objects import BusinessField, CompanyName


def test_company_name_rejects_empty():
    with pytest.raises(ValidationError):
        CompanyName.from_raw("")


def test_company_name_rejects_whitespace():
    with pytest.raises(ValidationError):
        CompanyName.from_raw("   ")


def test_company_name_strips_value():
    name = CompanyName.from_raw("  Acme  ")
    assert name.value == "Acme"
    assert name.normalized == "acme"


def test_business_field_rejects_empty():
    with pytest.raises(ValidationError):
        BusinessField.from_raw("")


def test_company_draft_validates_fields():
    company = Company.draft("Acme", "IT")
    assert company.id is None
    assert company.name.value == "Acme"
    assert company.field.value == "IT"


def test_company_update_replaces_values():
    company = Company.draft("Acme", "IT")
    updated = company.update("NewCo", "Finance")
    assert updated.name.value == "NewCo"
    assert updated.field.value == "Finance"


def test_company_ensure_unique_name_raises_conflict():
    company = Company.draft("Acme", "IT")
    with pytest.raises(ConflictError):
        company.ensure_unique_name(company.name, exists=lambda _: True)


def test_company_ensure_unique_name_passes_when_available():
    company = Company.draft("Acme", "IT")
    company.ensure_unique_name(company.name, exists=lambda _: False)


def test_tenant_scope_allows_superadmin():
    TenantScope.enforce(
        is_superadmin=True,
        current_user_company_id=1,
        target_company_id=99,
    )


def test_tenant_scope_denies_cross_company():
    with pytest.raises(ForbiddenError):
        TenantScope.enforce(
            is_superadmin=False,
            current_user_company_id=1,
            target_company_id=2,
        )


def test_role_policy_allows_permitted_role():
    RolePolicy.require("superadmin", ["superadmin", "admin"])


def test_role_policy_denies_forbidden_role():
    with pytest.raises(ForbiddenError):
        RolePolicy.require("employee", ["superadmin"])
