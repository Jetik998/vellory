from sqlalchemy import select, or_
from app.services.avatars import update_avatar_file, delete_avatar_file
from app.core.db_utils import save_and_refresh
from app.models.user import User
from app.security.password import get_password_hash
from app.schemas.users import UserRegister, UserInDB


# Получить пользователя из базы данных, по username или email
async def db_get_user(
    session, username: str | None = None, email: str | None = None
) -> User | None:
    """
    Ищет пользователя по username ИЛИ email.
    Возвращает первого найденного.
    """
    stmt = select(User).where(or_(User.username == username, User.email == email))
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


# async def db_get_user_by_username_or_email(
#         session,
#         username: str | None = None,
#         email: str | None = None
# ) -> User | None:
#     """
#     Ищет пользователя по username ИЛИ email.
#     Возвращает первого найденного.
#     """
#     stmt = select(User).where(or_(User.username == username, User.email == email))
#
#     result = await session.execute(stmt)
#     return result.scalar_one_or_none()


# async def db_user_name_exists(username: str, session) -> bool:
#     stmt = select(exists().where(User.username == username))
#     result = await session.execute(stmt)
#     return result.scalars().first()
#
#
# async def db_user_email_exists(user_email: str, session) -> bool:
#     stmt = select(exists().where(User.email == user_email))
#     result = await session.execute(stmt)
#     return result.scalars().first()


async def db_add_user(user: UserRegister, session):
    hashed_password = get_password_hash(user.password)
    db_user_model = UserInDB(**user.model_dump(), hashed_password=hashed_password)
    db_user = User(**db_user_model.model_dump())
    await save_and_refresh(session, db_user)
    return db_user


async def db_update_user_avatar(file, user, session):
    """
    Обновляет аватар пользователя.

    Выполняет проверку файла, сохраняет изображение с безопасным именем,
    присваивает пользователю путь к новому файлу и фиксирует изменения в БД.

    Args:
        file: Загруженный файл (UploadFile).
        user: Пользователь, чей аватар обновляется.
        session: Сессия базы данных.

    Returns:
        Пользователь с обновлённым путём к аватару.
    """
    new_avatar = await update_avatar_file(file)
    if new_avatar:
        await delete_avatar_file(str(user.avatar))
        user.avatar = new_avatar
    else:
        return None
    await save_and_refresh(session, user)
    return user
