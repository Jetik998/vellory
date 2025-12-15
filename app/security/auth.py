from app.crud.users import db_get_user
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
