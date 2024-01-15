from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from app.db.engine import Base, engine
from app.api.api_v1.api import api_router
from app.core.config import settings
from app.api.deps import get_db
from app.db.init_db import init_db
import contextlib


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


get_db_wrapper = contextlib.contextmanager(get_db)


def init_data():
    with get_db_wrapper() as db:
        init_db(db)


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)
origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
    init_data()
