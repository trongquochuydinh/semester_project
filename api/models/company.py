from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.db.db_engine import Base

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    field = Column(String)

    users = relationship(
        "User",
        passive_deletes=True
    )

    items = relationship(
        "Item",
        passive_deletes=True
    )
