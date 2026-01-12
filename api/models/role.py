# Import SQLAlchemy components for ORM model definition
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Import database base class for model inheritance
from api.db.db_engine import Base


class Role(Base):
    """
    Role model for permission-based access control system.

    Defines user permission levels and access rights throughout the application.
    Each user is assigned exactly one role that determines their capabilities.

    Role Hierarchy (typical setup):
        - superadmin: Full system access across all companies
        - admin: Full access within assigned company
        - manager: Management functions within company
        - user: Basic user operations within company

    Features:
        - Hierarchical permission structure via rank
        - Unique role names for consistent authorization
        - Extensible for custom permission levels
    """
    __tablename__ = "roles"

    # --- Primary Key ---
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,               # Unique role identifier
    )

    # --- Role Definition ---
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
        unique=True,                    # Enforce unique role names (e.g., 'admin', 'user')
    )

    rank: Mapped[int] = mapped_column(
        Integer,
        nullable=False,                 # Numerical hierarchy for permission comparison
    )

    # -------------------------
    # Relationships
    # -------------------------

    users = relationship(
        "User",
        back_populates="role",          # Access all users with this role
    )

# --- Role System Design Notes ---
# Permission Hierarchy:
# - Higher rank numbers = more permissions
# - Example: superadmin(100) > admin(80) > manager(60) > user(40)
# - Allows programmatic permission comparisons
#
# Authorization Patterns:
# - Role-based: Check user.role.name in ['admin', 'manager']
# - Rank-based: Check user.role.rank >= required_rank
# - Fine-grained: Custom logic per role type
#
# Common Roles:
# - superadmin: Cross-company system administration
# - admin: Company-level administration and user management
# - manager: Department/team management functions
# - employee: Basic operations and data entry
#
# Extensibility:
# - Add new roles without code changes
# - Role permissions defined in application logic
# - Database only stores role metadata
