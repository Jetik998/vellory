from fastapi import APIRouter

from app.web.routers import auth

web_router = APIRouter()

web_router.include_router(auth.router)
