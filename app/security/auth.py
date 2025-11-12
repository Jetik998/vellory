from app.crud.users import db_get_user
from app.security.password import verify_password


async def authenticate_user(email: str, password: str, session):
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
    user = await db_get_user(session, email=email)
    if not user and not verify_password(password, user.hashed_password):
        return None
    return user
