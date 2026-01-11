from sqlalchemy.orm import Session
from api.models.oauth import UserOAuthAccount

def get_oauth_account_by_provider_user_id(
    db: Session,
    provider: str,
    provider_user_id: str,
):
    return (
        db.query(UserOAuthAccount)
        .filter_by(
            provider=provider,
            provider_user_id=provider_user_id,
        )
        .first()
    )


def create_oauth_account(
    db: Session,
    *,
    user_id: int,
    provider: str,
    provider_user_id: str,
    provider_email: str,
):
    oauth = UserOAuthAccount(
        user_id=user_id,
        provider=provider,
        provider_user_id=provider_user_id,
        provider_email=provider_email,
    )
    db.add(oauth)
    db.commit()
    return oauth
