from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from api.domain import ConflictError, ForbiddenError, NotFoundError, ValidationError


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(NotFoundError)
    async def handle_not_found(_: Request, exc: NotFoundError):
        return JSONResponse(status_code=404, content={"detail": str(exc)})

    @app.exception_handler(ForbiddenError)
    async def handle_forbidden(_: Request, exc: ForbiddenError):
        return JSONResponse(status_code=403, content={"detail": str(exc)})

    @app.exception_handler(ConflictError)
    async def handle_conflict(_: Request, exc: ConflictError):
        return JSONResponse(status_code=409, content={"detail": str(exc)})

    @app.exception_handler(ValidationError)
    async def handle_validation(_: Request, exc: ValidationError):
        return JSONResponse(status_code=422, content={"detail": str(exc)})
