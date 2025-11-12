from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()


def get_password_hash(password):
    """
    Генерирует хеш для заданного пароля.

    Параметры
    ----------
    password : str
        Пароль в открытом виде.

    Возвращает
    -------
    str
        Хешированный пароль.
    """
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    """
    Проверяет соответствие введённого пароля его хешу.

    Параметры
    ----------
    plain_password : str
        Пароль в открытом виде.
    hashed_password : str
        Хеш пароля, сохранённый в базе данных.

    Возвращает
    -------
    bool
        True, если пароль корректен, иначе False.
    """
    return pwd_context.verify(plain_password, hashed_password)
