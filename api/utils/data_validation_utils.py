from datetime import datetime
from decimal import Decimal
from email.utils import parseaddr
from fastapi import HTTPException

from api.schemas.item_schema import ItemWriter
from api.schemas.user_schema import UserWriter

from api.models import Item

def normalize_string(value: str, field_name: str) -> str:
    if value is None:
        raise HTTPException(422, f"{field_name} is required")

    if not isinstance(value, str):
        raise HTTPException(422, f"{field_name} must be a string")

    value = value.strip()
    if not value:
        raise HTTPException(422, f"{field_name} cannot be empty")

    return value

def start_of_day(dt: datetime) -> datetime:
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)

def end_of_day(dt: datetime) -> datetime:
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)

def validate_user_data(data: UserWriter):
    username = normalize_string(data.username, "Username")
    email = normalize_string(data.email, "Email").lower()
    role_name = normalize_string(data.role, "Role")

    if not username:
        raise HTTPException(422, "Username is required")

    if not email:
        raise HTTPException(422, "Email is required")

    if not role_name:
        raise HTTPException(422, "Role is required")

    if not data.company_id:
        raise HTTPException(422, "Company is required")
    
    if not is_valid_email(email):
        raise HTTPException(422, "Invalid email format")
    
def validate_company_data(data):
    name = normalize_string(data.name, "Company name")
    field = normalize_string(data.field, "Field")

    if not name:
        raise HTTPException(422, "Username is required")
    
    if not field:
        raise HTTPException(422, "Field is required")

def is_valid_email(email: str) -> bool:
    name, addr = parseaddr(email)
    return "@" in addr

def validate_item_data(data: ItemWriter):
    name = normalize_string(data.name, "Item name")

    price, quantity = validate_item_numbers(
        data.price,
        data.quantity,
    )

    return name, price, quantity

def validate_item_numbers(price_raw, quantity_raw):
    try:
        price = Decimal(price_raw)
    except Exception:
        raise HTTPException(422, "Invalid price")

    try:
        quantity = int(quantity_raw)
    except Exception:
        raise HTTPException(422, "Invalid quantity")

    if price < 0:
        raise HTTPException(422, "Price must be >= 0")

    if quantity < 0:
        raise HTTPException(422, "Quantity must be >= 0")

    return price, quantity

def validate_order_type(order_type_raw: str):
    order_type = normalize_string(order_type_raw, "order_type")
    if order_type not in ["sale", "restock"]:
        raise HTTPException(422, "Order type must be sale or restock")
    return order_type.lower()

def validate_order_item(
    *,
    item: Item,
    quantity: int,
    order_type: str,
):
    if not item.is_active:
        raise HTTPException(
            status_code=409,
            detail=f"Item '{item.name}' is disabled"
        )

    if quantity <= 0:
        raise HTTPException(
            status_code=422,
            detail="Quantity must be greater than zero"
        )

    if order_type == "sale" and quantity > item.quantity:
        raise HTTPException(
            status_code=403,
            detail=f"Insufficient stock for '{item.name}'"
        )

    return {
        "item": item,
        "quantity": quantity,
        "unit_price": item.price,
    }
