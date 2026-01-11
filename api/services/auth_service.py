from typing import Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from api.config import GITHUB_CLIENT_ID, GITHUB_REDIRECT_URI
from api.db.oauth_db import (
    create_oauth_account,
    get_oauth_account_by_provider_user_id,
)
from api.db.user_db import (
    clear_login_session,
    establish_login_session,
    get_user_by_identifier as db_get_user_by_identifier,
    get_user_data_by_id as db_get_user_data_by_id,
    get_oauth_providers,
)
from api.integrations.github_client import (
    exchange_code_for_token,
    fetch_user,
)
from api.models.user import User
from api.schemas import LoginResponse, MessageResponse
from api.schemas.user_schema import OAuthInfo
from api.utils import (
    create_access_token,
    verify_password,
    create_oauth_state,
    UserAlreadyLoggedInError,
    InvalidCredentialsError,
    UserDisabledError,
)
from api.utils.auth_utils import consume_oauth_state, oauth_error_redirect


# =====================================================
# Shared login core
# =====================================================

def login_user_object(user: User, db: Session) -> LoginResponse:
    """
    Issue session + JWT + LoginResponse for an already authenticated user.
    Used by password login and OAuth login.
    """
    session_id = establish_login_session(user)

    token = create_access_token(
        user.id,
        user.role.name,
        session_id=session_id,
    )

    providers = get_oauth_providers(db, user.id)

    return LoginResponse(
        access_token=token,
        token_type="bearer",
        id=user.id,
        username=user.username,
        role=user.role.name,
        company_id=user.company_id,
        oauth_info=OAuthInfo(
            github="github" in providers
        ),
    )


# =====================================================
# Password login
# =====================================================

def login_user(identifier: str, password: str, db: Session) -> LoginResponse:
    try:
        user = verify_user(identifier, password, db)
    except UserDisabledError:
        raise HTTPException(403, "This account has been disabled")
    except InvalidCredentialsError:
        raise HTTPException(406, "Invalid username or password")

    try:
        return login_user_object(user, db)
    except UserAlreadyLoggedInError:
        raise HTTPException(409, "User is already logged in elsewhere")


def verify_user(identifier: str, password: str, db: Session) -> User:
    user = db_get_user_by_identifier(db, identifier)
    if not user:
        raise InvalidCredentialsError()

    if not verify_password(password, user.password_hash):
        raise InvalidCredentialsError()

    if not user.is_active:
        raise UserDisabledError()

    return user


# =====================================================
# Logout
# =====================================================

def logout_user(current_user: User, db: Session) -> MessageResponse:
    clear_login_session(current_user)
    return MessageResponse(
        message="User logged out successfully"
    )


# =====================================================
# GitHub OAuth – start flows
# =====================================================

def start_github_login() -> str:
    """
    Start GitHub OAuth flow for LOGIN (no session).
    """
    state = create_oauth_state(user_id=None)

    return (
        "https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={GITHUB_REDIRECT_URI}"
        "&scope=read:user user:email"
        f"&state={state}"
    )


def start_github_link(user_id: int) -> str:
    """
    Start GitHub OAuth flow for LINKING an existing user.
    """
    state = create_oauth_state(user_id)

    return (
        "https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={GITHUB_REDIRECT_URI}"
        "&scope=read:user user:email"
        f"&state={state}"
    )


# =====================================================
# GitHub OAuth callback (LOGIN + LINK)
# =====================================================

def handle_github_callback(code: str, state: str, db: Session) -> str:
    """
    Handle GitHub OAuth callback.
    Returns redirect URL for the web_app.
    """
    user_id: Optional[int] = consume_oauth_state(state)

    access_token = exchange_code_for_token(code)
    github_user = fetch_user(access_token)

    github_id = str(github_user["id"])
    github_email = str(github_user.get("email"))

    oauth_account = get_oauth_account_by_provider_user_id(
        db,
        provider="github",
        provider_user_id=github_id,
    )

    # -------------------------
    # LOGIN FLOW
    # -------------------------
    if user_id is None:
        if not oauth_account:
            return oauth_error_redirect(
                "GitHub account is not linked to any user"
            )

        user = db_get_user_data_by_id(db, oauth_account.user_id)
        if not user or not user.is_active:
            return oauth_error_redirect(
                "User account is disabled"
            )

        try:
            login_response = login_user_object(user, db)
        except UserAlreadyLoggedInError:
            return oauth_error_redirect(
                "User is already logged in elsewhere"
            )

        return (
            "http://localhost:8000/auth/oauth-success"
            f"?token={login_response.access_token}"
        )

    # -------------------------
    # LINK FLOW
    # -------------------------
    if oauth_account:
        return oauth_error_redirect("GitHub account already linked")

    create_oauth_account(
        db,
        user_id=user_id,
        provider="github",
        provider_user_id=github_id,
        provider_email=github_email,
    )

    return "http://localhost:8000/auth/oauth-linked"
