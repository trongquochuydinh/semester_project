# Import validation utilities
from datetime import datetime
from decimal import Decimal
from email.utils import parseaddr
from fastapi import HTTPException

# Import schemas and models for validation
from api.schemas.item_schema import ItemWriter
from api.schemas.user_schema import UserWriter
from api.models import Item

def normalize_string(value: str, field_name: str) -> str:
    """
    Sanitize and validate string input with error handling.
    
    Ensures string fields are properly formatted and not empty
    with descriptive error messages.
    
    Args:
        value: Input string to normalize
        field_name: Field name for error messages
        
    Returns:
        str: Trimmed, validated string
        
    Raises:
        HTTPException: For null, non-string, or empty values
    """
    if value is None:
        raise HTTPException(422, f"{field_name} is required")

    if not isinstance(value, str):
        raise HTTPException(422, f"{field_name} must be a string")

    value = value.strip()
    if not value:
        raise HTTPException(422, f"{field_name} cannot be empty")

    return value

def start_of_day(dt: datetime) -> datetime:
    """Set datetime to beginning of day (00:00:00.000)."""
    return dt.replace(hour=0, minute=0, second=0, microsecond=0)

def end_of_day(dt: datetime) -> datetime:
    """Set datetime to end of day (23:59:59.999)."""
    return dt.replace(hour=23, minute=59, second=59, microsecond=999999)

def validate_user_data(data: UserWriter):
    """
    Validate user creation/edit data with comprehensive checks.
    
    Ensures all required user fields are present and properly formatted
    including username, email, role, and company assignment.
    
    Args:
        data: User data from request (UserCreateRequest or UserEditRequest)
        
    Raises:
        HTTPException: For missing, invalid, or improperly formatted data
        
    Validation includes:
        - Required field presence
        - Email format validation
        - String field normalization
        - Company assignment validation
    """
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
    """
    Validate company creation/edit data.
    
    Ensures company name and business field are properly specified
    for multi-tenant organization setup.
    
    Args:
        data: Company data from request
        
    Raises:
        HTTPException: For missing or invalid company information
    """
    name = normalize_string(data.name, "Company name")
    field = normalize_string(data.field, "Field")

    if not name:
        raise HTTPException(422, "Company name is required")
    
    if not field:
        raise HTTPException(422, "Field is required")

def is_valid_email(email: str) -> bool:
    """
    Validate email format using standard parsing.
    
    Uses email.utils.parseaddr for RFC-compliant email validation
    with basic format checking.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if email format is valid
    """
    name, addr = parseaddr(email)
    return "@" in addr

def validate_item_data(data: ItemWriter):
    """
    Validate item creation/edit data including pricing and inventory.
    
    Ensures product information is properly formatted with valid
    pricing and quantity values.
    
    Args:
        data: Item data from request
        
    Returns:
        tuple: (name, price, quantity) - validated and converted values
        
    Validation includes:
        - Product name normalization
        - Price conversion to Decimal for accuracy
        - Quantity conversion to integer
        - Non-negative value constraints
    """
    name = normalize_string(data.name, "Item name")

    price, quantity = validate_item_numbers(
        data.price,
        data.quantity,
    )

    return name, price, quantity

def validate_item_numbers(price_raw, quantity_raw):
    """
    Validate and convert item pricing and inventory numbers.
    
    Converts string inputs to appropriate numeric types with
    business rule validation.
    
    Args:
        price_raw: Raw price input (string or number)
        quantity_raw: Raw quantity input (string or number)
        
    Returns:
        tuple: (Decimal price, int quantity) - validated values
        
    Raises:
        HTTPException: For invalid formats or negative values
    """
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
    """
    Validate and normalize order type designation.
    
    Ensures order type is one of the allowed values for
    proper order processing workflow.
    
    Args:
        order_type_raw: Raw order type input
        
    Returns:
        str: Normalized order type ('sale' or 'restock')
        
    Raises:
        HTTPException: For invalid order type values
        
    Business rules:
        - 'sale': Customer purchase (decreases inventory)
        - 'restock': Inventory replenishment (increases inventory)
    """
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
    """
    Validate individual order item with inventory and business rules.
    
    Ensures ordered items are available, active, and quantities
    are sufficient for the requested operation.
    
    Args:
        item: Product item from database
        quantity: Requested quantity
        order_type: Type of order (sale/restock)
        
    Returns:
        dict: Validated item data with pricing
        
    Raises:
        HTTPException: For inactive items, invalid quantities, or insufficient stock
        
    Business rules:
        - Items must be active for ordering
        - Quantities must be positive
        - Sales require sufficient inventory
        - Current pricing captured for historical accuracy
    """
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
        "unit_price": item.price,  # Capture current pricing
    }
