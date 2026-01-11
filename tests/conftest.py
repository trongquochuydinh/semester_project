import pytest
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from werkzeug.security import generate_password_hash

from api.main import app
from api.db.db_engine import Base
from api.models.company import Company
from api.models.role import Role
from api.models.user import User
from api.models.item import Item
from api.models.order import Order
from api.models.order_item import OrderItem

from api.dependencies import get_current_user, get_db

# -------------------------
# Test client fixture
# -------------------------

@pytest.fixture
def client():
    return TestClient(app)

def override_get_current_user(user):
    def _override():
        return user
    return _override

@pytest.fixture
def override_get_db(db):
    def _override():
        yield db
    return _override

@pytest.fixture(autouse=True)
def clear_dependency_overrides():
    yield
    app.dependency_overrides.clear()

@pytest.fixture
def auth_client_factory(client, override_get_db):
    def _factory(user):
        app.dependency_overrides[get_current_user] = override_get_current_user(user)
        app.dependency_overrides[get_db] = override_get_db
        return client
    return _factory

@pytest.fixture
def client_with_db(client, db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    yield client

    app.dependency_overrides.clear()

# -------------------------
# Database session fixture
# -------------------------
@pytest.fixture
def db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    Base.metadata.create_all(bind=engine)

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()


# -------------------------
# Company
# -------------------------
@pytest.fixture
def company(db):
    company = Company(
        name="Test Company",
        field="Testing",
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company

@pytest.fixture
def company2(db):
    company = Company(
        name="Test Company2",
        field="Testing",
    )
    db.add(company)
    db.commit()
    db.refresh(company)
    return company

# -------------------------
# Roles
# -------------------------
@pytest.fixture
def role_superadmin(db):
    role = Role(name="superadmin", rank=1)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@pytest.fixture
def role_admin(db):
    role = Role(name="admin", rank=2)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@pytest.fixture
def role_manager(db):
    role = Role(name="manager", rank=3)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


@pytest.fixture
def role_employee(db):
    role = Role(name="employee", rank=4)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


# -------------------------
# Users (one per role)
# -------------------------
@pytest.fixture
def superadmin(db, role_superadmin):
    user = User(
        username="superadmin_user",
        email="superadmin@example.com",
        password_hash="hashed-password",
        company_id=None,  # superadmin is global
        role_id=role_superadmin.id,
        is_active=True,
        status="offline",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def admin(db, company, role_admin):
    user = User(
        username="admin_user",
        email="admin@example.com",
        password_hash=generate_password_hash("admin123"),
        company_id=company.id,
        role_id=role_admin.id,
        is_active=True,
        status="offline",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def manager(db, company, role_manager):
    user = User(
        username="manager_user",
        email="manager@example.com",
        password_hash="hashed-password",
        company_id=company.id,
        role_id=role_manager.id,
        is_active=True,
        status="offline",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def employee(db, company, role_employee):
    user = User(
        username="employee_user",
        email="employee@example.com",
        password_hash="hashed-password",
        company_id=company.id,
        role_id=role_employee.id,
        is_active=True,
        status="offline",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# -------------------------
# Item
# -------------------------
@pytest.fixture
def item(db, company):
    item = Item(
        name="Test Item",
        sku="TEST-001",
        price=100,
        quantity=10,
        company_id=company.id,
        is_active=True,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# -------------------------
# Order
# -------------------------
@pytest.fixture
def order(db, company, employee):
    order = Order(
        status="pending",
        order_type="sale",
        user_id=employee.id,
        company_id=company.id,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


# -------------------------
# OrderItem
# -------------------------
@pytest.fixture
def order_item(db, order, item):
    order_item = OrderItem(
        order_id=order.id,
        item_id=item.id,
        quantity=2,
        unit_price=item.price,
    )
    db.add(order_item)
    db.commit()
    db.refresh(order_item)
    return order_item
