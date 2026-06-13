from pydantic import BaseModel, Field
from typing import Dict, Any


class PaginationRequest(BaseModel):
    limit: int = Field(default=10, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
    filters: Dict[str, Any] = {}

class PaginationResponse(BaseModel):
    total: int
    data: list
