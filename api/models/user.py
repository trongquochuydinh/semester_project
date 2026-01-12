from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from api.db.db_engine import Base


class User(Base):
    """
    User model for authentication, authorization, and user management.
    
    Supports multiple authentication methods (password + OAuth) with role-based
    access control and multi-tenant company association.
    
    Features:
        - Username/email + password authentication
        - OAuth provider integration (GitHub, etc.)
        - Role-based permissions system
        - Session management for security
        - Multi-tenant company association
        - Account status tracking (active/inactive)
        - Login activity monitoring
    """
    __tablename__ = "users"

    # --- Primary Key ---
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,                      # Index for efficient lookups
    )

    # --- Authentication Fields ---
    username: Mapped[str] = mapped_column(
        String,
        unique=True,                     # Enforce username uniqueness
        nullable=False,
        index=True,                      # Index for login lookups
    )

    email: Mapped[str] = mapped_column(
        String,
        unique=True,                     # Enforce email uniqueness
        nullable=False,
        index=True,                      # Index for login lookups
    )

    password_hash: Mapped[str] = mapped_column(
        String,
        nullable=False,                  # Hashed password (never store plaintext)
    )

    # --- Session and Status Management ---
    status: Mapped[str] = mapped_column(
        String,
        default="offline",               # Track online/offline status
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,                    # Soft delete: False = disabled account
    )

    last_login: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,                   # Null for users who never logged in
    )

    session_id: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,                   # Unique session identifier for security
    )

    # --- Multi-tenant Association ---
    company_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),  # Delete user if company deleted
        nullable=True,                   # Allow users without company (system users)
    )

    # --- Authorization ---
    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("roles.id"),          # Link to role for permissions
        nullable=False,                  # Every user must have a role
    )

    # -------------------------
    # Relationships
    # -------------------------

    role = relationship(
        "Role",
        back_populates="users",          # Access user's role and permissions
    )

    company = relationship(
        "Company",
        back_populates="users",          # Access user's company context
        passive_deletes=True,            # Handle CASCADE delete efficiently
    )

    orders = relationship(
        "Order",
        back_populates="user",           # Access orders created by this user
    )

    oauth_accounts = relationship(
        "UserOAuthAccount",
        back_populates="user",           # Access linked OAuth providers
        cascade="all, delete-orphan",    # Delete OAuth links when user deleted
    )


