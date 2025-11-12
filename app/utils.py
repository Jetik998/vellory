from datetime import datetime
import pytz
from sqlalchemy import inspect
from sqlalchemy.exc import NoInspectionAvailable


def time():
    moscow_tz = pytz.timezone("Europe/Moscow")
    now = datetime.now(moscow_tz)
    return now.replace(microsecond=0, tzinfo=None)


def db_obj_to_dict(obj):
    """
    Преобразует ORM-объект SQLAlchemy в словарь Python.

    Параметры:
        obj: SQLAlchemy ORM экземпляр (например, объект модели User).

    Возвращает:
        dict: Словарь, где ключи — имена колонок таблицы,
              значения — текущие значения этих полей в объекте.
        None: если передан None.

    Исключения:
        TypeError: если объект не является экземпляром ORM-модели SQLAlchemy.

    Пример:
        user = User(id=1, username="alice", email="a@b.c")
        db_obj_to_dict(user)
        # -> {'id': 1, 'username': 'alice', 'email': 'a@b.c'}
    """
    if obj is None:
        return None
    try:
        mapper = inspect(obj).mapper
    except NoInspectionAvailable:
        raise TypeError("db_obj_to_dict expects a SQLAlchemy ORM instance")
    return {c.key: getattr(obj, c.key, None) for c in mapper.column_attrs}
