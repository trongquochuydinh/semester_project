from api.db.db_engine import SessionLocal


def get_db():
    """
    FastAPI dependency that provides database session with automatic transaction management.

    Yields:
        Session: SQLAlchemy database session for the current request

    Transaction Management:
        - Commits transaction on successful completion
        - Rolls back transaction on any exception
        - Always closes session to prevent connection leaks

    Usage:
        @router.post("/users/")
        def create_user(user_data: dict, db: Session = Depends(get_db)):
            # Database operations here
            return result

    Design Pattern: Context manager ensures proper resource cleanup
    """
    # Create new database session for this request
    db = SessionLocal()

    try:
        # Yield session to the route function
        yield db

        # If no exception occurred, commit the transaction
        db.commit()

    except:
        # If any exception occurred, rollback all changes
        db.rollback()

        # Re-raise the exception to be handled by FastAPI
        raise

    finally:
        # Always close the session to return connection to pool
        db.close()


# --- Database Session Lifecycle ---
# 1. New session created for each HTTP request
# 2. Session yielded to route handler for database operations
# 3. On success: Changes committed automatically
# 4. On error: Changes rolled back, exception propagated
# 5. Session always closed regardless of success/failure
#
# Benefits:
# - Automatic transaction management
# - Connection pooling and resource cleanup
# - Request isolation (each request gets its own session)
# - Exception safety with guaranteed rollback on errors