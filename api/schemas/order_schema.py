from decimal import Decimal
from pydantic import BaseModel
from typing import List

class OrderCreateRequest(BaseModel):
    order_type: str
    items: List[dict]