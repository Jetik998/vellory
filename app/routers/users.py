from fastapi import APIRouter, Depends
from app.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated


router = APIRouter(prefix="/auth", tags=["tasks"])
SessionDep = Annotated[AsyncSession, Depends(get_session)]