from fastapi import APIRouter
from webapps.houses import route_houses
from webapps.auth import route_login


api_router = APIRouter()
api_router.include_router(route_houses.router, prefix="", tags=["houses options"])
api_router.include_router(route_login.router, prefix="", tags=["HomePage"])



