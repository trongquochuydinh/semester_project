from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional

from api.db.db_engine import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    username: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String,
        default="offline",
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    last_login: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
    )

    session_id: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    company_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=True,
    )

    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("roles.id"),
        nullable=False,
    )

    # -------------------------
    # Relationships
    # -------------------------

    role = relationship(
        "Role",
        back_populates="users",
    )

    company = relationship(
        "Company",
        back_populates="users",
        passive_deletes=True,
    )

    orders = relationship(
        "Order",
        back_populates="user",
    )

    oauth_accounts = relationship(
        "UserOAuthAccount",
        back_populates="user",
        cascade="all, delete-orphan",
    )

