from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db.db_engine import Base


class UserOAuthAccount(Base):
    """
    OAuth account model for external authentication provider integration.

    Links user accounts to external OAuth providers (GitHub, Google, etc.) to enable
    social login and account linking functionality. Each record represents one
    external authentication method linked to an internal user account.

    Features:
        - Multiple OAuth providers per user support
        - Provider-specific user identification
        - Email verification and account matching
        - Account linking timestamp tracking
        - Cascade deletion with parent user account

    OAuth Flow Integration:
        1. User initiates OAuth login with provider
        2. Provider redirects with authorization code
        3. System exchanges code for access token
        4. System fetches user profile from provider
        5. System creates/updates UserOAuthAccount record
        6. User authenticated via linked account

    Security Design:
        - Provider user IDs prevent account takeover
        - Email verification enables account matching
        - Multiple providers supported per user (GitHub + Google)
        - Automatic cleanup when user account deleted
    """
    __tablename__ = "user_oauth_accounts"

    # --- Primary Key ---
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,                     # Index for efficient lookups
    )

    # --- User Association ---
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),  # Delete when user deleted
        nullable=False,
        index=True,                     # Index for user lookup queries
    )

    # --- OAuth Provider Information ---
    provider: Mapped[str] = mapped_column(
        String,
        nullable=False,                 # OAuth provider name (github, google, microsoft, etc.)
    )

    provider_user_id: Mapped[str] = mapped_column(
        String,
        nullable=False,                 # User's unique ID from OAuth provider
    )

    provider_email: Mapped[str] = mapped_column(
        String,
        nullable=True,                  # User's email from OAuth provider (may be private)
    )

    # --- Metadata ---
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,        # When this OAuth link was created
        nullable=False,
    )

    # -------------------------
    # Relationships
    # -------------------------

    user = relationship(
        "User",
        back_populates="oauth_accounts", # Access parent user account
    )

# --- OAuth Integration Design Notes ---
# Provider Support:
# - Common providers: github, google, microsoft, facebook, twitter
# - provider field stores lowercase provider identifier
# - Extensible to add new OAuth providers without schema changes
#
# Account Linking:
# - Users can link multiple OAuth providers to one account
# - Each provider+user combination should be unique (add unique constraint)
# - provider_email enables account matching during signup
# - Supports both new user creation and existing account linking
#
# Security Considerations:
# - provider_user_id prevents account hijacking through email spoofing
# - Email may be None if user's email is private on provider
# - Account matching should validate email across providers
# - Consider rate limiting OAuth attempts to prevent abuse
#
# Data Privacy:
# - Only essential OAuth data stored (no access tokens)
# - Access tokens used temporarily for profile fetch, then discarded
# - Provider email stored for account verification only
# - Users maintain control over linked providers
#
# Business Logic:
# - Login: Check if OAuth account exists, authenticate user
# - Linking: Add OAuth account to existing authenticated user
