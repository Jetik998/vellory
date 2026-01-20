from app.models import User


def create_test_user():
    """Функция для создания объекта пользователя"""
    return User(
        id=1,
        email="test@example.com",
        username="testuser",
        hashed_password="fake_hashed_password",
        avatar=None,
        tasks=[],
    )
