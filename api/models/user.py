from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, joinedload
from api.db.db_engine import Base, SessionLocal
from werkzeug.security import check_password_hash, generate_password_hash

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=True)
    roles = relationship('UserRole', back_populates='user')

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    users = relationship('UserRole', back_populates='role')

class UserRole(Base):
    __tablename__ = 'user_roles'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', back_populates='roles')
    role = relationship('Role', back_populates='users')

def get_user_by_username_or_email(identifier):
    session = SessionLocal()
    try:
        return session.query(User).options(
            joinedload(User.roles).joinedload(UserRole.role)
        ).filter((User.username == identifier) | (User.email == identifier)).first()
    finally:
        session.close()

def verify_user(identifier, password):
    user = get_user_by_username_or_email(identifier)
    if user and user.verify_password(password):
        return user
    return None
