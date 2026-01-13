from fastapi import APIRouter

from app.api.routers import tasks, auth, users, system

api_router = APIRouter()

api_router.include_router(system.router)
api_router.include_router(tasks.router)
api_router.include_router(auth.router)
api_router.include_router(users.router)
