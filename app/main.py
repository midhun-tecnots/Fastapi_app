from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routers.users import router as users_router
from app.api.v1.routers.products import router as products_router
from app.api.v1.routers.orders import router as orders_router
from app.graphql.schema import graphql_app


def create_app() -> FastAPI:
    app = FastAPI(title="Summit Market API", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(users_router, prefix="/api/v1", tags=["users"])
    app.include_router(products_router, prefix="/api/v1", tags=["products"])
    app.include_router(orders_router, prefix="/api/v1", tags=["orders"])

    app.mount("/graphql", graphql_app)
    return app


app = create_app()
