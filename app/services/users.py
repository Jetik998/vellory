from fastapi import HTTPException, status

from app.api.dependencies import SessionDep
from app.crud.users import db_add_user, db_get_user
from app.schemas.users import UserRegister, UserRegisterResponse


async def register_user(
    user: UserRegister, session: SessionDep
) -> UserRegisterResponse:
    """
    Регистрация нового пользователя.

    Проверяет уникальность username и email перед созданием аккаунта.
    Возвращает данные зарегистрированного пользователя.
    """
    if await db_get_user(session, user.username, str(user.email)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username or email already exists",
        )
    await db_add_user(user, session)
    return UserRegisterResponse(
        username=user.username, message="User registered successfully"
    )
