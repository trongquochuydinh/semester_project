# Import SQLAlchemy components for database connection and ORM setup
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Optional

# Import database configuration from application config
from api.config import host, dbname, user, password

# Global database engine variable (initialized conditionally)
DB: Optional[Engine] = None

# Validate database configuration before creating engine
if any(db_info is None for db_info in [host, dbname, user, password]):
    """
    Database configuration validation and error reporting.
    
    Checks if any required database configuration parameters are missing.
    Provides clear error messaging for debugging configuration issues.
    """
    # Create list of configuration parameter names and values for checking
    db_info = [("host", host), ("dbname", dbname),
               ("user", user), ("password", password)]
    
    # Identify which configuration parameters are missing
    none_variables = [name for name, value in db_info if value is None]
    print(f"The following variables are None: {', '.join(none_variables)}")

else:
    """
    Database engine initialization with PostgreSQL connection.
    
    Creates SQLAlchemy engine with connection pooling and optimization settings.
    Only initializes if all configuration parameters are available.
    """
    # Build PostgreSQL connection string from configuration
    db_string = "postgresql://{2}:{3}@{0}/{1}".format(
        host, dbname, user, password)
    
    # Create database engine with connection pooling configuration
    DB = create_engine(
        db_string,
        pool_size=10,        # Number of connections to maintain in pool
        max_overflow=20,     # Additional connections when pool is full
        pool_timeout=30,     # Seconds to wait for connection from pool
        pool_recycle=3600    # Seconds before recreating connections (1 hour)
    )

# Create session factory bound to database engine
SessionLocal = sessionmaker(
    autocommit=False,    # Manual transaction control for data integrity
    autoflush=False,     # Manual flush control for optimization
    bind=DB              # Bind to database engine
)

# Base class for all SQLAlchemy models/tables
Base = declarative_base()

# --- Database Connection Design Notes ---
# Connection pooling optimizes performance for concurrent requests
# Session factory provides consistent database session configuration
# Manual commit/flush control allows for better transaction management
# Base class enables declarative model definitions throughout application
# Configuration validation prevents runtime errors with clear error messages
# Pool settings tuned for typical web application load patterns