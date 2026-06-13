from dataclasses import dataclass, replace
from typing import Callable, List, Optional

from api.domain.exceptions import ConflictError
from api.domain.value_objects import BusinessField, CompanyName


@dataclass(frozen=True)
class Company:
    id: Optional[int]
    name: CompanyName
    field: BusinessField

    @classmethod
    def draft(cls, name: str, field: str) -> "Company":
        return cls(
            id=None,
            name=CompanyName.from_raw(name),
            field=BusinessField.from_raw(field),
        )

    @classmethod
    def from_persistence(cls, id: int, name: str, field: Optional[str]) -> "Company":
        return cls(
            id=id,
            name=CompanyName.from_raw(name),
            field=BusinessField.from_optional(field),
        )

    def update(self, name: str, field: str) -> "Company":
        return replace(
            self,
            name=CompanyName.from_raw(name),
            field=BusinessField.from_raw(field),
        )

    def ensure_unique_name(
        self,
        name: CompanyName,
        *,
        exists: Callable[[str], bool],
    ) -> None:
        if exists(name.normalized):
            raise ConflictError("Company with this name already exists")


@dataclass(frozen=True)
class CompanyList:
    companies: List[Company]


@dataclass(frozen=True)
class PaginatedCompanies:
    total: int
    data: List[Company]
