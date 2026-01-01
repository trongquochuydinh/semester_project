from sqlalchemy import (
    Column,
    Integer,
    Text,
    TIMESTAMP,
    ForeignKey,
    CheckConstraint,
    func
)
from sqlalchemy.orm import relationship
from api.db.db_engine import Base  # adjust import to your project


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    status = Column(Text, nullable=False, server_default="pending")

    order_type = Column(Text, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())

    completed_at = Column(TIMESTAMP, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    company_id = Column(Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'completed', 'cancelled')",
            name="orders_status_check"
        ),
        CheckConstraint(
            "order_type IN ('sale', 'restock')",
            name="orders_order_type_check"
        ),
    )

    # Relationships (optional but recommended)
    user = relationship("User")
    company = relationship("Company")
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )
