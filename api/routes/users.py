from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from api.models.user import verify_user

router = APIRouter(prefix="/api", tags=["users"])

class LoginRequest(BaseModel):
    identifier: str  # username or email
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    company_id: Optional[int] = None
    roles: List[str]

@router.post("/login", response_model=UserResponse)
def login(data: LoginRequest):
    user = verify_user(data.identifier, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Get roles as a list of strings
    roles = [ur.role.name for ur in user.roles]
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        company_id=user.company_id,
        roles=roles
    )
