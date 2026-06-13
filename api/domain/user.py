from dataclasses import dataclass
from typing import List, Optional

from api.domain.exceptions import ValidationError
from api.domain.value_objects import Email, Username


@dataclass(frozen=True)
class UserDraft:
    username: Username
    email: Email
    company_id: int
    role_name: str

    @classmethod
    def from_raw(
        cls,
        username: str,
        email: str,
        company_id: Optional[int],
        role: str,
    ) -> "UserDraft":
        if not company_id:
            raise ValidationError("Company is required")
        role_name = role.strip().lower() if role else ""
        if not role_name:
            raise ValidationError("Role is required")
        return cls(
            username=Username.from_raw(username),
            email=Email.from_raw(email),
            company_id=company_id,
            role_name=role_name,
        )


@dataclass(frozen=True)
class UserProfile:
    username: str
    email: str
    company_id: int
    role: str


@dataclass(frozen=True)
class CreateUserResult:
    message: str
    initial_password: str


@dataclass(frozen=True)
class UserStats:
    total_users: int
    online_users: int


@dataclass(frozen=True)
class CurrentUserProfile:
    id: int
    username: str
    role: str
    company_id: Optional[int]
    oauth_github: bool


@dataclass(frozen=True)
class PaginatedUsers:
    total: int
    data: List[dict]
