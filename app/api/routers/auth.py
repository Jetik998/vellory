from fastapi import APIRouter, status
from fastcrud.exceptions.http_exceptions import UnauthorizedException

from app.enums import Tags

from app.security.auth import authenticate_user
from app.schemas.users import UserRegister, UserRegisterResponse, UserEmail
from app.schemas.auth import TokenResponse, Login
from app.api.dependencies import SessionDep, FormDataDep
from app.security.jwt import create_tokens
from app.services.users import register_user

router = APIRouter(prefix="/api/auth", tags=[Tags.auth])


@router.post(
    "/register",
    summary="Регистрация пользователя",
    status_code=status.HTTP_201_CREATED,
)
async def register(user: UserRegister, session: SessionDep) -> UserRegisterResponse:
    return await register_user(user, session)


async def get_email_for_authenticate_user(user_data: Login, session) -> UserEmail:
    user = await authenticate_user(str(user_data.email), user_data.password, session)
    if not user:
        raise UnauthorizedException("Incorrect username or password")
    return user.email


async def login(user_data: Login, session) -> dict[str, str]:
    user = await authenticate_user(str(user_data.email), user_data.password, session)
    if not user:
        raise UnauthorizedException("Incorrect username or password")

    tokens = create_tokens(user.email)
    return tokens


@router.post(
    "/token", summary="Вход в систему и выдача токена", response_model=TokenResponse
)
async def token(form_data: FormDataDep, session: SessionDep) -> TokenResponse:
    tokens = await login(form_data, session)
    access_token = tokens.get("access_token")
    return TokenResponse(access_token=access_token, token_type="bearer")
