from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.crud.users import db_user_exists, db_add_user
from app.services.auth import authenticate_user
from app.shemas.users import Register
from app.dependencies import SessionDep, FormDataDep
from security.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", summary="Регистрация пользователя")
async def register(user: Register, session: SessionDep):
    if await db_user_exists(
        user.username, session
    ):  # Если db_user не False, значит такой пользователь уже существует
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    await db_add_user(user, session)
    return {"message": "User created successfully"}


@router.post("/token", summary="Вход в систему и выдача токена")
async def login(form_data: FormDataDep, session: SessionDep):
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
