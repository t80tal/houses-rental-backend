from fastapi import APIRouter
from apis.routes import route_houses, route_users, route_login

api_routers = APIRouter()

api_routers.include_router(route_houses.router, prefix="/houses", tags=["houses_category"])
api_routers.include_router(route_users.router, prefix="", tags=["houses_category"])
api_routers.include_router(route_login.router, prefix="/login", tags=["login"])
