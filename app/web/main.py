from fastapi import APIRouter
from app.web.routers import auth, pages, tasks, users

web_router = APIRouter()

web_router.include_router(auth.router)
web_router.include_router(pages.router)
web_router.include_router(tasks.router)
web_router.include_router(users.router)
