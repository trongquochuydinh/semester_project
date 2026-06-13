from dataclasses import dataclass
from decimal import Decimal
from email.utils import parseaddr
from typing import List, Optional

from api.domain.exceptions import ForbiddenError, ValidationError


@dataclass(frozen=True)
class CompanyName:
    value: str

    @classmethod
    def from_raw(cls, raw: str) -> "CompanyName":
        if not raw or not raw.strip():
            raise ValidationError("Company name is required")
        return cls(value=raw.strip())

    @property
    def normalized(self) -> str:
        return self.value.lower()


@dataclass(frozen=True)
class BusinessField:
    value: str

    @classmethod
    def from_raw(cls, raw: str) -> "BusinessField":
        if not raw or not raw.strip():
            raise ValidationError("Field is required")
        return cls(value=raw.strip())

    @classmethod
    def from_optional(cls, raw: Optional[str]) -> "BusinessField":
        if not raw or not raw.strip():
            return cls(value="")
        return cls(value=raw.strip())


@dataclass(frozen=True)
class ItemName:
    value: str

    @classmethod
    def from_raw(cls, raw: str) -> "ItemName":
        if not raw or not raw.strip():
            raise ValidationError("Item name is required")
        return cls(value=raw.strip())


@dataclass(frozen=True)
class Money:
    value: Decimal

    @classmethod
    def from_raw(cls, raw) -> "Money":
        try:
            price = Decimal(raw)
        except Exception:
            raise ValidationError("Invalid price")
        if price < 0:
            raise ValidationError("Price must be >= 0")
        return cls(value=price)


@dataclass(frozen=True)
class Quantity:
    value: int

    @classmethod
    def from_raw(cls, raw) -> "Quantity":
        try:
            quantity = int(raw)
        except Exception:
            raise ValidationError("Invalid quantity")
        if quantity < 0:
            raise ValidationError("Quantity must be >= 0")
        return cls(value=quantity)


@dataclass(frozen=True)
class Username:
    value: str

    @classmethod
    def from_raw(cls, raw: str) -> "Username":
        if not raw or not raw.strip():
            raise ValidationError("Username is required")
        return cls(value=raw.strip())


@dataclass(frozen=True)
class Email:
    value: str

    @classmethod
    def from_raw(cls, raw: str) -> "Email":
        if not raw or not raw.strip():
            raise ValidationError("Email is required")
        normalized = raw.strip().lower()
        _, addr = parseaddr(normalized)
        if "@" not in addr:
            raise ValidationError("Invalid email format")
        return cls(value=normalized)
