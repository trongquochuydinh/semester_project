from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from api.db.db_engine import Base
from werkzeug.security import check_password_hash

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    status = Column(String, default="offline", nullable=False)
    last_login = Column(DateTime, nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)

    roles = relationship("UserRole", back_populates="user")
    company = relationship("Company", backref="users")

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def get_role(self):
        return self.roles[0] if self.roles else None


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    users = relationship("UserRole", back_populates="role")


class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="roles")
    role = relationship("Role", back_populates="users")
