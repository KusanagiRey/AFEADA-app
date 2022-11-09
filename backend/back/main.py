from fastapi import FastAPI

from routers.user_router import user_router
from routers.admin_router import admin_router


def create_app() -> FastAPI:
    app = FastAPI(
        title='AFEADA',
        version='0.0.1a',
    )

    app.include_router(user_router)
    app.include_router(admin_router)

    return app

app = create_app()