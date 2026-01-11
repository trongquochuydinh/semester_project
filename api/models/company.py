from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.db.db_engine import Base


class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,
    )

    field: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    # -------------------------
    # Relationships
    # -------------------------

    users = relationship(
        "User",
        back_populates="company",
        cascade="all, delete-orphan",
    )

    items = relationship(
        "Item",
        back_populates="company",
        cascade="all, delete-orphan",
    )

    orders = relationship(
        "Order",
        back_populates="company",
        cascade="all, delete-orphan",
    )
