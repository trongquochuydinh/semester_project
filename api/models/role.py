from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from api.db.db_engine import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    rank = Column(Integer, nullable=False, index=True)

    users = relationship("User", back_populates="role")
