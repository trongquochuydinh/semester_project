# Import FastAPI framework for building REST API
from fastapi import FastAPI
# Import Uvicorn ASGI server for running the FastAPI application
import uvicorn
# Import OS module for environment variable access
import os

# Import API route modules for different business domains
from api.routes.users import router as users_router           # User management and authentication routes
from api.routes.companies import router as companies_router   # Company CRUD operations and management
from api.routes.items import router as items_router           # Product/item catalog management
from api.routes.orders import router as orders_router         # Order processing and lifecycle management

# Initialize FastAPI application instance
# This creates the main application object that will handle all HTTP requests
app = FastAPI(
    title="Business Management API",           # API documentation title
    description="REST API for business management system with multi-tenant support",
    version="1.0.0",                          # API version for client compatibility
)

# --- Register API Route Modules ---
# Include all route modules to make their endpoints available
# Each router handles a specific business domain with related operations

app.include_router(users_router)        # /api/users/* - User authentication, profile management, user CRUD
app.include_router(companies_router)    # /api/companies/* - Company management, multi-tenant operations
app.include_router(items_router)        # /api/items/* - Product catalog, inventory management
app.include_router(orders_router)       # /api/orders/* - Order creation, processing, fulfillment

# --- Application Entry Point ---
if __name__ == "__main__":
    def run_service():
        """
        Start the FastAPI application using Uvicorn ASGI server.
        
        Configuration:
            - host="0.0.0.0": Accept connections from any IP address (allows external access)
            - port: Configurable via PORT_APP environment variable, defaults to 8500
            - reload: Auto-restart on code changes (development mode)
            - workers: Number of worker processes (production scaling)
        """
        uvicorn.run(
            app,                                           # FastAPI application instance
            host="0.0.0.0",                               # Listen on all network interfaces
            port=int(os.environ.get("PORT_APP", 8500)),   # Port from environment or default 8500
            # reload=True,                                # Uncomment for development auto-reload
            # workers=4,                                  # Uncomment for production multi-worker setup
            # access_log=True,                            # Enable request logging
        )

    # Start the API server
    run_service()
#
# API Documentation:
#   - Swagger UI: http://localhost:8500/docs
#   - OpenAPI JSON: http://localhost:8500/openapi.json