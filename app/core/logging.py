import logging
from logging.handlers import RotatingFileHandler
from app.core.config import BASE_DIR

LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging():
    """Настройка логирования для приложения"""

    # Проверяем, не настроено ли уже логирование
    root_logger = logging.getLogger()
    if root_logger.handlers:
        return  # Логирование уже настроено

    log_file = LOGS_DIR / "app.log"

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10 МБ
        backupCount=2,
        encoding="utf-8",
    )

    # Форматтер для более читаемого вывода
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s:%(filename)s:%(lineno)d %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """Получить логгер с указанным именем"""
    return logging.getLogger(name)


logger = logging.getLogger(__name__)
