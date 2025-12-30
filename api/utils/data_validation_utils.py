from decimal import Decimal
from email.utils import parseaddr
from fastapi import HTTPException

from api.schemas.item_schema import ItemWriter
from api.schemas.user_schema import UserWriter


def normalize_string(value: str, field_name: str) -> str:
    if value is None:
        raise HTTPException(400, f"{field_name} is required")

    if not isinstance(value, str):
        raise HTTPException(400, f"{field_name} must be a string")

    value = value.strip()
    if not value:
        raise HTTPException(400, f"{field_name} cannot be empty")

    return value

def validate_user_data(data: UserWriter):
    username = normalize_string(data.username, "Username")
    email = normalize_string(data.email, "Email").lower()
    role_name = normalize_string(data.role, "Role")

    if not username:
        raise HTTPException(400, "Username is required")

    if not email:
        raise HTTPException(400, "Email is required")

    if not role_name:
        raise HTTPException(400, "Role is required")

    if not data.company_id:
        raise HTTPException(400, "Company is required")
    
    if not is_valid_email(email):
        raise HTTPException(400, "Invalid email format")

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
        raise HTTPException(400, "Invalid price")

    try:
        quantity = int(quantity_raw)
    except Exception:
        raise HTTPException(400, "Invalid quantity")

    if price < 0:
        raise HTTPException(400, "Price must be >= 0")

    if quantity < 0:
        raise HTTPException(400, "Quantity must be >= 0")

    return price, quantity