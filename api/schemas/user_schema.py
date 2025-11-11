from pydantic import BaseModel
from typing import List, Optional

class LoginRequest(BaseModel):
    identifier: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    email: str
    company_id: Optional[int] = None
    role_id: int

class RoleOut(BaseModel):
    id: int
    name: str

class RolesResponse(BaseModel):
    roles: List[RoleOut]

class LogoutRequest(BaseModel):
    user_id: int
