from fastapi import APIRouter, HTTPException, status
from app.enums import Tags

from app.security.auth import authenticate_user
from app.schemas.users import UserIn, UserRegisterResponse
from app.schemas.auth import TokenResponse
from app.api.dependencies import SessionDep, FormDataDep
from app.security.jwt import create_access_token
from app.services.users import register_user

router = APIRouter(prefix="/api/auth", tags=[Tags.auth])


@router.post(
    "/register",
    summary="Регистрация пользователя",
    status_code=status.HTTP_201_CREATED,
)
async def register(user: UserIn, session: SessionDep) -> UserRegisterResponse:
    return await register_user(user, session)


@router.post(
    "/token", summary="Вход в систему и выдача токена", response_model=TokenResponse
)
async def login(form_data: FormDataDep, session: SessionDep) -> TokenResponse:
    user = await authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return TokenResponse(access_token=access_token, token_type="bearer")
