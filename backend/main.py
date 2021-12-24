from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from core.config import settings
from db.session import engine
from db.base_class import Base
from apis.base import api_routers
from fastapi.middleware.cors import CORSMiddleware
from webapps.base import api_router as webapp_router


def create_tables():
    Base.metadata.create_all(bind=engine)


def include_routers(app):
    app.include_router(api_routers)
    app.include_router(webapp_router)


def start_application():
    app = FastAPI(title=settings.PROJECT_TITLE, version=settings.PROJECT_VERSION)
    create_tables()
    include_routers(app)
    return app


app = start_application()
