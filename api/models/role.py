from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db.db_engine import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    rank: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # -------------------------
    # Relationships
    # -------------------------

    users = relationship(
        "User",
        back_populates="role",
    )
