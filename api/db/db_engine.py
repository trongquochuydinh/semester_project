from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from config import host, dbname, user, password

if any(db_info is None for db_info in [host, dbname, user, password]):
    db_info = [("host", host), ("dbname", dbname),
               ("user", user), ("password", password)]
    # Check for None and print which ones are None
    none_variables = [name for name, value in db_info if value is None]
    print(f"The following variables are None: {', '.join(none_variables)}")

    DB = None

else:
    db_string = "postgresql://{2}:{3}@{0}/{1}".format(
        host, dbname, user, password)
    DB: Engine = create_engine(
        db_string,
        pool_size=10,        
        max_overflow=20,
        pool_timeout=30,       
        pool_recycle=3600     
    )

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=DB)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()
