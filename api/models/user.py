from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from api.db.db_engine import Base



class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="role")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)

    status = Column(String, default="offline", nullable=False)
    last_login = Column(DateTime, nullable=True)

    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    role = relationship("Role", back_populates="users")
    company = relationship("Company", backref="users")
