from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from api.domain.exceptions import ConflictError, ForbiddenError, ValidationError


class OrderType(str, Enum):
    SALE = "sale"
    RESTOCK = "restock"

    @classmethod
    def from_raw(cls, raw: str) -> "OrderType":
        if not raw or not str(raw).strip():
            raise ValidationError("Order type is required")
        normalized = str(raw).strip().lower()
        if normalized not in ("sale", "restock"):
            raise ValidationError("Order type must be sale or restock")
        return cls(normalized)


class OrderStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class StockAdjustment:
    item_id: int
    delta: int


@dataclass(frozen=True)
class OrderLineItem:
    item_id: int
    name: str
    quantity: int
    unit_price: Decimal

    @classmethod
    def from_request(
        cls,
        *,
        item_id: int,
        name: str,
        quantity: int,
        unit_price: Decimal,
        is_active: bool,
        available_quantity: int,
        order_type: OrderType,
    ) -> "OrderLineItem":
        if quantity <= 0:
            raise ValidationError("Quantity must be greater than zero")
        if not is_active:
            raise ConflictError(f"Item '{name}' is disabled")
        if order_type == OrderType.SALE and quantity > available_quantity:
            raise ForbiddenError(f"Insufficient stock for '{name}'")
        return cls(
            item_id=item_id,
            name=name,
            quantity=quantity,
            unit_price=unit_price,
        )


@dataclass
class Order:
    id: Optional[int]
    status: OrderStatus
    order_type: OrderType
    user_id: int
    company_id: int
    lines: List[OrderLineItem] = field(default_factory=list)
    created_at_fmt: Optional[str] = None
    completed_at_fmt: Optional[str] = None

    @classmethod
    def draft(cls, order_type: str, user_id: int, company_id: int) -> "Order":
        return cls(
            id=None,
            status=OrderStatus.PENDING,
            order_type=OrderType.from_raw(order_type),
            user_id=user_id,
            company_id=company_id,
        )

    def add_line(self, line: OrderLineItem) -> None:
        self.lines.append(line)

    def create_stock_adjustments(self) -> List[StockAdjustment]:
        if self.order_type == OrderType.SALE:
            return [
                StockAdjustment(item_id=line.item_id, delta=-line.quantity)
                for line in self.lines
            ]
        return []

    def cancel(self) -> List[StockAdjustment]:
        if self.status == OrderStatus.CANCELLED:
            raise ConflictError("Order is already cancelled")
        if self.status == OrderStatus.COMPLETED:
            raise ConflictError("Completed orders cannot be cancelled")

        self.status = OrderStatus.CANCELLED
        adjustments: List[StockAdjustment] = []
        for line in self.lines:
            if self.order_type == OrderType.SALE:
                adjustments.append(StockAdjustment(line.item_id, line.quantity))
            elif self.order_type == OrderType.RESTOCK:
                adjustments.append(StockAdjustment(line.item_id, -line.quantity))
        return adjustments

    def complete(self) -> List[StockAdjustment]:
        if self.status == OrderStatus.CANCELLED:
            raise ConflictError("Order is already cancelled")
        if self.status == OrderStatus.COMPLETED:
            raise ConflictError("Completed orders cannot be cancelled")

        self.status = OrderStatus.COMPLETED
        if self.order_type == OrderType.RESTOCK:
            return [
                StockAdjustment(item_id=line.item_id, delta=line.quantity)
                for line in self.lines
            ]
        return []


@dataclass(frozen=True)
class PaginatedOrders:
    total: int
    data: List[Order]


@dataclass(frozen=True)
class PaginatedOrderItems:
    total: int
    data: List[OrderLineItem]


@dataclass(frozen=True)
class OrderStatusCounts:
    pending: int
    completed: int
    cancelled: int

    def as_dict(self) -> dict:
        return {
            "pending": self.pending,
            "completed": self.completed,
            "cancelled": self.cancelled,
        }
