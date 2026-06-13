import re
from dataclasses import dataclass, replace
from typing import List, Optional
from uuid import uuid4

from api.domain.exceptions import ConflictError, ForbiddenError
from api.domain.value_objects import ItemName, Money, Quantity


class SkuGenerator:
    @staticmethod
    def generate(name: str) -> str:
        base = re.sub(r"[^A-Z0-9]", "", name.upper())
        base = base[:8] if base else "ITEM"
        return f"{base}-{uuid4().hex[:6].upper()}"


@dataclass(frozen=True)
class Item:
    id: Optional[int]
    name: ItemName
    sku: str
    price: Money
    quantity: Quantity
    company_id: int
    is_active: bool = True
    company_name: Optional[str] = None

    @classmethod
    def draft(
        cls,
        name: str,
        price,
        quantity,
        company_id: int,
    ) -> "Item":
        item_name = ItemName.from_raw(name)
        return cls(
            id=None,
            name=item_name,
            sku=SkuGenerator.generate(item_name.value),
            price=Money.from_raw(price),
            quantity=Quantity.from_raw(quantity),
            company_id=company_id,
            is_active=True,
        )

    @classmethod
    def from_persistence(
        cls,
        *,
        id: int,
        name: str,
        sku: str,
        price,
        quantity: int,
        company_id: int,
        is_active: bool,
        company_name: Optional[str] = None,
    ) -> "Item":
        return cls(
            id=id,
            name=ItemName.from_raw(name),
            sku=sku,
            price=Money.from_raw(price),
            quantity=Quantity.from_raw(quantity),
            company_id=company_id,
            is_active=is_active,
            company_name=company_name,
        )

    def update(self, name: str, price, quantity) -> "Item":
        return replace(
            self,
            name=ItemName.from_raw(name),
            price=Money.from_raw(price),
            quantity=Quantity.from_raw(quantity),
        )

    def toggle_active(self) -> "Item":
        return replace(self, is_active=not self.is_active)

    def can_fulfill(self, requested_quantity: int, order_type: str) -> None:
        if not self.is_active:
            raise ConflictError(f"Item '{self.name.value}' is disabled")

        if requested_quantity <= 0:
            raise ForbiddenError("Quantity must be greater than zero")

        if order_type == "sale" and requested_quantity > self.quantity.value:
            raise ForbiddenError(
                f"Insufficient stock for '{self.name.value}'"
            )


@dataclass(frozen=True)
class PaginatedItems:
    total: int
    data: List[Item]
