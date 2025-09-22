from fastapi import FastAPI, Request, HTTPException
import uvicorn
import os
from api.routes.users import router as users_router
from api.db.db_engine import SessionLocal
from api.models.user import User, paginate_users
from api.models.company import Company, paginate_companies
from typing import Any
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import and_

app = FastAPI()
app.include_router(users_router)

@app.post("/api/paginate")
async def paginate(request: Request):
    body = await request.json()
    table_name = body.get("table_name")
    limit = int(body.get("limit", 10))
    offset = int(body.get("offset", 0))
    filters = body.get("filters", {})
    db: Session = SessionLocal()
    try:
        handler_map = {
            "users": paginate_users,
            "companies": paginate_companies
            # Add more handlers as needed
        }
        handler = handler_map.get(table_name)
        if not handler:
            raise HTTPException(status_code=400, detail="Invalid table_name")
        return handler(db, limit, offset, filters)
    finally:
        db.close()

if __name__ == "__main__":
    def run_service():
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=os.environ.get("PORT_APP", 8500)
        )

    run_service()