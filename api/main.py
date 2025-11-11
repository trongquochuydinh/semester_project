from fastapi import FastAPI
import uvicorn
import os
from api.routes.users import router as users_router
from api.routes.companies import router as companies_router
from api.routes.paginate import router as paginate_router

app = FastAPI()
app.include_router(users_router)
app.include_router(companies_router)
app.include_router(paginate_router)

if __name__ == "__main__":
    def run_service():
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=os.environ.get("PORT_APP", 8500)
        )

    run_service()