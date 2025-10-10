from fastapi import APIRouter, HTTPException, status
from app.crud.users import db_user_exists, db_add_user
from app.services.auth import authenticate_user
from app.shemas.users import UserIn, UserRegisterResponse
from app.shemas.auth import TokenResponse
from app.core.dependencies import SessionDep, FormDataDep
from app.security.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    summary="Регистрация пользователя",
    status_code=status.HTTP_201_CREATED,
)
async def register(user: UserIn, session: SessionDep) -> UserRegisterResponse:
    if await db_user_exists(user.username, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    await db_add_user(user, session)
    return UserRegisterResponse(
        username=user.username, message="User registered successfully"
    )


@router.post(
    "/token", summary="Вход в систему и выдача токена", response_model=TokenResponse
)
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
