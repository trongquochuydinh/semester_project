from typing import List

from api.domain.company import Company as DomainCompany
from api.models.company import Company as CompanyEntity
from api.schemas import CompanyDetailResponse, CompanyOut, CompaniesResponse


def company_entity_to_domain(company: CompanyEntity) -> DomainCompany:
    return DomainCompany.from_persistence(
        id=company.id,
        name=company.name,
        field=company.field or "",
    )


def company_domain_to_entity(company: DomainCompany) -> CompanyEntity:
    return CompanyEntity(
        id=company.id,
        name=company.name.value,
        field=company.field.value,
    )


def company_domain_to_out(company: DomainCompany) -> CompanyOut:
    return CompanyOut(id=company.id, name=company.name.value)


def company_domain_to_detail_response(company: DomainCompany) -> CompanyDetailResponse:
    return CompanyDetailResponse(
        id=company.id,
        name=company.name.value,
        field=company.field.value,
    )


def company_domain_to_row(company: DomainCompany) -> dict:
    return {
        "id": company.id,
        "name": company.name.value,
        "field": company.field.value,
    }


def company_list_to_response(companies: List[DomainCompany]) -> CompaniesResponse:
    return CompaniesResponse(
        companies=[company_domain_to_out(company) for company in companies]
    )
