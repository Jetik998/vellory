from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import SessionDep
from app.core.exceptions import UnauthorizedException
from app.crud.users import db_get_user
from app.models import User
from app.schemas.auth import Login
from app.security.password import verify_password


async def authenticate_user(
    password: str, session, username: str = None, email: str = None
):
    """
    Аутентифицирует пользователя по адресу электронной почты и паролю.

    Параметры
    ----------
    email : str
        Адрес электронной почты пользователя.
    password : str
        Пароль пользователя в открытом виде.
    session :
        Асинхронная сессия базы данных для выполнения запросов.

    Возвращает
    -------
    user | None
        Объект пользователя, если аутентификация успешна, иначе None.
    """
    db_user = await db_get_user(session, username=username, email=email)
    if not db_user or not verify_password(password, db_user.hashed_password):
        return None
    return db_user


async def authenticate_user_flexible(
    user_data: Login | OAuth2PasswordRequestForm, session: SessionDep
) -> User:  # ✅ Возвращаем полный объект
    """Универсальная аутентификация"""

    if isinstance(user_data, Login):
        db_user = await authenticate_user(
            user_data.password, session, email=str(user_data.email)
        )
    else:
        db_user = await authenticate_user(
            user_data.password, session, username=user_data.username
        )

    if not db_user:
        raise UnauthorizedException("Incorrect username or password")

    return db_user
