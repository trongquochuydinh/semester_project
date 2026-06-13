import os

import uvicorn
from fastapi import FastAPI

from api.config import validate_config
from api.routes.auth import router as auth_router
from api.routes.companies import router as companies_router
from api.routes.items import router as items_router
from api.routes.orders import router as orders_router
from api.routes.users import router as users_router
from api.utils.exception_handlers import register_exception_handlers

validate_config()

app = FastAPI(
    title="Business Management API",
    description="REST API for business management system with multi-tenant support",
    version="1.0.0",
)

register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(companies_router)
app.include_router(items_router)
app.include_router(orders_router)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT_APP", 8500)),
    )
