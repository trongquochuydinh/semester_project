from decimal import Decimal
from pydantic import BaseModel
from typing import List

class OrderCreateRequest(BaseModel):
    order_type: str
    list_of_items: List[dict]