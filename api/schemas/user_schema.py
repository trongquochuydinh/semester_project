from pydantic import BaseModel
from typing import List, Optional


class UserWriter(BaseModel):
    username: str
    email: str
    company_id: Optional[int] = None
    role: str


class UserCreateResponse(BaseModel):
    message: str
    initial_password: str


class UserCreateRequest(UserWriter):
    pass


class UserEditRequest(UserWriter):
    pass


class UserEditResponse(UserWriter):
    pass


class UserGetResponse(UserWriter):
    pass


class UserCountResponse(BaseModel):
    total_users: int
    online_users: int


class RoleOut(BaseModel):
    name: str


class RolesResponse(BaseModel):
    roles: List[RoleOut]
