from sqlalchemy import Column, Integer, String
from api.db.db_engine import Base

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    industry = Column(String)

def paginate_companies(db, limit, offset, filters):
    query = db.query(Company)
    for key, value in filters.items():
        if hasattr(Company, key):
            query = query.filter(getattr(Company, key) == value)
    total = query.count()
    results = query.offset(offset).limit(limit).all()
    def to_dict(obj):
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    data = [to_dict(r) for r in results]
    return {"total": total, "data": data}
