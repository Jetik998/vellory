from fastapi.security import OAuth2PasswordRequestForm

from app.core.exceptions import UnauthorizedException, BadRequestException
from app.schemas.auth import Login
from app.security.auth import authenticate_user


async def get_identity_for_authenticate_user(
    user_data: Login | OAuth2PasswordRequestForm, session
) -> str:
    """
    Универсальная функция для аутентификации по email или username.
    Определяет, по какому полю аутентифицировать пользователя, на основе данных.
    """
    if isinstance(user_data, Login):  # Проверяем, есть ли email
        db_user = await authenticate_user(
            user_data.password, session, email=str(user_data.email)
        )

        if not db_user:
            raise UnauthorizedException("Incorrect email or password")
        return db_user.email
    elif isinstance(
        user_data, OAuth2PasswordRequestForm
    ):  # Проверяем, есть ли username
        db_user = await authenticate_user(
            user_data.password, session, username=user_data.username
        )
        if not db_user:
            raise UnauthorizedException("Incorrect username or password")
        return db_user.username
    else:
        raise BadRequestException("Invalid user data.")
