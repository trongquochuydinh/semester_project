from decimal import Decimal
from pydantic import BaseModel


class ItemWriter(BaseModel):
    name: str
    price: Decimal
    quantity: int

class ItemCreationRequest(ItemWriter):
    pass

class ItemGetResponse(ItemWriter):
    pass

class ItemEditRequest(ItemWriter):
    pass

class ItemEditResponse(ItemWriter):
    pass