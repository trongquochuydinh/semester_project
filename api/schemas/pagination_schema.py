from pydantic import BaseModel
from typing import Dict, Any


class PaginationRequest(BaseModel):
    limit: int = 10
    offset: int = 0
    filters: Dict[str, Any] = {}