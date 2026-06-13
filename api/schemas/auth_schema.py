from datetime import datetime
from typing import Optional, TypedDict

from pydantic import BaseModel


class LoginRequest(BaseModel):
    identifier: str
    password: str


class OAuthInfo(BaseModel):
    github: bool = False


class OAuthStateData(TypedDict):
    user_id: Optional[int]
    expires_at: datetime


class LoginResponse(BaseModel):
    id: int
    username: str
    access_token: str
    token_type: str
    role: str
    company_id: Optional[int] = None
    oauth_info: OAuthInfo


class LogoutRequest(BaseModel):
    user_id: int


class OAuthExchangeRequest(BaseModel):
    code: str
