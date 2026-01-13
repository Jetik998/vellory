# Вспомогательные функции
from sqlalchemy import text


def format_uptime(seconds: float) -> str:
    """Форматирует uptime в читаемый вид"""
    days = int(seconds // 86400)
    hours = int((seconds % 86400) // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)

    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    parts.append(f"{secs}s")

    return " ".join(parts)


async def check_dependencies() -> dict[str, str]:
    """
    Проверяет статус зависимостей (БД, Redis, внешние API).
    Замените на реальные проверки для вашего проекта.
    """
    from app.main import app
    from app.core.database import async_session

    dependencies = {}

    # Пример проверки базы данных
    try:
        async with async_session() as session:
            await session.execute(text("SELECT 1"))
            dependencies["database"] = "connected"
    except Exception as e:
        dependencies["database"] = f"error: {str(e)}"

    # Пример проверки Redis
    try:
        await app.state.redis.ping()
        dependencies["redis"] = "connected"
    except Exception as e:
        dependencies["redis"] = f"error: {str(e)}"

    return dependencies
