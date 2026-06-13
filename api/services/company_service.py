from typing import List, Optional
from sqlalchemy.orm import Session

from api.domain import (
    Company as DomainCompany,
    CompanyList,
    MessageResult,
    NotFoundError,
    PaginatedCompanies,
)
from api.domain.access import RolePolicy, TenantScope
from api.domain.mappers.company_mapper import (
    company_domain_to_entity,
    company_entity_to_domain,
)
from api.models import User, Company as CompanyEntity
from api.db.company_db import (
    get_company_data_by_id as db_get_company_data_by_id,
    create_company as db_create_company,
    edit_company as db_edit_company,
    company_exists_by_name_excluding_id as db_company_exists_by_name_excluding_id,
    delete_company as db_delete_company,
    company_exists_by_name as db_company_exists_by_name,
    list_companies as db_list_companies,
)


def create_company(db: Session, current_user: User, name: str, field: str) -> MessageResult:
    RolePolicy.require(current_user.role.name, ["superadmin"])

    company = DomainCompany.draft(name, field)
    company.ensure_unique_name(
        company.name,
        exists=lambda n: db_company_exists_by_name(db, n),
    )

    db_create_company(db, company_domain_to_entity(company))

    return MessageResult(message="Company created successfully.")


def edit_company(
    db: Session, current_user: User, company_id: int, name: str, field: str
) -> MessageResult:
    RolePolicy.require(current_user.role.name, ["superadmin"])

    entity = db_get_company_data_by_id(db, company_id)
    if not entity:
        raise NotFoundError("Company not found")

    company = company_entity_to_domain(entity).update(name, field)
    company.ensure_unique_name(
        company.name,
        exists=lambda n: db_company_exists_by_name_excluding_id(
            db=db,
            name=n,
            exclude_company_id=company_id,
        ),
    )

    db_edit_company(
        db=db,
        company=entity,
        updates={
            "name": company.name.value,
            "field": company.field.value,
        },
    )

    return MessageResult(message="Company was successfully updated.")


def delete_company(db: Session, current_user: User, company_id: int) -> MessageResult:
    RolePolicy.require(current_user.role.name, ["superadmin"])

    company = db_get_company_data_by_id(db, company_id)
    if not company:
        raise NotFoundError("Company not found")

    db_delete_company(db, company)

    return MessageResult(message="Company was successfully deleted.")


def get_info_of_company(db: Session, current_user: User, company_id: int) -> DomainCompany:
    RolePolicy.require(current_user.role.name, ["superadmin"])

    company = db_get_company_data_by_id(db, company_id)
    if not company:
        raise NotFoundError("Company not found")

    return company_entity_to_domain(company)


def list_companies(db: Session, current_user: User) -> CompanyList:
    RolePolicy.require(current_user.role.name, ["superadmin", "admin", "manager"])

    companies = db_list_companies(
        db=db,
        is_superadmin=current_user.role.name == "superadmin",
        user_company_id=current_user.company_id,
    )

    return CompanyList(
        companies=[company_entity_to_domain(company) for company in companies]
    )


def assert_user_company_scope(
    *,
    is_superadmin: bool,
    current_user_company_id: int,
    target_company_id: int,
):
    TenantScope.enforce(
        is_superadmin=is_superadmin,
        current_user_company_id=current_user_company_id,
        target_company_id=target_company_id,
    )


def assert_company_access(
    db: Session,
    *,
    is_superadmin: bool,
    current_user_company_id: int,
    company_id: Optional[int],
) -> DomainCompany:
    company = db_get_company_data_by_id(db, company_id)

    if not company:
        raise NotFoundError("Company not found")

    TenantScope.enforce(
        is_superadmin=is_superadmin,
        current_user_company_id=current_user_company_id,
        target_company_id=company.id,
    )

    return company_entity_to_domain(company)


def paginate_companies(
    db: Session,
    current_user: User,
    limit: int,
    offset: int,
    filters: dict,
) -> PaginatedCompanies:
    RolePolicy.require(current_user.role.name, ["superadmin"])

    query = db.query(CompanyEntity)

    for key, value in filters.items():
        if hasattr(CompanyEntity, key):
            query = query.filter(getattr(CompanyEntity, key) == value)

    total = query.count()
    results = query.offset(offset).limit(limit).all()

    return PaginatedCompanies(
        total=total,
        data=[company_entity_to_domain(company) for company in results],
    )
