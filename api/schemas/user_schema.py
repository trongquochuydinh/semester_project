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
    role: str
    company_id: Optional[int] = None

class UserWriter(BaseModel):
    username: str
    email: str
    company_id: Optional[int] = None
    role: str

class RoleOut(BaseModel):
    name: str

class RolesResponse(BaseModel):
    roles: List[RoleOut]

class LogoutRequest(BaseModel):
    user_id: int
