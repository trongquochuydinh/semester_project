from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Boolean,
    ForeignKey,
    DateTime,
    func
)
from sqlalchemy.orm import relationship

from api.db.db_engine import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False)
    sku = Column(String, nullable=False)

    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)

    is_active = Column(Boolean, nullable=False, default=True)

    company_id = Column(
        Integer,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False
    )

    # relationships
    company = relationship("Company")
