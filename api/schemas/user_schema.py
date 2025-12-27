from pydantic import BaseModel
from typing import List, Optional

# TODO: move login and logout schemas to auth_schema.py

class LoginRequest(BaseModel):
    identifier: str
    password: str

class LoginResponse(BaseModel):
    id: int
    username: str
    access_token: str
    token_type: str
    role: str
    company_id: Optional[int] = None

class LogoutRequest(BaseModel):
    user_id: int

class UserCreationResponse(BaseModel):
    message: str
    initial_password: str

class UserWriter(BaseModel):
    username: str
    email: str
    company_id: Optional[int] = None
    role: str

class UserCreateRequest(UserWriter):
    pass

class UserEditRequest(UserWriter):
    pass

class UserGetRequest(UserWriter):
    pass

class RoleOut(BaseModel):
    name: str

class RolesResponse(BaseModel):
    roles: List[RoleOut]
