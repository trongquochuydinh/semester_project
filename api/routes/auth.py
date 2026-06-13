from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from api.dependencies import get_current_user, get_db
from api.models.user import User
from api.schemas import LoginRequest, LoginResponse, MessageResponse
from api.schemas.auth_schema import OAuthExchangeRequest
from api.services import login_user, logout_user
from api.services.auth_service import (
    exchange_oauth_code,
    handle_github_callback,
    start_github_link,
    start_github_login,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login_user_endpoint(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    return login_user(request.identifier, request.password, db)


@router.post("/logout", response_model=MessageResponse)
def logout_user_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return logout_user(current_user, db)


@router.get("/github/login")
def github_login():
    redirect_url = start_github_login()
    return {"redirect_url": redirect_url}


@router.get("/github/link")
def link_github_account(
    current_user=Depends(get_current_user),
):
    redirect_url = start_github_link(current_user.id)
    return {"redirect_url": redirect_url}


@router.get("/github/callback")
def github_callback(
    code: str,
    state: str,
    db: Session = Depends(get_db),
):
    redirect_url = handle_github_callback(code, state, db)
    return RedirectResponse(url=redirect_url)


@router.post("/oauth/exchange", response_model=LoginResponse)
def oauth_exchange_endpoint(
    request: OAuthExchangeRequest,
):
    return exchange_oauth_code(request.code)
